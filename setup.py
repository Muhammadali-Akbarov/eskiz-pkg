from setuptools import setup, find_packages


setup(
    name='eskiz-pkg',
    version='1.3',
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
)
