from flask import jsonify, current_app, request

from app import app_bp
from app.models import User, ContextQuestion, DomainQuestion
import json
from bson import json_util


@app_bp.route('/user/create', methods=['POST'])
def create_user():
    try:
        db = current_app.config['db']
        username = request.json['username']
        password = request.json['password']

        user_data = User(username=username, password=password, status=True)
        result = db.users.insert_one(user_data.__dict__)

        inserted_user = db.users.find_one({"_id": result.inserted_id})
        return jsonify({
            "data": {'user': json_util.dumps(inserted_user)},
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/create', methods=['POST'])
def create_domain_questions():
    try:
        db = current_app.config['db']
        user_id = request.json['user_id']
        title = request.json['title']

        domain_question = DomainQuestion(user_id=user_id, title=title, search_result=[], act_questions=[])
        domain = db.users.insert_one(domain_question.__dict__)
        return jsonify({
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/list', methods=['POST'])
def get_user_domain_questions():
    try:
        db = current_app.config['db']
        user_id = request.json['user_id']

        item_cursor = db.domain_quesitons.find({'user_id': user_id})

        item_list = list(item_cursor)

        return jsonify({
            "data": {
                "domains": item_list
            },
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/update', methods=['POST'])
def update_questions():
    try:
        db = current_app.config['db']
        domain_id = request.json['domain_id']
        search_result = request.json['search_result']
        active_questions = request.json['active_questions']

        result = db.domain_quesitons.find_one({'_id': domain_id})
        db.users.update_one({"_id": domain_id}, {"search_result": search_result, "active_questions": active_questions})
        return jsonify({
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/', methods=['GET'])
def test():
    return jsonify({
        "data": {},
        "status": "success",
        "message": "Questions Created Successfully"
    }), 200