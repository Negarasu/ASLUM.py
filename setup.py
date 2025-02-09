from setuptools import setup, find_packages

setup(
    name='ASLUM.py', 
    version='0.4',
    author='Negar Rahmatollahi, Zhihua Wang, Ting Sun, Yihang Wang',
    author_email='nrahmato@asu.edu',
    license='MIT',
    description='ASLUM.py: A Python package for urban canopy modeling',
    python_requires='>=3.8',
    
    package_dir={'': 'src'},  # Ensure it correctly finds packages in "src/"
    packages=find_packages(where='src'),  # Automatically finds all sub-packages

    install_requires=[
        'requests>=2.27.1',
        'numpy',  
        'scipy',
        'matplotlib'
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
            'ASLUM = ASLUMpy.main:main'  
        ]
    }
)
