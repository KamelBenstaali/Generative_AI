from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
driver = webdriver.Chrome()

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
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Debug: Print the page source to verify the content


    # Use BeautifulSoup to prettify the HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pretty_html = soup.prettify()

    # Print the prettified HTML
    print(pretty_html)

finally:
    # Close the browser
    driver.quit()
