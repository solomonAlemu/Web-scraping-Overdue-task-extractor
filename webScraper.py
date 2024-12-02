# Selenium is a web automation framework that allows you to interact with web browsers.
from selenium import webdriver
# By provides a way to find elements on a web page by their id, name, class, etc.
from selenium.webdriver.common.by import By
# WebDriverWait provides a way to wait for an element to appear on a web page before continuing execution.
from selenium.webdriver.support.ui import WebDriverWait
# EC provides a set of conditions that can be used to wait for an element to appear on a web page.
from selenium.webdriver.support import expected_conditions as EC
#NoSuchElementException provides a way to handle exceptions that occur when an element cannot be found on a web page.
from selenium.common.exceptions import NoSuchElementException

class webScraper:

    def __init__(self):
        self.driver = webdriver.Chrome()
 
    def Wait_for_WebDriverWait_element(self, ID_element):
        # Create an instance of the WebDriverWait class.
        wait = WebDriverWait(self.driver, 10)
        # Wait for the element to become visible.
        wait.until(EC.visibility_of(self.driver.find_element(By.ID, ID_element)))

    def get_HTML_ID_element(self, ID_element):
        return self.driver.find_element(By.ID, ID_element)
    def set_HTML_ID_by_value(self, ID_element,value):
        self.driver.find_element(By.ID, ID_element).send_keys(value)
        
    def click_HTML_ID_button(self, ID_element):
        self.driver.find_element(By.ID, ID_element).click()
        #WebDriverWait(self.driver, 10).until(EC.url_to_be(self.driver.current_url))
        WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script("return document.readyState === 'complete'"))
    def click_HTML_ID_radio_box(self, ID_element):
        return self.driver.find_element(By.ID, ID_element).click()
        
    def get_HTML_TAG_in_HTML_ID_element(self, ID_element, index1, index2):
        table = self.driver.find_element(By.ID, ID_element)
        tbody = table.find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        # Note that Python list indexing starts at zero
        second_tr = trs[index1]
        tds = second_tr.find_elements(By.TAG_NAME, "td")
        third_td = tds[index2]
        return third_td
    def get_HTML_TAG_text(self, ID_element, index1, index2):
        table = self.driver.find_element(By.ID, ID_element)
        tbody = table.find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        # Note that Python list indexing starts at zero
        second_tr = trs[index1]
        tds = second_tr.find_elements(By.TAG_NAME, "td")
        third_td = tds[index2]
        return third_td.get_attribute("innerText")
    
    def get_HTML_TAG_hyperlink(self, ID_element, index1, index2):
        table = self.driver.find_element(By.ID, ID_element)
        tbody = table.find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        # Note that Python list indexing starts at zero
        second_tr = trs[index1]
        tds = second_tr.find_elements(By.TAG_NAME, "td")
        third_td = tds[index2]
        return third_td.get_attribute("href") 
    
    def get_HTML_TAG_innerHTML(self, ID_element, index1, index2):
        table = self.driver.find_element(By.ID, ID_element)
        tbody = table.find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        # Note that Python list indexing starts at zero
        second_tr = trs[index1]
        tds = second_tr.find_elements(By.TAG_NAME, "td")
        third_td = tds[index2]
        return third_td.get_attribute("innerHTML")  
     
    def select_from_drop_down_list(self, ID_element, value):
        # Find the element by its ID.
        element = self.driver.find_element(By.ID, ID_element)
        # Create a wait object with a timeout of 10 seconds
        wait = WebDriverWait(self.driver, 10)
        # Wait for the dropdown list to be visible
        wait.until(EC.visibility_of(element))         

        # Find the drop down list in the element.
        drop_down_list = element.find_element(By.TAG_NAME, "select")
    
        # Find the option with the specified value.
        option = drop_down_list.find_element(By.XPATH,"//option[text()='{}']".format(value))
    
        # Select the option.
        option.click()
                
    def login(self, url, username, password):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(url))
        # Find the username input box by its ID
        username_box = self.driver.find_element(by="id", value="j_username")
        # Send the value "username" to the username input box
        username_box.send_keys(username)
        # Find the password input box by its ID
        password_box = self.driver.find_element(by="id", value="j_password")
        # Send the value "password" to the password input box
        password_box.send_keys(password)
        # Click the login button
        self.Wait_for_WebDriverWait_element("idButtonLogin")
        self.click_HTML_ID_button("idButtonLogin")
        # Verify that the login was successful
        if (
            self.driver.find_element(by="id", value="idMxTitle").text == "MP Engineer To Do List"
        ):
            print("Login successful")
        else:
            print("Login failed")
            exit()
    def open_url(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(url))

    def current_url(self):
        return self.driver.current_url

    def close_driver(self):
        self.driver.close()
