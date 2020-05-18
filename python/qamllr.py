#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 INATEL
# 
# Implementation of QAMLLR function
# Data: 15/07/2019
# Owner: Alex Rosa
# Organization: INATEL
# Project: QAM Demodulator/Modem 5G
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

from random import randrange
import numpy as np
import math

def qamllr(r, const, map, noisevar):

    const.shape = (len(const),1)
    noisevar.shape = (len(noisevar),1)
    r.shape = (len(r),1)

    M = len(const)
    mu = int(math.log(M,2))
    n = len(r)
   
    dist = abs(np.tile(r,(1,M)) - np.tile(np.transpose(const),(n,1)))

    idx_and_mins = [ min(enumerate(column), key=lambda x: x[1])  for column in zip(*dist.T) ]
    index = []    
    for idx in idx_and_mins:
	    index.append(idx[0])

    dist = dist**2
   
	# Hard Decision symbols 
    d_hat = []
    m_hat = []
    for i in index:
        m_hat.extend(const[i])
        d_hat.append(i)
    m_hat = np.transpose([m_hat])
    d_hat = np.transpose([d_hat])

	# Limit the noise variance to a minimum of 10^-5 (-50 dB)
    for i in range(len(noisevar)):
    	if noisevar[i] < 0.0001:
    		noisevar[i] = 0.00001
    #noisevar = noisevar.astype(float)
    
	# LLR Calculation
    exp_mat = (np.exp(-(noisevar**-1)*dist)).T
    llr = np.zeros((mu, n))

	###########################
    for pos in range(0,mu):
		# get specific rows from exp_mat based on bitvec result, only the positions where bitget is 1... and convert list variable to numpy array
    	result_matrix1 = np.asarray([exp_mat[i] for i in range(len((bitget(map,pos)==0))) if (bitget(map,pos)==0)[i]]) 
    	result_matrix2 = np.asarray([exp_mat[i] for i in range(len((bitget(map,pos)==1))) if (bitget(map,pos)==1)[i]]) 
    	llr[((mu-1)-pos),:] = ((np.log(result_matrix1.sum(axis=0))) - (np.log(result_matrix2.sum(axis=0))))

    llr = np.transpose([llr.transpose().flatten()])

    llr[np.isnan(llr)] = 0 # if any, NaN values set to zero
    llr[llr > +14] = +14   # Limit LLR Value (P0/P1 > 1.2e6)
    llr[llr < -14] = -14   # Limit LLR Value (P1/P0 > 1.2e6)
    
    b_hat = (llr < 0).astype(int)

    
    #return llr, m_hat, d_hat, b_hat
    return (m_hat.T, d_hat.T)

def bitget(map,pos):
	bitgetvec = []
	for m in map:
		bitgetvec.append((m >> pos) &1)
	bitgetvec = np.asarray(bitgetvec)
	return bitgetvec