from setuptools import setup, find_packages
import csv2influx

test_require = []

install_requires = [
    'docopt==0.6.2',
    'pandas==0.24.2',
    'influxdb==5.2.3'
]

setup(
    name=csv2influx.__name__,
    version=csv2influx.__version__,
    long_description=csv2influx.__description__,
    keywords="CSV InfluxDB Visualizard",
    url="https://github.com/matteobogo/csv2influx-visualizard-companion",
    author=csv2influx.__author__,
    author_email=csv2influx.__email__,
    license=csv2influx.__license__,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=test_require,
)