[![CI Unit Test](https://github.com/symbiontDCOS/gobius/actions/workflows/actions.yml/badge.svg)](
https://github.com/symbiontDCOS/gobius/actions/workflows/actions.yml)


# Goby Installer  
Goby is a dialog based ncurses application that installs Symbiont SlimOS.  It is the core component of the
[netinstaller-oci](https://github.com/symbiontDCOS/netinstaller-osi) image.

## Building Goby  
We use the pants build system to make pex binary packages.  In fact, the pants executable is available right here in
the repo!  To spin up a quick build do:

```
./pants package src/python/gobius:goby
```

## Developing Goby  
The main tools we use for this purpose are `pants`, `flake8`, `mypy`, and `black`.  Color themes for goby are managed
in [netinstaller-oci](https://github.com/symbiontDCOS/netinstaller-osi).



