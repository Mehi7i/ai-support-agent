import requests
from main import extract_order_id, get_order_status, cancel_order, add_order, get_fact
from main import extract_order_id, get_order_status, cancel_order, add_order,get_fact

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
