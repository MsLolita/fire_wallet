import requests
import pyuseragents

from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

from data.captcha import ANTICAPTCHA_API_KEY, SITE_KEY, URL

from utils import str_to_file, logger


class FireWallet:
    referral = None

    def __init__(self, email: str, proxy: str = None):
        self.email = email
        self.proxy = f"http://{proxy}" if proxy else None

        self.headers = {
            'authority': 'getlaunchlist.com',
            'accept': 'application/json',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryXkMxhQQ5qzjCaJkc',
            'origin': 'https://wallet.joinfire.xyz',
            'referer': 'https://wallet.joinfire.xyz/',
            'user-agent': pyuseragents.random(),
        }

        self.session = requests.Session()

        self.session.headers.update(self.headers)
        self.session.proxies.update({'https': self.proxy, 'http': self.proxy})

    def enter_waitlist(self):
        url = 'https://getlaunchlist.com/s/QZhvlk'

        params = {
            'ref': FireWallet.referral,
        }

        g_recaptcha_response = FireWallet.__bypass_captcha()

        data = ('------WebKitFormBoundaryXkMxhQQ5qzjCaJkc\r\nContent-Disposition: form-data; '
                f'name="g-recaptcha-response"\r\n\r\n{g_recaptcha_response}\r\n------WebKitFormBoundaryXkMxhQQ5qzjCaJkc'
                f'\r\nContent-Disposition: form-data; name="email"\r\n\r\n{self.email}'
                '\r\n------WebKitFormBoundaryXkMxhQQ5qzjCaJkc--\r\n')

        response = self.session.post(url, params=params, data=data)

        return response.json()

    @staticmethod
    def __bypass_captcha():
        solver = recaptchaV2Proxyless()
        # solver.set_verbose(1)
        solver.set_key(ANTICAPTCHA_API_KEY)
        solver.set_website_url(URL)
        solver.set_website_key(SITE_KEY)

        token = solver.solve_and_return_solution()

        if not token:
            logger.error(f"{token} Failed to solve captcha! Please put your API key in data/captcha/__init__.py")
            exit()

        return token

    def logs(self):
        file_msg = f"{self.email}|{self.proxy}"
        str_to_file(f"data\\logs\\success.txt", file_msg)

    def logs_fail(self, msg: str = ""):
        file_msg = f"{self.email}|{self.proxy}"
        str_to_file(f"data\\logs\\failed.txt", file_msg)
        logger.error(f"Failed {self.email} {msg}")

