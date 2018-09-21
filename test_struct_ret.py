from ctypes import *


lib_name = 'libs/c_library_struct_ret.so'
test_lib = CDLL(lib_name)

class POINT(Structure):
    _fields_ = [('x', c_int),
                ('y', POINTER(c_float))]

test_lib.get_point.restype = c_void_p

p1 = POINT.from_address( test_lib.get_point())

print (p1.x, p1.y[:4])



test_lib.free_point(byref(p1))
del p1