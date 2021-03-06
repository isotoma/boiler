from setuptools import setup, find_packages
import os

version = '0.0.0dev'

setup(name='Boiler',
      version=version,
      url="http://yaybu.com/",
      description="Yaybu Boiler",
      long_description=open("README.rst").read(),
      author="Isotoma Limited",
      author_email="support@isotoma.com",
      license="Apache Software License",
      classifiers = [
          "Intended Audience :: System Administrators",
          "Operating System :: POSIX",
          "License :: OSI Approved :: Apache Software License",
      ],
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['yaybu'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'yaybu',
          'yay >= 0.0.24',
      ],
      entry_points = {
        "console_scripts": [
            'boil=yaybu.boiler.scripts.boil:run',
            'boiler=yaybu.boiler.scripts.boiler:run',
            ],
        "boiler.service": [
            "services = yaybu.boiler.services",
            ],
        "boiler.task": [
            "tasks = yaybu.boiler.tasks",
            ],
        }
      )

