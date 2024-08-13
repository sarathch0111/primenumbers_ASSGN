from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

url = "https://hprera.nic.in/PublicDashboard"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
actions = ActionChains(driver)

all_data = []

try:
    
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link.active[data-toggle='tab'][data-target='#reg-Projects']"))
    )
    
    main_container = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "px-2.pt-2"))
    )
    
    col_lg_6_divs = main_container.find_elements(By.CLASS_NAME, "col-lg-6")
    
    for div in col_lg_6_divs[:6]:
        
        inner_div = div.find_element(By.CLASS_NAME, "shadow.py-3.px-3.font-sm.radius-3.mb-2")
        
        anchor = inner_div.find_element(By.TAG_NAME, "a")
        
        driver.execute_script("arguments[0].click();", anchor)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-borderless.table-sm.table-responsive-lg.table-striped.font-sm"))
        )
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        data = {}
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                if key in ["GSTIN No.", "PAN No.", "Name", "Permanent Address"]:
                    data[key] = value
        
        all_data.append(data)
        
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close[data-dismiss='modal']"))
        )
        close_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    if all_data:
        print("\nCollected Data:")
        for i, data in enumerate(all_data, 1):
            print(f"\nData for project {i}:")
            for key, value in data.items():
                print(f"{key}: {value}")
            print("-" * 50)
    else:
        print("No data was collected.")

    time.sleep(5)
    driver.quit()