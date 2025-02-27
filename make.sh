sudo apt update
sudo apt install python3-venv

python3 -m venv myenv
source myenv/bin/activate


sudo apt install python3-pip3

# Install Python3 and pip if they are not already installed
sudo apt install -y python3 python3-pip

# Download and install Google Chrome
wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome.deb
rm google-chrome.deb

# Install necessary Python packages
pip3 install selenium pandas webdriver-manager
sudo apt install chromedriver
