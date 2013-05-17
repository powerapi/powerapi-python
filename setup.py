try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='powerapi-python',
    version='0.1.1',
    description='Python API for PowerSchool',
    url='https://github.com/powerapi/powerapi-python',
    author='Henri Watson',
    author_email="henri@henriwatson.com",
    license='MIT',
    keywords='powerschool',
    packages=['powerapi'],
    zip_safe=False,
    install_requires=[
        'requests'
    ]
)

