from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Import Keys here
import pandas as pd

class MXIScraper:
    def __init__(self, headless: bool = False, driver_path: str = None):
        """
        Initialize the web scraper with optional parameters for headless mode and custom driver path.
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('MXIScraper')

        # Set up Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
        else:
            chrome_options.add_argument("--start-maximized")
        # Initialize the web driver
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(chrome_options)

    def _init_driver(self, options):
        """Initialize the Chrome web driver."""
        try:
            driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
            self.logger.info("Web driver initialized successfully.")
            return driver
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize web driver: {e}")
            raise
    def Wait_for_element_ID(self, ID_element):
        # Create an instance of the WebDriverWait class.
        wait = WebDriverWait(self.driver, 10)
        # Wait for the element to become visible.
        wait.until(EC.visibility_of(self.driver.find_element(By.ID, ID_element)))

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        Wait for an element to be visible on the page.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            self.logger.info(f"Element found: {value}")
            return element
        except TimeoutException:
            self.logger.warning(f"Element not found within {timeout} seconds: {value}")
            return None

    def get_element(self, by: By, value: str):
        """
        Retrieve a web element based on the provided selector.
        """
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            self.logger.error(f"Element not found: {value}")
            return None

    def send_keys_to_element(self, by: By, value: str, text: str):
        """
        Send keys to a specific element on the page.
        """
        element = self.get_element(by, value)
        if element:
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys to element: {value}")

    def click_element(self, by: By, value: str):
        """
        Click on a specific element on the page.
        """
        element = self.wait_for_element(by, value)
        if element:
            element.click()
            self.logger.info(f"Clicked element: {value}")
            self.wait_for_page_load()

    def wait_for_page_load(self, timeout: int = 10):
        """
        Wait until the page is fully loaded.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded successfully.")
        except TimeoutException:
            self.logger.warning("Page load timeout.")

    def select_from_dropdown(self, by: By, value: str, option_text: str):
        """
        Select an option from a dropdown list.
        """
        dropdown = self.get_element(by, value)
        if dropdown:
            try:
                dropdown.find_element(By.XPATH, f"//option[text()='{option_text}']").click()
                self.logger.info(f"Selected option '{option_text}' from dropdown: {value}")
            except NoSuchElementException:
                self.logger.error(f"Option '{option_text}' not found in dropdown: {value}")

    def login(self, url: str, username: str, password: str, username_field_id: str, password_field_id: str, login_button_id: str):
        """
        Automate the login process.
        """
        self.driver.get(url)
        self.wait_for_page_load()

        self.send_keys_to_element(By.ID, username_field_id, username)
        self.send_keys_to_element(By.ID, password_field_id, password)
        self.click_element(By.ID, login_button_id)
        if (self.driver.find_element(by="id", value="idHeaderMaintenixLogo")):
            self.logger.info("Login attempt completed.")
        else:
            self.logger.info("Login attempt failed.")
            exit()

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
    
    def execute_script(self, script: str):
        """
        Execute JavaScript on the current page.
        """
        try:
            result = self.driver.execute_script(script)
            self.logger.info(f"Executed script: {script}")
            return result
        except WebDriverException as e:
            self.logger.error(f"Error executing script: {e}")
            return None

    def get_current_url(self) -> str:
        """Return the current URL."""
        return self.driver.current_url

    def take_screenshot(self, filename: str):
        """Take a screenshot of the current page."""
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved as: {filename}")

    def close(self):
        """Close the web driver."""
        self.driver.quit()
        self.logger.info("Web driver closed.")

    def open_url(self, url: str):
        """Open a URL in the browser."""
        self.driver.get(url)
        self.wait_for_page_load()

    def get_html_element_text(self, by: By, value: str, index1: int, index2: int) -> str:
        """
        Retrieve text from a nested HTML element specified by its ID and tag indices.
        """
        element = self.get_element(by, value)
        if element:
            try:
                tbody = element.find_element(By.TAG_NAME, "tbody")
                trs = tbody.find_elements(By.TAG_NAME, "tr")
                selected_tr = trs[index1]
                tds = selected_tr.find_elements(By.TAG_NAME, "td")
                selected_td = tds[index2]
                return selected_td.get_attribute("innerText")
            except (NoSuchElementException, IndexError):
                self.logger.error("Error navigating nested HTML elements.")
                return ""
        return ""
    def send_ENTER_keys_element(self, by: By, value: str):
        """Open a URL in the browser."""
        input_element = self.get_element(By.ID,value)
        if input_element:
           input_element.send_keys(Keys.ENTER)  # Simulate pressing Enter key
        self.wait_for_page_load()
        
    def submit_form(self, form_name):
        form = self.driver.find_element(By.NAME, form_name)
        if form:
            self.driver.execute_script("arguments[0].submit();", form)
        
    def get_text_from_element(self, by, value):
        element = self.get_element(by, value)
        if element:
            return element.text
        return None    
    
    def get_elements_with_attributes(self, tag_name, attributes):
            elements = []
            try:
                # Construct a CSS selector from the attributes
                # Escape double quotes in attribute values
                attributes = {k: v.replace('"', '\\"') for k, v in attributes.items()}
                selector_parts = [f"{tag_name}[{k}='{v}']" for k, v in attributes.items()]
                selector = ' and '.join(selector_parts)
        
                # Add debug print to check the generated selector
                print(f"Generated CSS Selector: {selector}")
    
                # Use CSS_SELECTOR to find elements
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            except NoSuchElementException as e:
                print(f"Elements not found: {e}")
            except Exception as e:
                print(f"Error in selector: {e}")
            return elements
       
    def get_table_cell_text(self, table_id, row_index, col_index):
        table = self.get_element(By.ID, table_id)
        if table:
            rows = table.find_elements(By.TAG_NAME, "tr")
            if row_index < len(rows):
                cells = rows[row_index].find_elements(By.TAG_NAME, "td")
                if col_index < len(cells):
                    return cells[col_index].text
        return None 
       
    def click_link_by_text(self, link_text):
        try:
            link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
            link.click()
        except TimeoutException:
            print(f"Link with text '{link_text}' not found or not clickable.")    
    
    def click_link_by_element_tag(self, tag_name, attribute_name=None, attribute_value=None):
        try:
            if attribute_name and attribute_value:
                locator = (By.CSS_SELECTOR, f"{tag_name}[{attribute_name}='{attribute_value}']")
            else:
                locator = (By.TAG_NAME, tag_name)

            link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            link.click()
        except TimeoutException:
            print(f"Element with tag '{tag_name}' and attribute '{attribute_name}={attribute_value}' not found or not clickable.")
    
    def click_link_by_element_tag(self, table_id, row_index, col_index):
        try:
            # Find the table element by ID
            table = self.driver.find_element(By.ID, table_id)
            # Locate the tbody of the table
            tbody = table.find_element(By.TAG_NAME, "tbody")
            # Get all rows in the tbody
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            # Ensure the specified row index is within the range
            if row_index < len(rows):
                # Get all columns (td elements) in the specified row
                columns = rows[row_index].find_elements(By.TAG_NAME, "td")
                
                # Ensure the specified column index is within the range
                if col_index < len(columns):
                    # Find the hyperlink within the specified column
                    cell = columns[col_index]
                    link = cell.find_element(By.TAG_NAME, "a")  # Assuming the link is an <a> tag
                    
                    # Click the hyperlink
                    link.click()
                    WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script("return document.readyState === 'complete'"))
                else:
                    print(f"Column index {col_index} out of range.")
            else:
                print(f"Row index {row_index} out of range.")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        except TimeoutException as e:
            print(f"Timeout exception: {e}")
           
    def get_table_data(self, table_id):
        table = self.get_element(By.ID, table_id)
        if table:
            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                cols = [col.text for col in cols]
                data.append(cols)
            return data
        return []

    def download_table_to_excel(self, table_id, file_name):
        data = self.get_table_data(table_id)
        if data:
            df = pd.DataFrame(data)
            df.to_excel(file_name, index=False, header=False)
            print(f"Table data has been saved to {file_name}")
        else:
            print("No data found to save.")        
        
    def extract_first_items_if_condition_met(self, table_id,attribute_checks, row_index=0, matched_items=None):
        if matched_items is None:
            matched_items = []
    
        # Attempt to find the table and the rows
        try:
            table = self.driver.find_element(By.ID, table_id)
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
        except Exception as e:
            print("Error finding the table or rows:", e)
            return matched_items
    
        # Base case: if row_index is greater than or equal to the number of rows, stop recursion
        if row_index >= len(rows):
            return matched_items
    
        try:
            columns = rows[row_index].find_elements(By.TAG_NAME, "td")
    
            if len(columns) >= 5:
                fifth_column = columns[5]  # The fifth column is at index 4

                # Attempt to find the <a> tag within the fifth column and check attributes
                try:
                    links = fifth_column.find_elements(By.TAG_NAME, "a")
                    if links:
                        link = links[0]
                        style = link.get_attribute("style")
                       
                        # Check all attribute-value pairs
                        if all(f"{name}: {value}" in style for name, value in attribute_checks):
                            try:
                                 # Find all <a> elements in the third column (index 2)
                                 href_elements = columns[2].find_elements(By.TAG_NAME, "a")
                                 # Get the href attribute from the first <a> element if it exists
                                 href_links = href_elements[0].get_attribute("href") if href_elements else None
                                 print(f"Link: {href_links}")
                            except Exception as e: 
                                 print("Error processing href_links:", e)
                            matched_items.append([columns[1].text, columns[2].text, columns[5].text,href_links])  # Append as list (2D array)
                except Exception as e:
                    print("Error processing the fifth column:", e)
    
        except Exception as e:
            print(f"Error processing row {row_index}:", e)
    
        # Recursive call to check the next row
        return self.extract_first_items_if_condition_met(table_id,attribute_checks, row_index + 1, matched_items)

 
