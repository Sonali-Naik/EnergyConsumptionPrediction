import pandas as pd

state_to_region = {
    'Punjab': 'Northern Region',
    'Haryana': 'Northern Region',
    'Rajasthan': 'Northern Region',
    'Delhi': 'Northern Region',
    'UP': 'Northern Region',
    'Uttarakhand': 'Northern Region',
    'HP': 'Northern Region',
    'J&K': 'Northern Region',
    'Chandigarh': 'Northern Region',
    'Chhattisgarh': 'Western Region',
    'Gujarat': 'Western Region',
    'MP': 'Western Region',
    'Maharashtra': 'Western Region',
    'Goa': 'Western Region',
    'DD': 'Western Region',  # Assuming DD is Daman and Diu
    'DNH': 'Western Region',  # Assuming DNH is Dadra and Nagar Haveli
    'Essarsteel': 'Western Region',
    'AndhraPradesh': 'Southern Region',
    'Telangana': 'Southern Region',
    'Karnataka': 'Southern Region',
    'Kerala': 'Southern Region',
    'TamilNadu': 'Southern Region',
    'Pondy': 'Southern Region',  # Assuming Pondy is Puducherry
    'Bihar': 'Eastern Region',
    'DVC': 'Eastern Region',  # Assuming DVC is Damodar Valley Corporation
    'Jharkhand': 'Eastern Region',
    'Odisha': 'Eastern Region',
    'WestBengal': 'Eastern Region',
    'Sikkim': 'Eastern Region',
    'ArunachalPradesh': 'North-Eastern Region',
    'Assam': 'North-Eastern Region',
    'Manipur': 'North-Eastern Region',
    'Meghalaya': 'North-Eastern Region',
    'Mizoram': 'North-Eastern Region',
    'Nagaland': 'North-Eastern Region',
    'Tripura': 'North-Eastern Region',
    }

# Function to try parsing the date with each format
def parse_date(date_str):
    for date_format in date_formats:
        try:
            return pd.to_datetime(date_str, format=date_format)
        except ValueError:
            pass
    return pd.NaT  # Return NaT if none of the formats match

def clean_region_data(path):
    df_region = pd.read_csv(path + 'data/Region_data.csv')
    # Convert 'Date' column to datetime
    df_region['Date'] = pd.to_datetime(df_region['Date'], format='%d.%m.%y')

    # Convert specified columns to float
    float_columns = ['NR', 'WR', 'SR', 'ER', 'NER', 'Total']
    df_region[float_columns] = df_region[float_columns].replace('----------', -1000).replace('-', -1000).astype(float)
    df_region[float_columns] = df_region[float_columns].replace( -1000,0)
    df_region["Total_of_regions"] = df_region[['NR', 'WR', 'SR', 'ER', 'NER']].sum(axis=1)

    df_total = df_region[['Unnamed: 0', 'Date','Category','Total_of_regions','Total']]
    # df_total.Category.unique().tolist()
    df_total[df_total["Category"]=='7.30 0.00 0.00 2.49 0.74 10.53)']

    df_total = df_total[df_total["Category"] != '7.30 0.00 0.00 2.49 0.74 10.53)']
    df_total.reset_index(drop=True, inplace=True)

    df_total['Category2'] = df_total['Category'].str.replace(' ', '').str.lower()
    df_total['Category2'] = df_total['Category2'].replace({
    'demandmetduringeveningpeakhours(mw)': 'demandmetduringeveningpeakhours(mw)',
    'peakshortage(mw)': 'peakshortage(mw)',
    'energymet(mu)': 'energymet(mu)',
    'hydrogen(mu)': 'hydrogen(mu)',
    'windgen(mu)': 'windgen(mu)',
    'solargen(mu)': 'solargen(mu)',
    'energyshortage(mu)': 'energyshortage(mu)'
    })
    # df_total.Category2.unique().tolist()
    df_total['Category2'] = df_total['Category2'].replace({
    'demandmetduringeveningpeakhrs(mw)': 'Maximum Demand - Evening Peak (MW)',
    'peakshortage(mw)': 'Peak Shortage (MW)',
    'energymet(mu)': 'Energy Met (MU)',
    'hydrogen(mu)': 'Hydro Generation (MU)',
    'windgen(mu)': 'Wind Generation (MU)',
    'solargen(mu)': 'Solar Generation (MU)',
    'energyshortage(mu)': 'Energy Shortage (MU)',
    'schedule(mu)': 'Import/Export Schedule (MU)',
    'actual(mu)': 'Import/Export Actual (MU)',
    'o/d/u/d(mu)': 'Import/Export O/D/U/D (MU)',
    'central': 'Generation Outage Central Sector (MW)',
    'state': 'Generation Outage State Sector (MW)',
    'thermal(coal&lignite)': 'Coal Generation (MW)',
    'hydro': 'Hydro Generation (MW)',
    'nuclear': 'Nuclear Generation (MW)',
    'gas,naptha&diesel': 'Thermal lignite Gas, Naptha & Diesel Generation (MW)',
    'coal': 'Coal Generation (MW)',
    'lignite': 'Thermal lignite Gas, Naptha & Diesel Generation (MW)'
    })
    df_total['Category2'] = df_total['Category2'].str.replace(' ', '_').str.lower()
    df_total2 = df_total.drop(['Category',"Total"],axis=1)

    df_final = df_total2.pivot(index='Date', columns='Category2', values='Total_of_regions')

    # Reset the index to make 'Date' a column
    df_final.reset_index(inplace=True)

    df_final.to_csv(path + 'cleaned_data/cleaned_region_data.csv')


