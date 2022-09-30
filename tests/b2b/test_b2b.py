import pytest
import time
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import shutil

import os


# Register module level markers (applies to all tests in this file)
pytestmark = [pytest.mark.core, pytest.mark.b2b]


@pytest.mark.prod
def test_b2b(b2b_config):
    zip_images()
    # browser = b2b_config["browser"]

    # # Login to B2B Marketplace
    # browser.get(url=b2b_config["base_url"] + "/HallmarkGoldCrown/s/login/")
    # time.sleep(3)
    # username = browser.find_element_by_id("36:2;a")
    # username.send_keys(b2b_config['username'])
    # password = browser.find_element_by_id("48:2;a")
    # password.send_keys(b2b_config['password'])
    # login = browser.find_element_by_class_name("loginButton")
    # login.click()
    # time.sleep(3)

    # # Navigate to page with links to all Categories
    # browser.get(url=b2b_config["base_url"] + "/HallmarkGoldCrown/s/sample-tree-links")
    # time.sleep(10)

    # # Extract all Category links
    # catalog_pages = []
    # soup = BeautifulSoup(browser.page_source)
    # for link in soup.find_all('a'):
    #     # print(link.attrs.values())
    #     # print(link.name+" "+link.get('href'))
    #     if (link.has_attr('href')):
    #         if ("category-pdf" in link['href']):
    #             print(link['href'])
    #             catalog_pages.append(b2b_config["base_url"] + link['href'])

    # print("Found " + str(len(catalog_pages)) + " Categories")
    # time.sleep(10)

    # # Navigate to each category and capture the page
    # count = 0
    # for page in catalog_pages:
    #     # if count != 1:
    #     print("Capturing Category No: " + str(count).zfill(4) + " URL:" + page)
    #     # if(count == 1):
    #     browser.get(page)
    #     time.sleep(10)

    #     # Get the original window size so we can use it to reset the browser window later
    #     original_size = browser.get_window_size()

    #     # Get the full screen dimensions of the page, so that the screenshot is the entire page
    #     required_width = browser.execute_script('return document.body.parentNode.scrollWidth')
    #     required_height = browser.execute_script('return document.body.parentNode.scrollHeight')

    #     # Set window size to the required width and height
    #     browser.set_window_size(required_width, required_height)

    #     # Get the current page, and pull the header text from the page. We are stripping out
    #     # the spaces, and replacing with dashes, so that we can have friendly image names
    #     current_page = BeautifulSoup(browser.page_source)
    #     header_text = current_page.select('div.headerDiv')[0].text.replace(' ', '-')

    #     # Find the body element of the page, and then save the screenshot to the images folder with the
    #     # category name pulled from the header text as a .png
    #     browser.find_element_by_tag_name('body').screenshot('images/' + header_text + '.png')

    #     # Reset the window size to the original size, so that it can be set again with the next pages
    #     # window size
    #     browser.set_window_size(original_size['width'], original_size['height'])
        
    #     count = count + 1
    #     # else:
    #     #     break

    # # Once all of the catalog images have been generated, we need to zip and send to the S3 bucket
    # zip_images()

    # print("Job completed successfully on UTC:" + datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S"))
    # browser.quit()

def zip_images():
    # Get the current working directory
    cwd = os.getcwd()
    print(cwd)

    # Get todays current date
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(today)

    # @todo Create temp directory

    # Zip images folder
    # @todo make this work to save zip to temp directory
    shutil.make_archive(cwd + '/temp/' + today, 'zip', 'images')

    # Upload zip file to S3

    # Delete temp directory?

    # Delete images

    # Remove images from directory?

def upload_zip_file():
    # Figure out where to upload
    return

def send_email():
    # Send an email with success or failure
    return