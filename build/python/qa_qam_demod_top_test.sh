#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/alexrosa/Documentos/GNURADIO/5gIoT/gr-inatel5gllr/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/alexrosa/Documentos/GNURADIO/5gIoT/gr-inatel5gllr/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/alexrosa/Documentos/GNURADIO/5gIoT/gr-inatel5gllr/build/swig:$PYTHONPATH
/usr/bin/python2 /home/alexrosa/Documentos/GNURADIO/5gIoT/gr-inatel5gllr/python/qa_qam_demod_top.py 
