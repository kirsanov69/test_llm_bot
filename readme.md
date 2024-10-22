**AI Assistant Bot**
AI Assistant Bot is a conversational assistant built using Python and FastAPI. It can respond to user queries and perform tasks based on the conversation context.

**Features**
Conversational AI assistant

Handles user queries and tasks

Deployed on Heroku

Uses FastAPI for the web server

Dockerized for easy deployment

**Technologies**

Python 3.9

FastAPI: Web framework for building APIs

Docker: Containerization platform

Heroku: Cloud platform for deployment

Uvicorn: ASGI server for FastAPI

Requests: HTTP library for Python

**Architecture**

FastAPI Application: The main web server that handles incoming HTTP requests and processes them.

Webhook: Handles incoming POST requests from Telegram and processes user messages.

Logging: Logs events and errors for monitoring and debugging.

Docker: Used to create a container for the application, ensuring isolation and portability.

Heroku: Platform used for deploying and hosting the application.

Setup and Deployment

**Prerequisites**

Docker

Heroku CLI

Python 3.9

Local Setup

**Clone the repository:**

git clone https://github.com/kirsanov69/test_llm_bot

cd ai-assistant-bot

**Create a virtual environment and activate it:**

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install dependencies:**

pip install -r requirements.txt

**Run the application:**

uvicorn webhook:app --reload

**Docker Setup**

docker build -t ai-assistant-bot .

**Run the Docker container**

docker run -d -p 8000:8000 ai-assistant-bot

**Deployment on Heroku**

**Login to Heroku:**

heroku login

**Create a new Heroku application:**

heroku create your-app-name

**Set environment variables:**

heroku config:set BOT_TOKEN='your-bot-token'

heroku config:set GPT_TOKEN='your-gpt-token'

heroku config:set ASSISTANT_ID='your-assistant-id'

heroku config:set WEBHOOK_URL='https://your-app-name.herokuapp.com/webhook'

**Deploy the application:**

git add .

git commit -m "Initial commit"

git push heroku master

**Set the webhook for your bot:**

curl -F "url=https://your-app-name.herokuapp.com/webhook" https://api.telegram.org/bot<BOT_TOKEN>/setWebhook

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.


This README provides an overview of the AI Assistant Bot project, including setup instructions, deployment steps, and contact information.
