# LanguAI

LanguAI is an AI-powered language tutor web application. Users can register, log in, and interact with a conversational AI assistant to learn new languages through speech and text.

## Features

- User registration and authentication
- Select native and target languages
- Interactive lessons powered by OpenAI GPT and Whisper
- Speech-to-text and text-to-speech integration
- Persistent user sessions and conversation threads

## Getting Started

### Prerequisites

- Python 3.10+
- [OpenAI API key](https://platform.openai.com/)
- [Node.js](https://nodejs.org/) (for static assets, optional)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/langu-ai.git
    cd langu-ai
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Copy `.sample.env` to `.env` and fill in your OpenAI credentials:
    ```sh
    cp .sample.env .env
    ```

4. Run database migrations:
    ```sh
    alembic upgrade head
    ```

5. Start the server:
    ```sh
    uvicorn main:app --reload
    ```

6. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure

- `main.py` - FastAPI application entry point
- `user/` - User models, authentication, and routes
- `gpt/` - GPT and Whisper integration, lesson logic
- `static/` - Frontend JS/CSS assets
- `templates/` - Jinja2 HTML templates
- `alembic/` - Database migrations

## License

Apache 2.0. See [LICENSE](LICENSE).

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI](https://openai.com/)
