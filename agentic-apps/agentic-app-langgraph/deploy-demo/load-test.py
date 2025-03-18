from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time

# Define the Selenium test function
def run_selenium_test(instance_id):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run in headless mode for automation
    driver = webdriver.Chrome(options=options)

    driver.get("xxx")  # Ensure Streamlit app is running

    try:
        # Wait for API Status text to appear
        api_status = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'API Status')]"))
        )
        print(f"Instance {instance_id}: API Status Found: {api_status.text}")
    except Exception as e:
        print(f"Instance {instance_id}: Error finding API Status: {e}")

    try:
        # Wait for the text input field
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        input_field.send_keys(f"Give me IBM stock today?")
        print(f"Instance {instance_id}: Query entered successfully.")
    except Exception as e:
        print(f"Instance {instance_id}: Error finding input field: {e}")

    try:
        # Wait for the "Ask" button and click it
        ask_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div/button"))
        )
        ask_button.click()
        print(f"Instance {instance_id}: Clicked the 'Ask' button.")
    except Exception as e:
        print(f"Instance {instance_id}: Error finding Ask button: {e}")

    try:
        # Wait for the agent response
        agent_response_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Agentic Response')]"))
        )

        # Wait until text is updated in the response container
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[contains(text(),'Agentic Response')]"), "Agentic Response")
        )

        response_text = agent_response_div.text
        print(f"Instance {instance_id}: Agent Response: {response_text}")
    except Exception as e:
        print(f"Instance {instance_id}: Error finding response: {e}")

    driver.quit()


# Run 10 tests in parallel
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(run_selenium_test, i) for i in range(1, 11)]
        concurrent.futures.wait(futures)  # Wait for all tests to complete
