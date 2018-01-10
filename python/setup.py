from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext


class cython_build_ext(build_ext):
    def finalize_options(self):
        if self.distribution.ext_modules:
            nthreads = getattr(self, 'parallel', None)  # -j option in Py3.5+
            nthreads = int(nthreads) if nthreads else None
            from Cython.Build.Dependencies import cythonize
            self.distribution.ext_modules[:] = cythonize(
                self.distribution.ext_modules, nthreads=nthreads, force=self.force)
        build_ext.finalize_options(self)

cmdclass = {
    'build_ext': cython_build_ext
}

ext = Extension(
    'squish',
    ['squish.pyx'],
    include_dirs=['..'],
    library_dirs=['..'],
    libraries=['squish'],
    extra_link_args=['-fPIC'],
    language='c++',
)

setup(
    name='squish',
    version='1.0',
    author='Mathieu Virbel',
    author_email='mat@kivy.org',
    url='http://txzone.net/',
    license='LGPL',
    description='Python binding for libsquish',
    ext_modules=[ext],
    cmdclass=cmdclass,
    setup_requires=['Cython']
)
