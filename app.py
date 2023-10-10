from flask import Flask, render_template, request, url_for
from flask_cors import CORS
import pyodbc
ConnectionString = "Driver={Sql Server};"\
    "Server=DESKTOP-URCG1J0;"\
    "Database=phoneBook;"\
    "UID=sa;PWD=Abc@123"
sqlConnection = pyodbc.connect(ConnectionString)
sqlcommand = sqlConnection.cursor()
app = Flask(__name__)
CORS(app)

# return all data


def createRes(rawData):
    data = list()
    for i in rawData:
        person = dict()
        person['id'] = i[0]
        person['name'] = i[1]
        person['familyName'] = i[2]
        person['personalId'] = i[3]
        person['straightLine'] = i[4]
        person['internal'] = i[5]
        person['faxNumber'] = i[6]
        person['unit'] = i[7]
        data.append(person)
    return data


def createResBlog(rawData):
    data = list()
    for i in rawData:
        blog = dict()
        blog['id'] = i[0]
        blog['title'] = i[1]
        blog['txt'] = i[2]
        blog['created'] = i[3]
        data.append(blog)
    return data


def searchQuery(Name='', Fname='', NumId='', Unit=''):
    wherequery = ''
    if Name != '':
        wherequery += f"name Like '%{Name}%' "
    if Fname != '':
        if len(wherequery) > 0:
            wherequery += f" AND "
        wherequery += f"familyName Like '%{Fname}%' "
    if NumId != '':
        if len(wherequery) > 0:
            wherequery += f" AND "
        wherequery += f"personalId='{NumId}' "
    if Unit != '':
        if len(wherequery) > 0:
            wherequery += f" AND "
        wherequery += f"unit='{Unit}' "
    res = f"select * from dbo.PhoneDetail where {wherequery}" if len(
        wherequery) > 0 else f"select * from dbo.PhoneDetail"
    print(res)
    return res


@app.route("/getall", methods=["GET"])
def getall():
    query = "select * from dbo.PhoneDetail"
    sqlcommand.execute(query)
    rows = sqlcommand.fetchall()
    return createRes(rows)


@app.route("/getallblogs", methods=["GET"])
def getallblogs():
    query = "select * from dbo.blog"
    sqlcommand.execute(query)
    rows = sqlcommand.fetchall()
    return createResBlog(rows)


@app.route("/searchContacts", methods=["GET"])
def searchContacts():
    name = request.args.get('name') if request.args.get('name') else ''
    fname = request.args.get('fname') if request.args.get('fname') else ''
    numid = request.args.get('numid') if request.args.get('numid') else ''
    unit = request.args.get('unit') if request.args.get('unit') else ''
    searchQ = searchQuery(Name=name, Fname=fname, NumId=numid, Unit=unit)
    sqlcommand.execute(searchQ)
    rows = sqlcommand.fetchall()
    return createRes(rows)


def suggDef(key, ktype):
    wherequery = ''
    selector = 'name' if ktype == 'f' else 'familyName'
    if ktype == 'f':
        wherequery += f"name Like '%{key}%' "
    if ktype == 'l':
        wherequery += f"familyName Like '%{key}%' "
    res = f"select DISTINCT({selector}) from dbo.PhoneDetail where {wherequery}"
    return res


@app.route("/suggestion", methods=["GET"])
def suggestion():
    key = request.args.get('key')
    ktype = request.args.get('ktype')
    searchQ = suggDef(key=key, ktype=ktype)
    sqlcommand.execute(searchQ)
    rows = sqlcommand.fetchall()
    res = list()
    for item in rows:
        res.append(item[0])
    return res


@app.route("/getunits", methods=["GET"])
def getunits():
    query = "select DISTINCT(unit) from dbo.PhoneDetail"
    sqlcommand.execute(query)
    rows = sqlcommand.fetchall()
    res = list()
    for item in rows:
        res.append(item[0])
    return res


@app.route("/deleteuser", methods=["POST"])
def deleteuser():
    id = request.args.get('id') if request.args.get('id') else ''
    delquery = f"delete from dbo.PhoneDetail where id={id}"
    sqlcommand.execute(delquery)
    return "Success", 200,
