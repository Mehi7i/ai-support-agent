# AI Support Agent

A Python customer-support assistant powered by an LLM with **tool calling**. The model decides when to look up, cancel, or create an order, and a rule-based fallback keeps the bot working when the AI service is unavailable. It runs in the terminal and as a Telegram bot.

> **Demo:** [Watch a short demo](https://drive.google.com/file/d/1s-nIsdVPPJpeXPFGTC6lqAoaeNz33IEp/view?usp=sharing)
## Features

- **Tool-calling agent**: the model chooses and calls `get_order_status`, `cancel_order`, or `add_order` with the right order ID
- **Multi-step conversations**: asks for a missing order ID and remembers context per user
- **Automatic model fallback**: tries several OpenRouter models in order
- **Rule-based fallback**: if every AI model fails, the bot still answers using keyword-based intent detection
- **Order management**: status lookup, cancellation with status validation, creation with duplicate-ID checks
- **Input validation** for order IDs (including Persian digits)
- **Telegram bot interface** sharing the same core logic as the CLI
- **Facts feature** using the API Ninjas API
- **JSON-based storage** for order data
- **Environment-based configuration** for credentials
- **Automated tests** with pytest

## How It Works

1. The user's message, the conversation history, and a list of tools are sent to the model.
2. If the model needs data or wants to act, it calls a tool with an order ID.
3. The application runs the real function and returns the result to the model.
4. The model writes the final reply (up to 4 tool rounds per message).

If a model fails (rate limit, outage, no tool support), the next model in `OPENROUTER_MODELS` is tried. If all fail, the message is handled by the rule-based flow, so the user still gets an answer.

## Technologies

- Python
- OpenAI Python SDK (with OpenRouter)
- OpenRouter API (tool calling)
- python-telegram-bot
- Requests
- python-dotenv
- pytest
- Git & GitHub

## Requirements

- Python 3.10 or later
- An OpenRouter API key
- An API Ninjas API key (optional, for the facts feature)
- A Telegram bot token (optional, for the Telegram bot)

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

Create a `.env` file in the project root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
API_KEY=your_api_ninjas_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Optional: comma-separated models, tried in order
OPENROUTER_MODELS=poolside/laguna-s-2.1:free,nvidia/nemotron-3-ultra-550b-a55b:free

# Optional: only if Telegram is blocked on your network
TELEGRAM_PROXY=http://127.0.0.1:10809
```

- `OPENROUTER_API_KEY` is required for the AI agent.
- `API_KEY` is used to retrieve facts from API Ninjas.
- `TELEGRAM_BOT_TOKEN` is required only for the Telegram bot (create one with @BotFather).
- `OPENROUTER_MODELS` should list models that support tool calling. Free models change often, so check the OpenRouter models page for current ones.

Never commit your `.env` file or expose your API keys publicly.

## Usage

### Terminal

```bash
python main.py
```

Type a request and press Enter. Type `exit` or `خروج` to quit.

### Telegram bot

```bash
python telegram_bot.py
```

The terminal and Telegram versions share the same core logic in `main.py`.

## Example

```text
پیام شما: وضعیت سفارش 9999
سفارش 9999 شما تحویل داده شده است.

پیام شما: می‌خوام یه سفارش رو لغو کنم
لطفاً شماره سفارشی که می‌خواهید لغو کنید را بگویید.

پیام شما: 2468
سفارش 2468 با موفقیت لغو شد.
```

Order IDs and statuses depend on the contents of `orders.json`. Replies are written by the model, so the exact wording varies between runs.

## Testing

```bash
python -m pytest
```

The suite covers order logic, input validation, intent detection, API error handling, and the multi-step conversation flow.

## Limitations

- Free OpenRouter models can be rate-limited or unavailable at times; the fallback chain reduces but does not remove this.
- Orders are stored in a local JSON file, which is not suitable for many concurrent users. A database (e.g. SQLite or PostgreSQL) would be the next step.
- Cancellation currently happens without a confirmation step.

## Project Structure

```text
ai-support-agent/
├── main.py
├── telegram_bot.py
├── orders.json
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    ├── __init__.py
    └── test_main.py
```

The `.env` file and virtual environment stay local and must not be committed.

## Author

**Mehi7i**
