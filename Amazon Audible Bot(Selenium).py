import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
# options.add_argument('--headless')

website = "https://www.audible.com/search"

driver = webdriver.Chrome()
driver.get(website)
time.sleep(2)

# pagination
pagination = driver.find_element(By.XPATH, "//ul[contains(@class,'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page_no = pages[-2].text
last_page_no = int(last_page_no)

book_tittle = []
book_author = []
narrated_author = []
book_length = []
release_date = []
language_list = []
current_page = 1
while current_page <= last_page_no:
    print("Page No:", current_page)
    time.sleep(5)

    container = driver.find_element(By.CLASS_NAME, "adbl-impression-container ")
    products = container.find_elements(By.XPATH, "//*[@id='product-list-a11y-skiplink-target']/span/ul/li")

    for product in products:
        title = product.find_element(By.XPATH, ".//div/div[1]/div/div[2]/div/div/span/ul/li/h3/a").text
        book_tittle.append(title)

        author_element = product.find_element(By.XPATH,
                                              ".//div/div[1]/div/div[2]/div/div/span/ul/li[contains(., 'By:')]")
        author = author_element.text.split("By:")[1].strip()
        book_author.append(author)

        narrated_element = product.find_element(By.XPATH,
                                                ".//div/div[1]/div/div[2]/div/div/span/ul/li[contains(., 'By:')]/following-sibling::li[1]")
        print(narrated_element.text)
        narrated = narrated_element.text.split("by:")[1].strip()

        narrated_author.append(narrated)

        length_element = product.find_element(By.XPATH,
                                              ".//div/div[1]/div/div[2]/div/div/span/ul/li[contains(.,'Length:')]")
        length = length_element.text.split("Length:")[1].strip()
        book_length.append(length)

        release_element = product.find_element(By.XPATH,
                                               ".//div/div[1]/div/div[2]/div/div/span/ul/li[contains(.,'Release date:')]")
        release = release_element.text.split("Release date:")[1].strip()
        release_date.append(release)

        language_element = product.find_element(By.XPATH,
                                                ".//div/div[1]/div/div[2]/div/div/span/ul/li[contains(.,'Language:')]")
        language = language_element.text.split("Language:")[1].strip()
        language_list.append(language)
    current_page = current_page + 1
    time.sleep(5)
    next_button = driver.find_element(By.XPATH, "//span[contains(@class,'nextButton')]")
    next_button.click()
    time.sleep(2)

driver.quit()

df_books = pd.DataFrame({'Tittle': book_tittle, 'Author': book_author, 'Narrated': narrated_author,
                        'Length': book_length, 'Release': release_date, 'Language': language_list})
df_books.to_csv('Audio Books.csv', index=False)
