import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Неявное ожидание
@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()


def login(driver):
    driver.find_element(By.ID, 'email').send_keys('goga1111@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('111222')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )


def test_show_all_pets(driver):
    login(driver)
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


def test_show_all_character_pets(driver):
    login(driver)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card'))
    )
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_pets_list(driver):
    login(driver)
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]'))
    )

    number_my_pets = int(
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split('\n')[1].split('Питомцев:')[1])

    images_my_pets = driver.find_elements(By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]')
    images_count = sum(1 for img in images_my_pets if img.get_attribute('src') != '')

    assert number_my_pets / images_count <= 2

    all_my_names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    names_num = len([elt.text for elt in all_my_names if elt.text != ""])

    all_my_breeds = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
    breeds_num = len([elt.text for elt in all_my_breeds if elt.text != ""])

    all_my_ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')
    ages_num = len([elt.text for elt in all_my_ages if elt.text != ""])

    assert number_my_pets == names_num == breeds_num == ages_num

    names = [elt.text for elt in all_my_names]

    if len(names) != len(set(names)):
        print(f"Warning: There are {len(names) - len(set(names))} duplicate names.")