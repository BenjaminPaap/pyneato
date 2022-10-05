# pyneato

Python package to control a Neato vacuum robot 
managed via MyNeato app (starting from D8).

This package was mostly developed in order to control
a vacuum robot through [Home Assistant](https://www.home-assistant.io/).

This package is currently far from being finished. Contributions are welcome. 

## Usage

Use the sample script for a short introduction on
how to use this package.

Create a `.passwd` file containing your MyNeato password and
execute this command on the cli:

```bash
MYNEATO_USER=<YOUR_USERNAME> MYNEATO_PASSWORD=`cat .passwd` python pyneato/sample/sample.py
```

## Thanks

Thanks to @stianaske for his work on [pybotvac](https://github.com/stianaske/pybotvac). This
package is highly inspired by pybotvac because I don't really know much about python but wanted
to give it a shot.
