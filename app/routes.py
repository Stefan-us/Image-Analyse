from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.model import classifiers
from app.models import ClassificationHistory
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            model_name = request.form.get('model', 'resnet50')
            
            # Check if the file has already been classified with the same model
            existing_classification = ClassificationHistory.query.filter_by(filename=filename, model_name=model_name).first()
            if existing_classification:
                return render_template('result.html', filename=filename, class_name=existing_classification.class_name, confidence=existing_classification.confidence, filepath=filepath, model_name=existing_classification.model_name)
            
            print(f"Saving file to: {filepath}")
            file.save(filepath)
            print(f"File saved successfully: {os.path.exists(filepath)}")
            
            classifier = classifiers[model_name]()
            class_name, confidence = classifier.predict(filepath)
            print(f"Classified as: {class_name} with confidence: {confidence:.2%}")
            
            # Save classification to database
            new_classification = ClassificationHistory(filename=filename, class_name=class_name, confidence=confidence, model_name=model_name)
            db.session.add(new_classification)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                # Update existing entry if it was created in the meantime
                existing_classification = ClassificationHistory.query.filter_by(filename=filename, model_name=model_name).first()
                if existing_classification:
                    existing_classification.class_name = class_name
                    existing_classification.confidence = confidence
                    db.session.commit()
            
            return render_template('result.html', filename=filename, class_name=class_name, confidence=confidence, filepath=filepath, model_name=model_name)
    return render_template('index.html')

@bp.route('/history')
def history():
    classifications = ClassificationHistory.query.order_by(ClassificationHistory.timestamp.desc()).all()
    return render_template('history.html', classifications=classifications)

@bp.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)