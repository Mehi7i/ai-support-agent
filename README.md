# AI Support Agent

A Python-based customer support assistant that uses an AI model to understand user requests, manage orders, and retrieve interesting facts through external APIs.

## Features

- **AI-powered intent detection** using OpenRouter
- **Order status lookup** by order ID
- **Order cancellation** with status validation
- **Order creation** with duplicate ID validation
- **Multi-step conversations** for requests that require an order ID
- **JSON-based storage** for order data
- **Input validation** for order IDs
- **Error handling** for API requests
- **Environment-based configuration** for API credentials
- **Automated tests** using pytest

## Technologies

- Python
- OpenAI Python SDK
- OpenRouter API
- Requests
- JSON
- python-dotenv
- pytest
- Git & GitHub

## Requirements

- Python 3.10 or later
- An OpenRouter API key for AI-powered intent detection
- An API Ninjas API key for the facts feature

## Installation

Clone the repository:

```bash
git clone https://github.com/Mehi7i/ai-support-agent.git
cd ai-support-agent
```

Create and activate a virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root directory.

Add your API credentials:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
API_KEY=your_api_ninjas_api_key
```

- `OPENROUTER_API_KEY` is used for AI-powered intent detection.
- `API_KEY` is used to retrieve facts from API Ninjas.

Never commit your `.env` file or expose your API keys publicly.

## Run the Application

Start the assistant:

```bash
python main.py
```

Enter a request in the terminal. Type `exit` or `خروج` to quit.

## Example

```text
پیام شما: سلام
سلام! چطور می‌تونم کمکتون کنم؟

پیام شما: پیگیری سفارش 2469
در حال پردازش
```

The example order ID and its status depend on the contents of `orders.json`.

## Testing

Run the automated test suite:

```bash
python -m pytest
```

## Project Structure

```text
ai-support-agent/
├── main.py
├── orders.json
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    ├── __init__.py
    └── test_main.py
```

The `.env` file and virtual environment should remain local and must not be committed to the repository.

## Author

**Mehi7i**