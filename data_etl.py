from modules import download_daily_data, read_daily_region_data, read_daily_demand_data, read_daily_consumption
from utility import clean_data

# Input start year and end year
start_year = 2023
end_year = 2023
path = "C:/Sonali/ISB/Term5/FP2/Code/"

# Download daily data
download_daily_data.download_data(start_year, end_year, path)

# Download weekly data

# Collect region data
read_daily_region_data.get_region_data(path)
clean_data.clean_region_data(path)

# Collect demand data
read_daily_demand_data.get_demand_data(path)
clean_data.clean_demand_data(path)

# Collect consumption data
read_daily_consumption.get_daily_consumption(path)
clean_data.clean_monthly_consumption(path)