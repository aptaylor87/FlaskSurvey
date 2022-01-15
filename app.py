from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

RESPONSES_KEY = "responses"


survey = surveys.get('satisfaction')

app = Flask(__name__)

app.config['SECRET_KEY'] = "NoSecretsHere"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('home.html', survey=survey,)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/questions/<int:question_id>')
def ask_question(question_id):
    response = session[RESPONSES_KEY]
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
    response = session[RESPONSES_KEY]
    answer = request.form["options"]
    response.append(answer)
    session[RESPONSES_KEY] = response
    rlength = len(response)
    return redirect(f"/questions/{rlength}")

# Solution code
# from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
# from surveys import satisfaction_survey as survey

# # key names will use to store some things in the session;
# # put here as constants so we're guaranteed to be consistent in
# # our spelling of these
# RESPONSES_KEY = "responses"

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


# @app.route("/")
# def show_survey_start():
#     """Select a survey."""

#     return render_template("survey_start.html", survey=survey)


# @app.route("/begin", methods=["POST"])
# def start_survey():
#     """Clear the session of responses."""

#     session[RESPONSES_KEY] = []

#     return redirect("/questions/0")


# @app.route("/answer", methods=["POST"])
# def handle_question():
#     """Save response and redirect to next question."""

#     # get the response choice
#     choice = request.form['answer']

#     # add this response to the session
#     responses = session[RESPONSES_KEY]
#     responses.append(choice)
#     session[RESPONSES_KEY] = responses

#     if (len(responses) == len(survey.questions)):
#         # They've answered all the questions! Thank them.
#         return redirect("/complete")

#     else:
#         return redirect(f"/questions/{len(responses)}")


# @app.route("/questions/<int:qid>")
# def show_question(qid):
#     """Display current question."""
#     responses = session.get(RESPONSES_KEY)

#     if (responses is None):
#         # trying to access question page too soon
#         return redirect("/")

#     if (len(responses) == len(survey.questions)):
#         # They've answered all the questions! Thank them.
#         return redirect("/complete")

#     if (len(responses) != qid):
#         # Trying to access questions out of order.
#         flash(f"Invalid question id: {qid}.")
#         return redirect(f"/questions/{len(responses)}")

#     question = survey.questions[qid]
#     return render_template(
#         "question.html", question_num=qid, question=question)


# @app.route("/complete")
# def complete():
#     """Survey complete. Show completion page."""

#     return render_template("completion.html")


