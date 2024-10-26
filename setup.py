from os.path import dirname, join
from setuptools import setup, find_packages

# Project name
NAME = 'marchingcube'


setup(
    name=NAME,
    version=1.0,
    description="simple inmplement of marching cubes algorithm",
    author='Yi Gu',
    author_email='390512308@qq.com',
    license='License :: OSI Approved :: Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'pynrrd',
        'matplotlib',
        'tkinter',
        'scikit-image'
    ],
    entry_points={
        'console_scripts': [
		    'mc = marchingcube.main:main',
		],
    },
)