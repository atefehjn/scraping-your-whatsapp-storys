<b>Scraping WhatsApp Stories Using ChromeDriver</b>
<br>
Prerequisites:
Chrome Driver: Ensure you have the correct version of ChromeDriver for your operating system.

Selenium: You need to have the selenium package installed in your Python environment. Install it using:
<code>pip install selenium</code>
Steps to Avoid Re-Login on Every Run:
To ensure you don’t have to log in to WhatsApp every time you run the scraper, you can reuse your existing Chrome user profile. Here’s how to set it up:

Find Your Chrome User Data Directory:

Open Google Chrome.
In the address bar, type: chrome://version
Look for the Profile Path field and copy the directory path that ends with User Data (but exclude the profile folder like Default or Profile 1).
Modify the Code:

Use the path you found in the previous step and modify the chrome_options in the code. Here’s the updated code:<code>
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=chrome_options)
</code>

Replace <code>C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User</code> Data with your actual directory path. Ensure the slashes are escaped (\\).
Notes:
This approach prevents you from having to log in every time, as it uses the saved session in your Chrome profile.
Make sure the correct path to your Chrome user data directory is provided for this to work properly.
