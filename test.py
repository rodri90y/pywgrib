import ctypes

_sum = ctypes.CDLL('c_library.so')
_sum.our_function.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int))

def our_function(numbers):

    num_numbers = len(numbers)
    array_type = ctypes.c_int * num_numbers
    result = _sum.our_function(ctypes.c_int(num_numbers), array_type(*numbers))
    return int(result)



print(our_function([1,2,-3,4,-5,10]))