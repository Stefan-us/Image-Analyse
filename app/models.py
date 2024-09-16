from app import db
from datetime import datetime

class ClassificationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    model_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('filename', 'model_name', name='_filename_model_uc'),)

    def __repr__(self):
        return f'<ClassificationHistory {self.filename}>'
