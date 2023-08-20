import requests
import pyuseragents

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
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryABlvdAbnt4NhZtRB',
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

        data = (f'------WebKitFormBoundaryABlvdAbnt4NhZtRB\r\nContent-Disposition: form-data; name="email"\r\n\r\n'
                f'{self.email}\r\n------WebKitFormBoundaryABlvdAbnt4NhZtRB--\r\n')

        response = self.session.post(url, params=params, data=data)

        return response.json()

    def logs(self):
        file_msg = f"{self.email}|{self.proxy}"
        str_to_file(f"data\\logs\\success.txt", file_msg)

    def logs_fail(self, msg: str = ""):
        file_msg = f"{self.email}|{self.proxy}"
        str_to_file(f"data\\logs\\failed.txt", file_msg)
        logger.error(f"Failed {self.email} {msg}")

