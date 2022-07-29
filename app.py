from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "hoeidnpg5673cgidaencgikdo753489tuhik"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



question_idx = 0

@app.get('/')
def render_initial_page():
    """Displays the survey start page"""
    session["responses"] = []

    return render_template(
        '/survey_start.html',
        survey = survey)
    
@app.post('/begin')
def redirect_to_first_question():
    """Display survey question and choices"""

    return redirect('/question/0')

@app.get("/question/<int:question_idx>")
def display_question(question_idx):
    
    responses = session["responses"]

    if question_idx != len(responses):
        flash("""Hi there!! Please answer all questions in order. 
            Stop tinkering pls and thx""")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[question_idx]

    return render_template(
        '/question.html',
        question = question)


@app.post('/answer')
def take_answer_and_redirect():
    """Gets user answer, updates the answers list 
    and redirects the user to the next questions or shows them the completion page
    if the survey is finished"""
    
    answer = request.form["answer"]
    
    responses = session["responses"]
    responses.append(answer)
    session['responses'] = responses
    
    question_idx = len(responses)

    
    if question_idx == len(survey.questions):  
        return redirect("/completion")

    return redirect(f"/question/{question_idx}")

@app.get("/completion")
def thank_you():
    """Displays the completion page, and thanks the user"""

    return render_template("/completion.html")