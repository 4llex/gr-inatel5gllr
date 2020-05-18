#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
from qamllr import qamllr

class qam_demod_top(gr.sync_block):
    """
    docstring for block qam_demod_top
    """
    def __init__(self, const, map, noisevar):
        self.const = const
        self.map = map
        self.noisevar = noisevar
        gr.sync_block.__init__(self,
            name="qam_demod_top",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64,
            numpy.float32]
            )
        


    def work(self, input_items, output_items):
        in0 = input_items[0] 
        out = output_items[0]
        out1 = output_items[1]

        self.const = numpy.asarray(self.const)
        self.noisevar = (numpy.asarray(self.noisevar))

        out[:], out1[:] = qamllr(in0[0: len(output_items[0])], self.const, self.map, self.noisevar)
        #output_items[0][:] = out.reshape(len(output_items[0]))
        
        #print output_items[0].shape # (4096,1)
        #print out.shape             # (4096,)
        
        #out1 = out1.astype(float)

        #print (type(out1))
        #print (out)
        
        return len(output_items[0])

