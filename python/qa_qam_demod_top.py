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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from qam_demod_top import qam_demod_top
from numpy import array

class qa_qam_demod_top (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_QPSK (self):
        src_data = (0.98-1.02j, 1.03+1.2j, 0.9-1.08j, -1.1+1.1j)
        const = (-1+1j, -1-1j, 1+1j, 1-1j)
        map = (0, 1, 2, 3)
        noisevar = array([0.1])

        expected_const = (1-1j, 1+1j, 1-1j, -1+1j)
        expected_decimal = (3, 2, 3, 0)

        src = blocks.vector_source_c (src_data)

        qamllr = qam_demod_top (const, map, noisevar)

        dst = blocks.vector_sink_c ()
        dst2 = blocks.vector_sink_f ()

        self.tb.connect (src,qamllr)
        self.tb.connect ((qamllr,0), (dst,0))
        self.tb.connect ((qamllr,1), (dst2,0))
        self.tb.run ()

        # check data
        result_data = dst.data ()
        result_data2 = dst2.data ()
        self.assertFloatTuplesAlmostEqual (expected_const, result_data)
        self.assertFloatTuplesAlmostEqual (expected_decimal, result_data2)

    def test_002_16QAM (self):
        src_data = (-3.2+3.1j, -2.9+1.09j, -3.4-3.1j, -3.5-1.2j,
                    -1.1+3.3j, -1.9+2.02j, -1-3j, -1.6-1.1j, 
                    2.8+3.2j, 2.9+1.3j, +3-3j, 3-1j,
                    1+3j, 1+1j, 1-3j, 1-1j)
        const = (-3+3j, -3+1j, -3-3j, -3-1j,
                 -1+3j, -1+1j, -1-3j, -1-1j,
                  3+3j, 3+1j, +3-3j, 3-1j,
                  1+3j, 1+1j, 1-3j, 1-1j)
        map = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        noisevar = array([0.1])

        expected_const = (-3+3j, -3+1j ,-3-3j, -3-1j, 
                          -1+3j, -1+3j, -1-3j, -1-1j,
                           3+3j,  3+1j,  3-3j,  3-1j,
                           1+3j,  1+1j,  1-3j,  1-1j)
        expected_decimal = (0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

        src = blocks.vector_source_c (src_data)

        qamllr = qam_demod_top (const, map, noisevar)

        dst = blocks.vector_sink_c ()
        dst2 = blocks.vector_sink_f ()

        self.tb.connect (src,qamllr)
        self.tb.connect ((qamllr,0), (dst,0))
        self.tb.connect ((qamllr,1), (dst2,0))
        self.tb.run ()

        # check data
        result_data = dst.data ()
        result_data2 = dst2.data ()
        self.assertFloatTuplesAlmostEqual (expected_const, result_data)
        self.assertFloatTuplesAlmostEqual (expected_decimal, result_data2)
        
    

if __name__ == '__main__':
    gr_unittest.run(qa_qam_demod_top, "qa_qam_demod_top.xml")
