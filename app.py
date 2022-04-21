from flask import Flask, jsonify, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os



app = Flask(__name__)
# app.debug = True
PATH = os.path.abspath('.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/todos.db'.format(PATH)

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
class Todo(db.Model):
    id = db.Column(db.Integer(),primary_key=True,  nullable=False)
    content = db.Column(db.String(100), nullable=False)
    isCompleted = db.Column(db.Boolean(), default=False)


class TodoSchema(ma.Schema):
    '''March...'''
    class Meta:
        fields = ['id','content','isCompleted']

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

@app.route("/", methods=['GET'])
def index():
    return jsonify({"status" :'ok', 'code': 200})


@app.route("/api/v1/todos")
def get_todos():
    todos = Todo.query.all()
    return jsonify(todos_schema.dump(todos))

@app.route("/api/v1/add_todo", methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = Todo(content=data['content'])

    db.session.add(todo)
    db.session.commit()
    return jsonify({'response':'ok','code':200})

@app.route("/api/v1/delete_todo/<id>", methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    db.session.delete(todo)
    db.session.commit()
    # data = request.get_json()
    # todo = Todo(content=data['content'])

    # db.session.add(todo)
    # db.session.commit()
    return jsonify({'response':'ok','code':200, 'message':'Todo was deleted'})


@app.route("/api/v1/update_todo/<id>", methods=['PUT'])
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    data = request.get_json()

    todo.content = data['content']
    todo.isCompleted = data['isCompleted']

    db.session.commit()
    return jsonify({'message':''})



if __name__ == '__main__':
    app.run()
