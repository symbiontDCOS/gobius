# Goby Installer  
Goby is a dialog based ncurses application that installs Symbiont SlimOS.  It is the core component of the [netinstaller-oci](https://github.com/symbiontDCOS/netinstaller-osi) image.

## Building Goby  
We use the pants build system to make pex binary packages.  In fact, the pants executable is available right here in the repo!  To spin up a quick build do:

```
./pants package src/python/gobius:main
```

## Developing Goby  
Goby wraps bmaptool in a simple to use dialog application.  The main tools we use for this purpose are `flake8`, `mypy`, and `black`.  Color themes for goby 
are managed in [netinstaller-oci](https://github.com/symbiontDCOS/netinstaller-osi).



