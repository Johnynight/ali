import time
from urllib.parse import unquote, parse_qs
from playwright.sync_api import sync_playwright


class SisCat():
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




class PartsViz():
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.bearer_token = 1212
        self.cookies = None


    def decoded_str(self,formdata):
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
            print('olololol')
            browser.close()

        return self.bearer_token, self.cookies

# a = PartsViz(login='v363vc4', password='Vchurikov199707')
# print(a.parser()[0])


# aa = [{'name': 'renderCtx', 'value': '%7B%22pageId%22%3A%229eb003af-7649-454e-8de9-cd030ee3436e%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%22126e0b4f-cba6-4a0d-bdb8-f76bd1e6fc05%22%2C%22audienceIds%22%3A%226Au3o000000Kywj%2C6Au0H000000XZZa%22%7D', 'domain': 'cat.my.site.com', 'path': '/PartsViz/s', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 't', 'value': '!0vaFlJER5UsrfIGrfKp9YI2pARkJi5YS8O/yCf8GE+6HiX+CvWWacnC3MzF+OXsuC3USJWIP3jamDQ==', 'domain': 'cat.my.site.com', 'path': '/cometd/', 'expires': -1, 'httpOnly': True, 'secure': False, 'sameSite': 'Lax'}, {'name': 'BAYEUX_BROWSER', 'value': 'e1a918qb95xdoykh7lurvtpxd18kp', 'domain': 'cat.my.site.com', 'path': '/cometd/', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'CookieConsentPolicy', 'value': '0:1', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1744172933.516861, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'LSKey-c$CookieConsentPolicy', 'value': '0:1', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1744172933.517331, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'BrowserId', 'value': 'rJSC0PYpEe6xV2nqkfoKgg', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1744172934.769205, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}, {'name': 'BrowserId_sec', 'value': 'rJSC0PYpEe6xV2nqkfoKgg', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1744172934.769365, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'PF', 'value': 'vBtJkzuKD1k4zUgZMsVSuX', 'domain': 'fedlogin.cat.com', 'path': '/', 'expires': -1, 'httpOnly': True, 'secure': True, 'sameSite': 'None'}, {'name': 'SSOLangPref', 'value': 'en', 'domain': 'login.cat.com', 'path': '/', 'expires': 1743740935.353237, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}, {'name': 'SSOCookie', 'value': 'djM2M3ZjNHxjYXRyZWNpZD1wc3AtMDAwM2VlZTksT1U9cGVvcGxlLERDPWNhdCxEQz1jb218VnlhY2hlc2xhdiBDSFVSSUtPVnw3OS4xNDIuNTcuMjUyfHtvfUJPUlVTQU4gKEtBWkFLSFNUQU4pe2NhdEFmZmlsaWF0ZWRPcmdDb2RlfVYzNjN7Y2F0QWZmaWxpYXRpb259RGVhbGVye2NhdEFmZmlsaWF0aW9uQ29kZX1DRHtjYXRDVVBJRH0xNjAxNjM0NzE5e3NlY3VyaXR5Q2xhc3N9TGVnYWN5U2VjdXJpdHlDbGFzc3wxNzEyNjcyOTQzfDE3MTI2NTEzNDN8MzYwMDB8b0gvVGtzTmtMa1J3U3htc0FPU0w5WktxQUUwPTt8Mi4wLjB8WkRuV0FHTFViSFZKcUFqV0lBMTc5M09wMWpVRmNSR09PdGI0WHQ2a21oSTFXdzJzU1NKMEtRWm9LNThlSUNpTC9FdEUrZXliR29TczV0R0dVQUQ1cmlnTllJY0ZxSVpNZXpBWGNUdlFjaEdEK1lHSGFCVGl6QmF1dk1zTkZ6alI5UVZReEdSMEhJNk1HVXdXVjlrN2xXZ1ZDOFVOM29tdjIyNS9WMUNKMWxFc3VQMWd0MC8rb1BrRzJwelFyU1RyOXExdWZ5UGtrVnJjaVNWVEoxWlBCRHl2eXNnT0RQT2g1ZmNvVGRrbFo0NUxwL09oVVRIcmhiKzE4QUl1bEpHZ3dPK1V4OC9mNnc2TUVKV2NIMUxseS9QSzR1LzJCY1BLWmRQcjdySS9ZOFNJYmw4WjFTdXJDa0hRL3JtWGVWckFlNHpYb3R5b1h6S2pKa1NRR3dYQ0tnPT0_', 'domain': '.cat.com', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'JSESSIONID', 'value': '0000SaTaUoeKgsETmfDkYU-FKB5:1hgs8i5t6', 'domain': 'login.cat.com', 'path': '/', 'expires': -1, 'httpOnly': True, 'secure': False, 'sameSite': 'Lax'}, {'name': 'oinfo', 'value': 'c3RhdHVzPUFjdGl2ZSZ0eXBlPVVubGltaXRlZCtFZGl0aW9uJm9pZD0wMERpMDAwMDAwMGRNRnU=', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1717820944.448676, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'ssostartpage', 'value': 'https://fedlogin.cat.com/idp/SSO.saml2', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1717820945.183654, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'saml_request_id', 'value': '_2CAAAAY9RT-9FMDAwMDAwMDAwMDAwMDAwAAAA-JwYw6WZ5IPLYF-lETABAO22FoiSRzotzeQ0j69uC06q9pE_N_TmWrkjaG0dxohNCl5wexauYyajSEfgoKCjaEFfp3OPCzV26_UOjGHsoRU5uRiz1uhJmj44fA_ZXrKEay84F0dwHDoG6PRwMt90Bd0GKTe3ecw6JnuXh8rX1mJZwCZE8o7cOQwfF4qixHdkMhLJaqX2Jajp_oeh93CTzc8gHRmzmLgjr9gYABsVQ26V4N5pJSnfVlnpLSilMJ1HEw', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1717820945.184012, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'autocomplete', 'value': '0', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1717820945.184253, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'sid', 'value': '00Di0000000dMFu!AR8AQHTvQkDFXizCS9kGMhERjoiH71C6H9qj5XmTAiQrDBifPU0D1QD6_tYctvy6dWx4kXDXg77XvRZoglwqrQBCT6YdFha3', 'domain': 'cat.my.site.com', 'path': '/', 'expires': -1, 'httpOnly': True, 'secure': True, 'sameSite': 'None'}, {'name': 'sid_Client', 'value': 'o00000BHum00000000dMFu', 'domain': 'cat.my.site.com', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'clientSrc', 'value': '79.142.57.252', 'domain': 'cat.my.site.com', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'inst', 'value': 'APP_3o', 'domain': 'cat.my.site.com', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'oid', 'value': '00Di0000000dMFu', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1744172945.184626, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'sfdc-stream', 'value': '!CxA/gL5U8+kYFRdp9yx50K/HuVfOXhVfRMNegCjvMwHtDk6KvuQOdkQvzRDAoleM9tP1XaAgbOX513M=', 'domain': 'cat.my.site.com', 'path': '/', 'expires': 1712647748.496366, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}]
#
# s = PartsViz(login='v363vc4', password='Vchurikov199707')
# s.parser()