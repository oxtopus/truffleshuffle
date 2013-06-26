"""
Simple utility for sending chunked multipart S3 uploads.

Parallelism, and chunk size are command-line configurable.  AWS credentials 
derived from environment.

Usage:

    upload-s3-multipart [options] path bucket

Copyright 2013 Austin Marshall
https://github.com/oxtopus/ercot

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging
import string
import sys

from functools import partial
from io import BytesIO
from itertools import izip, repeat
from multiprocessing import Pool
from optparse import OptionParser

from boto.s3.connection import S3Connection

"""
Defaults
"""
DEFAULT_CHUNK_SIZE = 5242880
DEFAULT_NUM_PROCESSES = 2

"""
CLI options
"""
parser = OptionParser(usage='Usage: %prog [options] target bucket')

parser.add_option('-l', '--log',
  dest='log',
  default='INFO',
  help='Log level [Default: INFO]',
  metavar='LEVEL')

parser.add_option('-p', '--processes',
  dest='processes',
  default=DEFAULT_NUM_PROCESSES,
  help='Number of concurrent downloads [Default: %d]' % DEFAULT_NUM_PROCESSES,
  metavar='NUM',
  type='int')

parser.add_option('-k', '--key',
  dest='key',
  default=None,
  help='S3 Key',
  metavar='key')

parser.add_option('-c', '--chunk', '-s', '--size',
  dest='chunk_size',
  default=DEFAULT_CHUNK_SIZE,
  help='Chunk size (in bytes) [Default: %d]' % DEFAULT_CHUNK_SIZE,
  metavar='BYTES',
  type='int')


def read_in_chunks(infile, chunk_size=DEFAULT_CHUNK_SIZE):
  """ Yield binary chunks of size determined by chunk_size arg """
  seq = 1
  while True:
    chunk = infile.read(chunk_size)
    if chunk:
      yield seq, chunk
      seq += 1
    else:
      return


def upload_chunk(seq, chunk, bucket, multipart_id, prefix=''):
  """ Upload individual chunk """
  conn = S3Connection()
  bucket = conn.get_bucket(bucket)
  fp = BytesIO(chunk)
  for mp in bucket.get_all_multipart_uploads():
    if mp.id == multipart_id:
      logging.info('Uploading chunk %s:%s', multipart_id, seq, )
      mp.upload_part_from_file(fp=fp, part_num=seq)
      logging.info('Chunk %s:%s uploaded', multipart_id, seq, )


def split(payload):
  """ Call upload_chunk() w/ args derived from payload """
  seq, chunk = payload[0]
  if len(payload) > 1:
    args = payload[1]
    if len(payload) > 2:
      kwargs = payload[2]

  upload_chunk(seq, chunk, *args, **kwargs)


def upload(target, bucket,
    processes=DEFAULT_NUM_PROCESSES,
    chunk_size=DEFAULT_CHUNK_SIZE,
    key=None):
  """
  Upload target file via S3 multipart upload functionality
  """

  pool = Pool(processes=processes)

  with open(target, 'rb') as inp:
    conn = S3Connection()
    bucket = conn.get_bucket(bucket)
    mp = bucket.initiate_multipart_upload(key or target)

    logging.info('Uploading %s, multipart id=%s', target, mp.id)

    """
    Remaining *args, **kwargs to upload_chunk()
    """
    args = (bucket, mp.id, )
    kwargs = dict(prefix=target)

    """
    izip all input into a single iterable for consumption by Pool.map()
    """
    iterchunks = \
      izip(
        read_in_chunks(inp, chunk_size=chunk_size),
        repeat(args),
        repeat(kwargs)
      )

    pool.map(split, iterchunks)
    pool.close()
    pool.join()

    result = mp.complete_upload()
    key = bucket.get_key(target)
    key.set_acl('private')

    logging.info('Done. %s uploaded to S3 at %s', target, result.location)


def main():
  """
  Parse CLI options and call upload()
  """
  
  (options, args) = parser.parse_args()

  logging.basicConfig(level=getattr(logging, options.log.upper()))

  try:
    target, bucket, = args[:2] # First two CLI args
  
  except ValueError:
    parser.print_help()
    sys.exit()

  upload(target, bucket,
    processes=options.processes,
    chunk_size=options.chunk_size,
    key=options.key or target)

if __name__ == '__main__':
  main()
