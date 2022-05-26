from flask import Flask, redirect, url_for, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/latscrapdb"
mongo = PyMongo(app)

#def get_dbconnection():
#    myclient = pymongo.MongoClient('mongodb://localhost:27017/') #link mongoDB, note: koneksikan terlebih dahulu
#    mydb = myclient['latscrapdb'] #gantinama database kalian, kalau belum ada/belum buat bisa langsung dibuat disini contoh => mydb = myclient['databaseku']
#
#    mycol = mydb['buku'] #nama collection atau table, kalau belum ada lakukan sama seperti sebelumnya
#    
#    return mycol

@app.route("/")
def home():
    result = cursor.fetchall()
    datas = []
    for entry in result:
        record = {
            'id': entry[0],
            'cover': entry[1],
            'title': entry[2],
            'description': entry[3],
            'author': entry[4],
            'publisher': entry[5],
            'price': entry[11],
            'rating': entry[12]
        }
        datas.append(record)
    return render_template("index.html")

@app.route("/admin/scrape")
def scrape():
    return render_template("scrape.html")

#All the routings in our app will be mentioned here.
@app.route("/test")
def test():
    return "App is working perfectly"

if __name__ == "__main__":
    app.run(debug=True)