from flask import Blueprint, request

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST', 'GET'])
def login():
  data = request.form
  print(data)
  return "abc"
