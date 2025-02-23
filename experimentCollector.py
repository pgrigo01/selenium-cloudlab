import os
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# -------------------------------
# Setup WebDriver for Selenium
# -------------------------------

# Path to the chromedriver executable; adjust this path if necessary.
chromedriver_path = "/usr/bin/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Open the CloudLab login page.
driver.get("https://www.cloudlab.us/login.php")
# Initialize an explicit wait with a timeout of 10 seconds.
wait = WebDriverWait(driver, 10)

# -------------------------------
# Retrieve Credentials
# -------------------------------

# The script checks for a file named 'credentials.txt' in the current directory.
# This file is expected to contain the username on the first line and the password on the second line.
# Using this file allows you to store credentials securely and avoid manually entering them every time.
# If the file does not exist, the script will prompt you to enter your credentials manually.
USERNAME = ""
PASSWORD = ""

if os.path.exists("credentials.txt"):
    # Read credentials from the file if it exists.
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        USERNAME = lines[0].strip()  # First line: username
        PASSWORD = lines[1].strip()  # Second line: password
else:
    # If the file is not found, repeatedly prompt the user until valid credentials are provided.
    while USERNAME == "" or PASSWORD == "":
        USERNAME = input("Enter your username: ")
        # Using getpass.getpass hides the password input for security.
        PASSWORD = getpass.getpass("Enter your password: ")

# -------------------------------
# Main Script: Logging In and Data Extraction
# -------------------------------
try:
    # 1) Log in to CloudLab by locating the username and password input fields.
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "uid")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    # Locate and click the login button.
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "quickvm_login_modal_button")))
    login_button.click()
    print("Login successful!")

    # 2) Navigate to the Experiments tab after logging in.
    experiments_tab = wait.until(EC.element_to_be_clickable((By.ID, "usertab-experiments")))
    experiments_tab.click()
    print("Navigated to Experiments tab")

    # 3) Wait for the experiments table to load.
    time.sleep(3)
    experiment_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # 4) Extract table rows and header information.
    rows = experiment_table.find_elements(By.TAG_NAME, "tr")
    headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "th")]
    print("Extracted headers:", headers)

    # 5) Gather data from each row of the table (skipping the header row).
    experiments_data = []
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        experiments_data.append([c.text for c in cols])

    # 6) Convert the gathered data into a Pandas DataFrame with the headers as columns.
    df = pd.DataFrame(experiments_data, columns=headers)

    # 7) If a "Creator" column exists, filter the DataFrame to include only rows
    # where the creator matches the username used for login.
    if "Creator" in df.columns:
        df = df[df["Creator"] == USERNAME]
    else:
        print("No 'Creator' column found; skipping user-based filtering.")

    # 8) Save the DataFrame to a CSV file named 'cloudlab_experiments.csv'.
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
                    # If there is a clickable link inside the cell, use it.
                    management_node_link = cols[0].find_element(By.TAG_NAME, "a")
                except:
                    # Otherwise, treat the entire row as clickable.
                    management_node_link = row
                break

    if management_node_link:
        management_node_link.click()
        print("Clicked on 'management-node' experiment. Navigating to details page...")

        try:
            # Wait until the expiration element (with ID "quickvm_expires") is present.
            expiration_element = wait.until(
                EC.presence_of_element_located((By.ID, "quickvm_expires"))
            )
            
            # Additional wait until the expiration element's text is non-empty.
            WebDriverWait(driver, 10).until(
                lambda d: expiration_element.text.strip() != ""
            )

            expiration_text = expiration_element.text.strip()
            print("Expiration text found:", expiration_text)

            # Save the expiration text to 'managementNodeDuration.txt'
            with open("managementNodeDuration.txt", "w") as f:
                f.write(expiration_text + "\n")

            print("Saved management node expiration to 'managementNodeDuration.txt'")

        except Exception as ex:
            print("Could not locate the expiration element or text is empty:", ex)
    else:
        print("No row found with name 'management-node'.")

except Exception as e:
    # Handle any exceptions that occur during the process.
    print("Error:", e)

finally:
    # Pause briefly before closing the browser to allow any final actions to complete.
    time.sleep(5)
    driver.quit()
