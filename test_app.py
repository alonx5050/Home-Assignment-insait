import pytest
from unittest.mock import patch
from app import app, QnA

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client  # Provide app context for the test

# Mock the database model and methods
@patch('app.db.session.add')
@patch('app.db.session.commit')
@patch('app.QnA.query.filter_by')
def test_ask_endpoint(mock_filter_by, mock_commit, mock_add, client):
    # Mock the behavior of QnA query
    mock_filter_by.return_value.first.return_value = QnA(question='What is the capital of Israel?', answer='Jerusalem')

    # Post a question to the /ask endpoint
    response = client.post('/ask', json={'question': 'What is the capital of Israel?'})
    assert response.status_code == 200  # Ensure the response status is 200 OK
    data = response.get_json()
    assert 'answer' in data  # Ensure the response contains an answer
    assert 'Jerusalem' in data['answer']  # Check that 'Jerusalem' is part of the answer

    # Verify that database methods were called
    mock_add.assert_called_once()
    mock_commit.assert_called_once()
