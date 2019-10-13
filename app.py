#!/usr/bin/env python
from flask import Flask, redirect, render_template, request, session, url_for, send_from_directory
import random
import os
import datetime
from errors import *
from rng import RNG
app = Flask(__name__)
app.secret_key='very-secret-123'

@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    if request.method == 'POST':
        # initialize
        session['min'] = request.form['min']
        session['max'] = request.form['max']
        session['seen'] = []     
        session['exhausted'] = False
        return redirect(url_for('beforeRoll'))
    return render_template('index.html', error=None)

@app.route('/preRoll/', methods=['GET', 'POST'])
def beforeRoll():
    if session.get('min', None) is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        session['nNum'] = request.form['nNum']
        return redirect(url_for('roll'))
    return render_template('preRoll.html', error=None)

@app.route('/roll/')
def roll():
    try:
        min = int(session.get('min', None))
        max = int(session.get('max', None))
        nNum = int(session.get('nNum', None))
        seenList = session.get('seen', None)
    except TypeError as err:
        return redirect(url_for('index'))

    try:
        newNumbers = RNG(min, max, nNum, seenList)
    except NegativeNNum as err:
        return redirect(url_for('preRoll'))
    except InvalidRange as err:
        return redirect(url_for('index'))

    session['newNumbers'] = newNumbers
    seenList.append(newNumbers)
    session['seen'] = seenList
    return redirect(url_for('display'))

@app.route('/display/', methods=['GET', 'POST'])
def display():
    try:
        if request.method == 'POST':
            if request.form['button'] == 'Again?':
                return redirect(url_for('beforeRoll'))
            if request.form['button'] == 'View History':
                return redirect(url_for('history'))
            else:
                return redirect(url_for('index'))
        seenList = session.get('seen', None)
        count = 0
        for element in seenList:
            count += len(element)
        possibleNumbers = int(session.get('max', None)) - int(session.get('min', None)) + 1
        if count >= possibleNumbers:
            session['exhausted'] = True
    except TypeError as err:
        return redirect(url_for('index'))
    return render_template('display.html', printList=session.get('newNumbers'), exhausted = bool(session.get('exhausted', None)))

@app.route('/history/', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        if request.form['button'] == "Go back":
            return redirect(url_for('display'))
        elif request.form['button'] == "Start a new roll":
            return redirect(url_for('index'))
        elif request.form['button'] == "Save":
            return redirect(url_for('save'))
    seenNums = session.get('seen', None)
    if seenNums is None:
        return redirect(url_for('index'))
    return render_template('history.html', nums = seenNums)

@app.route('/save')
def save():
    try:
        fileName = "Lucky Draw " +  str(datetime.datetime.now())
        print(fileName)
        with open("static/"+fileName+".csv", 'w') as f:
            index = 0
            for roll in session.get('seen', None):
                index += 1
                f.write("Roll " + str(index) + "\n")
                subIndex = 0
                for num in roll:
                    subIndex += 1
                    f.write(str(subIndex) + ") " + str(num) + ",")
                f.write("\n")
        savesDir = os.path.join(os.path.dirname(__file__), "static/")
        print(savesDir)
    except TypeError as err:
        return redirect(url_for('index'))
    return send_from_directory(directory=savesDir, filename=fileName + ".csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
