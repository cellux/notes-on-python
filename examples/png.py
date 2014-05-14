import mmap, struct, contextlib, zlib

class PNGError(Exception):
    pass

def process_png_chunks(path, process_cb):
    with open(path) as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        with contextlib.closing(mm) as data:
            if data[0:8] != bytearray([137,80,78,71,13,10,26,10]):
                raise PNGError("Invalid PNG signature")
            pos = 8
            while pos < len(data):
                chunk_length = int(struct.unpack('>L', data[pos:pos+4])[0])
                chunk_type = data[pos+4:pos+8]
                chunk_data = buffer(data, pos+8, chunk_length)
                chunk_crc = int(struct.unpack('>L', data[pos+8+chunk_length:pos+8+chunk_length+4])[0])
                crc = zlib.crc32(chunk_type)
                crc = zlib.crc32(chunk_data, crc)
                if crc < 0: crc = (1<<32) + crc
                if chunk_crc != crc:
                    raise PNGError("Invalid CRC in PNG file, in file={0:X}, expected={1:X}".format(chunk_crc, crc))
                process_cb(chunk_type, chunk_data)
                pos = pos+4+4+chunk_length+4

def print_chunk_info(chunk_type, chunk_data):
    print "chunk: type={}, len={}".format(chunk_type, len(chunk_data))

process_png_chunks('/home/rb/Projects/mtpk/httpdocs/modules/overlay/images/close.png', print_chunk_info)
