from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import json

def monitor_requests(driver, url):
    """Monitors network requests sent by the browser."""
    try:
        driver.get(url)  # Use the URL from the argument
    except TimeoutException:
        pass
    except:
        pass

    # Get performance entries after page load
    try:
        log_entries = driver.get_log("performance")
    except:
        pass

    requests = []
    for entry in log_entries:
        try:
            obj = json.loads(entry["message"])
            message = obj.get("message")
            method = message.get("method")
            if method in ["Network.requestWillBeSentExtraInfo", "Network.requestWillBeSent"]:
                params = message.get("params")
                if params and "request" in params:
                    request_info = params["request"]
                    if request_info and "url" in request_info:
                        req_url = request_info["url"]
                        if not req_url.startswith("data:"):
                            requests.append(req_url)
        except:
            pass

    # Print the monitored requests
    for request in requests:
        print(request)

if __name__ == "__main__":
    # Check if a URL is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <URL>")
        sys.exit(1)

    urls = sys.argv[1]  # Get the URL from the first argument

    # Set up Chrome driver (replace with your preferred browser if needed)
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU usage to avoid potential issues
    options.add_argument("--no-sandbox")  # Required for running as root user in Linux
    options.add_argument("--disable-dev-shm-usage")  # Improve memory usage for headless mode in Linux
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        with open(urls, 'r') as urls_file:
            for url in urls_file:
                monitor_requests(driver, url.strip())
    except:
        pass
    finally:
        driver.quit()
