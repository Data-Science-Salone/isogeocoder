import warnings
warnings.filterwarnings('ignore')
import re
import pandas as pd
import numpy as np
import os
import shutil
import glob 
"""
  Isogeocoder is a tool that generates and assign standardized iso compliant unique identification number or coders for a location and entities.
isogeocoder is a tool that generates and assigns standardized iso compliant unique identification numbers or codes for entities based on location information. It can create and assign codes based on a country's administrative division (geo-location) or any administrative level depending on the use case. 
Examples include:
* Unique school identity for an education management information system.
* Unique health facility identity for a health management information system. 
* Standard administrative level geocode for country planning.
* Administrative level identity generation in digital addressing system.

"""
def data(path):
    """
        Parameters:
            path: dataset
        Returns:
            Dataframe of file
        Examples:
            data('csv/excel file')
    """
    name, extension = os.path.splitext(path)
    if extension == '.csv':
        df = pd.read_csv(path)
    elif extension == '.xlsx':
        df = pd.read_excel(path,index_col=0)
    else:
        df = "Unknown extension"
    return df

def level1(df,column,index=None):
    
    """
       Parameters:
           df: administrative level dataset as a pandas data frame
           column: the level column
           index: the starting index value 
        Returns:
            Dataframe of Level name and Code
        Examples:
            level_one(country_df,'region')
    """

    level_one_dir = 'level_one_files'
    if not os.path.exists(level_one_dir):
            os.mkdir(level_one_dir)
    else:
        shutil.rmtree(level_one_dir)
        os.mkdir(level_one_dir)

    if index is not None:
        df.index+=index
    else:
        index=1
    level_1_df_drop_duplicate = df.drop_duplicates(subset=[column])
    zfill = len(str(level_1_df_drop_duplicate.shape[0]))
    level_one = list(df[column].unique())
    level_code_col = '{}_code'.format(column)
    level_one_name = column
    level_one_len = len(level_one)
    level_code = []

    for i in range(level_one_len):
            ccode = i+index
            vcode = str(ccode)
            code = vcode.zfill(zfill)
            level_code.append(code)
    level_one_zip = list(zip(level_one,level_code))
    level_df = pd.DataFrame(level_one_zip,columns=[level_one_name,level_code_col])
    level_df[level_code_col] = level_df[level_code_col].astype(int).astype(str)
    level_df[level_one_name] = level_df[level_one_name].str.upper()
    level_df.reset_index(drop=True, inplace=True)
    level_df.to_csv(level_one_dir+"/level_one.csv",index=False)
    return level_df



def level2(df,level_one,column,index=None) :
    """
        Parameters:
           df: administrative level dataset as a pandas data frame
           level_one_df
           level_one: the level one dataframe
           column: the level column 
           index: the starting index value
        Returns:
            Dataframe of Level name and Code
        Examples:
            level_one(country_df,region_df,'district')
    """
    
    level_two_dir = 'level_two_files'
    if not os.path.exists(level_two_dir):
            os.mkdir(level_two_dir)
    else:
        shutil.rmtree(level_two_dir)
        os.mkdir(level_two_dir)
    if index is not None:
        df.index+=index
    else:
        index = 1
    
    levels = []
    level_one_col = level_one.columns[0]
    level_one_col_code = level_one.columns[1]
    level_code_col = '{}_code'.format(column)
    #zfill 
    current_level = df.drop_duplicates(subset=[column])
    Previous_level = current_level.groupby([level_one_col]).count()
    zfill = len(str(Previous_level.iloc[:, 0].max()))
    df[level_one_col] = df[level_one_col].str.upper()
    for index,row in level_one.iterrows():
        level_one_column = re.sub(r'[^a-zA-Z0-9]','_',row[0])
        level_two = df[df[level_one_col]==row[0]]
        level_two_uniq = list(level_two[column].unique())
        level_two_len = len(level_two_uniq)
        level_code = []
        lv = []
        levels.append(lv)
        for i in range(level_two_len):
            ccode = i+index
            vcode = str(ccode)
            code = vcode.zfill(zfill)
            coded = '{}{}'.format(row[1],code)
            level_code.append(coded)
        level_two_zip = list(zip(level_two_uniq,level_code))
        lv.append(np.array(list(level_two_zip)).tolist())
        for i in range(len(levels)):
            level_df = pd.DataFrame(levels[i][0],columns=[column,level_code_col])
            level_df[level_one_col] = row[0]
            level_df[level_one_col_code] = row[1]
            level_df[level_code_col] = level_df[level_code_col].astype(int).astype(str)
            level_df[column] = level_df[column].str.upper()
            level_df_final = level_df[[level_one_col,level_one_col_code,column,level_code_col]]
            level_df_final.to_csv(level_two_dir+"/{}_level_two.csv".format(level_one_column),index=False) 

    all_files = glob.glob(level_two_dir + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)       
    level_two_df_all = pd.concat(li, axis=0, ignore_index=True)
    level_two_df_all = level_two_df_all.drop_duplicates(subset=[level_code_col])
    level_two_df_all.reset_index(drop=True, inplace=True)
    level_two_df_all.to_csv(level_two_dir+"/level_two.csv",index=False)
    return level_two_df_all

