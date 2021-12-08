from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

url = 'https://mail.ru/'

driver.get(url)

elem = driver.find_element(By.CLASS_NAME, 'email-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.CLASS_NAME, 'password-input')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

letters = []

for i in range(30):
    letters_elements = driver.find_elements(By.CLASS_NAME, 'js-letter-list-item')
    action = ActionChains(driver)
    action.move_to_element(letters_elements[-1])
    action.perform()

    for elem in letters_elements:
        dict = {}
        try:
            link = elem.get_attribute('href')
        except:
            pass
        dict['link'] = link

        if dict not in letters:
            letters.append(dict)

for letter in letters:
    driver.get(letter['link'])
    letter_from_to = driver.find_elements(By.CLASS_NAME, 'letter-contact')
    date = driver.find_element(By.CLASS_NAME, 'letter__date').text
    letter_text = driver.find_element(By.CLASS_NAME, 'letter__body').text

    letter['from'] = letter_from_to[0].accessible_name
    letter['to'] = letter_from_to[1].accessible_name
    letter['date'] = date
    letter['letter_text'] = letter_text
