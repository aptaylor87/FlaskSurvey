from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

survey = surveys.get('satisfaction')

app = Flask(__name__)

app.config['SECRET_KEY'] = "NoSecretsHere"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


response = []
# rlength = len(response)
# choices = survey.questions[rlength].choices

@app.route('/')
def home_page():
    rlength = len(response)
    return render_template('home.html', survey=survey, rlength=rlength)

@app.route('/questions/<int:question_id>')
def ask_question(question_id):
    rlength = len(response)
    if (rlength == len(survey.questions)):
        return render_template('thanks.html', survey=survey) 
    else:
        if rlength != question_id:
            flash("Do not try to skip questions")
        choices = survey.questions[question_id].choices
        return render_template('question.html', survey=survey, rlength=rlength, choices=choices, response=response)
       

@app.route('/questions/answer', methods=["POST"])
def add_answer():
    answer = request.form["options"]
    response.append(answer)
    rlength = len(response)
    return redirect(f"/questions/{rlength}")


