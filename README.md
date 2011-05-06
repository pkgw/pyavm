PyAVM provides the ``AVM()`` class to retrieve [AVM](http://www.virtualastronomy.org/avm_metadata.php) meta-data from an image file:

    >>> from pyavm import AVM

To use, simply create an instance of this class using the filename of the
image (or any file-like object):

    >>> avm = AVM('myexample.jpg')

Then, you can view the contents by using

    >>> print avm

or

    >>> avm

Finally, the AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'

    >>> avm.Publisher
    'Chandra X-ray Observatory'