def level3(df,level_two,column,index=None) :
    """
        Parameters:
           df: administrative level dataset as a pandas data frame
           level_one_df
           level_two: the level two dataframe
           column: the level column 
           index: the starting index value
        Returns:
            Dataframe of Level name and Code
        Examples:
            level_one(country_df,region_df,'district')
    """
    level_three_dir = 'level_three_files'
    if not os.path.exists(level_three_dir):
            os.mkdir(level_three_dir)
    else:
        shutil.rmtree(level_three_dir)
        os.mkdir(level_three_dir)
    
    if index is not None:
        df.index+=index
    else:
        index = 1
       
    levels = []
    level_one_col = level_two.columns[0]
    level_one_col_code = level_two.columns[1]
    
    level_two_col = level_two.columns[2]
    level_two_col_code = level_two.columns[3]
    
    #zfill 
    current_level = df.drop_duplicates(subset=[column])
    Previous_level = current_level.groupby([level_two_col]).count()
    zfill = len(str(Previous_level.iloc[:, 0].max()))
    
    level_code_col = '{}_code'.format(column)
    df[level_two_col] = df[level_two_col].str.upper()
    for index,row in level_two.iterrows():
        level_two_column = re.sub(r'[^a-zA-Z0-9]','_',row[2])
        level_3_df_drop_duplicate = df.drop_duplicates(subset=[column])
        level_three = level_3_df_drop_duplicate[level_3_df_drop_duplicate[level_two_col]==row[2]]

        level_three_uniq = list(level_three[column].unique())
        level_three_len = len(level_three_uniq)
        level_three_code = []
        lv = []
        levels.append(lv)
        for i in range(level_three_len):
            ccode = i+index
            vcode = str(ccode)
            code = vcode.zfill(zfill)
            coded = '{}{}'.format(row[3],code)
            
            level_three_code.append(coded)
        level_three_zip = list(zip(level_three_uniq,level_three_code))
        lv.append(np.array(list(level_three_zip)).tolist())

        
        for i in range(len(levels)):
            level_df = pd.DataFrame(levels[i][0],columns=[column,level_code_col])
            level_df[level_one_col] = row[0]
            level_df[level_one_col_code] = row[1]
            level_df[level_two_col] = row[2]
            level_df[level_two_col_code] = row[3]
            level_df[level_code_col] = level_df[level_code_col].astype(int).astype(str)
            level_df[column] = level_df[column].str.upper()
            level_df_final = level_df[[level_one_col,level_one_col_code,level_two_col,level_two_col_code,column,level_code_col]]
            level_df_final.to_csv(level_three_dir+"/{}_level_three.csv".format(level_two_column),index=False) 
            

    all_files = glob.glob(level_three_dir + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)       
    level_df_all = pd.concat(li, axis=0, ignore_index=True)
    level_df_all = level_df_all.drop_duplicates(subset=[level_code_col])
    level_df_all.reset_index(drop=True, inplace=True)
    level_df_all.to_csv(level_three_dir+"/level_three.csv",index=False)
    return level_df_all

