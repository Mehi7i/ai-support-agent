import requests
from main import extract_order_id, get_order_status, cancel_order, add_order, get_fact,detect_intent,execute_order_action
from main import handle_order_request
def test_extract_order_id():
    assert extract_order_id("6958") == "6958"

def test_extract_order_id_from_sentence():
    assert extract_order_id("شماره سفارشم ۶۹۵۸ هست") == "6958"

def test_extract_order_id_not_found():
    assert extract_order_id("شماره سفارش کجاست؟") is None

def test_get_order_status():
    assert get_order_status("6958") == "لغو شده"

def test_get_order_status_not_found():
    assert get_order_status("1111") == "سفارش پیدا نشد"

def test_cancel_delivered_order():
    assert cancel_order("9999") == "این سفارش قبلاً تحویل داده شده و قابل لغو نیست."

def test_cancel_order_not_found():
    assert cancel_order("1111") == "سفارش پیدا نشد"

def test_cancel_order_success(monkeypatch, tmp_path):
    orders_file = tmp_path / "orders.json"

    orders_file.write_text(
        '{"2468": "در حال پردازش"}',
        encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)

    assert cancel_order("2468") == "سفارش 2468 با موفقیت لغو شد."

def test_add_order_success(monkeypatch, tmp_path):
    orders_file = tmp_path / "orders.json"

    orders_file.write_text(
        '{"2468": "در حال پردازش"}',
        encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)

    assert add_order("1357") == "سفارش 1357 با موفقیت ثبت شد."

def test_add_order_duplicate(monkeypatch, tmp_path):
    orders_file = tmp_path / "orders.json"

    orders_file.write_text(
        '{"2468": "در حال پردازش"}',
        encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)

    assert add_order("2468") == "این شماره سفارش قبلاً وجود دارد."

def test_get_fact_without_api_key():
    assert get_fact(None) is None

def test_get_fact_success(monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return [{"fact": "Python is a programming language."}]

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("main.requests.get", fake_get)

    assert get_fact("fake-api-key") == "Python is a programming language."

def test_get_fact_unauthorized(monkeypatch):
    class FakeResponse:
        status_code = 401
        text = "Unauthorized"

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("main.requests.get", fake_get)

    assert get_fact("fake-api-key") is None

def test_get_fact_request_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException()

    monkeypatch.setattr("main.requests.get", fake_get)

    assert get_fact("fake-api-key") is None

def test_detect_intent_with_extra_spaces():
    assert detect_intent("   پیگیری   ") == "order_status"

def test_detect_intent_status():
    assert detect_intent("وضعیت سفارش") == "order_status"

def test_detect_intent_cancel_with_abort():
        assert detect_intent("ابطال سفارش") == "cancel_order"

def test_detect_intent_add_order():
    assert detect_intent("ثبت سفارش") == "add_order"

def test_detect_intent_cancel_order():
    assert detect_intent("لغو سفارش") == "cancel_order"

def test_detect_intent_fact():
    assert detect_intent("یک دانستنی بگو") == "fact"

def test_detect_intent_unknown():
    assert detect_intent("سلام خوبی؟") == "unknown"

def test_detect_intent_cancel_with_kansel():
    assert detect_intent("کنسل سفارش") == "cancel_order"

def test_detect_intent_create_order():
    assert detect_intent("ایجاد سفارش") == "add_order"

def test_detect_intent_new_order():
    assert detect_intent("سفارش جدید") == "add_order"

def test_detect_intent_cancel_priority():
    assert detect_intent("لغو سفارش 6958") == "cancel_order"

def test_detect_intent_add_priority():
    assert detect_intent("ثبت سفارش 1234") == "add_order"

def test_extract_order_id_rejects_short_number():
    assert extract_order_id("123") is None

def test_extract_order_id_rejects_long_number():
    assert extract_order_id("123456789") is None

def test_execute_order_action_unknown_order():
    assert execute_order_action("1111", "order_status") == "سفارش پیدا نشد"

def test_execute_order_action_cancel_delivered_order():
    assert execute_order_action("9999", "cancel_order") == "این سفارش قبلاً تحویل داده شده و قابل لغو نیست."

def test_execute_order_action_invalid_action():
    assert execute_order_action("6958", "something") is None

def test_handle_order_request_with_order_id():
    assert handle_order_request("وضعیت سفارش 6958", "order_status") == "لغو شده"

def test_handle_order_request_without_order_id():
    assert handle_order_request("وضعیت سفارش", "order_status") is None

def test_handle_order_request_add_order():
    assert handle_order_request("ثبت سفارش 4321", "add_order") == "این شماره سفارش قبلاً وجود دارد."

def test_add_order_invalid_order_id():
    assert add_order("abc") == "شماره سفارش نامعتبر است."

def test_cancel_order_invalid_order_id():
    assert cancel_order("abc") == "شماره سفارش نامعتبر است."