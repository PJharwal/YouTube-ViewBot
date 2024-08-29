import time
import random
import requests  # Import the requests module

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options for headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")

# Function to get a proxy from the API
def get_proxy_from_api():
    # Replace with your proxy API endpoint and API key
    api_endpoint = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"  # Example endpoint
    api_key = "YOUR_API_KEY"  # Replace with your actual API key

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        proxy = response.json().get("proxy")
        return proxy
    else:
        print("Error getting proxy from API")
        return None

# Set up the browser automation tool
driver = webdriver.Chrome(options=options)

# Input parameters
url = input("Enter the YouTube live stream URL: ")
duration = int(input("Enter the duration in seconds: "))
views = int(input("Enter the number of views: "))

# Filter by channel ID or username
channel_id = ""  # Replace with your channel ID
channel_username = ""  # Replace with your channel username

def is_valid_channel(url):
    # Check if the URL belongs to the specified channel ID or username
    if f"https://www.youtube.com/channel/{channel_id}" in url or f"https://www.youtube.com/{channel_username}" in url:
        return True
    return False

# Function to simulate user interactions
def simulate_user_interactions(url):
    # Check if the URL belongs to the specified channel ID or username
    if not is_valid_channel(url):
        print("Invalid channel. Skipping...")
        return
    
    # Get a proxy from the API
    proxy = get_proxy_from_api()
    
    if proxy:
        # Set up the proxy in the Chrome options
        options.add_argument(f"--proxy-server={proxy}")
    
        # Open the browser with the new proxy settings
        driver = webdriver.Chrome(options=options)
    
        # Open the YouTube live stream URL
        driver.get(url)
    
        try:
            # Wait for the video to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "video-title")))
            
            # Play the video
            play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button.ytp-button")
            play_button.click()
            
            # Wait for the specified duration
            time.sleep(duration)
            
            # Simulate user interactions (e.g., scrolling, clicking, etc.)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "#video-title").click()
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred during interaction: {e}")
        finally:
            # Close the browser
            driver.quit()

# Main loop
for i in range(views):
    # Simulate user interactions
    simulate_user_interactions(url)
    
    # Wait for a random duration between 10 to 30 seconds
    time.sleep(random.randint(10, 30))
    
    # Print success message
    print(f"View {i+1} successful")

# Keep the script alive for 1 hour to ensure views are counted
time.sleep(3600)
