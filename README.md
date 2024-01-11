<h1 align="center">Welcome to Flashcard Manager API 👋</h1>
<p>
</p>

> The server part of the flashcard manager API, written as an engineering thesis project. For the client part, see [Flashcard Manager WEB](https://github.com/Aizu4/flashcard_manager_web)

## Technologies

* [Django](https://www.djangoproject.com/)
* [Django Ninja](https://django-ninja.dev/)
* [SQLite](https://www.sqlite.org/index.html)

## Prerequisites

To install the project, you need to have [Python](https://www.python.org/) installed on your computer.

## Install

Clone the repository

```sh
git clone https://github.com/Aizu4/flashcard_manager_api.git
```

Go to the project directory

```sh
cd flashcard_manager_api
```

Install dependencies

```sh
pip install -r requirements.txt
```

You will also need to set up the .env file based on the [.env.example](https://github.com/Aizu4/flashcard_manager_api/blob/master/.env.example) file. The variables are:

* SECRET_KEY - Django secret key (you can generate it [here](https://djecrety.ir/))
* OPENAI_API_KEY - OpenAI API key



## Usage

```sh
django-admin runserver
```

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_