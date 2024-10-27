<h1>API for Managing Posts and Comments with AI Moderation</h1>
<p align="left">
   <img src="https://img.shields.io/badge/Python-3.12.4-blue" alt="Python Version">
   <img src="https://img.shields.io/badge/FastAPI-0.115.2-yellow" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/SQLAlchemy-2.0.36-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Alembic-1.13.3-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Celery-5.4.0-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Flower-2.0.1-green" alt="Beautiful Soup Version">
<img src="https://img.shields.io/badge/Pytest-8.3.3-red" alt="Beautiful Soup Version">
</p>

## About

This project provides a simple API for managing posts and comments, with AI-based content moderation and automated responses. The API is built using FastAPI and Pydantic and includes essential features for user registration, login, post management, and comment management, along with comment and post activity analytics.

### Key Features

#### User Management
- User registration and authentication via JWT for secure session management.

#### Post&Comment Management
- Create, edit, and delete posts.
- Create, edit, and delete comments on posts.

#### AI Moderation
- Checks posts and comments for offensive language or insults and blocks any flagged content.

#### Comment Analytics:
- Provides the number of comments created and blocked over a specified period (by day).

#### Automated Reply Functionality:
- Automatic reply to comments with a user-defined delay. The response content is generated based on the post and the specific comment.


## Running with Docker ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

1. Clone the repository:

   `git clone https://github.com/Amato789/blog_SN`

2. Create an `.env` file and add your own data following the structure and path of the `.env_example` file.
3. Use `make app` to run application, database and all infrastructure.
4. Use `make app-logs` to follow the logs in app container.
5. Go to `http://0.0.0.0:8000/api/docs` link in your browser.



## Available commands:

`make app` - Up application and database infrastructure

`make app-logs` - Follow the logs in app container

`make app-down` - Down application and all infrastructure

`make app-shell` - Go to app shell

## Available services
`http://0.0.0.0:8000/api/docs` - application

`http://0.0.0.0:5555` - flower
