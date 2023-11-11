import json

from flask import Flask, jsonify, request
from pymongo import MongoClient

from app import app_bp

app = Flask(__name__)

# app.config[
#     "MONGODB_SETTINGS"] = {'host':
#                                "mongodb+srv://questionpro:aiml_capstone@questionpro.txcqcrj.mongodb.net/?retryWrites=true&w=majority"}
#
# db = MongoEngine(app)

clinet = MongoClient(
    'mongodb+srv://questionpro:aiml_capstone@questionpro.txcqcrj.mongodb.net/?retryWrites=true&w=majority')
db = clinet['questionpro']
app.config['db'] = db

# Register the blueprint
app.register_blueprint(app_bp, url_prefix='/api', db=db)

# @app.route('/')
# def create_question():
#     # online_users = mongo.db.users.find({"online": True})
#     # print(online_users)
#     return jsonify({
#         "data": {}
#     }), 200
# #
#
# # @app.route('/question/create', methods=['POST'])
# # def create_question():
# #     # online_users = mongo.db.users.find({"online": True})
# #     # print(online_users)
# #     return jsonify({
# #         "data": {}
# #     }), 200
#
#
# @app.route('/question/', methods=['GET'])
# def get_questions():
#     # online_users = mongo.db.users.find({"online": True})
#     # print(online_users)
#     return jsonify({
#         "data": [],
#         "status": "success",
#         "message": "Questions Created Successfully"
#     }), 200
#
#
# @app.route('/generate_question/', methods=['POST'])
# def generate_question():
#     if request.method == 'POST':
#         # data = json.loads(request.data)
#         print("ankjsdfjs")
#         data = request.data
#         print(data)
#
#         return jsonify({
#             "data": [],
#             "status": "success",
#             "message": "Questions Created Successfully"
#         }), 200


if __name__ == '__main__':
    app.run(debug=True)
