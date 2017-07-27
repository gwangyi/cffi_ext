from setuptools import setup

setup(
    name="cffi_ext",
    description="definition extractor for cffi",
    license="MIT",
    version="0.1",
    author="Sungkwang Lee",
    maintainer="Sungkwang Lee",
    author_email="gwangyi.kr@gmail.com",
    packages=["cffi_ext"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['cffi>=1.0.0', 'pycparserlibc'],
    dependency_links=[
        "git+https://github.com/gwangyi/pycparserlibc/#egg=pycparserlibc-0"
    ],
)
