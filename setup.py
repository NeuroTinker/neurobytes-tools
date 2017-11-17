from setuptools import setup

setup(
    name = "neurobytes",
    version = "0.17",
    description = "NeuroBytes Python Module and CLI",
    url = "https://github.com/NeuroTinker/neurobytes-python",
    author = "Jarod White",
    author_email = "jrwhite20@gmail.com",
    license = "GNU",
    packages = ["neurobytes", "neurobytes.interfaces", "neurobytes.firmware"],
    zip_safe = False,
    entry_points ={'console_scripts': ['neurobytes=neurobytes.cli:cli']},
    include_package_data=True,
    install_requires=[
        'click'
    ]
)
