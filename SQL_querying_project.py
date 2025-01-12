# This project demonstrates querying and analyzing real-world data from three interconnected datasets:
# Census data, Public Schools data, and Crime data in Chicago using SQLite as a relational database and Python.
# It involves various SQL queries to extract insights, such as crime patterns, community poverty levels, and school safety scores.
# This project is supposed to be run in the Jupyter Notebook environment.

import prettytable
import pandas as pd
import sqlite3

prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect('FinalDB.db')
cur = con.cursor

%load_ext sql

df = pd.read_csv('ChicagoCensusData.csv')
df1 = pd.read_csv('ChicagoPublicSchools.csv')
df2 = pd.read_csv('ChicagoCrimeData.csv')

%sql sqlite:///FinalDB.db

df.to_sql('CENSUS_DATA', con, if_exists = 'replace', index = False, method = 'multi')
df1.to_sql('CHICAGO_PUBLIC_SCHOOLS', con, if_exists = 'replace', index = False, method = 'multi')
df2.to_sql('CHICAGO_CRIME_DATA', con, if_exists = 'replace', index = False, method = 'multi')

# Find the total number of crimes recorded in the CRIME table.
%sql SELECT COUNT(*) FROM CHICAGO_CRIME_DATA;

# List community area names and numbers with per capita income less than 11000.
%sql SELECT COMMUNITY_AREA_NAME, COMMUNITY_AREA_NUMBER, PER_CAPITA_INCOME FROM CENSUS_DATA WHERE PER_CAPITA_INCOME < 11000;

# List all case numbers for crimes involving minors?(children are not considered minors for the purposes of crime analysis).
%sql SELECT CASE_NUMBER FROM CHICAGO_CRIME_DATA WHERE LOWER(DESCRIPTION) LIKE '%minor%';

# List all kidnapping crimes involving a child?
%sql SELECT * FROM CHICAGO_CRIME_DATA WHERE LOWER(PRIMARY_TYPE) = 'kidnapping' AND LOWER(DESCRIPTION) LIKE '%child%';

# List the kind of crimes that were recorded at schools. (No repetitions)
%sql SELECT DISTINCT(PRIMARY_TYPE) FROM CHICAGO_CRIME_DATA WHERE LOWER(LOCATION_DESCRIPTION) LIKE '%school%';

# List the type of schools along with the average safety score for each type.
%sql SELECT "Elementary, Middle, or High School" AS Type_Of_Schools, AVG(SAFETY_SCORE) AS Average_Safety_Score FROM CHICAGO_PUBLIC_SCHOOLS GROUP BY "Elementary, Middle, or High School"

# List 5 community areas with highest % of households below poverty line.
%sql SELECT COMMUNITY_AREA_NAME FROM CENSUS_DATA ORDER BY PERCENT_HOUSEHOLDS_BELOW_POVERTY DESC LIMIT 5;

# Which community area is most crime prone? Display the coumminty area number only.
%sql SELECT COMMUNITY_AREA_NUMBER FROM CHICAGO_CRIME_DATA GROUP BY COMMUNITY_AREA_NUMBER ORDER BY COUNT(COMMUNITY_AREA_NUMBER) DESC LIMIT 1;

# Use a sub-query to find the name of the community area with highest hardship index.
%sql SELECT COMMUNITY_AREA_NAME FROM CENSUS_DATA WHERE HARDSHIP_INDEX IN (SELECT MAX(HARDSHIP_INDEX) FROM CENSUS_DATA)

# Use a sub-query to determine the Community Area Name with most number of crimes?
%sql SELECT COMMUNITY_AREA_NAME FROM CENSUS_DATA WHERE COMMUNITY_AREA_NUMBER IN (SELECT COMMUNITY_AREA_NUMBER FROM CHICAGO_CRIME_DATA GROUP BY COMMUNITY_AREA_NUMBER ORDER BY COUNT(COMMUNITY_AREA_NUMBER) DESC LIMIT 1)
