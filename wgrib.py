import ctypes
import numpy as np


#cc -fPIC -shared -o c_library.so c_library.c

_c = ctypes.CDLL('wgrb.so')


LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)
_c.main.argtypes = (ctypes.c_int,LP_LP_c_char)


# argc = 2
# argv = (LP_c_char * (argc + 1))()
# enc_arg = '-V'.encode('utf-8')
# argv[0] = ctypes.create_string_buffer(enc_arg)
# enc_arg = './sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8')
# argv[1] = ctypes.create_string_buffer(enc_arg)

argc = 6
argv = (LP_c_char * (argc + 1))()

argv[1] = ctypes.create_string_buffer('-i'.encode('utf-8'))
argv[2] = ctypes.create_string_buffer('-text'.encode('utf-8'))
argv[3] = ctypes.create_string_buffer('./sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8'))
argv[4] = ctypes.create_string_buffer('-o'.encode('utf-8'))
argv[5] = ctypes.create_string_buffer('./sampledata/dump.out'.encode('utf-8'))

# print(_c.main(argc,argv))

_c.main(argc,argv)

# _c.gbr_reader('./sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8'))