
from setuptools import setup, find_packages

setup(
    name = 'footyanalytics',
    version = '0.0.1',
    description = 'Python tools to process and visualize soccer event data',
    author = 'Siddhant Rao',
    packages = find_packages(),
    author_email = 'sr692@cornell.edu',
    install_requires = [
        'requests==2.21.0',
        'pandas==0.25.0',
        'numpy==1.15.40',
        'scikit-learn==0.20.1',
        'matplotlib==3.0.2',
        'xgboost==1.1.1'
    ]
    )
    
