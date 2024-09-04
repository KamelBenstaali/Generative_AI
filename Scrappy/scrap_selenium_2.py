from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# Set up Selenium WebDriver with optimizations
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-images")  # Disable images
chrome_options.add_argument("--disable-javascript")  # Disable JavaScript

# Set page load strategy to eager to speed up page loads
chrome_options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the Google login page
    driver.get('https://accounts.google.com/signin')

    # Locate and fill the email/phone field
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'identifierId'))
    )
    email_field.send_keys('kamel.benstaali@banquealimentaire.org')
    email_field.send_keys(Keys.RETURN)

    # Wait for the password field to appear
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'Passwd'))  # Correct name attribute for Google login
    )
    password_field.send_keys('Benben98!')
    password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete
    WebDriverWait(driver, 10).until(
        EC.url_contains('myaccount.google.com')
    )

    # Navigate to the page you want to scrape after logging in
    driver.get('https://sites.google.com/banquealimentaire.org/ticadi/accueil')

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Get the entire DOM hierarchy
    page_source = driver.page_source

    # Use BeautifulSoup to prettify the HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    pretty_html = soup.prettify()

    # Save the prettified HTML to a file
    # with open('page_source.html', 'w', encoding='utf-8') as file:
    #     file.write(pretty_html)

finally:
    # Close the browser
    driver.quit()
