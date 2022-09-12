from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient


client = MongoClient('mongodb+srv://test:sparta@cluster0.nbw8ry5.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/perfume", methods=["GET"])
def perfume_get():
    perfumes = list(db.perfumes.find({}, {'_id': False}))
    return jsonify({'perfumes': perfumes})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)