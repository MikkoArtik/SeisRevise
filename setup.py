from setuptools import setup
from setuptools import find_packages

setup(name='SeisRevise',
      version='1.0.5',
      packages=find_packages(),
      description='Package for processing of microseismic data',
      author='Michael Chernov',
      author_email='mikkoartic@gmail.com',
      license='MIT',
      include_package_data=True,
      zip=False,
)
# install_requires = [
#       'SeisCore@git+https://github.com/MikkoArtik/SeisCore.git@dev#egg=SeisCore',
# ]