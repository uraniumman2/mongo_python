from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import re
from bson import BSON
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bigdata"
mongo = PyMongo(app)

@app.route('/')
def view_home():
    return render_template('/index.html',info={
        "users_count":mongo.db.users.count_documents({}),
        "users":mongo.db.users.find({})
    })
    
@app.route('/elements/view/users')
def view_users():
    return render_template('/elements/user/users.html', events=mongo.db.users.find({}))

@app.route('/elements/view/user/<string:id>')
def view_user(id):
    return render_template('/elements/user/view.html', event=mongo.db.users.find_one({"_id": ObjectId(id)}))

@app.route('/elements/delete/user/<string:id>', methods=['GET', 'POST'])
def delete_user(id):
    if id:
        mongo.db.users.delete_one({"_id": ObjectId(id)})
        return redirect('/')
    return 'FAILURE'

@app.route('/elements/edit/user/<string:id>', methods=['GET', 'POST'])
@app.route('/elements/edit/user/', methods=['GET', 'POST'])
@app.route('/elements/edit/user', methods=['GET', 'POST'])
def edit_event(id=None):
    if request.method == 'POST':
        name = request.values.get('name')
        if name:
            if not id:
                redirect_id = mongo.db.users.insert({"name": name})
                return redirect('/')
            else:
                mongo.db.users.update({"_id": ObjectId(id)}, {"name": name})
                redirect_id = id
                return redirect('/')
    return render_template('/elements/user/edit.html',
                           user=mongo.db.users.find_one({"_id": ObjectId(id)}),
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
