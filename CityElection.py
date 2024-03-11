from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def cityElectionResult():
    cityTurkey = []
    yesVoteCity = []
    noVoteCity = []

    if request.method == 'POST':
        input_value = request.form.get('cityName')
        city = input_value.upper() + '.json'

        try:
            df = pd.read_json(city)
            cityTurkey = df["İlçe Adı"].tolist()
            yesVoteCity = df["Evet Oranı"].str.replace("%", "").str.replace(
                ',', '.').astype(float).apply(lambda x: '{:.2f}'.format(x)).tolist()
            noVoteCity = df["Hayır Oranı"].str.replace("%", "").str.replace(
                ',', '.').astype(float).apply(lambda x: '{:.2f}'.format(x)).tolist()
        except FileNotFoundError:
            error_message = "Veri bulunamadı."
            return render_template("city.html", error_message=error_message)

    return render_template("city.html",
                           cityTurkey=cityTurkey,
                           yesVoteCity=yesVoteCity,
                           noVoteCity=noVoteCity)


if __name__ == "__main__":
    app.run()
