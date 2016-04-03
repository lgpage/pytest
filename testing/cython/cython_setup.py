

if __name__ == "__main__":
    import os
    import sys
    import glob
    from setuptools import setup, Extension

    cython_directives = {
        'embedsignature': True,  # needed to embed docstrings in ext module
        }

    try:
        sys.argv.remove("--use-cython")
        use_cython = True
    except ValueError:
        use_cython = False

    root = os.path.dirname(__file__)
    if use_cython:
        ext_files = glob.glob(os.path.join(root, 'src', '*.pyx'))
        ext_files.append(os.path.join(root, 'src', 'pure_py_module.py'))
    else:
        ext_files = glob.glob(os.path.join(root, 'src', '*.c'))

    extensions = []
    include_dirs = [os.path.abspath(os.path.join(root, 'clib'))]
    include_dirs.append(os.path.abspath(os.path.join(root, 'src')))
    for file_ in ext_files:
        dep_files = []
        pyx_file, ext = os.path.splitext(file_)
        pxd_file = os.path.join(pyx_file, ".pxd")
        if os.path.exists(pxd_file):
            dep_files.append(pxd_file)

        extensions.append(Extension(pyx_file, [file_],
                                    depends=dep_files,
                                    include_dirs=include_dirs))

    if use_cython:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext
        extensions = cythonize(extensions, force=True,
                               compiler_directives=cython_directives)
    else:
        from distutils.command.build_ext import build_ext

    setup(
        name="cythontests",
        version="0.1",
        description="build cython extension modules for pytest tests",
        ext_modules=extensions,
        cmdclass = {
            'build_ext': build_ext,
            }
        )
