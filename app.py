from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
question_idx =0

@app.get('/')
def render_initial_page():
    
    return render_template(
        '/survey_start.html',
        survey_title = survey.title,
        survey_instructions = survey.instructions)
    
@app.post('/begin')
def redirect_to_first_question():

    return redirect('/question/0')

@app.get('/question/<int:question_idx>')
def display_question(question_idx):
    
    question = survey.questions[question_idx]
    choices = question.choices

    return render_template(
        '/question.html',
        question = question,
        choices = choices)


# @app.post('/answer')
# def take_answer_and_redirect():
#     request.

