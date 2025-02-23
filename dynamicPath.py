from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager  # new import

# Automatically download and set up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open CloudLab login page
driver.get("https://www.cloudlab.us/login.php")
wait = WebDriverWait(driver, 10)

with open("credentials.txt", "r") as f:
    lines = f.readlines()
    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()

try:
    # 1) Log in
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "uid")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "quickvm_login_modal_button")))
    login_button.click()
    print("Login successful!")

    # 2) Navigate to Experiments tab
    experiments_tab = wait.until(EC.element_to_be_clickable((By.ID, "usertab-experiments")))
    experiments_tab.click()
    print("Navigated to Experiments tab")

    # 3) Wait for the table to load
    time.sleep(3)

    # 4) Locate the table (adjust selector as needed)
    experiment_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # 5) Extract rows
    rows = experiment_table.find_elements(By.TAG_NAME, "tr")

    # 6) Extract headers from the first row
    headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]
    print("Extracted headers:", headers)

    # 7) Gather table data from subsequent rows
    experiments_data = []
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        experiments_data.append([col.text for col in columns])

    # 8) Convert to DataFrame
    df = pd.DataFrame(experiments_data, columns=headers)

    # 9) Filter rows to keep ONLY those where "Creator" matches your username (pgrigo01)
    if "Creator" in df.columns:
        df = df[df["Creator"] == USERNAME]
    else:
        print("No 'Creator' column found; cannot filter by username.")

    # 10) Save filtered DataFrame to CSV
    df.to_csv("cloudlab_experiments.csv", index=False)
    print("Filtered data saved to 'cloudlab_experiments.csv'")

except Exception as e:
    print("Error:", e)

finally:
    time.sleep(5)
    driver.quit()
