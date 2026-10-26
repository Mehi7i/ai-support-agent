import os
import json
import requests
import re
from dotenv import load_dotenv
from openai import OpenAI

def load_orders():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("فایل سفارش‌ها پیدا نشد.")
        return {}

    except json.JSONDecodeError:
        print("فایل سفارش‌ها خراب است.")
        return {}
    
def detect_intent(message):
    message = message.strip()
    cancel_words = ("لغو", "کنسل", "ابطال")
    add_words = ("ثبت", "ایجاد", "جدید")
    if any(word in message for word in cancel_words) and "سفارش" in message:
        return "cancel_order"
    if any(word in message for word in add_words) and "سفارش" in message:
        return "add_order"
    
    status_words = ("سفارش", "پیگیری", "وضعیت")
    fact_words = ("fact", "دانستنی", "حقیقت", "واقعیت")

    if any(word in message for word in status_words):
        return "order_status"

    if any(word in message for word in fact_words):
        return "fact"
    
    return "unknown"

def detect_intent_with_ai(message, api_key):
    if not api_key:
        return None

    headers = {
        "X-Api-Key": api_key
    }

    data = {
        "message": message
    }

    try:
        response = requests.post(
            "https://api.api-ninjas.com/v1/textclassify",
            headers=headers,
            json=data
        )
    except requests.RequestException as e:
        print("Request failed:", e)
        return None

    if response.status_code == 200:
        return response.json()

    print("API error:", response.status_code)
    print("Response:", response.text)
    return None



def extract_order_id(message):
    message = message.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    match = re.search(r"(?<!\d)\d{4,8}(?!\d)", message)

    if match:
        return match.group()

    return None


def is_valid_order_id(order_id):
    return order_id.isdigit() and 4 <= len(order_id) <= 8

def get_order_status(order_id):
    if not is_valid_order_id(order_id):
        return "شماره سفارش نامعتبر است."
    orders=load_orders()
    return orders.get(order_id, "سفارش پیدا نشد")


def cancel_order(order_id):
    if not is_valid_order_id(order_id):
        return "شماره سفارش نامعتبر است."
    orders = load_orders()

    if order_id not in orders:
        return "سفارش پیدا نشد"

    if orders[order_id] == "تحویل داده شده":
      return "این سفارش قبلاً تحویل داده شده و قابل لغو نیست."

    if orders[order_id] == "لغو شده":
      return "این سفارش قبلاً لغو شده است."

    orders[order_id] = "لغو شده"

    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

    return f"سفارش {order_id} با موفقیت لغو شد."


def add_order(order_id):
    if not is_valid_order_id(order_id):
        return "شماره سفارش نامعتبر است."

    orders = load_orders()

    if order_id in orders:
        return "این شماره سفارش قبلاً وجود دارد."

    orders[order_id] = "در حال پردازش"

    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

    return f"سفارش {order_id} با موفقیت ثبت شد."


def get_fact(api_key):
    if not api_key:
        print("api key not found")
        return None
    headers = {
              "X-Api-Key": api_key
            }
    try:
            response = requests.get(
            "https://api.api-ninjas.com/v1/facts",
            headers=headers
            )
    except requests.RequestException as e:
        print("Request failed:", e)
        return None
    if response.status_code == 200:
        data = response.json()
        return data[0]["fact"]
    
    elif response.status_code == 400:
             print("درخواست نامعتبر")
    elif response.status_code == 401:
            print("احراز هویت ناموفق")
    elif response.status_code == 429:
            print("تعداد درخواست‌ها بیش از حد")
    elif response.status_code == 500:
            print("خطای سرور")
    print("API error:", response.status_code)
    print("Response:", response.text)
    return None

def execute_order_action(order_id, action):
    if action == "order_status":
        return get_order_status(order_id)

    elif action == "cancel_order":
        return cancel_order(order_id)

    elif action == "add_order":
        return add_order(order_id)

    return None



def detect_intent_ai(client, message):
    valid_intents = {
        "order_status",
        "cancel_order",
        "add_order",
        "fact",
        "greeting",
        "unknown"
    }

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": """
تو یک دستیار پشتیبانی مشتری هستی.
وظیفه تو تشخیص نیت اصلی کاربر است.

فقط یکی از این مقادیر را برگردان:
order_status
cancel_order
add_order
fact
greeting
unknown

قوانین تشخیص:
- order_status: کاربر درباره وضعیت یا پیگیری سفارش سؤال می‌کند.
- cancel_order: کاربر درخواست لغو سفارش دارد.
- add_order: کاربر می‌خواهد سفارش جدید ثبت کند.
- fact: کاربر درخواست یک دانستنی یا حقیقت عمومی دارد.
- greeting: کاربر سلام می‌کند یا احوال‌پرسی می‌کند.
- unknown: پیام نامرتبط است یا در هیچ‌کدام از دسته‌های بالا قرار نمی‌گیرد.

اگر مطمئن نیستی، unknown را برگردان.
فقط نام یکی از مقادیر بالا را برگردان و هیچ توضیح دیگری ننویس.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        intent = response.choices[0].message.content

        if not intent:
            return "unknown"

        intent = intent.strip().lower()

        if intent not in valid_intents:
            return "unknown"

        return intent

    except Exception as error:
        print(f"خطا در ارتباط با سرویس هوش مصنوعی: {error}")
        return "unknown"

user_states = {}  # user_id -> {"pending_action": ...}

ORDER_INTENTS = ("order_status", "cancel_order", "add_order")

def handle_message(user_id, text, client, api_key):
    text = text.strip()
    if not text:
        return None

    state = user_states.get(user_id)
    if state:
        return handle_pending(user_id, text, state)

    intent = detect_intent_ai(client, text)

    if intent in ORDER_INTENTS:
        order_id = extract_order_id(text)
        if order_id:
            return execute_order_action(order_id, intent)
        user_states[user_id] = {"pending_action": intent}
        return "لطفاً شماره سفارش را وارد کنید."

    if intent == "fact":
        return get_fact(api_key) or "الان نتونستم دانستنی پیدا کنم."

    if intent == "greeting":
        return "سلام! چطور می‌تونم کمکتون کنم؟"

    return "متوجه درخواستت نشدم. لطفاً واضح‌تر بیان کن."


def handle_pending(user_id, text, state):
    if text in ("لغو", "ولش کن"):
        user_states.pop(user_id)
        return "باشه، درخواست لغو شد."

    if "سفارش" in text:
        user_states.pop(user_id)
        return "لطفاً درخواست خود را دوباره وارد کنید."

    order_id = extract_order_id(text)
    if not order_id:
        return "لطفاً شماره سفارش معتبر وارد کنید."

    action = state["pending_action"]
    user_states.pop(user_id)
    return execute_order_action(order_id, action)


def main():
    load_dotenv()

    api_key = os.getenv("API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    if not openrouter_api_key:
        print("خطا: کلید OPENROUTER_API_KEY در فایل .env تنظیم نشده است.")
        return

    client = OpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    while True:
        try:
            user_message = input("پیام شما: ").strip()

            if not user_message:
                continue

            if user_message.lower() in ("exit", "خروج"):
                print("خدانگهدار!")
                break

            reply = handle_message("cli", user_message, client, api_key)
            if reply:
                print(reply)

        except (KeyboardInterrupt, EOFError):
            print("\nخدانگهدار!")
            break


if __name__ == "__main__":
    main()