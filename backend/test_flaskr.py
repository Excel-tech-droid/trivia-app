import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "excel123", "localhost:5432", self.database_name
        )

        setup_db(self.app, self.database_path)
        self.new_question = {"question": "who is the richest man on earth",
                             "answer": "Elon Musk", "difficulty": 2, "category": 2}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Send a request with a page data greater than available pages
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={"difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'who'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['questions'][1]['id'], 12)
        self.assertEqual(
            data['questions'][1]['question'],
            'Who invented Peanut Butter?')

    def test_create_new_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # @TODO: fix issue of status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])
        question = Question.query.filter_by(id=data['created']).first()
        question.delete()

    def test_create_questions_without_the_required_fields(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        # @TODO: fix issue of status code
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question(self):
        # To test the delete endpoint, a question that we would delete later should be created
        question = Question(
            question=self.new_question['question'],
            answer=self.new_question['answer'],
            category=self.new_question['category'],
            difficulty=self.new_question['difficulty'])
        question.insert()

        res = self.client().delete('/questions/{}'.format(question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question.id)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_play_quiz_game(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [2, 6],
                                       'quiz_category': {
                                     'type': 'Entertainment',
                                     'id': '5'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)
        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 6)

    def test_422_play_quiz_fails(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
