from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

service = Service('/home/nik/chromedriver-linux64/chromedriver')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
)

def main():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://labs.perplexity.ai/')

    select_element = Select(driver.find_element(By.ID, "lamma-select"))
    select_element.select_by_value("llama-3.1-70b-instruct")

    user_question = input("Введите ваш вопрос: ")
    message_input = driver.find_element(By.TAG_NAME, "textarea")
    message_input.send_keys(user_question )

    send_button = driver.find_element(By.XPATH, "//button[@aria-label='Submit']")
    send_button.click()

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Ask Perplexity']"))
        )
        html_content = driver.page_source
        process_html(html_content)

    except Exception:
        print("Элемент 'Ask Perplexity' не найден.")

    driver.quit()

def process_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    span_elements = soup.find_all('span')

    for index, span in enumerate(span_elements):
        span_text = span.get_text(strip=True)
        if span_text and index >= 3:
            print(span_text)

if __name__ == "__main__":
    main()
