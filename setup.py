from setuptools import setup

setup(
    name='oit-chatbot',
    packages=['oit_chatbot'],
    include_package_data=True,
    install_requires=[
        'flask',
        'textblob',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
