#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 18:12:04 2022

@author: tj_hou
"""

import argparse
import LS1
import Approx
import BnB
import LS2

if __name__ == '__main__':

	parser=argparse.ArgumentParser(description='Wrapper Function for Vertex Cover Graphs')
	parser.add_argument('-inst',action='store',type=str,required=True,help='Input graph datafile')
	parser.add_argument('-alg',action='store',type=str,required=True,help='Input Alg  [BnB|Approx|LS1|LS2]')
	parser.add_argument('-time',action='store',default=600,type=float,required=False,help='Cutoff running time (s)')
	parser.add_argument('-seed',action='store',default=1000,type=int,required=False,help='Random Seed for algorithm')	
	args=parser.parse_args()
    
if args.alg == 'Approx':
    Approx.main(args.inst,args.seed,args.time)
            
elif args.alg == 'LS1':
    LS1.main(args.inst,args.seed,args.time) 

elif args.alg == 'BnB':
    BnB.main(args.inst,args.seed,args.time) 
    
elif args.alg == 'LS2':
    LS2.main(args.inst,args.seed,args.time)
                
else:
    print('Inputted incorrect algorithm option, please try any of: [BnB|Approx|LS1|LS2]')