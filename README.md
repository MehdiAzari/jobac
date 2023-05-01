# Jobac

Jobac is a personal project to practice django-rest-framework. It provides RESTful APIs for freelancers and recruiters application. It enables recruiters to post job openings and search for freelancers while allowing freelancers to search for job openings and apply for them.

## Installation

1. Install Python 3.6 or higher
2. Clone the Jobac repository
3. Create a virtual environment and activate it
4. Install the required packages by running `pip install -r requirements.txt`
5. Create the database by running `python manage.py migrate`
6. (Optional) Load initial data by running `python manage.py loaddata initial_data.json`

## Usage

1. Run the development server by running `python manage.py runserver`
2. Access the application at `http://127.0.0.1:8000/`

## Features

Jobac provides the following main features:
- Recruiters can create, update, and delete job openings
- Recruiters can search for freelancers by skillset
- Freelancers can search for job openings
for freelancers and recruitre's application