def clean_monthly_consumption(path):
    df_consumption = pd.read_csv(path + 'data/Energy_Consumption_data_2018_2023.csv')
    df_consumption2 = df_consumption.drop(['Railways_NR', 'DNHDDPDCL', 'AMNSIL', 'BALCO',
       'Railways_ER', 'Ladakh', 'NR', 'WR', 'SR', 'ER', '4469.4'],axis=1)
    
    # Create a new DataFrame for region-wise consumption
    df_consumption_region = pd.DataFrame()
    df_consumption_region['Date'] = df_consumption2['Date']

    # Iterate through the columns of df_consumption and aggregate the consumption values for each region
    for state, region in state_to_region.items():
        df_consumption_region[region] = df_consumption_region.get(region, 0) + df_consumption2[state]

    # Fill NaN values with 0
    df_consumption_region = df_consumption_region.fillna(0)

    # Rename columns
    df_consumption_region = df_consumption_region.rename(columns={
        'Northern Region': 'NR',
        'Western Region': 'WR',
        'Southern Region': 'SR',
        'Eastern Region': 'ER',
        'North-Eastern Region': 'NER'
    })

    # Calculate the 'Total' column
    df_consumption_region['Total_consumption'] = df_consumption_region[['NR', 'WR', 'SR', 'ER', 'NER']].sum(axis=1)
    date_formats = ['%m/%d/%Y', '%d-%m-%Y']
    # Apply the function to the "Date" column
    df_consumption_region['Date'] = df_consumption_region['Date'].apply(parse_date)
    df_consumption_total = df_consumption_region[['Date','Total_consumption']]

    df_final1 = df_consumption_total
    df_final1.to_csv(path + 'cleaned_data/cleaned_consumption.csv')

