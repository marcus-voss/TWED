from distutils.core import setup, Extension
import numpy
# define the extension module
TWED = Extension('TWED', sources=['TWED.c'], include_dirs=[numpy.get_include()])

# run the setup
setup(
	name="twed",
	license="MIT",
	author="Pierre-Francois Marteau",
	ext_modules=[TWED],
	url = 'https://github.com/pfmarteau/TWED'
)