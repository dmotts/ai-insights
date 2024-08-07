from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_form_submission():
    driver = webdriver.Chrome()
    driver.get('http://localhost:5000')

    # Fill out the form
    driver.find_element(By.ID, 'clientName').send_keys('John Doe')
    driver.find_element(By.ID, 'clientEmail').send_keys('john.doe@example.com')
    industry_dropdown = driver.find_element(By.ID, 'industry')
    for option in industry_dropdown.find_elements(By.TAG_NAME, 'option'):
        if option.text == 'Technology':
            option.click()
            break

    driver.find_element(By.ID, 'question1').send_keys('Optimizing processes')
    driver.find_element(By.ID, 'question2').send_keys('Improving UX')
    driver.find_element(By.ID, 'question3').send_keys('Data analysis')
    driver.find_element(By.ID, 'question4').send_keys('Automation')
    driver.find_element(By.ID, 'question5').send_keys('AI in future growth')

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Wait for the result
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'result')))

    # Validate result
    download_link = driver.find_element(By.ID, 'downloadLink')
    assert download_link.is_displayed()

    driver.quit()
