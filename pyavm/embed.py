import struct

from .jpeg import is_jpeg, JPEGFile, JPEGSegment
from .png import is_png, PNGFile, PNGChunk


def embed_xmp(image_in, image_out, xmp_packet):

    if is_jpeg(image_in):

        # Check length
        if len(xmp_packet) >= 65503:
            raise Exception("XMP packet is too long to embed in JPG file")

        # XMP segment
        xmp_segment = JPEGSegment()

        # APP1 marker
        xmp_segment.bytes = "\xff\xe1"

        # Length of XMP packet + 2 + 29
        xmp_segment.bytes += struct.pack('>H', len(xmp_packet) + 29 + 2)

        # XMP Namespace URI (NULL-terminated)
        xmp_segment.bytes += "http://ns.adobe.com/xap/1.0/\x00"

        # XMP packet
        xmp_segment.bytes += xmp_packet

        # Read in input file
        jpeg_file = JPEGFile.read(image_in)

        # Need to check there isn't alrady XMP meta-data

        # Position at which to insert the packet
        markers = [x.type for x in jpeg_file.segments]

        if 'APP1' in markers:  # Put it after existing APP1
            index = markers.index('APP1') + 1
        elif 'APP0' in markers:  # Put it after existing APP0
            index = markers.index('APP0') + 1
        elif 'SOF' in markers:
            index = markers.index('SOF')
        else:
            raise ValueError("Could not find SOF marker")

        # Insert segment into JPEG file
        jpeg_file.segments.insert(index, xmp_segment)
        jpeg_file.write(image_out)

    elif is_png(image_in):

        xmp_chunk = PNGChunk()

        # Keyword
        xmp_chunk.data = b'XML:com.adobe.xmp'

        # Null separator
        xmp_chunk.data += b'\x00'

        # Compression flag
        xmp_chunk.data += b'\x00'

        # Compression method
        xmp_chunk.data += b'\x00'

        # Null separator
        xmp_chunk.data += b'\x00'

        # Null separator
        xmp_chunk.data += b'\x00'

        # Text
        xmp_chunk.data += xmp_packet

        # Set type
        xmp_chunk.type = b'iTXt'

        # Read in input file
        png_file = PNGFile.read(image_in)

        # Need to check there isn't alrady XMP meta-data

        # Insert chunk into PNG file
        png_file.chunks.insert(1, xmp_chunk)
        png_file.write(image_out)

    else:

        raise Exception("Only JPG and PNG files are supported at this time")
