import os
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Get the API key from the .env file via environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

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
    
        completion = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )

        
        answer = completion.choices[0].message.content.strip()

        
        new_qna = QnA(question=question, answer=answer)
        db.session.add(new_qna)
        db.session.commit()

        return jsonify({'question': question, 'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')