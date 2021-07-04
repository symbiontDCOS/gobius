from setuptools import setup, find_packages

setup(
    name="gobius",
    version="2107rc1",
    description="SymbiontDCOS Installer",
    url="https://github.com/symbiontDCOS/gobius",
    maintainer="Robert Callicotte",
    maintainer_email="symbiont-devel@symbiont.org",
    license="MIT",
    python_requires=">=3.7",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gobius = gobius.main:main',
            ],
        },
)
