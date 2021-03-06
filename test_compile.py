import py

from openscad_utils import *


temppath = py.test.ensuretemp('MCAD')

def pytest_generate_tests(metafunc):
    if "modpath" in metafunc.funcargnames:
        for fpath, modnames in collect_test_modules().items():
            os.system("cp %s %s/" % (fpath, temppath))
            if "modname" in metafunc.funcargnames:
                for modname in modnames:
                    metafunc.addcall(funcargs=dict(modname=modname, modpath=fpath))
            else:
                metafunc.addcall(funcargs=dict(modpath=fpath))


def test_module_compile(modname, modpath):
    tempname = modpath.basename + '-' + modname + '.scad'
    fpath = temppath.join(tempname)
    stlpath = temppath.join(tempname + ".stl")
    f = fpath.open('w')
    f.write("""
//generated testfile
use <%s>

%s();
""" % (modpath, modname))
    f.flush
    output = call_openscad(path=fpath, stlpath=stlpath, timeout=5)
    print output
    assert output[0] is 0
    assert "warning" or "error" not in output[2].strip().lowercase()
    assert len(stlpath.readlines()) > 2

def test_file_compile(modpath):
    stlpath = temppath.join(modpath.basename + "-test.stl")
    output = call_openscad(path=modpath, stlpath=stlpath)
    print output
    assert output[0] is 0
    assert "warning" or "error" not in output[2].strip().lowercase()
    assert len(stlpath.readlines()) == 2


