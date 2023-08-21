import time
from concurrent.futures import ThreadPoolExecutor

from utils import shift_file, logger
from utils.auto_generate.emails import generate_random_emails
from utils.file_to_list import file_to_list
from firewallet import FireWallet


class AutoReger:
    def __init__(self):
        self.emails_path: str = "data\\inputs\\emails.txt"
        self.proxies_path: str = "data\\inputs\\proxies.txt"

        self.success = 0
        self.custom_user_delay = None

    def get_accounts(self, referrals_amount: int = 100):
        emails = file_to_list(self.emails_path)
        proxies = file_to_list(self.proxies_path)

        if not emails:
            logger.info(f"Generated random emails!")
            emails = generate_random_emails(referrals_amount)

        min_accounts_len = len(emails)

        accounts = []

        for i in range(min_accounts_len):
            accounts.append((emails[i], proxies[i] if len(proxies) > i else None))

        return accounts

    def remove_account(self):
        return shift_file(self.emails_path), shift_file(self.proxies_path)

    def start(self):
        referral_link = input("Referral link (https://wallet.joinfire.xyz/?ref=fI1CcF or press Enter): ")

        FireWallet.referral = referral_link.split('ref=')[-1]


        threads = input("Enter amount of threads: ")

        if threads.isnumeric() and int(threads) > 0:
            threads = int(threads)
        else:
            threads = 1

        self.custom_user_delay = input("Delay in seconds: ")

        if self.custom_user_delay.isnumeric():
            self.custom_user_delay = float(self.custom_user_delay)
        else:
            self.custom_user_delay = 0

        referrals_amount = int(input("Referrals amount: "))

        accounts = self.get_accounts(referrals_amount)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.register, accounts)

        if self.success:
            logger.success(f"Successfully registered {self.success} accounts :)")
        else:
            logger.warning(f"No accounts registered :(")

    def register(self, account: tuple):
        fire_wallet = FireWallet(*account)
        is_ok = False
        res_msg: str = ""

        try:
            time.sleep(self.custom_user_delay)

            resp_json = fire_wallet.enter_waitlist()

            if resp_json.get("ok"):
                is_ok = True

                if resp_json['usersReferred']:
                    logger.info(f"{fire_wallet.email} | Referrals: {resp_json['usersReferred']} | Position: {resp_json['position']}")
                else:
                    logger.success(f"Register {fire_wallet.email}")

        except Exception as e:
            logger.error(f"Error {e}")

        self.remove_account()

        if is_ok:
            fire_wallet.logs()
            self.success += 1
        else:
            fire_wallet.logs_fail(res_msg)

    @staticmethod
    def is_file_empty(path: str):
        return not open(path).read().strip()
