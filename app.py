import os
import re
import time
import requests
from bs4 import BeautifulSoup
import html2text
import subprocess

class TeleScraper:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.base_url = f"{self.channel_url}?embed=1&mode=tme"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.post_count = 0
        self.configs = []

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def html_to_text(self, html):
        h = html2text.HTML2Text()
        h.body_width = 0
        h.ignore_links = True
        h.ignore_emphasis = True
        h.ignore_images = True
        h.protect_links = True
        h.unicode_snob = True
        h.wrap_links = False
        h.wrap_lists = False
        h.decode_errors = 'ignore'

        text = h.handle(html)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'^[ \t]*[\\`]', '', text, flags=re.MULTILINE)
        return text.strip()

    def is_valid_config(self, content):
        valid_starts = ('vless://', 'vmess://', 'ss://', 'trojan://', 'ssr://')
        return content.startswith(valid_starts)

    def fetch_configs(self):
        try:
            offset = 0
            while len(self.configs) < 100:
                url = f"{self.base_url}&offset={offset}"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                messages = soup.find_all('div', class_='tgme_widget_message_bubble')
                if not messages:
                    break
                
                for message in messages:
                    content_elem = message.find('div', class_='tgme_widget_message_text')
                    if content_elem:
                        content = self.html_to_text(str(content_elem))
                        if self.is_valid_config(content):
                            self.configs.append(content)
                            self.post_count += 1
                            if len(self.configs) >= 100:
                                break

                offset += 20
                time.sleep(1)

        except requests.exceptions.RequestException as err:
            print(f"Error fetching posts: {err}")

    def save_configs(self):
        with open('config.txt', 'w', encoding='utf-8') as f:
            for config in self.configs:
                f.write(f"{config}\n")

    def run(self):
        self.fetch_configs()
        self.save_configs()
        self.clear_screen()
        print(f"Scraped {len(self.configs)} valid configs from {self.channel_url}")
        print("Configs have been saved to config.txt")
        
        # Run check.py to remove duplicates
        subprocess.run(['python', 'check.py'], check=True)
        print("Duplicate configs have been removed.")

if __name__ == '__main__':
    channel_url = 'https://t.me/s/v2ray_configs_pool'
    scraper = TeleScraper(channel_url)
    scraper.run()
