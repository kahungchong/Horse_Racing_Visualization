import json
import pandas as pd

from flask import request
from flask import render_template
from flask import jsonify
from app import app

@app.route('/')
@app.route('/index')
def index():
    df_horse = pd.read_csv(os.path.join(DATADIR, "horse_info.csv"))
    df_record = pd.read_csv(os.path.join(DATADIR, "past_record.csv"))

    chart_horse = df_horse.to_dict(orient="records")
    chart_record = df_record.to_dict(orient="records")

    chart_horse = json.dumps(chart_horse, indent=2)
    chart_record = json.dumps(chart_record, indent=2)

    data = {"horse_data": chart_horse, "record_data": chart_record}

    return render_template('index.html', title='HKJC horse racing visualization', data=data)


@app.route('/getRecordData', methods=['POST'])
def getRecordData():
    data = json.loads(request.form.get('data'))
    id = data["id"]

    all_record = pd.read_csv(os.path.join(DATADIR, "recordHorse/all_record.csv"))
    record_result = all_record[all_record.HorseID == id]
    attributes = ["Rtg", "Pla", "RaceDate", 'Dist', 'FinishTime', "DeclarHorseWt"]
    record_result = record_result[attributes]
    record_result.index = pd.RangeIndex(len(record_result))
    filename = "recordHorse/result_" + id + ".csv"
    record_result.to_csv(os.path.join(DATADIR, filename), index=False)

    result = dict()
    result['state'] = True
    return jsonify(result)

@app.route('/getManData', methods=['POST'])
def getPersonData():
    data = json.loads(request.form.get('data'))
    identity = data["id"]

    df_man_horse = pd.read_csv('static/dataset/edit_horse.csv')
    targeted_horse_info = df_man_horse[df_man_horse['HorseID'] == str(identity)]

    result = dict()
    result['id'] = identity
    result['name'] = str(targeted_horse_info['Name'].values[0])
    result['country'] = str(targeted_horse_info['Country'].values[0])
    result['age'] = str(targeted_horse_info['Age'].values[0])
    result['color'] = str(targeted_horse_info['Color'].values[0])
    result['trainer'] = str(targeted_horse_info['Trainer'].values[0])
    result['owner'] = str(targeted_horse_info['Owner'].values[0])

    result['golden_medal'] = str(targeted_horse_info['123Starts'].values[0])[0]
    result['silver_medal'] = str(targeted_horse_info['123Starts'].values[0])[2]
    result['bronze_medal'] = str(targeted_horse_info['123Starts'].values[0])[4]
    return jsonify(result)