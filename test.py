from flask import Flask, render_template, request, jsonify, abort, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import math

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.nbw8ry5.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 전체 보기 기능
@app.route("/")
def home():
    perfumes = db.perfumes
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 6, type=int)
    datas = list(perfumes.find({}).skip((page - 1) * limit).limit(limit))
    print(datas)

    total = perfumes.count_documents({})
    last_page_num = math.ceil(total / limit)

    block_size = 5
    block_num = int((page-1)/ block_size)
    block_start = int((block_size * block_num) + 1)
    block_last = math.ceil(block_start + (block_size - 1))
    if request.args.get(type) == 'json':
        return jsonify({'perfumes': datas})
    else:
        return render_template(
            "test_index.html",
            datas=datas,
            limit=limit,
            page=page,
            block_start=block_start,
            block_last=block_last,
            last_page_num=last_page_num
        )

@app.route("/perfume", methods=["GET"])
def perfume_get():
    perfumes = db.perfumes
    datas = list(perfumes.find({}, {'_id': False}))

    return jsonify({'perfumes': datas})


# 좋아요 업데이트 하기
@app.route("/perfume/like",methods=["POST"])
def perfume_like():
    id_receive = request.form['id_give']
    if id_receive is not None:
        db.perfumes.update_one(
            {'id': id_receive}, {
                '$set': {'like': 1 }
            }
        )
    return jsonify({'msg': '좋이요!'})

@app.route("/perfume/nolike", methods=["POST"])
def perfume_nolike():
    id_receive = request.form['id_give']
    if id_receive is not None:
        db.perfumes.update_one(
            {'id': int(id_receive)}, {
                '$set': {'like': 0}
            }
        )
    return jsonify({'msg':'좋아요 취소!'})



# 상세 보기 기능
@app.route("/perfume")
def view_perfume():
    product_id = request.args.get("product")
    if product_id is not None:
        perfumes = db.perfumes
        data = perfumes.find_one({"_id": ObjectId(product_id)})
        if data is not None:
            result = {
                "_id": data["_id"],
                "id": data["id"],
                "img": data["img"],
                "name": data["name"],
                "desc": data["desc"],
                "brand": data["brand"],
                "like": data["like"]
            }
            comment = db.perfumes_comment
            comments = list( comment.find({"root_idx": str(data.get("_id"))}) )

            return render_template(
                "view_perfume.html",
                result=result,
                comments=comments
            )
    return abort(404)


# 상세 보기 페이지 댓글 쓰기 기능
@app.route("/comment_write", methods=["GET","POST"])
def comment_write():
    if request.method == "POST":
        root_idx = request.form.get("root_idx")
        comment_recieve = request.form.get("comment")
        print(comment_recieve)
        if comment_recieve != "":
            perfume_comment = db.perfumes_comment
            comment = {
                "root_idx": str(root_idx),
                "comment": comment_recieve
            }
            x = perfume_comment.insert_one(comment)
            print(x.inserted_id)
        else:
            print('입력된 데이터가 없습니다.')
        return redirect(url_for("view_perfume", product=root_idx))
    return ''

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)