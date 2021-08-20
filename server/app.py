from logging import DEBUG
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import pymysql

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app,resources = {r'/*':{'origins':'*'}})

@app.route('/labor-reduction',methods=['GET'])
def data_laborReduction():
    conn = pymysql.connect(host="localhost",user="root",password="chenyang123",database="web")
    sql = "SELECT * FROM Labor_Reduction"
    df1 = pd.read_sql_query(sql, con=conn)
    return df1.to_json(orient='index')

@app.route('/ci-saving',methods=['GET'])
def data_ciSaving():
    conn = pymysql.connect(host="localhost",user="root",password="chenyang123",database="web")
    sql = "SELECT * FROM CI_Saving"
    df2 = pd.read_sql_query(sql, con=conn)
    return df2.to_json(orient='index')

@app.route('/ci-project',methods=['GET'])
def data_ciProject():
    conn = pymysql.connect(host="localhost",user="root",password="chenyang123",database="web")
    sql = "SELECT * FROM CI_projects"
    df3 = pd.read_sql_query(sql, con=conn)
    return df3.to_json(orient='index')

if __name__ == '__main__':
    app.run()