from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from PIL import Image
import io
import os
from threading import Thread
from image_to_text import convert_image_to_text  # replace with your actual module and function

def screenshot_and_convert(offset, image_name, image_folder, text_folder, url):
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
        
        # Scroll to the offset
        driver.execute_script(f"window.scrollTo(0, {offset});")
        
        # Press escape to possibly close pop-ups
        actions = ActionChains(driver)
        time.sleep(1)  # allow time for the page to load
        actions.send_keys(Keys.ESCAPE).perform()

        time.sleep(1)  # allow time for the page to settle
        screenshot = driver.get_screenshot_as_png()
        
        # Save each slice with offset number
        new_name = f"{image_name}_{offset}"
        slice_save_path = f"{image_folder}{new_name}.png"
        Image.open(io.BytesIO(screenshot)).save(slice_save_path)

        # Convert the image to text
        convert_image_to_text(new_name, image_folder=image_folder, text_folder=text_folder)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()

def take_screenshots_and_convert_to_text(url, image_name, image_folder='images/', text_folder='text/'):
    # Get scroll height
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    total_height = driver.execute_script("return document.body.scrollHeight")
    print(f"Total height is: {total_height}")
    driver.quit()

    offsets = range(0, total_height, 900)  # assuming each slice captures 900 pixels
    threads = [Thread(target=screenshot_and_convert, args=(offset, image_name, image_folder, text_folder, url)) for offset in offsets]
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Usage
# url = 'https://medium.com/blockchain/bitcoin-explained-91a868c65b27'
# iamge_name = 'bitcoin'
# take_screenshots_and_convert_to_text(url, iamge_name)