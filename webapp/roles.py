from flask import Blueprint, request

roles = Blueprint("roles", __name__)

@roles.route("/login", methods=['POST', 'GET'])
def login():
  data = request.form
  print(data)
  return "abc"
