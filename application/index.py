from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, get_scorer, get_scorer_names, make_scorer
from joblib import load  # Assuming your TPOT pipeline is saved in a joblib file
import calendar
import joblib

path = "C:/Sonali/ISB/Term5/FP2/Code/"

def data_process(month_name, year):
    path = "C:/Sonali/ISB/Term5/FP2/Code/"
    existing_data1 = pd.read_csv(path + "data/generation4_data.csv")
    existing_data1 = existing_data1.drop(["index"],axis=1)

    existing_data1.drop_duplicates(inplace=True)

    # Create a new DataFrame without duplicates
    existing_data1_no_duplicates = existing_data1.drop_duplicates()

    year = int(year)

    #Get subset
    existing_data = existing_data1_no_duplicates[existing_data1_no_duplicates['Year']==year]
    column_name = "Month_" + month_name
    existing_data = existing_data[existing_data[column_name] == True]
    existing_data = existing_data.reset_index()
    # Assuming 'Date' is the index, if not, set it as the index
    existing_data.set_index('Date', inplace=True)

    # Extract features for both datasets
    X_existing = existing_data[['Year', 'tavg', 'tmin', 'tmax', 'prcp', 'Month_August', 'Month_December', 'Month_February', 'Month_January',
        'Month_July', 'Month_June', 'Month_March', 'Month_May',
        'Month_November', 'Month_October', 'Month_September']]
   # Standardize the features
    scaler = StandardScaler()
    X_existing_scaled = scaler.fit_transform(X_existing)
    return X_existing


def get_month_year(month, year):
    month = int(month)
    year = int(year)
    if month == 1:
        req_month = 12
        req_year = year - 1
    else:
        req_month = month - 1
        req_year = year
    return req_month, req_year


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def main():
    return render_template("home.html")

@app.route("/AboutUs")
def aboutus():
    return render_template("group8.html")
    
@app.route("/output", methods =["GET", "POST"])
def output():
    if request.method == "POST":
        #extract form components
        month_year = request.form.get("bdaymonth")
        watt = request.form.get("lname")
        category = request.form.get("categories")

        date_lst = month_year.split("-")
        month = date_lst[1]
        year = date_lst[0]
        month, year = get_month_year(month, year)
        month_name = calendar.month_name[int(month)]

        X_existing_scaled = data_process(month_name, year)
        # print(X_existing)

        #Read models
        tpot_hydro_gen_model = joblib.load(path + 'tpot_model/tpot_hydro_gen_model.pkl')
        tpot_solar_gen_model = joblib.load(path + 'tpot_model/tpot_solar_gen_model.pkl')
        tpot_thermal_gen_model = joblib.load(path + 'tpot_model/tpot_thermal_gen_model.pkl')
        tpot_wind_gen_model = joblib.load(path + 'tpot_model/tpot_wind_gen_model.pkl')

        # # Make predictions for each dependent variable
        y_pred_hydro = tpot_hydro_gen_model.predict(X_existing_scaled)
        y_pred_solar = tpot_solar_gen_model.predict(X_existing_scaled)
        y_pred_thermal = tpot_thermal_gen_model.predict(X_existing_scaled)
        y_pred_wind = tpot_wind_gen_model.predict(X_existing_scaled)

        hydro = round(y_pred_hydro.mean(), 2)
        solar = round(y_pred_solar.mean(), 2)
        thermal = round(y_pred_thermal.mean(), 2)
        wind = round(y_pred_wind.mean(), 2)

        total = hydro + solar + thermal + wind
        print(total)

        return render_template("output.html", hydro = hydro, solar = solar, thermal = thermal, wind = wind, total = total)
    
    elif request.method == 'GET':
        return 'A GET request was made'
    
    else:
        return 'Not a valid request method for this route'
    
if __name__ == "__main__":
    app.run(debug=True)