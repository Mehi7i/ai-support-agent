# AI Support Agent

A simple Python-based customer support agent that understands user requests, manages orders, and retrieves facts from an external API.

## Features

* Detects user intent
* Checks order status
* Cancels orders
* Creates new orders
* Stores orders in a JSON file
* Handles missing or corrupted JSON files
* Supports multi-step conversations
* Retrieves interesting facts using an external API
* Handles API errors
* Uses environment variables for API credentials

## Project Structure

```text
ai-support-agent/
│
├── main.py
├── orders.json
├── requirements.txt
├── .gitignore
└── .env
```

## Requirements

* Python 3.10+
* An API Ninjas API key for the facts feature

## Installation

Clone the repository:

```bash
git clone https://github.com/Mehi7i/ai-support-agent.git
cd ai-support-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory:

```env
API_KEY=your_api_key_here
```

Do not upload the `.env` file to GitHub.

## Run

Start the application with:

```bash
python main.py
```

## Example

```text
پیام شما: میخوام سفارشم رو لغو کنم
INTENT: cancel_order

پیام شما: 6958
سفارش 6958 با موفقیت لغو شد.
```

## Technologies

* Python
* JSON
* Requests
* python-dotenv
* REST API
* Git & GitHub

## Author

Mehi7i
