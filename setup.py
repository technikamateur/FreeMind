from setuptools import setup

setup(
    name='FreeMind',
    packages=['FreeMind'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'apscheduler'
    ],
)
