import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, NumberRange, StopValidation, InputRequired

import urllib.request
import json


class CheckInteger(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if " " in field.data:
            message = field.gettext('Field must not contain spaces')
            raise ValidationError(message)
        if "." in field.data:
            message = field.gettext('Field must contain integer value')
            raise ValidationError(message)

class CheckFloat(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if " " in field.data:
            message = field.gettext('Field must not contain spaces')
            raise StopValidation(message)
        if field.data.count('.') > 1:
            message = field.gettext('Field must contain float value with 1 dot')
            raise StopValidation(message)

class ClientDataForm(FlaskForm):
    age = IntegerField('Возраст', validators=[InputRequired(), CheckInteger()])
    sex = IntegerField('Пол (0 - женщина; 1 - мужчина', validators=[InputRequired(), CheckInteger(), NumberRange(0, 1)])
    cp = IntegerField('Боль в груди (от 0 до 3)', validators=[InputRequired(), CheckInteger(), NumberRange(0, 3)])
    trestbps = IntegerField('Артериальное давление', validators=[InputRequired(), CheckInteger()])
    chol = IntegerField('Уровень холестерина', validators=[InputRequired(), CheckInteger()])
    fbs = IntegerField('Уровень сахара (от 0 до 1))', validators=[InputRequired(), CheckInteger(), NumberRange(0, 1)])
    restecg = IntegerField('Результаты электрокардиографии (от 0 до 2', validators=[InputRequired(), CheckInteger(), NumberRange(0, 2)])
    thalach = IntegerField('Максимальная частота пульса', validators=[InputRequired(), CheckInteger()])
    exang = IntegerField('Стенокардия (0 или 1)', validators=[InputRequired(), CheckInteger(), NumberRange(0, 1)])
    oldpeak = FloatField('Депрессия ST', validators=[InputRequired(), CheckFloat()])
    slope = IntegerField('Наклон сегмента ST (от 0 до 2)', validators=[InputRequired(), CheckInteger(), NumberRange(0, 2)])
    ca = IntegerField('Количество крупных сосудов (от 0 до 4)', validators=[InputRequired(), CheckInteger(), NumberRange(0, 4)])
    thal = IntegerField('0 = нормально; 1 = исправленный дефект; 2 = обратимый дефект', validators=[InputRequired(), CheckInteger(), NumberRange(0, 2)])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    body = {'age': age,
            'sex': sex,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['age'] = request.form.get('age')
        data['sex'] = request.form.get('sex')
        data['cp'] = request.form.get('cp')
        data['trestbps'] = request.form.get('trestbps')
        data['chol'] = request.form.get('chol')
        data['fbs'] = request.form.get('fbs')
        data['restecg'] = request.form.get('restecg')
        data['thalach'] = request.form.get('thalach')
        data['exang'] = request.form.get('exang')
        data['oldpeak'] = request.form.get('oldpeak')
        data['slope'] = request.form.get('slope')
        data['ca'] = request.form.get('ca')
        data['thal'] = request.form.get('thal')
        
        # data = {key: str(value) for key, value in data.items()}
        print('try predicting')
        try:
            response = str(get_prediction(data['age'],
                                          data['sex'],
                                          data['cp'],
                                          data['trestbps'],
                                          data['chol'],
                                          data['fbs'],
                                          data['restecg'],
                                          data['thalach'],
                                          data['exang'],
                                          data['oldpeak'],
                                          data['slope'],
                                          data['ca'],
                                          data['thal']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
