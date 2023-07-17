from setuptools import setup
import imp


with open('README.md') as file:
    long_description = file.read()

version = imp.load_source('epic_kitchens_united.version', 'epic_kitchens_united/version.py')

setup(
    name='epic_kitchens_united',
    version=version.version,
    description='python package designed to merge two CSV (EPIC KITCHENS, EPIC SOUNDS) files into a single file while organizing the combined data based on timestamp',
    author='Lauren N. Pryor', 
    author_email='lpryor@caltech.edu',
    url='',
    download_url='https://github.com/iranroman/epic-kitchens-united',
    packages=['epic_kitchens_united'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='csv timestamp EPIC KITCHENS EPIC SOUNDS audio video audiovisual',
    license='Creative Commons Attribution',
    classifiers=[
            "License :: Creative Commons Attribution 4.0",
            "Programming Language :: Python",
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Topic :: Multimedia :: Sound/Audio :: Analysis",
            "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        ],
    install_requires=[
        'numpy>=1.24.4',
        'matplotlib',
        'pandas',
        'tqdm'
    ],
)