def level4(df,level_three,column,index=None) :
    """
        Parameters:
            df: administrative level dataset as a pandas data frame
            level_three_df
            level_three: the level three dataframe
            column: the level column 
            index: the starting index value
        Returns:
            Dataframe of Level name and Code
        Examples:
            level_one(country_df,region_df,'district')
    """

    level_four_dir = 'level_four_files'
    if not os.path.exists(level_four_dir):
            os.mkdir(level_four_dir)
    else:
        shutil.rmtree(level_four_dir)
        os.mkdir(level_four_dir)
    if index is not None:
        df.index+=index
    else:
        index = 1

    levels = []
    level_one_col = level_three.columns[0]
    level_one_col_code = level_three.columns[1]

    level_two_col = level_three.columns[2]
    level_two_col_code = level_three.columns[3]

    level_three_col = level_three.columns[4]
    level_three_col_code = level_three.columns[5]

    #zfill 
    current_level = df.drop_duplicates(subset=[column])
    Previous_level = current_level.groupby([level_three_col]).count()
    zfill = len(str(Previous_level.iloc[:, 0].max()))

    #Name the coded column in the dataframe
    level_code_col = '{}_code'.format(column)
    
    df[level_three_col] = df[level_three_col].str.upper()

    for index,row in level_three.iterrows():
        level_three_column = re.sub(r'[^a-zA-Z0-9]','_',row[4])
        df_clean = df.drop_duplicates(subset=[column])
        level_df = df_clean[df_clean[level_three_col]==row[4]]
        level_df.reset_index(drop=True, inplace=True)
        level_df.index = list(level_df.index)
        level_df[level_code_col] = str(row[5])+(level_df.index+index).astype(str).str.zfill(zfill)
        level_df[level_code_col] = level_df[level_code_col].astype(int).astype(str)
        level_df[column] = level_df[column].str.upper()
        level_df[level_one_col] = row[0]
        level_df[level_one_col_code] = row[1]
        level_df[level_two_col] = row[2]
        level_df[level_two_col_code] = row[3]

        level_df[level_three_col] = row[4]
        level_df[level_three_col_code] = row[5]
        level_df_final = level_df[[level_one_col,level_one_col_code,level_two_col,level_two_col_code,level_three_col,level_three_col_code,column,level_code_col]]
        level_df_final.to_csv(level_four_dir+"/{}_level_four.csv".format(level_three_column),index=False)
    all_files = glob.glob(level_four_dir + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)       
    level_df_all = pd.concat(li, axis=0, ignore_index=True)
    level_df_all = level_df_all.drop_duplicates(subset=[level_code_col])
    level_df_all.reset_index(drop=True, inplace=True)
    level_df_all.to_csv(level_four_dir+"/level_four.csv",index=False)
    return level_df_all

def categorical(df,column,encoding_type=None,index=None):
    """
      Parameters:
           df: administrative level dataset as a pandas data frame
           column: the level column 
           encoding_type: output type eg  letter or number coding
           index: the starting index value
      Returns:
            Dataframe of Level name and Code
      Examples:categorical(school_data,'sch_type',encoding_type='string')
    """    
    categorical_dir = 'categorical'
    if not os.path.exists(categorical_dir):
            os.mkdir(categorical_dir)
    else:
        shutil.rmtree(categorical_dir)
        os.mkdir(categorical_dir)
    categories = df[column].unique()
    encoding_type_cap = encoding_type.capitalize()
    if index is not None:
        df.index=+index
    else:
        index = 1
    alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    lss = []
    for index in range(0,len(categories)):
        if 0 <= index < len(categories):
            if encoding_type_cap == 'Alphabet' or encoding_type_cap == 'String' or encoding_type_cap == 'Letter':
                 l = [categories[index],alpha[index]]
            else:
                 l = [categories[index],index+index]
            lss.append(l)
        else:
            print("Index ",index," not in range")
    level_code_col = '{}_code'.format(column)
    level_df = pd.DataFrame(lss,columns=[column,level_code_col])
    level_df.to_csv(categorical_dir+"/categorical_encoding.csv",index=False)
    return level_df

