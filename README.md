
# Full Stack API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.


The application features:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2. Delete questions.
3. Add questions and require that they include question and answer text. 
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
 

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## DOCUMENTATION
## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/questions`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.



### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not allowed 
- 500: Internal Server Error 




### Resource Endpoints 
#### GET /questions
- General:
    - An endpoint to handle GET requests for questions, including pagination.
    - Returns a list of categories, question objects, success value, and total number of questions and current category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "humerus",
      "category": 1,
      "difficulty": 2,
      "id": 40,
      "question": "What is the longest bone in the body"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Elon Musk",
      "category": 1,
      "difficulty": 1,
      "id": 86,
      "question": "who is the richest man on earth"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "Elon Musk",
      "category": 2,
      "difficulty": 1,
      "id": 83,
      "question": "who is the richest man on earth"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 10
}

```
#### GET /categories
- General:
    - An endpoint to handle GET requests for all available categories.
    - Returns a list of categories of questions available in the app and a success value
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
#### GET /categories/{category_id}/questions
- General:
    - A GET endpoint to get questions based on category. 
    - Returns a list of questions for the given category id if it exists, the current category, the total number for questions and a success value
    - The category id must be an integer
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` {
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "humerus",
      "category": 1,
      "difficulty": 2,
      "id": 40,
      "question": "What is the longest bone in the body"
    },
    {
      "answer": "Elon Musk",
      "category": 1,
      "difficulty": 1,
      "id": 86,
      "question": "who is the richest man on earth"
    }
  ],
  "success": true,
  "total_questions": 5
}

```
#### DELETE /questions/{question_id}
- General:
    - An endpoint to DELETE question using a question ID. 
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
-Sample: `curl -X DELETE http://127.0.0.1:5000/questions/25?page=2`
```
{
  "deleted": 25,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### POST /questions

- General:
    - An endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
-Sample: `curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question":"who is the richest man in the world", "answer":"Elon Musk", "category":"2", "difficulty":"2"}'`
```
{
  "created": 26,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Elon Musk",
      "category": 2,
      "difficulty": 2,
      "id": 26,
      "question": "who is the richest man in the world"
    }
  ],
  "success": true,
  "total_questions": 20
}
```




#### POST /questions/search

- General:

    - A POST endpoint to get questions based on a search term. 
    - It returns any questions for whom the search term is a substring of the question, the current category, the total questions that match  and a success value
-Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`
```
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Elon Musk",
      "category": 2,
      "difficulty": 2,
      "id": 26,
      "question": "who is the richest man in the world"
    }
  ],
  "success": true,
  "total_questions": 4
}
```


#### POST /quizzes

- General:
    - A POST endpoint to get questions to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
    {'':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
-Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": 1}, "previous_questions":[20, 21]}'`
```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```


## Deployment N/A

## Authors
Oluwadarasimi Okeniyi Based on the Udacity Nanodegree 'FullStack Development'

## Acknowledgements 
The awesome team Ubuntu at Udacity