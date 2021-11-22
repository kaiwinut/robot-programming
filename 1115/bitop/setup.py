from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
	Extension("bitboard",
				["bitboard.pyx", "bitop.c"],
				libraries = ["m"])
]

setup(
	name = "ffi cython test",
	cmdclass = {"build_ext": build_ext},
	ext_modules = ext_modules
)