from datetime import datetime

import requests
from flask import jsonify, current_app, request

from app import app_bp
from app.models import User, ContextQuestion, DomainQuestion
import json
from bson import json_util, ObjectId

from app.utils import generate_unique_hex


@app_bp.route('/user/create', methods=['POST'])
def create_user():
    try:
        db = current_app.config['db']
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']

        # Check if the username is already taken
        existing_user = db.users.find_one({"username": username})
        if existing_user:
            return jsonify({"status": "error", "message": "Username already exists"}), 400

        user_data = User(username=username, password=password, first_name=first_name, last_name=last_name, status=True)
        result = db.users.insert_one(user_data.__dict__)

        inserted_user = db.users.find_one({"_id": result.inserted_id})
        inserted_user['_id'] = str(inserted_user['_id'])

        return jsonify({
            "data": {'user': inserted_user},
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/user/login', methods=['POST'])
def login_user():
    try:
        db = current_app.config['db']
        username = request.json['username']
        password = request.json['password']
        print(username, password)

        # Check if the user with the given username exists
        user = db.users.find_one({"username": username})
        print("here")
        if user and user['password'] == password:
            # Authentication successful
            user['_id'] = str(user['_id'])
            return jsonify({
                "data": {'user': user},
                "status": "success",
                "message": "Login Successful"
            }), 200
        else:
            # Authentication failed
            return jsonify({
                "status": "error",
                "message": "Invalid username or password"
            }), 401

    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key in JSON request: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/create', methods=['POST'])
def create_domain_questions():
    try:
        db = current_app.config['db']
        user_id = request.json['user_id']
        domain_id = request.json['domain_id']
        title = request.json['title']
        context_list = request.json['context_list']

        domain_question = DomainQuestion(user_id=user_id, domain_id=domain_id, title=title,
                                         created_date=datetime.utcnow(),
                                         context_list=context_list)

        db.domain_questions.insert_one(domain_question.__dict__)
        return jsonify({
            "status": "success",
            "message": "Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/update', methods=['POST'])
def update_domain_questions():
    try:
        db = current_app.config['db']
        user_id = request.json['user_id']
        domain_id = request.json['domain_id']
        title = request.json['title']
        context_list = request.json['context_list']

        dict_update = {
            "title": title,
            "context_list": context_list
        }
        db.domain_questions.update_one({"domain_id": domain_id, "user_id": user_id}, {"$set": dict_update})
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
        domain_id = request.json['domain_id']

        item_cursor = db.domain_questions.find_one({"user_id": user_id, "domain_id": domain_id})
        if item_cursor:
            item_cursor['_id'] = str(item_cursor['_id'])
        else:
            return jsonify({
                "status": "success",
                "message": "Domain not context not found"
            }), 400
        return jsonify({
            "data": {
                "domain_context": item_cursor
            },
            "status": "success",
            "message": "Questions listed Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/active_question', methods=['POST'])
def active_questions():
    try:
        db = current_app.config['db']
        domain_id = request.json['domain_id']
        active_questions = request.json['active_questions']

        dict_question = {
            "domain_id": domain_id,
            "exam_id": generate_unique_hex(),
            "active_questions": active_questions
        }
        new_question = db.active_questions.insert_one(dict_question)
        inserted_one = db.active_questions.find_one({"_id": new_question.inserted_id})
        inserted_one['_id'] = str(inserted_one['_id'])
        print(inserted_one)
        return jsonify({
            "data": {
                "exam_id": inserted_one['exam_id']
            },
            "status": "success",
            "message": "Active Questions Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/question/domain/publish', methods=['POST'])
def publish_question():
    try:
        db = current_app.config['db']
        domain_id = request.json['domain_id']

        item_cursor = db.active_questions.find_one({"domain_id": domain_id})
        return jsonify({
            "data": {
                "exam_id": item_cursor['exam_id']
            },
            "status": "success",
            "message": "Active Questions Published Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/answer/domain/grade', methods=['POST'])
def grade_answer():
    try:
        db = current_app.config['db']
        student_number = request.json['student_number']
        email = request.json['email']
        student_name = request.json['student_name']
        exam_id = request.json['exam_id']
        answer_list = request.json['answer_list']
        inserted_domain = db.active_questions.find_one({"exam_id": exam_id})

        answer_list_updated = []
        student = db.graded_answer.find_one({"student_number": student_number})
        print(student)
        if not student:
            for key, item in enumerate(inserted_domain['active_questions']):
                item['answer'] = answer_list[key]['answer']
                item['fullmarks'] = int(item['full_marks'])
                answer_list_updated.append(item)

            # Formate of object in answer list {"context":"", "question":"","answer":"", "total_marks":""}
            # target_url = 'http://0.0.0.0:8000/'
            target_url = 'http://answer-grading.ewhsg8ejbgetdbe3.eastus.azurecontainer.io:8000/'
            graded_answer_list = []
            for item in answer_list_updated:
                try:
                    # Make the POST request
                    response = requests.get(target_url, json=item)
                    if response.status_code == 200:
                        # Parse the JSON response
                        result = response.json()
                        item['marks'] = result['marks']
                    else:
                        return jsonify({
                            "status": "fail",
                            "message": response.text
                        }), 400
                except:
                    return jsonify({
                        "status": "fail",
                        "message": "fail to grade"
                    }), 400

                graded_answer_list.append(item)

            # Graded Answer Dictionary
            graded_answer_dict = {
                "student_number": student_number,
                "email": email,
                "student_name": student_name,
                "exam_id": exam_id,
                "graded_answer_list": graded_answer_list
            }
            print(graded_answer_dict)
            db.graded_answer.insert_one(graded_answer_dict)
            return jsonify({
                "status": "success",
                "message": "Answer was Graded Successfully"
            }), 200
        else:
            return jsonify({
                "status": "fail",
                "message": "Student has already submitted the answers"
            }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/domain/add', methods=['POST'])
def create_domain():
    try:
        db = current_app.config['db']
        domain_name = request.json['domain_name']
        domain_id = request.json['domain_id']
        user_id = request.json['user_id']

        domain_dict = {
            "user_id": user_id,
            "domain_name": domain_name
        }

        if domain_id:
            domain_id = ObjectId(domain_id)
            db.domain.update_one({"_id": domain_id}, {"$set": domain_dict})
            inserted_domain = db.domain.find_one({"_id": domain_id})

        else:
            domain_new = db.domain.insert_one(domain_dict)
            inserted_domain = db.domain.find_one({"_id": domain_new.inserted_id})

            # Create Context for specific Domain
            domain_question = DomainQuestion(user_id=user_id, domain_id=str(inserted_domain['_id']), title="Untitled",
                                             created_date=datetime.utcnow(),
                                             context_list=[])

            db.domain_questions.insert_one(domain_question.__dict__)

        inserted_domain['_id'] = str(inserted_domain['_id'])

        return jsonify({
            "data": {"domain_detail": inserted_domain},
            "status": "success",
            "message": "Domain Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/domain/list', methods=['POST'])
def domain_list():
    try:
        db = current_app.config['db']
        user_id = request.json['user_id']

        item_cursor = db.domain.find({'user_id': user_id})

        item_list = list(item_cursor)

        for item in item_list:
            item['_id'] = str(item['_id'])

        return jsonify({
            "data": {"domain_list": item_list[::-1]},
            "status": "success",
            "message": "Domain Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/exam', methods=['POST'])
def get_exam():
    try:
        db = current_app.config['db']
        exam_id = request.json['exam_id']
        item_cursor = db.active_questions.find_one({'exam_id': exam_id})

        for item in item_cursor['active_questions']:
            del item['context']
        print(item_cursor)
        return jsonify({
            "data": {"exam_id": item_cursor['exam_id'],
                     "active_questions": item_cursor['active_questions']},
            "status": "success",
            "message": "Domain Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/exam/result', methods=['POST'])
def get_exam_result():
    try:
        db = current_app.config['db']
        exam_id = request.json['exam_id']

        active_question = db.active_questions.find_one({'exam_id': exam_id})
        active_question['_id'] = str(active_question['_id'])

        item_cursor = db.graded_answer.find({'exam_id': exam_id})
        item_list = list(item_cursor)
        for item in item_list:
            item['_id'] = str(item['_id'])

        return jsonify({
            "data": {
                "active_question": active_question,
                "student_answers": item_list,

            },
            "status": "success",
            "message": "Domain Created Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/domain/exam_id/list', methods=['POST'])
def get_domain_exams():
    try:
        db = current_app.config['db']
        domain_id = request.json['domain_id']

        item_cursor = db.active_questions.find({'domain_id': domain_id})
        item_list = list(item_cursor)

        exam_list = []
        for item in item_list:
            exam_list.append(item['exam_id'])

        return jsonify({
            "data": {
                "exam_list": exam_list[::-1],
            },
            "status": "success",
            "message": "Fetch Exam List Successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app_bp.route('/generate/sequence', methods=['POST'])
def generate_question_sequence():
    context = {"context": request.json['context'],
               "answer": request.json['answer'],
               "answer_start": str(request.json['answer_start'])}

    try:
        target_url = "http://question-seq2seq.g3cgeba9fff2gcg5.eastus2.azurecontainer.io:8000/seq2seq"
        response = requests.post(target_url, data=context, headers={
        })

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"status": "failed", "message": "Failed to generate questions"}), 400
    except:
        return jsonify({"status": "failed", "message": "Failed to generate questions"}), 400
