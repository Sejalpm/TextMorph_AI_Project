from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Text_Morph',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Jeevan HS',
    author_email='jeevang1405@gmail.com',
    description='Advanced Text Summarization and Paraphrasing Project',
    python_requires='>=3.10',
)