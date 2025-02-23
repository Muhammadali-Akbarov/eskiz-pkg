import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name='eskiz-pkg',
    version='1.5',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    url='https://github.com/Muhammadali-Akbarov/eskiz-pkg',
    keywords='eskiz sms smspy eskizuz eskiz-pkg sms-service smsuz',
    install_requires=[
        'requests',
        'pydantic'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
