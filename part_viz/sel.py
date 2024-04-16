import time
from urllib.parse import unquote, parse_qs
from playwright.sync_api import sync_playwright


class SisCat:
    def __init__(self, parts: list, login: str, password: str):
        self.parts = parts
        self.login = login
        self.password = password
        self.bearer_token = None

    def log_request_headers(self, request):
        auth_header = request.headers.get('authorization')
        if auth_header and auth_header.startswith('Bearer '):
            self.bearer_token = auth_header.split(' ')[1]

    def parser(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()

            context.on("request", self.log_request_headers)

            page = context.new_page()
            page.goto('https://sis2.cat.com/#/')
            username_input = page.wait_for_selector("id=signInName")
            username_input.type(self.login, delay=1)
            username_input.press('Enter')
            password_input = page.wait_for_selector('id=password')
            time.sleep(2)
            password_input.type(self.password, delay=3)
            password_input.press('Enter')
            page.wait_for_timeout(20000)

        return self.bearer_token


class PartsViz:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.bearer_token = 1212
        self.cookies = None

    def decoded_str(self, formdata):
        decoded = unquote(formdata)
        parsed_data = parse_qs(decoded)
        return parsed_data.get('aura.token', [None])[0]

    def log_request_data(self, request):
        if request.method == "POST":
            post_data_bytes = request.post_data_buffer
            if post_data_bytes:
                self.bearer_token = self.decoded_str(post_data_bytes)

    def convert_cookies_to_dict(self, cookies_list):
        cookies_dict = {}
        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict

    def parser(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            context.on("request", self.log_request_data)

            page = context.new_page()
            page.goto('https://cat.my.site.com/PartsViz/s/')
            user_name = page.wait_for_selector('input[placeholder="Username"]')
            user_name.fill(self.login)
            time.sleep(2)
            user_name.press('Enter')
            user_password = page.wait_for_selector('input[placeholder="Password"]', timeout=10000)
            user_password.fill(self.password)
            time.sleep(2)
            user_password.press('Enter')

            page.wait_for_timeout(20000)

            raw_cookies = context.cookies()
            self.cookies = self.convert_cookies_to_dict(raw_cookies)
            print('Token has been received')
            browser.close()

        return self.bearer_token, self.cookies
