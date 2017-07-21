from FreeMind import db

class logs(db.Model):
   __tablename__ = 'logs'
   time = db.Column(db.Integer, primary_key=True)
   level = db.Column(db.Integer)
   message = db.Column(db.String)

   def __init__(self, time, level, message):
        self.time = time
        self.level = level
        self.message = message