def uniqueid(df,level_four_df,column,index=None):
    """
        Parameters:
               df: administrative level dataset as a pandas data frame
               level_three: the level three dataframe
               column: the level column 
               index: the starting index value
    """
    
    if index is not None:
        df.index+=index
    else:
        index = 1
    zfill = len(str(df.shape[0]))
    prevoius_level = list(level_four_df.columns)
    #Name the coded column in the dataframe
    level_code_col = '{}_code'.format(column)
    df[level_code_col] = (df.index+index).astype(str).str.zfill(zfill)
    columns = [pcolumn for pcolumn in level_four_df if "code" not in pcolumn]
    columns.append(column)
    columns.append(level_code_col)
    return df

def gencode(level_df,uniqueid_df,cat_df=None,level_column = None,uniqueid_column=None,title=None,sep=None):
    columns = [pcolumn for pcolumn in level_df if "code" not in pcolumn]
    cat_df_col_ = cat_df.columns[0]
    df = pd.merge(level_df,uniqueid_df,on=columns,how='inner')
    df_final = pd.merge(df,cat_df,on=cat_df_col_,how='inner')
    if 'code' in level_column:
         level_column = level_column
    else:
         level_column = '{}_code'.format(level_column)

    if 'code' in uniqueid_column:
         uniqueid_column = uniqueid_column
    else:
         uniqueid_column = '{}_code'.format(uniqueid_column)
    if cat_df_col_ is None:
        cat_df_col = ''
    else:
         cat_df_col = '{}_code'.format(cat_df_col_) 
    if sep is not None and cat_df is None:
        cat_type = df_final.dtypes[cat_df_col]
        if cat_type != 'object':
            df_final[cat_df_col] = df_final[cat_df_col].astype(int).astype(str)
        df_final[title] = df_final[level_column].astype(int).astype(str)+sep+df_final[uniqueid_column].astype(str)
    elif sep is not None and cat_df is not None:
        cat_type = df_final.dtypes[cat_df_col]
        if cat_type != 'object':
            df_final[cat_df_col] = df_final[cat_df_col].astype(int).astype(str)
        
        df_final[title] = df_final[level_column].astype(int).astype(str)+sep+df_final[cat_df_col]+sep+df_final[uniqueid_column].astype(str) 
    elif sep is None and cat_df is not None:
        cat_type = df_final.dtypes[cat_df_col]
        if cat_type != 'object':
            df_final[cat_df_col] = df_final[cat_df_col].astype(int).astype(str)
        
        df_final[title] = df_final[level_column].astype(int).astype(str)+df_final[cat_df_col]+df_final[uniqueid_column].astype(str)  
    else:
        cat_df_col = cat_df_col_
        df_final[title] = df_final[level_column].astype(int).astype(str)+df_final[uniqueid_column].astype(str)
    return df_final
def code_generator(geocode,level,number_of_schools):
    codes = []
    last_id = schools_df.shape[0]
    for i in range(number_of_schools):
        last_id = last_id+1
        code = '{}-{}-{}'.format(str(geocode),str(level),str(last_id))
        codes.append(code)
        #send the generate emis code to update schools_df
           #to do
    return codes

def alpha_coder(level_df,column,add_char=None,clen = None):
        """
         Parameters:
                   level_df: administrative level dataset as a pandas data frame
                   column: the level column 
                   clen: the character lenght for the alpha code
                   add_char: prepend character where where level name do not meet coding lenght
              Returns:
                    Dataframe of Level name and Code
              Examples:alpha_coder(District,column='iddistrict',clen=3,add_char='D')
        """
        alpha_dir = 'alpha_coding'
        if not os.path.exists(alpha_dir):
                os.mkdir(alpha_dir)
        else:
                pass
        codes = []
        for index,row in level_df.iterrows():
            if add_char is not None:
                match_letter = add_char
            else:
                match_letter = ""

            if re.search(r"\s", row[column]):
                chars = row[column].split(" ")
                chars_len = len(chars)
                first_chars = [ s[0] for s in row[column].split() ]

                if chars_len ==2:

                    first_two_chars = chars[0][:1]

                    alpha =(''.join([first_two_chars,first_chars[1]]))
                else:
                    alpha = (''.join(first_chars))  
            else:
                alpha = row[column][:clen]
            if len(alpha) == 2:
                alpha = '{}{}'.format(alpha,match_letter)

            codes.append([row[column],alpha])
        df_alpha = pd.DataFrame(codes,columns=[column,'alpha_code'])
        df = pd.merge(level_df,df_alpha,on=column,how='inner')
        df.reset_index(drop=True, inplace=True)
        df.to_csv(alpha_dir+"/{}.csv".format(column),index=False)
        return df
