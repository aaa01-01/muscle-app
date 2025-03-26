from datetime import datetime
from app import db

class TrainingRecord(db.Model):
    __tablename__ = 'training_record'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'exercise': self.exercise,
            'weight': self.weight,
            'reps': self.reps,
            'sets': self.sets
        }