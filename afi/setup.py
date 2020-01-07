import setuptools

with open('README.md') as f:
	extd_desc = f.read()

setuptools.setup(
	name = 'afi',
	license = 'MIT',
	version = '0.0.2',
	packages = ['afi'],
	package_dir={'afi': './'},
	long_description = extd_desc,
	author='Supratik Chatterjee',
	author_email = 'supratikdevm96@gmail.com',
	description = 'Automatic File Identifier',
	keywords= 'extensions signatures filehandling file identification',
	install_requires=['requests','urllib3','bs4'],
	entry_points = {'console_scripts': ['afi = afi:main'],},
	project_urls = {'Source' : 'https://github.com/supratikchatterjee16/afi', 
					'Issues' : 'https://github.com/supratikchatterjee16/afi/issues'},
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
