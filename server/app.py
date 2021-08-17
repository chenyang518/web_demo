from logging import DEBUG
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import pymysql

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app,resources = {r'/*':{'origins':'*'}})

@app.route('/ping',methods=['GET'])
def ping_pong():
    conn = pymysql.connect(host="localhost",user="root",password="chenyang123",database="web")
    sql = "SELECT * FROM Labor_Reduction"
    df1 = pd.read_sql_query(sql, con=conn)
    # sql = "SELECT * FROM CI_Saving"
    # df2 = pd.read_sql_query(sql,con=conn)
    # sql = "SELECT * FROM CI_projects_on_EC_approval"
    # df3 = pd.read_sql_query(sql,con=conn)
    # data = {'data1':df1.to_json(orient='index'), 'data2':df2.to_json(orient='index'), 'data3':df3.to_json(orient='index')}
    return df1.to_json(orient='index')

@app.route('/labor-reduction',methods=['GET'])
def data_laborReduction():
    conn = pymysql.connect(host="localhost",user="root",password="chenyang123",database="web")
    sql = "SELECT * FROM Labor_Reduction"
    df1 = pd.read_sql_query(sql, con=conn)
    return df1.to_json(orient='index')


if __name__ == '__main__':
    app.run()