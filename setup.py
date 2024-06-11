
from setuptools import setup, find_packages

setup(
    name='ASLUM.py',
    version='0.4',
    author='NegarRahmatollahi, ZhihuaWang, TingSun',
    author_email='nrahmato@asu.edu',
    license='MIT',
    description='Description of your package',
    python_requires='>=3.8',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests>=2.27.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': [
            'ASLUM.py = ASLUMpy.main:main'
        ]
    }
)
