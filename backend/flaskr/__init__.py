import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginate the results of question query


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

# get the current category of a question


def get_current_category(current_questions):
    categoriesList = Category.query.all()
    categories = {}

    for category in categoriesList:
        categories[category.id] = category.type

    current_category = next(
        (categories.get(item) for item in categories if item == current_questions[1].get('category')), None)

    return [categories, current_category]


# check if a question has already been asked
def filter_prev_question(prev_questions, id):
    for prev_id in prev_questions:
        if prev_id == id:
            return True
    return False

# check values of input fields for creating questions


def check_values(values):
    for value in values:
        if value == '':
            return True
    return False


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={'/': {'origins': '*'}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
# CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def retrieve_categories():
        categoriesList = Category.query.order_by(Category.id).all()
        categories = {}
        for category in categoriesList:
            categories[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": categories
        })
    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        else:
            category_values = get_current_category(current_questions)
            categories = category_values[0]
            current_category = category_values[1]
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(current_questions),
                    "categories": categories,
                    "current_category": current_category
                }
            )
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(404)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        if body is None:
            abort(400)

        new_question = body.get('question', None)
        new_category = body.get('category', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)

        values = [new_question, new_answer, new_difficulty, new_category]
        check = check_values(values)
        if check == True:
            abort(400)
        try:
            question = Question(question=new_question, category=new_category, answer=new_answer,
                                difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()

        search = body.get('searchTerm', None)
        if search == '':
            abort(422)
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search))).all()
            if len(selection) == 0:
                abort(404)
            else:
                questions = paginate_questions(request, selection)
                category_values = get_current_category(questions)
                current_category = category_values[1]
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(selection),
                    'current_category': current_category
                })
        except:
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).first()
        if (category is None):
            abort(400)
        questionsList = Question.query.filter_by(category=category.id).all()
        questions = paginate_questions(request, questionsList)
        num_questions = len(questions)
        current_category = category.type

        return jsonify(
            {
                "success": True,
                'questions': questions,
                'total_questions': num_questions,
                'current_category': current_category
            }
        )

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        body = request.get_json()
        category = body.get('quiz_category', None)
        prev_questions = body.get('previous_questions', None)

        try:
            category = int(category['id'])
            if(category == 0):
                question_set = Question.query.all()
            else:
                question_set = Question.query.filter_by(
                    category=category).all()
            num_questions = []

            for question in question_set:
                if filter_prev_question(prev_questions, question.id) is False:
                    num_questions.append(question)

            if len(num_questions) <= 0:
                return jsonify({
                    'success': False
                })

            random.shuffle(num_questions)
            next_question = num_questions[0].format()

            return jsonify({
                'success': True,
                'question': next_question
            })

        except:
            abort(422)

    '''   
  @TODO:  
  Create error handlers for all expected errors 
  including 404 and 422.   
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server error"
        }), 500

    return app