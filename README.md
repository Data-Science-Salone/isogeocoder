## **About isogeocoder**
isogeocoder is a tool that generates and assigns standardized iso compliant unique identification numbers or codes for entities based on location information. It can create and assign codes based on a country's administrative division (geo-location) or any administrative level depending on the use case. Examples include:

* Unique school identity for an education management information system.
* Unique health facility identity for a health management information system. 
* Standard administrative level geocode for country planning.
* Administrative level identity generation in digital addressing system.

## Dependencies
   Dependencies
isogeocoder is built on the pandas framework; so all pandas operations can work on isogeocoder. Dataframes generated from each administrative level are saved as CSV files.

We also recommended using the Jupyter notebook.

##  Installation
Install isogeocoder with pip3

```python
pip3 install isogeocoder
```
      
##   Usage/Examples
isogeocoder is a combination of two libraries, one is the iso library, a standard country dataset manipulation; and the geo library which generates administrative level code on your dataset and generates a unique id using the index of your entity dataset. In the examples, we use the Sierra Leone school list provided by the MInistry of Basic and Senior Secondary Education, dataset [Sierra Leone School List](https://raw.githubusercontent.com/MBSSE-SL/isogeocoder/main/sl_school_list.csv)
   

   **GEO Examples**:
   
   Generating a unique school identity for an EMIS system
      
```python
from  isogeocoder import geo
```
```python
schools_df = geo.data('sl_school_list.csv')
```
```python
#columns
schools_df.columns 
#output
Index(['idregion', 'iddistrict', 'idchiefdom', 'idsection', 'sch_type',
       'idschool_name'],
      dtype='object')
Region = geo.level1(schools_df,'idregion')
Region
District = geo.level2(schools_df,Region,'iddistrict')
District
Chiefdom = geo.level3(schools_df,District,'idchiefdom')
Chiefdom
Section = geo.level4(schools_df,Chiefdom,'idsection')
Section
<<<<<<< HEAD
Schools = geo.uniqueid(schools_df,Section,'idschool_name')
Schools
=======
>>>>>>> 1bbc060061aa62acd289c8d1934f713be29d7028
School_Type = geo.categorical(schools_df,'sch_type',encoding_type='integer')
School_Type
school_masterlist = geo.gencode(Section,Schools,cat_df=School_Type,level_column='idchiefdom',uniqueid_column='idschool_name_edited_code',title='emis_code',sep='-')
school_masterlist
```

Generating administrative level coding in digital addressing system


```python
from  isogeocoder import geo
```
```python
schools_df = geo.data('sl_school_list.csv')
```
```python
#columns
schools_df.columns 
#output
Index(['idregion', 'iddistrict', 'idchiefdom', 'idsection', 'sch_type',
       'idschool_name'],
      dtype='object')
Region = geo.level1(schools_df,'idregion')
Region
District = geo.level2(schools_df,Region,'iddistrict')
District
Chiefdom = geo.level3(schools_df,District,'idchiefdom')
Chiefdom
Section = geo.level4(schools_df,Chiefdom,'idsection')
Section
Region_Alpha = geo.alpha_coder(Region,column='idregion',clen=2)
District_alpha = geo.alpha_coder(District,column='iddistrict',clen=3,add_char='D')
Alpha_df = geo.alpha_merger(region_alpha,district_alpha,'idregion',sufixs=['Reg','Dis'],level=1,sep='-')
Chiefdom_level = Chiefdom[['iddistrict_code','idchiefdom','idchiefdom_code']]
Chiefdom_Alpha= geo.alpha_merger_l3(alpha_df,Chiefdom_level,'idchiefdom_code','iddistrict_code',2,sep='-')
Section_level =   Section[['idchiefdom_code','idsection','idsection_code']]
digital_addressing = geo.alpha_merger_l4(l3,Section_level,'idsection_code','idchiefdom_code',4,sep='-')
digital_addressing
```

**ISO Example**:

```python
import pandas as pd
from  isogeocoder import iso
continents_df = pd.read_csv(iso.countries_data())
subdivision_df = pd.read_csv(iso.subdiv_data())
iso.continents(continents_df)
dataframe of subregions in a continent
iso.subregions(continents_df,'Africa',level=1,sep='-')
iso.countries(continents_df,'Africa',level=2,sep='-')
iso.country(subdivision_df,'Sierra Leone')

```

## Documentation 

Documentation is available  [here](https://github.com/MBSSE-SL/isogeocoder/blob/gh-pages/documentation.md) 

## Contributing

PR requests are highly welcome, fork and commit your changes 

## Authors

- [moinina](https://github.com/moinina)
- [mjames21](https://github.com/mjames21)
- [Mosesvb](https://github.com/Mosesvb)

 
## License

[MIT](https://choosealicense.com/licenses/mit/)  
       
