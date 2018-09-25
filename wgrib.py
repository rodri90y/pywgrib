from ctypes import *
import numpy as np


#cc -fPIC -shared -o c_library.so c_library.c

class GBR_DATA(Structure):
    _fields_ = [('n', c_int),
                ('pos', c_int),
                ('datetime', c_char_p),
                ('shortName', c_char_p),
                ('name', c_char_p),
                ('typeOfLevel', c_char_p),
                ('level', c_int),
                ('nx', c_int),
                ('ny', c_int),
                ('values', POINTER(c_float))]




_c = CDLL('wgrb.so')


LP_c_char = POINTER(c_char)
LP_LP_c_char = POINTER(LP_c_char)
_c.main.argtypes = (c_int, LP_LP_c_char)


# argc = 2
# argv = (LP_c_char * (argc + 1))()
# enc_arg = '-V'.encode('utf-8')
# argv[0] = ctypes.create_string_buffer(enc_arg)
# enc_arg = './sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8')
# argv[1] = ctypes.create_string_buffer(enc_arg)

# argc = 6
# argv = (LP_c_char * (argc + 1))()
#
# argv[1] = create_string_buffer('-i'.encode('utf-8'))
# argv[2] = create_string_buffer('-text'.encode('utf-8'))
# argv[3] = create_string_buffer('./sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8'))
# argv[4] = create_string_buffer('-o'.encode('utf-8'))
# argv[5] = create_string_buffer('./sampledata/dump.out'.encode('utf-8'))

# print(_c.main(argc,argv))

# _c.main(argc,argv)


_c.gb_reader.argtypes = [c_char_p, c_int]
_c.gb_reader.restype = POINTER(GBR_DATA)
res = _c.gb_reader(create_string_buffer('./sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8')), 0)

print(res[0].pos)
# print(res.nx, res.ny)
# print(res.datetime)