def alpha_merger(df1,df2,merger_column,sufixs= [],level=None,sep=None):
    """
     Parameters:
               df1: first alpha_coder dataframe
               df2: second alpha_coder dataframe
               merge_col: the unique column to marge the two dataframes
               sufixs: suffixes for indentcal column names in both dataframes
               level: the codeing level
               sep: the special character for seperator
          Returns:
                Dataframe of Level name and Code
          Example:alpha_merger(Region,District,'idregion',sufixs=['Reg','Dis'],level=2,sep='-')
    """
    alpha_merger_dir = 'alpha_merger'
    if not os.path.exists(alpha_merger_dir):
        os.mkdir(alpha_merger_dir)
    else:
        shutil.rmtree(alpha_merger_dir)
        os.mkdir(alpha_merger_dir)
    alpha1 = 'alpha_code{}'.format(sufixs[0])
    alpha2 = 'alpha_code{}'.format(sufixs[1])
    df = pd.merge(df1,df2,on=merger_column,how='inner',suffixes=sufixs)
    if level == 2:
        if sep is not None:
             df['alpha_code']= df[alpha1]+sep+df[alpha2]
        else:
            df['alpha_code']= df[alpha1]+df[alpha2]

    else:
        df['alpha_code']= df[alpha2]
    df.reset_index(drop=True, inplace=True)
    df.to_csv(alpha_merger_dir+"/alpha_merger.csv",index=False)   
    return df

def  alpha_merger_l3(alpha_df,level3_df,level3_alpha_column,merger_column,digits,sep= None):
    """
     Parameters:
               alpha_df: first alpha_coder dataframe
               level3_df: the level three dataframe
               level3_alpha_column:the column to use for the coding
               merger_column: the unique column to marge the two dataframes
               digits: how many digits to remove from left
               sep: the special character for seperator
          Returns:
                Dataframe of Level name and Code
          Example:alpha_merger_l3(alpha_df,Chiefdom_level,'idchiefdom_code','iddistrict_code',2,sep='-')
    """
    alpha_merger_l3_dir = 'alpha_merger_l3'
    if not os.path.exists(alpha_merger_l3_dir):
        os.mkdir(alpha_merger_l3_dir)
    else:
        pass
    level3_df['code3'] = level3_df[level3_alpha_column].astype(str).str[digits:]
    df = pd.merge(alpha_df,level3_df,on=merger_column,how='inner')
    if sep is not None:
        df['l3_alpha_code']= df['alpha_code']+sep+df['code3']
    else:
        df['l3_alpha_code']= df['alpha_code']+df['code3']

    df.reset_index(drop=True, inplace=True)
    df.to_csv(alpha_merger_l3_dir+"/{}.csv".format(level3_alpha_column),index=False)
    return df 


def  alpha_merger_l4(alpha_df,level4_df,level4_alpha_column,merger_column,digits,sep=None):
    """
     Parameters:
               alpha_df: first alpha_coder dataframe
               level4_df: the level four dataframe
               level4_alpha_column:the column to use for the coding
               merger_column: the unique column to marge the two dataframes
               digits: how many digits to remove from left
          Returns:
                Dataframe of Level name and Code
          Examples:alpha_merger(rg,dg,'idregion',sufixs=['Reg','Dis'],level=2,sep='-')
    """
    alpha_merger_l4_dir = 'alpha_merger_l4'
    if not os.path.exists(alpha_merger_l4_dir):
        os.mkdir(alpha_merger_l4_dir)
    else:
        pass
    level4_df['code4'] = level4_df[level4_alpha_column].astype(str).str[digits:]
    df = pd.merge(alpha_df,level4_df,on=merger_column,how='inner')
    if sep is not None:
        df['l4_alpha_code']= df['l3_alpha_code']+sep+df['code4']
    else:
        df['l4_alpha_code']= df['l3_alpha_code']+df['code4']
    df.reset_index(drop=True, inplace=True)
    df.to_csv(alpha_merger_l4_dir+"/{}.csv".format(level4_alpha_column),index=False)
    return df 