from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from json import dump


def configuration():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://readrate.com/rus/books")
    return driver


# Чтобы увидеть полный список необходимо прожать 20 раз на клавишу Показать ещё
def open_full_books_list(driver):
    sleep(2)
    for i in range(20):
        btn = driver.find_element(by=By.LINK_TEXT, value="Показать ещё")
        btn.click()
        sleep(2)


def extract_data_from_page(driver):
    books = driver.find_elements(by=By.CLASS_NAME, value="book")
    return list(map(extract_data_from_book, books))


def extract_data_from_book(book):
    return {"title": book.find_element(by=By.TAG_NAME, value="h4").text,
            "author": book.find_element(by=By.CSS_SELECTOR, value="*.text-dark.link").text,
            "genre": detect_genre(book),
            "readers": book.find_element(by=By.CSS_SELECTOR,
                                         value="*.list-inline-item.reading").find_element(by=By.TAG_NAME,
                                                                                        value="span").text,
            "postponed": book.find_element(by=By.CSS_SELECTOR,
                                           value="*.list-inline-item.planned").find_element(by=By.TAG_NAME,
                                                                                          value="span").text,
            "read": book.find_element(by=By.CSS_SELECTOR,
                                      value="*.list-inline-item.read").find_element(by=By.TAG_NAME,
                                                                                  value="span").text,
            "notFinished": book.find_element(by=By.CSS_SELECTOR,
                                             value="*.list-inline-item.not-finish-read").find_element(by=By.TAG_NAME,
                                                                                                    value="span").text
            }


# Жанра на сайте может и не быть, selenium даст исключение
def detect_genre(book):
    try:
        return list(map(lambda x: x.text, book.find_elements(by=By.CSS_SELECTOR, value="*.link.d-block")))
    except NoSuchElementException:
        return []


def save_to_json(data, filename="data.json"):
    with open(filename, "w") as outfile:
        dump(data, outfile)


if __name__ == "__main__":
    main_driver = configuration()
    open_full_books_list(main_driver)
    main_data = extract_data_from_page(main_driver)
    save_to_json(main_data)
    main_driver.quit()
