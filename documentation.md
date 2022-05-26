 isogeocoder is a combination of two libraries, one is the **iso** library, standard countries dataset manipulation, and the **geo** library which generates administrative level code on your dataset and generates id using the index of your entity dataset.  
```python
from  isogeocoder import geo,iso
```

##  geo
```python
       geo.data(path) -  
            Parameters:
                path: dataset
            Returns:
                Dataframe of file
            Examples:
               country_df =  geo.data('csv/excel file')
   
       geo.level1(df,column):
           Parameters:
               df: administrative level dataset as a pandas data frame
               column: the level column to generate identity on
            Returns:
                Dataframe of Level name and Code
            Examples:
                region_df = geo.level1(country_df,'region')
        
        geo.level2(df,level1,column) :
            Parameters:
               df: administrative level dataset as a pandas data frame
               level_one_df
               level_one: the level one dataframe
               column: the level column to generate identity on 
            Returns:
                Dataframe of Level name and Code
            Examples:
              district_df = geo.level2(country_df,region_df,'district')
                
         geo.level3(df,level2,column) :
            Parameters:
               df: administrative level dataset as a pandas data frame
               level_one_df
               level_one: the level one dataframe
               column: the level column 
            Returns:
                Dataframe of Level name and Code
            Examples:
                chiefdom_df = geo.level3(country_df,district_df,'chiefdom')
                
         geo.level4(df,level3,column)
            Parameters:
                df: administrative level dataset as a pandas data frame
                level3: the level three dataframe
                column: the level column to generate identity on
            Returns:
                Dataframe of Level name and Code
            Examples:
                section_df = geo.level4(country_df,chiefdom_df,'section')
  
          geo.uniqueid(df,level4,column)
             Parameters:
                 df: entity dataset with administrative level columns as a pandas data frame
                 level_four_df =  the level four dataframe
                 column: the level column to generate identity on 
            Returns:
                  Dataframe of entity name and Code
            Examples:
                  schools = geo.uniqueid(school_list,section_df,'idschool_name')
            
          geo.categorical(df,column,encoding_type=None)
            Parameters:
                 df: entity dataset with administrative level columns as a pandas data frame
                 column: the level column,to categories 
                 encoding_type: output type eg  letter or number coding
            Returns:
                  Dataframe of categorical column and Code
            Examples:
                  school_types = geo.categorical(school_list,'sch_type',encoding_type='string')
            
          geo.gencode(level_df,uniqueid_df,cat_df=None,level_column = None,uniqueid_column=None,title=None,sep=None)
           Parameters:
                 level_df: the level four dataframe
                 uniqueid_df: the unique identity dataframe
                 cat_df: the categorical dataframe
                 level_column: the level column to generate identity on  
                 uniqueid_column: the unique identity column from the entity dataframe
                 title: provide title for your indentity column
                 sep: the seperator to use which divide the admininstative level and entity indentites
            Returns:
                  Dataframe of merged administrative level and entity
            Examples:
                school_masterlist = geo.gencode(section_df,schools,cat_df=school_types,level_column='chiefdom',uniqueid_column='school_name_code',title='emis_code',sep='-')
            
        geo.alpha_coder(level_df,column,add_char=None,clen = None):
             Parameters:
                       level_df: administrative level dataset as a pandas data frame
                       column: the level column 
                       clen: the character lenght for the alpha code
                       add_char: prepend character where where level name do not meet coding lenght
                  Returns:
                        Dataframe of Level name and Code
                  Examples:
                         region_alpha = geo.alpha_coder(region_df,column='region',clen=2)
                         district_alpha = geo.alpha_coder(district_df,column='district',clen=3,add_char='D')
   
          geo.alpha_merger(df1,df2,merger_column,sufixs= [],level=None,sep=None):
               Parameters:
                     df1: first alpha_coder dataframe
                     df2: second alpha_coder dataframe
                     merge_col: the unique column to marge the two dataframes
                     sufixs: suffixes for indentcal column names in both dataframes
                     level: the codeing level
                     sep: the special character for seperator
                Returns:
                      Dataframe of Level name and Code
                Example:
                   alpha_df =  geo.alpha_merger(region_df,district_df,'region',sufixs=['Reg','Dis'],level=2,sep='-')
                
         geo.alpha_merger_l3(alpha_df,level3_df,level3_alpha_column,merger_column,digits,sep= None):
             Parameters:
                       alpha_df: first alpha_coder dataframe
                       level3_df: the level three dataframe
                       level3_alpha_column:the column to use for the coding
                       merger_column: the unique column to marge the two dataframes
                       digits: how many digits to remove from left
                       sep: the special character for seperator
                  Returns:
                        Dataframe of Level name and Code
                  Example:
                       l3_alpha_df = geo.alpha_merger_l3(alpha_df,chiefdom_df,'chiefdom_code','district_code',2,sep='-')
                       
          geo.alpha_merger_l4(alpha_df,level4_df,level4_alpha_column,merger_column,digits,sep=None):
                 Parameters:
                           alpha_df: first alpha_coder dataframe
                           level4_df: the level four dataframe
                           level4_alpha_column:the column to use for the coding
                           merger_column: the unique column to marge the two dataframes
                           digits: how many digits to remove from left
                      Returns:
                            Dataframe of Level name and Code
                      Example:
                            digital_address_id = geo.alpha_merger_l4(l3_alpha_df,section_df,'section_code','chiefdom_code',4,sep='-')
  ```
  ##  iso
  ```python
          iso.countries_data()
             Returns:
                 [link to countries with iso code dataset](https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/countries_iso.csv)
             Example:
                 continent_df = pd.read_csv(iso.countries_data())
                 
          iso.subdiv_data()
             Returns:
                 [link to countries with iso code dataset](https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/countries_subdivision_iso.csv)
             Example:
                 subdivisions_df = pd.read_csv(iso.subdiv_data())
           
          iso.continents(df)
              Parameters:
                    df:continents dataframe
              Returns:
                     Dataframe of continets
              Example:
                     iso.continents(continent_df)
                 
          iso.subregions(df,continent = None,level=None,sep=None)
              Parameters:
                   df:continent dataframe
                   continent:select countries from continenet
                   level:how many levels to jion to create the identity
                   sep:
              Returns:
                    Dataframe of continets with sub regions
              Example:
                   iso.subregions(countries_df,'Africa',level=1,sep='-')
                   
          iso.countries(df,continent=None,level=None,sep=None)
              Parameters:
                   df:continent dataframe
                   continent:select countries from continenet
                   sep: the special character for seperator
              Returns:
                   Dataframe of countries
              Example:
                    iso.countries(continent_df,'Africa',level=2,sep='-')
                   
                   
           iso.country(df,country =None)
              Parameters:
                 df:continent dataframe
                 country:select country from continenet dataframe
              Return:
                  Dataframe of a country and it subdivisions
              Example:
                 iso.country(subdivisions_df,'Sierra Leone')
```
                    
               
                   
              
          
          
