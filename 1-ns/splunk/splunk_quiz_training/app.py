from flask import Flask, render_template, request, redirect, url_for, session
import json5 as json
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

def answers_to_indices(answer):
    return [ord(char) - ord('A') for char in answer]

@app.route('/', methods=['GET'])
def index():
    session.clear()

    # Load questions from questions.json
    with open('output.json5', 'r') as file:
        questions_data = json.load(file)

    # Shuffle the questions
    random.shuffle(questions_data)
    session['questions_data'] = questions_data[:5]  # Limit to 5 questions and store in session

    session['score'] = 0
    session['current_question_index'] = 0

    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'questions_data' not in session or 'current_question_index' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_answers = request.form.getlist('answer')
        current_question_data = session['questions_data'][session['current_question_index']]
        correct_answer_indices = answers_to_indices(current_question_data['answer'])
        user_answer_indices = [int(index) for index in user_answers]
        
        user_choices = [current_question_data['choices'][index] for index in user_answer_indices]
        correct_choices = [current_question_data['choices'][index] for index in correct_answer_indices]
        
        session['previous_correct_answer'] = ', '.join(correct_choices)
        session['user_answer_string'] = ', '.join(user_choices)
        
        if set(user_answer_indices) == set(correct_answer_indices):
            session['score'] += 1
        
        session['current_question_index'] += 1
        
        explanation = current_question_data.get('explanation')
        session['explanation'] = explanation if explanation else "No explanation provided."
        
        # Check if all questions have been answered
        if session['current_question_index'] >= len(session['questions_data']):
            # Instead of redirecting to results, redirect to answer to show the last question's answer and explanation
            session['show_results_after_answer'] = True  # Use this flag to indicate that after showing the last answer, results should be shown
            return redirect(url_for('answer'))
        else:
            return redirect(url_for('answer'))
    
    current_question_data = session['questions_data'][session['current_question_index']]
    return render_template('question.html', question=current_question_data, question_number=session['current_question_index'] + 1)

@app.route('/answer', methods=['GET'])
def answer():
    if 'current_question_index' not in session or session['current_question_index'] > len(session['questions_data']):
        # If there's no current question index or it's beyond the questions list, redirect to index
        return redirect(url_for('index'))

    show_results_button = False
    if 'show_results_after_answer' in session and session['show_results_after_answer']:
        # If it's time to show results after this answer, indicate that a "Continue to Results" button should be shown
        show_results_button = True
        # Optionally clear the flag here if you don't need it anymore
        # session.pop('show_results_after_answer', None)

    question_number = session['current_question_index']

    # Render the answer template with the flag to show or hide the results button
    return render_template('answer.html',
                           previous_correct_answer=session.get('previous_correct_answer'),
                           user_answer=session.get('user_answer_string'), 
                           question_number=question_number,  # Adjusted to match the question number
                           explanation=session.get('explanation'),
                           show_results_button=show_results_button)


@app.route('/results', methods=['GET'])
def results():
    # Check if the needed keys exist in the session
    if 'score' in session and 'questions_data' in session:
        # Retrieve and store session data in local variables before clearing
        correct = session['score']
        total = len(session['questions_data'])
        
        # Clear the session data immediately to ensure it's not reused
        session.clear()
        
        # Render and return the template using the local variables
        return render_template('results.html', correct=correct, total=total)
    else:
        # Handle the case where the session does not contain the expected data
        return "Error: Session data is missing."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False, debug=True)
