
import warnings
warnings.filterwarnings('ignore')
import re
import pandas as pd
import numpy as np
import os
import shutil
import glob 
import io
"""
  isogeocoder is a tool that generates and assigns standardized iso compliant unique identification numbers or codes for entities based on location information. It can create and assign codes based on a country's administrative division (geo-location) or any administrative level depending on the use case. 
Examples include:
* Unique school identity for an education management information system.
* Unique health facility identity for a health management information system. 
* Standard administrative level geocode for country planning.
* Administrative level identity generation in digital addressing system.

"""
def countries_data():
    df = 'https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/countries_iso.csv'
    return df
def subdiv_data():
    df = 'https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/countries_subdivision_iso.csv'
    return df
def subregions(df,continent = None,level=None,sep=None):
    countries = df.drop_duplicates(subset=['Alpha-3 code'])
    if continent is not None:
        continent = continent.capitalize()
        df = df[df['Continet'].str.capitalize()==continent]
    df = df.drop_duplicates(subset=['Subregions'])
    zfill = len(str(df['M49code_Subregions'].max()))
    zfill_c = len(str(df['M49code_continent'].max()))
    if level != None and sep == None:
        df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfill)+'-'+df['M49code_Subregions'].astype(str).str.zfill(zfill)
    elif sep != None:
         df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfill)+sep+df['M49code_Subregions'].astype(str).str.zfill(zfill)
    else:
        df['Subregions_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)
    df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfill)
    df = df[['Continet','M49code_continent','Continent_code','Subregions','M49code_Subregions','Subregions_code']]
    return df

def continents(df):
  
    df = df.drop_duplicates(subset=['Alpha-3 code'])
    df = df.drop_duplicates(subset=['Continet'])
    df = df[['Continet','M49code_continent']]
    zfill = len(str(df['M49code_continent'].max()))
    df['Continet_code'] = df['M49code_continent'].astype(str).str.zfill(zfill)
    return df

def countries(df,continent=None,level=None,sep=None):
    countries_df = pd.read_csv('https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/countries_iso.csv')
    countries = countries_df.drop_duplicates(subset=['Alpha-3 code'])
    
    if continent == None:
        df = countries
    else:
        continent = continent.capitalize()
        df = countries[countries['Continet'].str.capitalize()==continent]
    df = df.drop_duplicates(subset=['Country'])
    zfill = len(str(df['M49code_Subregions'].max()))
    zfillc = len(str(df['M49code_continent'].max()))
    zfill_country = len(str(df['M49Code_country'].max()))
    if (level != None or level !=1) and sep == None:
        df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
        df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)+'-'+df['M49code_Subregions'].astype(str).str.zfill(zfill)
        df['country_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)+'-'+df['M49Code_country'].astype(str).str.zfill(zfill)
    if level == 1 and sep == None:
        df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
        df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)+'-'+df['M49code_Subregions'].astype(str).str.zfill(zfill)
        df['country_code'] = df['Subregions_code'].astype(str).str.zfill(zfill)+'-'+df['M49Code_country'].astype(str).str.zfill(zfill)
    elif level == 2 and sep == None:
        df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
        df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)+'-'+df['M49code_Subregions'].astype(str).str.zfill(zfill)
        df['country_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)+'-'+df['M49Code_country'].astype(str).str.zfill(zfill)
  
    elif sep != None:
        df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
        df['Subregions_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)+sep+df['M49code_Subregions'].astype(str).str.zfill(zfill)
        df['country_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)+sep+df['M49Code_country'].astype(str).str.zfill(zfill)   
    else:
        df['Subregions_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)
        df['country_code'] = df['M49Code_country'].astype(str).str.zfill(zfill_country)    
        df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
    
    df = df[['Continet','M49code_continent','Continent_code','Subregions','M49code_Subregions','Subregions_code','Country','Alpha-3 code','M49Code_country','country_code']]
    return df

def country(df,country =None):
    zfill_country = len(str(df['M49Code_country'].max()))
    zfill = len(str(df['M49code_Subregions'].max()))
    zfillc = len(str(df['M49code_continent'].max()))
    df['Subregions_code'] = df['M49code_Subregions'].astype(str).str.zfill(zfill)
    df['country_code'] = df['M49Code_country'].astype(str).str.zfill(zfill_country)    
    df['Continent_code'] = df['M49code_continent'].astype(str).str.zfill(zfillc)
    df = df[['Continet','M49code_continent','Continent_code','Subregions','M49code_Subregions','Subregions_code','Country','M49Code_country','country_code','Alpha-3 code','Alpha-2 code','Subdivision category',
           'Subdivision name', '3166-2 code', 'sub-code']]

    if country is not None:
            country = country.capitalize()
            df = df[(df['Country'].str.capitalize()==country) | (df['Alpha-2 code'].str.upper()==country.upper()) | (df['Subregions'].str.capitalize()==country.capitalize()) | (df['Continet'].str.capitalize()==country.capitalize())]
    df = df.drop_duplicates(subset=['3166-2 code'])
    return df
        
def gencode(level_df,uniqueid_df,cat_df=None,level_column=None,uniqueid_column=None,columns=None,title=None,sep=None):
        column = columns
        
        df = pd.merge(level_df,uniqueid_df,on=column,how='inner')
        if cat_df is not None:
            cat_df_col_ = cat_df.columns[0]
            df_final = pd.merge(df,cat_df,on=cat_df_col_,how='inner')
        else:
            df_final = df
        
        if sep is not None:
            df_final[title] = df_final[level_column].astype(str)+sep+df_final[uniqueid_column].astype(str)
        else:
            cat_df_col = cat_df_col_
            df_final[title] = df_final[level_column].astype(str)+df_final[uniqueid_column].astype(str)
        return df_final