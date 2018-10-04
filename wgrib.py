from ctypes import *
import numpy as np


#cc -fPIC -shared -o c_library.so c_library.c

class GBR_DATA(Structure):
    _fields_ = [('n', c_int),
                ('pos', c_int),
                ('parmID', c_int),
                ('center', c_int),
                ('subcenter', c_int),
                ('model', c_int),
                ('datatype', c_int),
                ('datetime', c_char_p),
                ('timeref', c_char_p),
                ('shortName', c_char_p),
                ('name', c_char_p),
                ('typeOfLevel', c_char_p),
                ('level', c_int),
                ('nx', c_int),
                ('ny', c_int),
                ('projection', c_char_p),
                ('coordinates', c_float * 4),
                ('dxdy', c_float * 2),
                ('values', POINTER(c_float))]




_c = CDLL('wgrb.so')

msg_size = c_int(10)

_c.gb_reader.argtypes = [c_char_p, POINTER(c_int), c_int]
_c.gb_reader.restype = POINTER(GBR_DATA)
res = _c.gb_reader(create_string_buffer('./sampledata/WRFPRS_d01.2018090407.grib1'.encode('utf-8')), msg_size, 0)


for i in range(msg_size.value-1):

    nxny = res[i].nx * res[i].ny

    for key, typ in GBR_DATA._fields_:

        v = getattr(res[i], key)

        if type(typ) == type(c_float*1):
            v = np.array(v)

        if type(typ) == type(POINTER(c_float)):
            v = np.ctypeslib.as_array(v,shape=(nxny,))

        print("{0}: {1}".format(key,v))


    print()

