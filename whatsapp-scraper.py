import os
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Bot:
    def __init__(self):
        # Set up logging
        os.environ['DISPLAY'] = ':0'
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'whatsapp_bot.log')

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger()

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("user-data-dir=/tmp/.org.chromium.Chromium.qqng94")
        # download_dir = os.path.join(os.getcwd(), "WhatsApp_Status")
        self.download_dir = '/home/atefe_hjn97/Documents/VScode/instagramBot/WhatsApp_Status'
        os.makedirs(self.download_dir, exist_ok=True)  # Create the folder if it doesn't exist
        prefs = {"download.default_directory": self.download_dir}  # Specify the download directory
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.waits = WebDriverWait(self.driver, 10)
        self.waits2 = WebDriverWait(self.driver, 1)

    def remove_duplicates(self):
        files = os.listdir(self.download_dir)
        seen = {}
        
        for file in files:
            # Use regex to find the base name without the copy suffix
            match = re.match(r'(.*?)( \(\d+\))?\.jpeg$', file)
            if match:
                base_name = match.group(1)
                if base_name in seen:
                    # Remove the duplicate file
                    os.remove(os.path.join(self.download_dir, file))
                    self.logger.info(f"Removed duplicate file: {file}")
                else:
                    seen[base_name] = True

    def Login(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            self.driver.maximize_window()
            self.logger.info("Opening WhatsApp Web. Please scan the QR code.")
            # print("Scan QR Code, and then wait for login confirmation...")
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            # print(f"Error during login: {e}")

    def download_status(self):
        status_count = 0  # Counter for statuses
        try:
            # Click on "My Status"
            btn_status = self.waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Status"]')))
            btn_status.click()
            self.logger.info('Clicked on "Status"')

            btn_mystatus = self.waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="My status"]')))
            btn_mystatus.click()
            self.logger.info('Clicked on "My status"')

            while True:
                status_count += 1  # Increment status counter
                self.logger.info(f"Viewing status {status_count}")

                try:
                    # Click on the "Pause" button to prevent auto-transition
                    btn_pause = self.waits2.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[3]/div/div/div/span/div/div/div/div[2]/div[3]/div/div/button/button')))
                    btn_pause.click()
                    self.logger.info("Paused the status")

                    # Open menu options
                    btn_menu = self.waits2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="menu"]')))
                    btn_menu.click()

                    # Attempt to download the status
                    try:
                        btn_download = self.waits2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Download"]')))
                        btn_download.click()
                        self.logger.info(f"Downloaded status {status_count}")

                    except (TimeoutException, NoSuchElementException):
                        self.logger.warning(f"No downloadable image/video for status {status_count}")

                    # Click "Next" to proceed to the next status
                    btn_next = self.waits2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > span:nth-child(4) > div > div > div > div.x10l6tqk.x13vifvy.x1tav4y9.x1ey2m1c.xv97iv4.xzuapc8.xqvfhly.xr1yuqi.x4ii5y1.x1ypdohk.x66m237.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x1vx7kgm')))
                    btn_next.click()
                    self.logger.info("Moved to the next status")

                except (TimeoutException, NoSuchElementException) as e:
                    self.logger.error(f"Error while navigating or downloading status {status_count}: {e}")
                    break  # Exit loop when no "Next" button is found

            self.logger.info(f"Total statuses viewed: {status_count}")

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            # print(f"An error occurred: {e}")

    def close(self):
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    test = Bot()
    test.Login()
    test.download_status()
    test.remove_duplicates()  # Call the remove_duplicates method
    test.close()