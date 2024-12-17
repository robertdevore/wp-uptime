import requests
import time
import csv
import random
import threading
from datetime import datetime

# List of URLs to monitor
urls = [
    "https://automattic.com/", "https://wordpress.com/", "https://ma.tt/", "https://jetpack.com/",
    "https://woocommerce.com/", "https://akismet.com/", "https://gravatar.com/", "https://simplenote.com/",
    "https://longreads.com/", "https://dayoneapp.com/", "https://pocketcasts.com/", "https://tumblr.com/",
    "https://wpvip.com/", "https://crowdsignal.com/", "https://get.blog/", "https://wp.me/",
    "https://public-api.wordpress.com/", "https://developer.wordpress.com/", "https://en.blog.wordpress.com/",
    "https://wordpress.org/", "https://codex.wordpress.org/", "https://developer.wordpress.org/", "https://make.wordpress.org/",
    "https://learn.wordpress.org/", "https://wordpress.tv/", "https://bbpress.org/", "https://buddypress.org/",
    "https://glotpress.org/", "https://translate.wordpress.org/", "https://jobs.wordpress.net/", "https://plan.wordcamp.org/",
    "https://central.wordcamp.org/", "https://wordcamp.org/", "https://wpjobmanager.com/", "https://vaultpress.com/",
    "https://polldaddy.com/", "https://intensedebate.com/", "https://wpcalypso.wordpress.com/", "https://jetpack.me/",
    "https://wpcloud.io/", "https://happy.tools/", "https://woopayroll.com/", "https://simplenote.blog/",
    "https://simplechart.io/", "https://distributed.blog/", "https://wordpressfoundation.org/", "https://automattic.design/",
    "https://ownyourcontent.blog/", "https://wp.com/"
]

# Generate unique CSV filename with current datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"uptime_log_{timestamp}.csv"

# Track downtime start and end
downtime_data = {}

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# List of randomized user-agent headers (30 in total)
headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 8.1; Nexus 5X Build/OPM6.171019.030.H1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 11; ONEPLUS A6013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 7.0; Nexus 6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}
]

# Function to initialize the CSV file with headers
def initialize_csv(file):
    with open(file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Downtime Start", "Downtime End", "Total Downtime (s)", "Date"])

# Function to log downtime to the CSV
def log_downtime(url, start_time, end_time):
    total_downtime = (end_time - start_time).total_seconds()
    date = end_time.strftime("%Y-%m-%d")
    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([url, start_time, end_time, total_downtime, date])

# Function to check the status of a URL
def check_status(url):
    try:
        headers = random.choice(headers_list)  # Randomize headers
        response = requests.get(url, timeout=5, headers=headers)
        return response.status_code == 200  # True if site is up, False otherwise
    except requests.RequestException:
        return False  # Site is down or unreachable

# Function to handle downtime monitoring for a specific URL
def monitor_downtime(url):
    downtime_start = downtime_data[url]
    print(f"{YELLOW}Monitoring {url} every second until it comes back up...{RESET}")
    while True:
        if check_status(url):
            downtime_end = datetime.now()
            print(f"{GREEN}{url} is back up at {downtime_end}{RESET}")
            log_downtime(url, downtime_start, downtime_end)
            del downtime_data[url]  # Remove from downtime tracking
            break
        time.sleep(1)  # Check every second

# Function to continuously monitor a single URL
def monitor_url(url):
    while True:
        status = check_status(url)
        current_time = datetime.now()

        if status:
            # If site was down and is now back up, log the downtime
            if url in downtime_data:
                downtime_start = downtime_data[url]
                print(f"{GREEN}{url} is back up at {current_time}{RESET}")
                log_downtime(url, downtime_start, current_time)
                del downtime_data[url]
            else:
                print(f"{GREEN}{url} is up at {current_time}{RESET}")
        else:
            # If site is down and was not already noted as down, note the start time
            if url not in downtime_data:
                print(f"{RED}{url} went down at {current_time}{RESET}")
                downtime_data[url] = current_time
                # Start a new thread to monitor the downed site every second
                threading.Thread(target=monitor_downtime, args=(url,), daemon=True).start()

        # Wait for a randomized interval between 10 and 20 seconds
        wait_time = random.randint(10, 20)
        time.sleep(wait_time)

# Main function to initialize CSV and start monitoring each URL in a separate thread
def main():
    # Initialize the CSV file
    initialize_csv(csv_file)

    print(f"{CYAN}Monitoring started. Press Ctrl+C to stop.{RESET}")
    try:
        # Start a thread for each URL
        for url in urls:
            threading.Thread(target=monitor_url, args=(url,), daemon=True).start()

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n{CYAN}Monitoring stopped.{RESET}")

# Start the monitoring script
if __name__ == "__main__":
    main()
