# from . import db

# class Role(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100))
#   user = db.relationship('User', uselist=False, backref='role')

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100))
#   role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
