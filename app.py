from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from resumeParsing import matchingPer
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

job_desc = '''
Job Title: Data Scientist

Company: [Company Name]

Location: [Location]

Job Type: [Full-time/Part-time/Internship]

Job Summary:
About the role:
We are looking for a skilled Data Scientist to join our team. As a Data Scientist, you will be responsible for analyzing complex datasets, developing predictive models, and providing valuable insights to drive business decision-making.

Responsibilities:
Analyze and interpret large datasets to provide actionable insights.
Develop machine learning models and algorithms for predictive analysis.
Collaborate with cross-functional teams to understand business needs and deliver solutions.
Create data visualizations to communicate findings effectively.
Stay updated with the latest trends and technologies in data science.

Responsibilities (Day-to-day):
Analyze data using statistical methods.
Develop predictive models and algorithms.
Collaborate with teams to understand business requirements.
Create data visualizations.
Stay updated with industry trends.

Skills Required:
Python
Machine Learning
Data Analysis
Statistical Analysis
Data Visualization
Communication Skills

Eligibility:
Bachelor's/Master's degree in Computer Science, Statistics, Mathematics, or related field.
[X years] of experience in data science or related field.
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def display_resumes():
    resumes = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(".pdf"):
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            matchPer = matchingPer(resume_path, job_desc)
            resumes.append({
                "Name": matchPer['name'],
                "Percentage": matchPer['per']
            })
    return jsonify(resumes)

@app.route('/', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)
