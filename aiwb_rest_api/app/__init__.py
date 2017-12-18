from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from app import models
from flask import Flask, request, jsonify, make_response
# from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from app import models,db




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = models.User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = models.User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = models.User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = models.User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = models.User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = models.User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = models.User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/dataset', methods=['GET'])
#@token_required
def get_all_todos():
    #todos = models.Dataset.query.filter_by(user_id=current_user.id).all()
    datasets = models.Dataset.query.all()

    output = []

    for dataset in datasets:

        output.append(dataset.to_json())

    return jsonify({'datasets' : output})
#
# @app.route('/todo/<todo_id>', methods=['GET'])
# @token_required
# def get_one_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
#
#     if not todo:
#         return jsonify({'message' : 'No todo found!'})
#
#     todo_data = {}
#     todo_data['id'] = todo.id
#     todo_data['text'] = todo.text
#     todo_data['complete'] = todo.complete
#
#     return jsonify(todo_data)

@app.route('/dataset', methods=['POST'])
#@token_required
def create_todo():
    data = request.get_json()

    # new_dataset = Todo(text=data['text'], complete=False, user_id=current_user.id)
    # db.session.add(new_todo)
    # db.session.commit()

    datasetobject = models.Dataset.from_json(data)
    datasetobject.save()
    for x in data.get("data"):
        imageobject = models.Image.from_json(x, datasetobject)
        imageobject.save()
        for y in x.get("annotationHistory", imageobject):
            annotationobject = models.AnnotationSession.from_json(y, imageobject)
            annotationobject.save()
            for z in y.get("clusters", annotationobject):
                clusterobject = models.Cluster.from_json(z, annotationobject)
                clusterobject.save()

    return jsonify({'message' : "Dataset created!"})
#
# @app.route('/todo/<todo_id>', methods=['PUT'])
# @token_required
# def complete_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
#
#     if not todo:
#         return jsonify({'message' : 'No todo found!'})
#
#     todo.complete = True
#     db.session.commit()
#
#     return jsonify({'message' : 'Todo item has been completed!'})
#
# @app.route('/todo/<todo_id>', methods=['DELETE'])
# @token_required
# def delete_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
#
#     if not todo:
#         return jsonify({'message' : 'No todo found!'})
#
#     db.session.delete(todo)
#     db.session.commit()
#
#     return jsonify({'message' : 'Todo item deleted!'})

if __name__ == '__main__':
    app.run(debug=True)
