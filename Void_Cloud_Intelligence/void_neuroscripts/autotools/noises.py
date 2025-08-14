from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Setup ChromeDriver path if needed
service = Service()
driver = webdriver.Chrome(service=service)

url = 'https://noises.online/'

driver.get(url)

time.sleep(2)  # wait for page load

try:
    element = driver.find_element(By.ID, 'paper')
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
    """, element)
    print("Div removed.")
except Exception as e:
    print("Div not found or error:", e)

# Keep browser open so you can inspect
input("Press Enter to close...")

driver.quit()
