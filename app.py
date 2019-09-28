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
        session['rolls'] = 0
        session['exhausted'] = False;
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
    newNumbers=[]
    if (bool(session.get('exhausted', None)) != True):
        newNumbers = RNG(min, max, nNums, seenList)
        for num in newNumbers:
            seenList.append(num)
        session['seen'] = seenList
        session['rolls'] += 1
        if len(session.get('seen', None)) == max:
            session['exhausted'] = True
    return render_template('display.html', printList=newNumbers, exhausted=bool(session.get('exhausted', None)), nNums=nNums, rolls=session.get('rolls',None))

    

if __name__ == '__main__':
    app.run(debug=True, port=4000)
