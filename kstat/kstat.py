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
import libkstat


class Kstat():
    def __init__(self, module='', instance=-1, name=''):
        self._ctl = libkstat.kstat_open()
        self._module = module
        self._inst = instance
        self._name = name

    def __del__(self):
        libkstat.kstat_close(self._ctl)

    def __str__(self):
        s = 'Module: {0}, instance: {1}, name: {2}'.format(self._module, self._inst, self._name) 
        return s

    def __repr__(self):
        s = 'Kstat("{0}", {1}, "{2}")'.format(self._module, self._inst, self._name) 
        return s

    def lookup(self):
        libkstat.kstat_lookup(self._ctl, self._module, self._inst, self._name)

    def __getitem__(self, triplet):
        module, instance, name = triplet
        ksp = libkstat.kstat_lookup(self._ctl, module, instance, name)
	if not ksp:
            raise KeyError(triplet)
        libkstat.kstat_read(self._ctl, ksp, None)
        ks = ksp.contents
        if ks.ks_type == libkstat.KSTAT_TYPE_RAW:
            pass
        elif ks.ks_type == libkstat.KSTAT_TYPE_NAMED:
            value = dict()
            print ks.ks_data
            datap = C.cast(ks.ks_data, C.POINTER(libkstat.kstat_named))
            for i in range(ks.ks_ndata):
                print datap
                print datap.contents
                #print datap[i].contents
                value[datap[i].name] = 0
        elif ks.ks_type == libkstat.KSTAT_TYPE_INTR:
            pass
        elif ks.ks_type == libkstat.KSTAT_TYPE_IO:
            pass
        elif ks.ks_type == libkstat.KSTAT_TYPE_TIMER:
            pass
        else:
            pass

        return value

    def dump(self):
        kc = self._ctl.contents
        ksp = kc.kc_chain
        while ksp:
            ks = ksp.contents
            print ks.ks_module, ks.ks_instance, ks.ks_name, libkstat.kstat_type_names[ks.ks_type], ks.ks_class, ks.ks_ndata, ks.ks_data_size
            ksp = ks.ks_next
        pass 


class KstatValue():
    pass


class NamedKstat(KstatValue):
    def __init__(self):
        pass


def main():
    import pprint as pp
    k = Kstat()
    pp.pprint(k)
    #k.dump()
    pp.pprint(k[('unix', 0, 'kstat_types')])
    #k.lookup()


if __name__ == '__main__':
    main()
