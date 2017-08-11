from FreeMind import app
from flask import render_template
from FreeMind.action.actions import getHddSumary
from FreeMind.action.properties import Pi, Master
from FreeMind.config import hddList

@app.route('/')
def renderMaster():
    hdds = getHddSumary()
    return render_template('master.html', hdds=hdds, lastBackup=Master.backup.getLastSuccessfull().time)

@app.route('/slave')
def renderSlave():
    return ''
