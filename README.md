truffleshuffle
==============

Command line utility for uploading large files to AWS S3 via [Multipart Upload](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingRESTAPImpUpload.html)
w/ configurable concurrency and chunk size.

Install
-------

First, clone this repository:

    git clone git://github.com/oxtopus/truffleshuffle.git
    cd truffleshuffle

Install via setup.py:

    python setup.py install

...or [easy_install](http://pythonhosted.org/distribute/easy_install.html):

    easy_install .

...or [pip](http://www.pip-installer.org/en/latest/):

    pip install .

Alternatively, you can invoke the ``upload`` module in the ``truffleshuffle`` 
package directly:

    python -m truffleshuffle.upload

Usage
-----

Once installed, you can use the ``upload-s3-multipart`` CLI utility:

    upload-s3-multipart --help

[Boto](http://boto.readthedocs.org/en/latest/) is required.  See 
[Boto Config](http://boto.readthedocs.org/en/latest/boto_config_tut.html) for 
configuration instructions.
