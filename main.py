import os
import json
import requests
import re
from dotenv import load_dotenv

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

    if ("لغو" in message or "کنسل" in message) and "سفارش" in message:
     return "cancel_order"

    if ("ثبت" in message or "ایجاد" in message or "جدید" in message) and "سفارش" in message:
     return "add_order"
    
    if "سفارش" in message or "پیگیری" in message:
        return "order_status"
    
    if "fact" in message or "دانستنی" in message or "حقیقت" in message or "واقعیت" in message:
     return "fact"
    
    return "unknown"


def extract_order_id(message):
    match = re.search(r"\b\d{4,8}\b", message)

    if match:
        return match.group()

    return None

def get_order_status(order_id):
    orders=load_orders()
    return orders.get(order_id, "سفارش پیدا نشد")


def cancel_order(order_id):
    orders=load_orders()
    if order_id not in orders:
        return "سفارش پیدا نشد"
    if orders[order_id] == "تحویل داده شده":
        return "این سفارش قبلاً تحویل داده شده و قابل لغو نیست."
    orders[order_id] = "لغو شده"

    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)
    return f"سفارش {order_id} با موفقیت لغو شد."


def add_order(order_id):
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


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    waiting_for_order_id = False
    pending_action = None

    while True:
        user_message = input("پیام شما:")

        if user_message == "exit" or user_message == "خروج":
            print("goodBy")
            break

        if waiting_for_order_id:
            if user_message == "لغو" or user_message == "ولش کن":
                waiting_for_order_id = False
                pending_action = None
                print("باشه درخواست لغو شد")
                continue


            order_id = extract_order_id(user_message)

            if order_id:
                if pending_action == "order_status":
                    status = get_order_status(order_id)
                    print(status)

                elif pending_action == "cancel_order":
                     result = cancel_order(order_id)
                     print(result)

                elif pending_action == "add_order":
                    result = add_order(order_id)
                    print(result)
                waiting_for_order_id = False
                pending_action = None

            else:
                print("لطفاً شماره سفارش معتبر وارد کنید.")

            continue

        intent = detect_intent(user_message)
        print("INTENT:", intent)

        if intent == "order_status":
            order_id = extract_order_id(user_message)

            if order_id:
                status = get_order_status(order_id)
                print(status)

            else:
                print("لطفاً شماره سفارش را وارد کنید.")
                waiting_for_order_id = True
                pending_action = "order_status"


        elif intent == "cancel_order":
            order_id = extract_order_id(user_message)
            if order_id:
                result = cancel_order(order_id)
                print(result)

            else:
                print("لطفاً شماره سفارش را وارد کنید.")
                waiting_for_order_id = True
                pending_action = "cancel_order"


        elif intent == "add_order":
            order_id=extract_order_id(user_message)
            if order_id:
                result=add_order(order_id)
                print(result)
            else:
                print("لطفاً شماره سفارش را وارد کنید.")
                waiting_for_order_id = True
                pending_action = "add_order"

        elif intent == "fact":
            fact = get_fact(api_key)

            if fact:
                print(fact)

        else:
            print("I don't understand your request yet.")

if __name__ == "__main__":
    main()
    
