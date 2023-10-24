import os
import glob
import pandas as pd
import numpy as np
import re

def read_file(keyword):
    data_dir = '/home/cgomez/Pegasus/DRG_pred/data'
    os.chdir(data_dir)
    all_files = glob.glob('*.{}'.format('csv'))
    
    for file in all_files:
        if re.search(keyword, file):
            df = pd.read_csv(file)
            
            return df
        
def bin_by_acuity(df):
    df['DRG_bin_acuity'] = np.nan

    for ix in range(len(df)):
        text = df['DRG_Description'].iloc[ix]

        try:
            if "WITH CC/MCC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITH CC/MCC"
        
            elif "WITH MCC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITH MCC"
        
            elif "WITH CC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITH CC"
        
            elif "WITHOUT MCC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITHOUT MCC"
        
            elif "WITHOUT CC/MCC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITHOUT CC/MCC"
        
            elif "WITHOUT CC" in text:
                df['DRG_bin_acuity'].iloc[ix] = "WITHOUT CC"

            else:
                df['DRG_bin_acuity'].iloc[ix] = "Not Specified"
        
        except:
            print(f'Exception on index {ix}')

    return df

def bin_by_reference(df):
    #read in drgref excel file into a dataframe
    drg_reference = pd.read_excel('drgcrossref.xlsx', usecols=['MSDRG_code', 'CCMCC'], header=0)
    
    df['DRG_bin_reference'] = np.nan
    
    #for row in df, grab the DRG and look up the complications in the Excel df
    for ix in range(len(df)):
        DRG = df.iloc[ix]['Concurrent MS-DRG']
        DRG_bin = drg_reference[drg_reference['MSDRG_code'] == DRG]['CCMCC']
        df['DRG_bin_reference'].iloc[ix] = DRG_bin
        
    return df

def bin_admitdx(df):
    icd_chapters = pd.read_excel('ICD_Chapters.xlsx', header=0)
    df['icd_chapter'] = np.nan
    df['icd_family'] = np.nan
    
    for ix in range(len(df)):
        diag_admitting = df['Diag Admitting'].iloc[ix]
        try:
            char = diag_admitting[0]
            ICD_chapter = icd_chapters[icd_chapters['Letter'] == char]['Diagnosis Bin']
            icd_family = diag_admitting.split('.')[0]
            df['icd_chapter'].iloc[ix] = ICD_chapter
            df['icd_family'].iloc[ix] = icd_family
        except:
            print(f"Exception on index {ix}")
                  
    return df

def remove_whitespace(df_col):
    for ix in range(len(df_col)):
        df_col.iloc[ix] = df_col.iloc[ix].strip()
    return df_col

def add_num_chars(df):
    df['num_chars'] = np.nan
    
    for ix in range(len(df)):
        try:
            df['num_chars'].iloc[ix] = len(df.iloc[ix]['Diag Admitting'])

        except:
            print(f"exception on {ix}")

    return df