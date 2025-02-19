from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to chromedriver
chromedriver_path = "/usr/bin/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Open CloudLab login page
driver.get("https://www.cloudlab.us/login.php")

# Wait for elements to be present
wait = WebDriverWait(driver, 10)

with open("credentials.txt", "r") as f:
    lines = f.readlines()
    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()
    
try:
    # Find username and password input fields (update the selectors if needed)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "uid")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    # Type the credentials
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    # Locate and click the login button using its ID
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "quickvm_login_modal_button")))
    login_button.click()

    print("Login successful!")

    # Wait for the Experiments tab to be clickable
    experiments_tab = wait.until(EC.element_to_be_clickable((By.ID, "usertab-experiments")))
    experiments_tab.click()

    print("Navigated to Experiments tab")

    # Wait for the experiment table to load
    time.sleep(3)

    # Locate the experiment table
    experiment_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Extract all rows
    rows = experiment_table.find_elements(By.TAG_NAME, "tr")

    # Extract column headers
    headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]

    # Store experiment data
    experiments_data = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, "td")
        experiments_data.append([col.text for col in columns])

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(experiments_data, columns=headers)

    # Save to CSV file
    df.to_csv("cloudlab_experiments.csv", index=False)
    print("Experiment data saved to 'cloudlab_experiments.csv'")

except Exception as e:
    print("Error:", e)

finally:
    # Keep browser open for debugging, or close it after a few seconds
    time.sleep(10)
    driver.quit()