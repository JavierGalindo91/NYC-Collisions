import pandas as pd, os
from collision_cleaner import getBorough, nyc_borough
os.chdir(r'C:\Users\javie\OneDrive\Documents\NYC_Data_Engineer_Project\collisions_data - Copy')
path = os.getcwd()

individual_crash_df = pd.read_csv("collisions_processed_bulk.csv", header=[0])
individual_crash_df['crash_date#Borough'] = individual_crash_df['crash_date'].astype(str) + individual_crash_df['Boroughs']
individual_crash_df.to_csv("collisions_processed_bulk.csv", encoding='utf-8', index=False)