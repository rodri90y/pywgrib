from ctypes import *
import numpy as np
from packstorm.modeltools import ModelApi

# cc -fPIC -shared -o c_library.so c_library.c


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
                ('p1', c_int),
                ('p2', c_int),
                ('time_unit', c_int),
                ('time_range', c_int),
                ('projection', c_char_p),
                ('coordinates', c_float * 4),
                ('dxdy', c_float * 2),
                ('values', POINTER(c_float))]


_c = CDLL('libs/wgrb.so')
msg_size = c_int(10)
_c.gb_reader.argtypes = [c_char_p, POINTER(c_int), c_int]
_c.gb_reader.restype = POINTER(GBR_DATA)

class GribMessage:
    def __init__(self):
        self.n = None
        self.pos = None
        self.parmID = None
        self.center = None
        self.subcenter = None
        self.model = None
        self.datatype = None
        self.datetime = None
        self.timeref = None
        self.shortName = None
        self.name = None
        self.typeOfLevel = None
        self.level = list()
        self.nx = None
        self.ny = None
        self.p1 = None
        self.p2 = None
        self.time_unit = None
        self.time_range = None
        self.projection = None
        self.coordinates = None
        self.dxdy = None
        self.values = None
        self.raw_msg = None

        self.vars = [x for x in dir(self) if '__' not in x]

    def __str__(self):
        _string = self.__dict__
        del _string['raw_msg'], _string['vars']
        return str(string)
    
    def __getitem__(self, key):
        if key in self.vars:
            return getattr(self, key, None)
        else:
            return None
        
    def __setitem__(self, key, value):
        if key in dir(self):
            setattr(self, key, value)

    def to_dict(self):
        ret_dict = self.__dict__
        del ret_dict['vars'], ret_dict['raw_msg']
        return ret_dict

    
class GribApi:

    def __init__(self, path, verbose=False):
        self.verbose = verbose
        self.path = path
        self.variables = None
        self.latitude = None
        self.longitude = None
        self.variables = list()
        self.shape = None
        self.data = dict()
        self.time = list()
        self.time_units = None
        self.LATITUDE_FIELD = ['LAT', 'XLAT', 'NLAT']
        self.LONGITUDE_FIELD = ['LON', 'XLON', 'ELON']
        self.messages = None
        self.data = self.load_data(path)
        


    def load_data(self, path):
        '''Load a dictionary with grib messages with variable shortname as a key, 
        in value is used a GribMessage object to store the info
        
        Arguments:
            path {path} -- the path to the grib file
        
        Returns:
            dict -- Key: variable, value: GribMessage
        '''

        
        res = _c.gb_reader(create_string_buffer(path.encode('utf-8')), msg_size, 0)
        self.messages = res
        try:
            res.contents
        except ValueError:
            print('[A] Something wrong with file, check manually!')
            return None

        tmp = dict()
        for i in range(msg_size.value-1):
            if self.latitude is None:
                self.latitude = np.linspace(res[i].coordinates[0], res[i].coordinates[2], num=res[i].ny)
            if self.longitude is None:
                self.longitude = np.linspace(res[i].coordinates[1], res[i].coordinates[3], num=res[i].nx)

            if self.time_units is None:
                if 'hr' in res[i].timeref.decode('utf-8'):
                    date_time = res[i].datetime.decode('utf-8')
                    self.time_units = f'hours since {date_time}'

            if not self.time:
                self.time.append(res[i].p1)

            var = res[i].shortName.decode('utf-8').lower()
            lvlType = res[i].typeOfLevel.decode('utf-8')
            if 'hybrid' in lvlType:
                var = var + 'h{lev}'.format(lev=res[i].level)
            elif '2 m' in lvlType:
                var = var + '2m'
            elif '10 m' in lvlType:
                var = var + '10m'
            
            elif 'high trop' in lvlType:
                var = var + 'htf'
            elif 'tropopause' in lvlType:
                var = var + 'trpp'
            elif 'isotherm' in lvlType:
                var = var + 'isthrm'
            elif 'sfc' in lvlType:
                var = var + 'sfc'
            elif '0-10 cm' in lvlType:
                var = var + '0_10cm'
            elif '10-40 cm' in lvlType:
                var = var + '10_40cm'
            elif '40-100 cm' in lvlType:
                var = var + '40_100cm'
            elif '100-200 cm' in lvlType:
                var = var + '100_200cm'
            elif '30-0 mb' in lvlType:
                var = var + '30_0mb'
            elif '300 cm' in lvlType:
                var = var + '300cm'
            elif '180-0 mb' in lvlType:
                var = var + '180_0mb'
            elif '90-0 mb' in lvlType:
                var = var + '90_0mb'
            elif '255-0 mb' in lvlType:
                var = var + '255_0mb'
            elif '500-1000 mb' in lvlType:
                var = var + '500_1000mb'
            elif '0-3000 m' in lvlType:
                var = var + '0_3000m'
            elif '3000-0 m' in lvlType:
                var = var + '3000_0m'
            elif '0-100 cm' in lvlType:
                var = var + '0_100cm'
            elif 'cld top' in lvlType:
                var = var + 'clt'
            elif 'cloud ceiling' in lvlType:
                var = var + 'clceil'
            elif 'cld base' in lvlType:
                var = var + 'clbase'

            if self.verbose:
                print(res[i].n, res[i].shortName.decode('utf-8'), res[i].name.decode('utf-8'), 
                       res[i].typeOfLevel.decode('utf-8'), res[i].level, var)

            if var in tmp:
                tmp[var].level.append(res[i].level)

                if tmp[var].values.ndim == 2:
                    dump = np.ones((2,tmp[var].ny, tmp[var].nx)) * np.nan

                    dump[0] = tmp[var].values
                    dump[1] = np.ctypeslib.as_array(res[i].values, shape=(ny, nx))
                    tmp[var].values = dump
                else:
                    dump = np.ones((1, tmp[var].ny, tmp[var].nx)) * np.nan
                    dump[0] = np.ctypeslib.as_array(res[i].values, shape=(ny, nx))
                    tmp[var].values = np.concatenate((tmp[var].values, dump))
                                    
            else:
                
                self.variables.append(var)
                tmp[var] = GribMessage()
                tmp[var].raw_msg = res[i]
                for key, typ in GBR_DATA._fields_:
                    
                    nx, ny = res[i].nx, res[i].ny
                    v = getattr(res[i], key)

                    if type(typ) == type(c_float*1):
                        v = np.array(v)

                    elif type(typ) == type(POINTER(c_float)):
                        v = np.ctypeslib.as_array(v, shape=(ny, nx))
                    
                    elif typ == c_char_p:
                        v = v.decode('utf-8')

                    if key != 'level': 
                        setattr(tmp[var], key, v)
                    else:
                        tmp[var].level.append(v)       
 
        return tmp

    def __get_netcdf_var(self, style, n):
        for k, v in style.items():
            if n in v:
                return k
        return None

    def close(self):
        
        _c.free_file(byref(self.messages))


    def to_dict(self):
        ret_dict = {k: v.to_dict() for k, v in self.data.items()}
        return ret_dict

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    
    def __getattr__(self, key):
        if key in self.data:
            return self.__getitem__(key)
        elif key in self.__dict__:
            return self.__dict__[key]
        






