import types
import array #use array for converting from string to list (struct is too slow)
import logging

try:
    import numpy
except:
    numpy = None

try:
    import Numeric
except:
    Numeric = None
    if numpy is None:
        logging.getLogger('SpecClient').warning('No Numeric arrays support, use Python array instead - cannot load Numeric')
        
(ARRAY_DOUBLE, ARRAY_FLOAT, ARRAY_LONG, ARRAY_ULONG, ARRAY_SHORT, \
 ARRAY_USHORT, ARRAY_CHAR, ARRAY_UCHAR, \
 ARRAY_STRING, ARRAY_NUMERIC) = (5,6,7,8,9,10,11,12,13,14)

(ARRAY_MIN, ARRAY_MAX) = (ARRAY_DOUBLE, ARRAY_STRING)

if numpy is not None:
    SPEC_TO_NUMPY = {
        ARRAY_CHAR   :  numpy.byte,
        ARRAY_UCHAR  :  numpy.ubyte,
        ARRAY_SHORT  :  numpy.short,
        ARRAY_USHORT :  numpy.ushort,
        ARRAY_LONG   :  numpy.int32,
        ARRAY_ULONG  :  numpy.uint32,
        ARRAY_FLOAT  :  numpy.float32,
        ARRAY_DOUBLE :  numpy.float64
        }

    NUMPY_TO_SPEC = {
        numpy.ubyte : ARRAY_CHAR,
        numpy.uint : ARRAY_ULONG,
        numpy.uint16 : ARRAY_USHORT,
        numpy.uint32 : ARRAY_ULONG,
        numpy.uint8 : ARRAY_CHAR,
        numpy.ushort : ARRAY_USHORT,
        numpy.short : ARRAY_SHORT,
        numpy.int32 : ARRAY_LONG,
        numpy.int8 : ARRAY_CHAR,
        numpy.float : ARRAY_FLOAT,
        numpy.float32 : ARRAY_FLOAT,
        numpy.float64 : ARRAY_DOUBLE
        }

NUMERIC_TO_SPEC = {
    '1' :  ARRAY_CHAR,
    'b' :  ARRAY_UCHAR,
    's' :  ARRAY_SHORT,
    'w' :  ARRAY_USHORT, #added
    'l' :  ARRAY_LONG,
    'u' :  ARRAY_ULONG, #added
    'f' :  ARRAY_FLOAT,
    'd' :  ARRAY_DOUBLE
    }

SPEC_TO_NUMERIC = {
    ARRAY_CHAR   :  '1',
    ARRAY_UCHAR  :  'b',
    ARRAY_SHORT  :  's',
    ARRAY_USHORT :  'w',  # was 's', Works with input array of type long
    ARRAY_LONG   :  'l',
    ARRAY_ULONG  :  'u',  # was 'l', Doesn't really work well
    ARRAY_FLOAT  :  'f',
    ARRAY_DOUBLE :  'd'
    }

ARRAY_TO_SPEC = {
    'b' :  ARRAY_CHAR,
    'B' :  ARRAY_UCHAR,
    'h' :  ARRAY_SHORT,
    'H' :  ARRAY_USHORT,
    'l' :  ARRAY_LONG,
    'L' :  ARRAY_ULONG,
    'i' :  ARRAY_LONG,
    'I' :  ARRAY_ULONG,
    'f' :  ARRAY_FLOAT,
    'd' :  ARRAY_DOUBLE
    }

SPEC_TO_ARRAY = {
    ARRAY_CHAR   :  'b',
    ARRAY_UCHAR  :  'B',
    ARRAY_SHORT  :  'h',
    ARRAY_USHORT :  'H',  
    ARRAY_LONG   :  'l',
    ARRAY_ULONG  :  'L',  
    ARRAY_FLOAT  :  'f',
    ARRAY_DOUBLE :  'd'
    }
    

class SpecArrayError(Exception):
    pass


def isArrayType(datatype):
    return type(datatype) == types.IntType and datatype >= ARRAY_MIN and datatype <= ARRAY_MAX


def SpecArray(data, datatype = ARRAY_CHAR, rows = 0, cols = 0):

    if isinstance(data, SpecArrayData):
        # create a SpecArrayData from a SpecArrayData ("copy" constructor)
        return SpecArrayData(data.data, data.type, data.shape)

    if datatype == ARRAY_STRING:
        # a list of strings
        newArray = filter(None, [x != chr(0) and x or None for x in data.split(chr(0))])
        return newArray
    else:
        newArray = None
        
    if numpy is not None or Numeric is not None:
        if(numpy is not None and type(data) == numpy.ndarray or
           Numeric is not None and type(data) == Numeric.ArrayType):
            # convert from a Numeric array to a SpecArrayData instance
            if len(data.shape) == 1:
                rows = 1
                cols = data.shape[0]
            elif len(data.shape) == 2:
                rows = data.shape[0]
                cols = data.shape[1]
            else:
                raise SpecArrayError, "Spec arrays cannot have more than 2 dimensions"

            try:
                if(numpy is not None and type(data) == numpy.ndarray) :
                    numtype = data.dtype.type
                    datatype = NUMPY_TO_SPEC[numtype]
                else:
                    numtype = data.typecode()
                    datatype = NUMERIC_TO_SPEC[numtype]
            except KeyError:
                data = ''
                datatype = ARRAY_CHAR
                rows = 0
                cols = 0
                logging.getLogger('SpecClient').error("Numerical type '%s' not supported" , numtype)
            else:
                if len(data.shape) == 2:
                    rows, cols = data.shape
                else:
                    rows,cols = data.shape[0],1
                data = data.tostring() #astype(datatype).tostring()
            
            newArray = SpecArrayData(data, datatype, (rows, cols))
        else:
            # return a new array from data
            try:
                if numpy: numtype = SPEC_TO_NUMPY[datatype]
                else: numtype = SPEC_TO_NUMERIC[datatype]
            except:
                raise SpecArrayError, 'Invalid Spec array type'
            else:
                if numpy:
                    newArray = numpy.fromstring(data, dtype=numtype)
                else:
                    data = array.array(SPEC_TO_ARRAY[datatype], data).tolist()
                    newArray = Numeric.array(data, typecode=numtype, savespace=1)
    else:
        if isArrayType(datatype):
            newArray = SpecArrayData(data, datatype)
        else:
            raise SpecArrayError, 'Invalid Spec array type'

    if newArray is not None:
        if (rows == 1):
            newArray.shape = (cols, ) #Spec convention
        else:
            newArray.shape = (rows, cols)

    return newArray


class SpecArrayData:
    def __init__(self, data, datatype, shape):
        self.data = data
        self.type = datatype
        self.shape = shape


    def tostring(self):
        return str(self.data)














