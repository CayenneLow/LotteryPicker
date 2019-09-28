#!/usr/bin/env python
from flask import Flask, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
import random
from rng import RNG, Error, Exhausted, checks
app = Flask(__name__)
Bootstrap(app)
app.secret_key='very-secret-123'

@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    if request.method == 'POST':
        # calculate RNG
        min = request.form['min']
        max = request.form['max']
        nNums = request.form['nNums']
        session['min'] = min
        session['max'] = max
        session['nNums'] = nNums
        try:
            checks(int(min), int(max), int(nNums))
        except Error as e:
            return render_template('index.html', error=e)
        return redirect(url_for('display'))
    return render_template('index.html', error=None)

@app.route('/display/', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        if request.form['button'] == 'Again?':
            #refresh
            return redirect(url_for('display'))
        else:
            return redirect(url_for('index'))
    # ensure control flow
    if 'min' not in session:
        return redirect(url_for('index'))

    min = int(session.get('min', None))
    max = int(session.get('max', None))
    nNums = int(session.get('nNums', None))
    if 'seen' not in session:
        session['seen'] = []     
    seenList = session.get('seen', None)
    exhausted = False
    try:
        session['seen'] = RNG(min, max, nNums, seenList)
        print(session['seen'])
    except Exhausted as e:
        exhausted = True
    indexToStartOutputting = len(seenList) - nNums
    return render_template('display.html', printList=seenList[indexToStartOutputting:len(seenList)], exhausted=exhausted, nNums=nNums)

    

if __name__ == '__main__':
    app.run(debug=True, port=4000)
