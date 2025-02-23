import os
import getpass
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

driver.get("https://www.cloudlab.us/login.php")
wait = WebDriverWait(driver, 10)

# Check if credentials.txt exists
if os.path.exists("credentials.txt"):
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        USERNAME = lines[0].strip()
        PASSWORD = lines[1].strip()
else:
    # Prompt the user to enter their credentials
    USERNAME = input("Enter your username: ")
    # Using getpass hides the password input
    PASSWORD = getpass.getpass("Enter your password: ")

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

    # 3) Wait for table to load
    time.sleep(3)
    experiment_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # 4) Extract rows & headers
    rows = experiment_table.find_elements(By.TAG_NAME, "tr")
    headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "th")]
    print("Extracted headers:", headers)

    # 5) Gather data
    experiments_data = []
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        experiments_data.append([c.text for c in cols])

    # 6) Convert to DataFrame
    df = pd.DataFrame(experiments_data, columns=headers)

    # 7) Filter by Creator (if exists)
    if "Creator" in df.columns:
        df = df[df["Creator"] == USERNAME]
    else:
        print("No 'Creator' column found; skipping user-based filtering.")

    # 8) Save DataFrame to CSV
    df.to_csv("cloudlab_experiments.csv", index=False)
    print("Data saved to 'cloudlab_experiments.csv'")

    # ----------------------------------------------------------------
    # 9) Locate and click the experiment named "management-node"
    # ----------------------------------------------------------------
    rows = experiment_table.find_elements(By.TAG_NAME, "tr")
    management_node_link = None
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 0:
            name_text = cols[0].text.strip().lower()
            if name_text == "management-node":
                try:
                    # If there's a clickable link in the cell
                    management_node_link = cols[0].find_element(By.TAG_NAME, "a")
                except:
                    # Otherwise, click the row itself
                    management_node_link = row
                break

    if management_node_link:
        management_node_link.click()
        print("Clicked on 'management-node' experiment. Navigating to details page...")

        try:
            # Wait until the <span> with ID "quickvm_expires" is present
            expiration_element = wait.until(
                EC.presence_of_element_located((By.ID, "quickvm_expires"))
            )
            
            # Additional wait until the element's text is non-empty
            WebDriverWait(driver, 10).until(
                lambda d: expiration_element.text.strip() != ""
            )

            expiration_text = expiration_element.text.strip()
            print("Expiration text found:", expiration_text)

            # Save that to another file
            with open("managementNodeDuration.txt", "w") as f:
                f.write(expiration_text + "\n")

            print("Saved management node expiration to 'managementNodeDuration'")

        except Exception as ex:
            print("Could not locate the expiration element or text is empty:", ex)
    else:
        print("No row found with name 'management-node'.")

except Exception as e:
    print("Error:", e)

finally:
    time.sleep(5)
    driver.quit()
