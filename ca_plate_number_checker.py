import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set your configs
WEBDRIVER_WAIT_MS = 500
CHECK_INTERVAL_SECONDS = 2

CURRENT_PLATE = 'YOUR_PLATE_NUMBER'
VIN = 'YOUR_VIN_LAST_3_DIGITS'
PLATE_NUMBER_LIST_PATH = 'plate_numbers.txt'
PLATE_NUMBER_RESULT_PATH = 'plate_result.txt'
ACKNOWLEDGE_URL = 'https://www.dmv.ca.gov/wasapp/ipp2/initPers.do'
PLATE_MAX_LEN = 7
PLATE_VALID_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789 '


def load_plate_number_list(path):
  plate_number_list = []
  f = open(path,'r')
  for line in f.readlines():
    line = line.replace('\n', '')
    line = "{:<7}".format(line)
    plate_number_list.append(line)
  return plate_number_list

def save_avalablity_list(path, content):
  f = open(path, "a")
  f.write(content + '\n')
  f.close()

# Returns empty string if it has invalid characters or exceeds the max length.
# Otherwise, converts letters to uppercase and fills spaces in the end.
def convert_plate_number(string):
  if len(string) > PLATE_MAX_LEN:
    return ''
  string = string.upper().ljust(PLATE_MAX_LEN)
  for c in string:
    if c not in PLATE_VALID_CHARS:
      return ''
  return string


def is_available_plate_number(driver, plate_number):
  driver.get(ACKNOWLEDGE_URL)
  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PersonalizedFormBean"]/div[1]/fieldset/ul/li/label')))
  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/div[1]/fieldset/ul/li/label').click()
  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/div[2]/button').click()
  # driver.find_element_by_name('method').click()

  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.NAME, 'plateType')))
  driver.find_element_by_id('vehicleType').send_keys('Auto')
  driver.find_element_by_id('licPlateReplaced').send_keys(CURRENT_PLATE)
  driver.find_element_by_id('last3Vin').send_keys(VIN)

  # driver.find_element_by_id('isRegExpire60N').click()
  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/fieldset/div[5]/div[2]/label').click()
  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/fieldset/div[6]/div[2]/label').click()

  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/fieldset/div[6]/div[2]/label').click()

  driver.find_element_by_xpath('//*[@id="plate_R"]/div/div/label').click()
  driver.find_element_by_xpath('//*[@id="PersonalizedFormBean"]/div/button').click()


  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.NAME, 'plateChar6')))
  for i in range(len(plate_number)):
    driver.find_element_by_name('plateChar%d' % i).send_keys(plate_number[i])
  # driver.find_elements_by_tag_name('input')[10].click()
  
  driver.find_element_by_xpath('//*[@id="plate-configurator"]/div[2]/button').click()

  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.ID, 'footer')))
  list = driver.find_elements_by_id('meaning')
  return len(list) > 0


if __name__ == "__main__":
  driver = webdriver.Chrome(ChromeDriverManager().install())
  plate_number_list = load_plate_number_list(PLATE_NUMBER_LIST_PATH)
  for plate_number in plate_number_list:
    converted_plate_number = convert_plate_number(plate_number)
    is_available = False
    if len(converted_plate_number) > 0:
      is_available = is_available_plate_number(driver, converted_plate_number)
    result = '%s\t%s\t%s' % (plate_number, converted_plate_number, is_available)
    print(result)
    if is_available:
      save_avalablity_list(PLATE_NUMBER_RESULT_PATH, result)
    time.sleep(CHECK_INTERVAL_SECONDS)
  driver.quit()