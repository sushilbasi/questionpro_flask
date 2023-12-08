from pymongo import MongoClient
from datetime import datetime


class User:
    def __init__(self, username, password, first_name, last_name, status):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
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
    def __init__(self, user_id,domain_id, title, created_date, context_list):
        self.user_id = user_id
        self.domain_id = domain_id
        self.title = title
        self.created_date = created_date
        self.context_list = context_list
