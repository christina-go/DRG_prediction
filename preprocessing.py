import os
import glob
import pandas as pd
import numpy as np
import re

from helpers import *

def preprocessing_df(df):
    #limit MED services 
    excluded_med_svcs = ['OBS', 'NBN', 'PSY']
    meds_only = df[~df['Med Svc'].isin(excluded_med_svcs)]
    meds_only.reset_index(drop=True, inplace=True)

    #clean LOS
    outer_data = np.nanquantile(meds_only['LOS'], 0.95)
    cleaned_df = meds_only[meds_only['LOS'] <= outer_data]
    cleaned_df.reset_index(drop=True, inplace=True)

    #remove divisions M (mental health), h (holtz), r (rehab)
    cleaned_df['Division'] = remove_whitespace(cleaned_df['Division'])
    divisions = ['N', 'S', 'J', 'W']
    cleaned_df = cleaned_df[cleaned_df['Division'].isin(divisions)]

    #bin the 'Diag Admitting' feature
    cleaned_df.dropna(subset='Diag Admitting', inplace=True)
    cleaned_df.reset_index(inplace=True, drop=True)
    cleaned_df = bin_admitdx(cleaned_df)
    cleaned_df['icd_chapter'] = cleaned_df['icd_chapter'].astype('str')
    cleaned_df['icd_family'] = cleaned_df['icd_family'].astype('str')

    #calc num of characters in diag admitting and add as feature
    cleaned_df = add_num_chars(cleaned_df)

    #bin the target and set dtype
    cleaned_df = bin_by_reference(cleaned_df)
    cleaned_df['DRG_bin_reference'] = cleaned_df['DRG_bin_reference'].astype('str')
    #cleaned_df['DRG_bin_acuity'] = cleaned_df['DRG_bin_acuity'].astype('str')

    #keep cols I want to use for feature selection
    cols_to_keep = ['DRG_bin_reference', 'icd_chapter', 'icd_family', 'num_chars',
                'Division', 'Med Svc', 'Patient Age', 'Race', 'Sex',
                'Diag Admitting']


    filtered_df = cleaned_df[cols_to_keep]

    return filtered_df

