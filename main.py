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
from info_extractor import InformationExtractor
from concurrent.futures import ThreadPoolExecutor

def screenshot_and_convert(offset, image_name, image_folder, text_folder, url, query):
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
        with open(f"{text_folder}{new_name}.txt", "r") as file:
            text = file.read()
        extractor = InformationExtractor()
        result = extractor.extract(query, text)
        print(result)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        return result

def take_screenshots_and_convert_to_text(url, image_name, query, image_folder='images/', text_folder='text/'):
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
    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Start all threads and collect their return values
        futures = [executor.submit(screenshot_and_convert, offset, image_name, image_folder, text_folder, url, query) for offset in offsets]

    # Wait for all threads to finish and collect their results
    results = [future.result() for future in futures]

    # Call the extract_from_history function with the results
    extractor = InformationExtractor()
    final_result = extractor.extract_from_history(results, query)

    return final_result


def query_website(url, query):
    website_name = url.split('//')[-1].split('/')[0].split('.')[0]  # Extract the name of the website from the url, excluding '.com'
    return take_screenshots_and_convert_to_text(url, website_name, query)



# Usage
# url = 'https://sugarspunrun.com/vanilla-cake-recipe/'
# iamge_name = 'cake'
# query = 'Give me just the ingredients from the following.'
# info = take_screenshots_and_convert_to_text(url, iamge_name, query)
# print(info)

# TODO take a screenshot of just half the page, get a wider window, etc. Will do after I create aws server to do this.