def clean_demand_data(path):
    df_demand = pd.read_csv(path + 'Dailydata/Demand_data.csv')
    df_demand2 = df_demand.copy()
    df_demand = df_demand2.copy()
    df_demand['States'].unique()
    state_to_region2 = {
    'Punjab': 'Northern Region',
#    'punjab': 'Northern Region',
    'Haryana': 'Northern Region',
    'Rajasthan': 'Northern Region',
    'Delhi': 'Northern Region',
    'UP': 'Northern Region',
    'Uttarakhand': 'Northern Region',
    'HP': 'Northern Region',
    'J&K': 'Northern Region',
    'j&k(ut)andladakh(ut)': 'Northern Region',
    'j&k(ut)&ladakh(ut)': 'Northern Region',
    'Chandigarh': 'Northern Region',
    'railways_north':'Northern Region',
    'Chhattisgarh': 'Western Region',
    'Gujarat': 'Western Region',
    'MP': 'Western Region',
    'Maharashtra': 'Western Region',
    'Goa': 'Western Region',
    'DD': 'Western Region',  # Assuming DD is Daman and Diu
    'DNH': 'Western Region',  # Assuming DNH is Dadra and Nagar Haveli
    'Essarsteel': 'Western Region',
    'Andhra Pradesh': 'Southern Region',  # Corrected spelling
    'andhrapradesh': 'Southern Region',  #
    'Telangana': 'Southern Region',
    'Karnataka': 'Southern Region',
    'Kerala': 'Southern Region',
    'Tamil Nadu': 'Southern Region',  # Corrected spelling
    'Puducherry': 'Southern Region',  # Assuming Pondy is Puducherry
    'puducherry': 'Southern Region',  # Assuming Pondy is Puducherry
    'pondy': 'Southern Region',
    'tamilnadu':'Southern Region', 
    'Bihar': 'Eastern Region',
    'DVC': 'Eastern Region',  # Assuming DVC is Damodar Valley Corporation
    'Jharkhand': 'Eastern Region',
    'Odisha': 'Eastern Region',
    'West Bengal': 'Eastern Region',
    'westbengal':'Eastern Region',
    'Sikkim': 'Eastern Region',
    'Arunachal Pradesh': 'North-Eastern Region',
    'arunachalpradesh':'North-Eastern Region',
    'Assam': 'North-Eastern Region',
    'Manipur': 'North-Eastern Region',
    'Meghalaya': 'North-Eastern Region',
    'Mizoram': 'North-Eastern Region',
    'Nagaland': 'North-Eastern Region',
    'Tripura': 'North-Eastern Region',
    'railways_east': 'Eastern Region',
    'dnhddpdcl':  'Western Region'
    }
    state_to_region1 = pd.DataFrame([state_to_region2])
    state_to_region1 = state_to_region1.T
    state_to_region1 = state_to_region1.reset_index()
    state_to_region1.columns = ['States', 'Regions']
    state_to_region1.States = state_to_region1.States.str.lower()
    state_to_region3 = state_to_region1.set_index(["States"])
    df_demand = df_demand[(df_demand["States"]!="amnsil")&(df_demand["States"]!="balco")]

    try:
        df_demand['Regions'] = df_demand['States'].apply(lambda x: state_to_region3.loc[x, 'Regions'])
    except KeyError as e:
        print(f"KeyError: {e}")
        # Handle the error, for example, by providing a default region or dropping the row.
    df_demand = df_demand.drop(["States"],axis=1)
    df_demand2 = df_demand.drop(['Sr no.',"Regions"],axis=1)

    df_demand2['Max. Demand Met during the day (MW)']=df_demand2['Max. Demand Met during the day (MW)'].replace("-",0).astype(float)
    df_demand2['OD(+)/UD(-) (MU)']=df_demand2['OD(+)/UD(-) (MU)'].replace("-",0).astype(float)
    df_demand2[ 'Max OD (MW)']=df_demand2[ 'Max OD (MW)'].replace("-",0).astype(float)
    df_demand2[ 'Shortage during maximum Demand (MW)']=df_demand2[ 'Shortage during maximum Demand (MW)'].replace("-",0).astype(float)

    df_demand2['Date'] = pd.to_datetime(df_demand2['Date'], format='%d.%m.%y')

    # Group by 'Date' and calculate the sum
    sum_by_date = df_demand2.groupby('Date').sum()

    # Reset the index to make 'Date' a column again
    sum_by_date.reset_index(inplace=True)

    df_final2 = sum_by_date.drop(['Energy Shortage (MU)','Energy Met (MU)',],axis=1)
    df_final2.to_csv(path + 'cleaned_data/cleaned_demand_data.csv')

    # # Merge data frames on 'Date' column
    # merged_df = pd.merge(df_final, df_final1, on='Date', how='outer')
    # merged_df2 = pd.merge(merged_df, df_final2, on='Date', how='outer')

    # merged_df3 = merged_df2.dropna()
