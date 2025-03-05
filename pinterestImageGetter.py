import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
inital_url = "https://www.pinterest.com"

class TestApp:

    def getPins(self, url, pick):
        # Set up the webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode (without opening a window)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load and ensure content is visible
        time.sleep(7)  # Allow extra time for dynamic content to load

        # Initialize lists for URLs
        image_urls = []
        new_image_urls = []

        # Extract image URLs function
        def extract_images(append_to_new=False):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            pin_divs = soup.find_all('div', class_="Yl- MIw Hb7")
            for pin in pin_divs:
                style = pin.get('style', '')
                img_url = None
                if 'background-image' in style:
                    img_url = style.split('url("')[1].split('")')[0]
                else:
                    img_tag = pin.find('img')
                    if img_tag and img_tag.get('src'):
                        img_url = img_tag['src']

                if img_url:
                    if append_to_new:
                        if img_url not in new_image_urls and img_url not in image_urls:
                            new_image_urls.append(img_url)
                    else:
                        if img_url not in image_urls:
                            image_urls.append(img_url)

        # Initial extraction
        extract_images()

        # Print out the initial list of image URLs
        if image_urls:
            print(f"Found {len(image_urls)} images:")
            for img_url in image_urls:
                print(img_url)
        else:
            print("No image URLs found.")

        # Scroll and extract more images if the user wants
        while True:
            more = input("If you wish for more images, press 1. Otherwise, press 2: ")
            if more == "1":
                scroll_pause_time = 3  # Adjust pause time for your connection speed
                last_height = driver.execute_script("return document.body.scrollHeight")

                # Scroll to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)

                # Check if new content is loaded
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("No more content to load.")
                    break  # Exit if no new content is loaded

                # Extract newly loaded images
                extract_images(append_to_new=True)

                # Print new images only
                if new_image_urls:
                    print(f"Here are the new images ({len(new_image_urls)}):")
                    for img_url in new_image_urls:
                        print(img_url)
                    image_urls.extend(new_image_urls)  # Add new images to the main list
                    new_image_urls.clear()  # Reset for the next scroll
                else:
                    print("No new images found.")
            else:
                print("Exiting.")
                break

        driver.quit()  # Close the browser after scraping

    
    def getSearchParamaters(self):
        searchparemeters = []
        with open('searchQueries.csv') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            for row in csvreader:
                searchparemeters.append(row[0].replace(" ","%20"))
        return searchparemeters
    
    def run(self):
        # get search paramaters
        parameters = self.getSearchParamaters()
        # for every query in our parameters list
        for query in parameters:
            searchUrl = inital_url + "/search/pins/?q=" + query
            pinList = self.getPins(searchUrl,2)
            print(searchUrl)
        
        return self
    
def userPrompt():
    holder = input("What are you looking for? ")
    with open('searchQueries.csv', mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([holder])


if __name__ == "__main__":
    userPrompt()
    scraper = TestApp().run()