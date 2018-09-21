#!/usr/bin/env python

import ctypes

_c = ctypes.CDLL('libs/c_library_str_ret.so')


class STR(ctypes.Structure):
  _fields_ = [
    ('sentence', ctypes.c_char_p),
    ('nb_points', ctypes.c_int)
  ]



_c.increment_string.argtypes = [ctypes.c_char_p, ctypes.c_int]
_c.increment_string.restype = ctypes.c_char_p



ptr_test = ctypes.pointer(STR(**{'sentence':"A nice sentence to test.".encode('utf-8'),'nb_points':0}))
print(ptr_test.contents.sentence)

ptr_test.contents.sentence = _c.increment_string(ptr_test.contents.sentence, 2)
ptr_test.contents.sentence = _c.increment_string(ctypes.c_char_p("A nice sentence to test.".encode('utf-8')),
                                                 ctypes.c_int(2))
print(ptr_test.contents.sentence)

