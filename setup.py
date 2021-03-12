try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'name': 'F477_legacy_maker',
	'description': 'This system creates "ANY" and "LTE" coverages within the legacy supported area and reports the coverage at block group level',
	'author': "Murtaza NASAFI",
	'e-mail': "murtaza.nasafi@fcc.gov",
	'version': '0.1dev',
	'license': 'Creative Commons Attribution-Noncommercial-Share Alike license',
	'install_requires': ['nose', 'arcpy', 'pandas', 'zipfile', 'shutil', 'fnmatch'],
	'packages': ['tests', 'F477_legacy_maker', 'bin',]

}

setup(**config)