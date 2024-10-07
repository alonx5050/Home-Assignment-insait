from flask import Flask, request, jsonify
import openai
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Hardcode your OpenAI API key directly into the project
openai.api_key = 'sk-NKm6WwaP26nAwZJC1_Z64Zdn8a3nTjgCJ0FnJBJIV6T3BlbkFJlVSpTqWin-BFY5KEDdhnxs7ndDfj7NJro1AOMgH14A'  # Replace this with your actual OpenAI API key

# PostgreSQL connection string (make sure this matches your Docker configuration)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/qna_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model to store questions and answers
class QnA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

# Endpoint to handle questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        # Use OpenAI API to generate an answer
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # You can use 'gpt-3.5-turbo' if you don't have access to GPT-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()

        # Save the question and answer to the database
        new_qna = QnA(question=question, answer=answer)
        db.session.add(new_qna)
        db.session.commit()

        return jsonify({'question': question, 'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
