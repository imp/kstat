#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Copyright 2011 Grigale Ltd. All rigths reserved.
# Use is sujbect to license terms.
#
import ctypes as C


KSTAT_TYPE_RAW = 0
KSTAT_TYPE_NAMED = 1
KSTAT_TYPE_INTR = 2
KSTAT_TYPE_IO = 3
KSTAT_TYPE_TIMER = 4

kstat_type_names = {
    KSTAT_TYPE_RAW: 'raw', KSTAT_TYPE_NAMED: 'named',
    KSTAT_TYPE_INTR: 'intr', KSTAT_TYPE_IO: 'io', KSTAT_TYPE_TIMER: 'timer'
    }

KSTAT_STRLEN = 31

hrtime_t = C.c_longlong
kid_t = C.c_int
kstat_string = C.c_char * KSTAT_STRLEN

class kstat(C.Structure):
    pass

kstat_p = C.POINTER(kstat)

kstat._fields_ = [
    ('ks_crtime', hrtime_t),
    ('ks_next', kstat_p),
    ('ks_kid', kid_t),
    ('ks_module', kstat_string),
    ('ks_resv', C.c_ubyte),
    ('ks_instance', C.c_int),
    ('ks_name', kstat_string),
    ('ks_type', C.c_ubyte),
    ('ks_class', kstat_string),
    ('ks_flags', C.c_ubyte),
    ('ks_data', C.c_void_p),
    ('ks_ndata', C.c_uint),
    ('ks_data_size', C.c_size_t),
    ('ks_snaptime', hrtime_t),

    ('ks_update', C.c_void_p),
    ('ks_private', C.c_void_p),
    ('ks_snapshot', C.c_void_p),
    ('ks_lock', C.c_void_p)
]


#/*
# * kstat_open() returns a pointer to a kstat_ctl_t.
# * This is used for subsequent libkstat operations.
# */
#typedef struct kstat_ctl {
#        kid_t   kc_chain_id;    /* current kstat chain ID       */
#        kstat_t *kc_chain;      /* pointer to kstat chain       */
#        int     kc_kd;          /* /dev/kstat descriptor        */
#} kstat_ctl_t;

class kstat_ctl(C.Structure):
    _fields_ = [
        ('kc_chain_id', kid_t),
        ('kc_chain', C.POINTER(kstat)),
        ('kc_kd', C.c_int)
    ]


#typedef struct kstat_named {
#        char    name[KSTAT_STRLEN];     /* name of counter */
#        uchar_t data_type;              /* data type */
#        union {
#                char            c[16];  /* enough for 128-bit ints */
#                int32_t         i32;
#                uint32_t        ui32;
#                struct {
#                        union {
#                                char            *ptr;   /* NULL-term string */
#                                char            __pad[8]; /* 64-bit padding */
#                        } addr;
#                        uint32_t        len;    /* # bytes for strlen + '\0' */
#                } str;
#/*
# * The int64_t and uint64_t types are not valid for a maximally conformant
# * 32-bit compilation environment (cc -Xc) using compilers prior to the
# * introduction of C99 conforming compiler (reference ISO/IEC 9899:1990).
# * In these cases, the visibility of i64 and ui64 is only permitted for
# * 64-bit compilation environments or 32-bit non-maximally conformant
# * C89 or C90 ANSI C compilation environments (cc -Xt and cc -Xa). In the
# * C99 ANSI C compilation environment, the long long type is supported.
# * The _INT64_TYPE is defined by the implementation (see sys/int_types.h).
# */
##if defined(_INT64_TYPE)
#                int64_t         i64;
#                uint64_t        ui64;
##endif
#                long            l;
#                ulong_t         ul;
#
#                /* These structure members are obsolete */
#
#                longlong_t      ll;
#                u_longlong_t    ull;
#                float           f;
#                double          d;
#        } value;                        /* value of counter */
#} kstat_named_t;

KSTAT_DATA_CHAR = 0
KSTAT_DATA_INT32 = 1
KSTAT_DATA_UINT32 = 2
KSTAT_DATA_INT64 = 3
KSTAT_DATA_UINT64 = 4
KSTAT_DATA_STRING = 9

class addr_union(C.Union):
    _fields_ = [
        ('ptr', C.c_char_p),
        ('__pad', C.c_char * 8),
    ]


class str_struct(C.Structure):
    _fields_ = [
        ('addr', addr_union),
        ('len', C.c_uint32),
    ]


class value_union(C.Union):
    _fields_ = [
        ('c', C.c_char * 16),
	('i32', C.c_int32),
	('ui32', C.c_uint32),
	('i64', C.c_int64),
	('ui64', C.c_uint64),
    ]


class kstat_named(C.Structure):
    _fields_ = [
        ('name', kstat_string),
        ('data_type', C.c_ubyte),
        ('value', value_union),
    ]


_libkstat = C.CDLL('libkstat.so.1')

kstat_ctl_p = C.POINTER(kstat_ctl)

kstat_open = _libkstat.kstat_open
kstat_open.argtypes = []
kstat_open.restype = kstat_ctl_p


kstat_close = _libkstat.kstat_close
kstat_close.argtypes = [kstat_ctl_p]


kstat_read = _libkstat.kstat_read
kstat_read.argtypes = [kstat_ctl_p, kstat_p, C.c_void_p]
kstat_read.restype = kid_t


kstat_write = _libkstat.kstat_write
kstat_write.argtypes = [kstat_ctl_p, kstat_p, C.c_void_p]
kstat_write.restype = kid_t


kstat_chain_update = _libkstat.kstat_chain_update
kstat_chain_update.argtypes = [kstat_ctl_p]
kstat_chain_update.restype = kid_t


kstat_lookup = _libkstat.kstat_lookup
kstat_lookup.argtypes = [kstat_ctl_p, C.c_char_p, C.c_int, C.c_char_p]
kstat_lookup.restype = kstat_p


kstat_data_lookup = _libkstat.kstat_data_lookup
kstat_data_lookup.argtypes = [kstat_p]
kstat_data_lookup.restype = C.c_void_p

