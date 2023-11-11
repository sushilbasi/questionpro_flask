from pymongo import MongoClient
from datetime import datetime


class User:
    def __init__(self, username, password, status):
        self.username = username
        self.password = password
        self.status = status


class GeneratedQuestion:
    def __init__(self, question, status):
        self.question = question
        self.status = status


class ContextQuestion:
    def __init__(self, context, generated_questions):
        self.context = context
        self.generated_questions = generated_questions


class ActiveQuestion:
    def __init__(self, question, mark):
        self.question = question
        self.mark = mark


class DomainQuestion:
    def __init__(self, user_id, title, created_date, search_result, act_questions):
        self.user_id = user_id
        self.title = title
        self.created_date = datetime.utcnow()
        self.search_result = search_result
        self.act_questions = act_questions
