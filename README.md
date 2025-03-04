# Selenium CloudLab

This repository contains a simple automation script (`experimentCollector.py`) that uses [Selenium](https://www.selenium.dev/) to log in to [CloudLab](https://www.cloudlab.us/) and retrieve data about your experiments. The script will save your experiment data into a CSV file named **`cloudlab_experiments.csv`**.

## Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- **Google Chrome** installed (the script uses the Chrome WebDriver) (if not it will be installed with make.sh).

## Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/pgrigo01/selenium-cloudlab.git
   cd selenium-cloudlab

  Run make.sh:
  This script creates a Python virtual environment called myenv and installs all the required Python dependencies (e.g., Selenium, webdriver_manager).
  
  After running this, you should see (myenv) at the start of your terminal prompt, indicating you’re in the virtual environment.

    source make.sh

    
2. **Providing Credentials**

In order for the script to log in and retrieve your experiments, you need to provide your CloudLab username and password.
       
**Usage**

Once your credentials are ready and you have activated the virtual environment (by running source make.sh), simply run:
    
    python experimentCollector.py

 **What the Script Does**
    Prompts the user to login with username and password.
    Logs into CloudLab using your provided credentials.
    Navigates to your list of experiments.
    Extracts the experiment table data.
    Saves the data into a CSV file named cloudlab_experiments.csv.
    Finds an experiment named management-node (if it exists) and retrieves its expiration date, saving that to managementNodeDuration.txt.

3. **Files and Directories**

    experimentCollector.py: The main Selenium script that performs data collection.

    myenv/: The Python virtual environment directory created by make.sh.

    cloudlab_experiments.csv: The CSV file containing your experiment data.
  
    managementNodeDuration.txt: The file containing the expiration date of the management-node experiment (if found).
  
    make.sh: Script to create/activate the virtual environment and install dependencies.

4. **Security Notes

   Credentials: If you use credentials.txt, keep it private. Do not commit this file to any public repository.

   HTTPS: All login information is transmitted via HTTPS to CloudLab.

   Temporary Data: Selenium creates a temporary user data directory for Chrome. This directory is generally removed after the script completes.
