truffleshuffle
==============

Command line utility for uploading large files to AWS S3 via [Multipart Upload](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingRESTAPImpUpload.html)

Install
-------

First, clone this repository:

    git clone git://github.com/oxtopus/truffleshuffle.git
    cd truffleshuffle

Install via setup.py:

    python setup.py install

or easy_install:

    easy_install .

or pip:

    pip install .

Usage
-----

Once installed, you can use the ``upload-s3-multipart`` CLI utility:

    upload-s3-multipart --help

[boto](http://boto.readthedocs.org/en/latest/) is required.  See 
[Boto Config](http://boto.readthedocs.org/en/latest/boto_config_tut.html) for 
configuration instructions.
