from flask import Flask, render_template
import pandas as pd

app = Flask("weather")
data = pd.read_csv("data_small(A)/stations.txt", skiprows=17)
data = data[['STAID', "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", var=data.to_html())


@app.route("/api/v1/<date>/<station>")
def about(date, station):
    filename = "data_small(A)/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]["   TG"].squeeze() / 10
    return {'date': date,
            'station': station,
            'temperature': temperature}


@app.route("/api/v1/<station>")
def with_data(station):
    filename = "data_small(A)/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient='records')
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def with_year(station, year):
    filename = "data_small(A)/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='records')
    return result


app.run(debug=True)
