#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Julia Coxen
SI507. Disucssion 001: Tuesdays 4pm
"""

#import csv
import pandas as pd
import glob
import os


def collect_RubRatings_data():
#   walks through directory    
    os.chdir('/Users/julia 1/Desktop/FinalProject/UPLOADtoGIT')
    
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
#   combine all files in the list
    combined_csv= pd.DataFrame().append([pd.read_csv(f, low_memory=False) for f in all_filenames ], sort = False)
#    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], sort = False)
    
    #export to csv  
    combined_csv.to_csv( "RR_combined.csv", index=False, encoding='utf-8-sig') 
    #    
    return combined_csv
collect_RubRatings_data()
    

