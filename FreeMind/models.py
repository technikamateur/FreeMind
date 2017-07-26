from FreeMind import db
import time

class LogMessage(db.Model):
   __tablename__ = 'logs'
   id = db.Column(db.Integer, primary_key=True)
   time = db.Column(db.Integer)
   level = db.Column(db.Integer)
   message = db.Column(db.String)

   def __init__(self, level, message):
        self.time = int(time.time())
        self.level = level
        self.message = message

class PiOsUpdate(db.Model):
   __tablename__ = 'pi_os_update'
   id = db.Column(db.Integer, primary_key=True)
   time = db.Column(db.Integer)
   success = db.Column(db.Boolean)
   status = db.Column(db.String)

   def __init__(self, status, success=False):
        self.time = int(time.time())
        self.success = success
        self.status = status

class PiFmUpdate(db.Model):
   __tablename__ = 'pi_fm_update'
   id = db.Column(db.Integer, primary_key=True)
   time = db.Column(db.Integer)
   success = db.Column(db.Boolean)
   status = db.Column(db.String)

   def __init__(self, status, success=False):
        self.time = int(time.time())
        self.success = success
        self.status = status

class PiHddStatus(db.Model):
   __tablename__ = 'pi_hdd_status'
   id = db.Column(db.Integer, primary_key=True)
   time = db.Column(db.Integer)
   success = db.Column(db.Boolean)
   status = db.Column(db.String)

   def __init__(self, status, success=False):
        self.time = int(time.time())
        self.success = success
        self.status = status

class Backup(db.Model):
   __tablename__ = 'backups'
   id = db.Column(db.Integer, primary_key=True)
   time = db.Column(db.Integer)
   success = db.Column(db.Boolean)
   status = db.Column(db.String)

   def __init__(self, status, success=False):
        self.time = int(time.time())
        self.success = success
        self.status = status
