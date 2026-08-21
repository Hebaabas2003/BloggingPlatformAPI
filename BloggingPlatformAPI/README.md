# Blogging Platform API

A simple RESTful API for a personal blogging platform built using Python, Flask, and SQLite.

Project URL: https://roadmap.sh/projects/blogging-platform-api

## Features

- Create a new blog post
- Get all blog posts
- Get a single blog post by ID
- Update an existing blog post
- Delete a blog post
- Search posts by title, content, or category
- SQLite database
- Basic validation and error handling

## Technologies

- Python
- Flask
- SQLite

## Endpoints

### Create Post

POST /posts

### Get All Posts

GET /posts

### Get Single Post

GET /posts/<id>

### Update Post

PUT /posts/<id>

### Delete Post

DELETE /posts/<id>

### Search Posts

GET /posts?term=tech

## Run the Project

Install the required dependency:

```bash
pip install -r requirements.txt