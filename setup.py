from setuptools import setup

setup(
    name = "neurobytes",
    version = "0.20",
    description = "NeuroBytes Python Module and CLI",
    url = "https://github.com/NeuroTinker/neurobytes-python",
    author = "Jarod White",
    author_email = "jarod@neurotinker.com",
    license = "GNU",
    packages = ["neurobytes", "neurobytes.interfaces", "neurobytes.firmware"],
    zip_safe = False,
    entry_points ={'console_scripts': ['neurobytes=neurobytes.cli:cli']},
    include_package_data=True,
    install_requires=[
        'click',
        'numpy==1.8.2',
        'matplotlib==1.4.2',
        'six==1.9'
    ]
)
