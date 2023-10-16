from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from PIL import Image
import io
import os

def take_full_screenshot(url, save_path):
    # Configure WebDriver to run headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Initialize WebDriver (assuming Chrome)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the URL
        driver.get(url)
        
        # Press escape twice to possibly close pop-ups
        actions = ActionChains(driver)
        time.sleep(1)
        actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
        # Get scroll height
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # List to hold individual image slices
        slices = []
        
        # Scroll and capture slices

        for offset in range(0, total_height, 900):  # assuming each slice captures 900 pixels
            print(offset)
            driver.execute_script(f"window.scrollTo(0, {offset});")
            time.sleep(2)  # allow time for the page to settle
            screenshot = driver.get_screenshot_as_png()
            slices.append(Image.open(io.BytesIO(screenshot)))
                    # Save each slice with offset number
            slice_save_path = f"{save_path}_{offset}.png"
            Image.open(io.BytesIO(screenshot)).save(slice_save_path)
        
        # Concatenate image slices
        screenshot = Image.new('RGB', (slices[0].width, total_height))
        offset = 0
        for slice in slices:
            screenshot.paste(slice, (0, offset))
            offset += slice.height
        
        # Save the screenshot
        screenshot.save(save_path)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()

# Usage
url = 'https://www.mamaknowsglutenfree.com/easy-gluten-free-bread'
save_path = 'images/gluten-free-bread.png'
take_full_screenshot(url, save_path)
