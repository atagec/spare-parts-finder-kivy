import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class GenelOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive

    def getGenelOtoVariables(self):
            mainURL = "https://b4b.geneloto.com.tr/"
            homeURL = "https://b4b.geneloto.com.tr/Home"
            searchURL = "https://b4b.geneloto.com.tr/Search";
            data1 = ['', '', '', '', '', 'GENEL OTO', '', '', '', '']
            customer_code_value = 'G3600';
            user_code_value = 'G3600'
            password_value = 'GENELOTO'

            return mainURL, homeURL, searchURL, data1, customer_code_value, user_code_value, password_value;


    async def loginGenelOtoUser(self, customer_code_value, user_code_value, password_value, searchURL):
        customer_code = self.driver.find_element(By.ID, "CustomerCode") 
        user_code = self.driver.find_element(By.ID, "UserCode") 
        password = self.driver.find_element(By.ID, "Password") 
        login_button = self.driver.find_element(By.ID, "btnLogin") 
        # FILL DOM ELEMENTS
        customer_code.send_keys(customer_code_value)
        user_code.send_keys(user_code_value)
        password.send_keys(password_value)
        login_button.click();
        print('logged in')

        self.searchGenelOtoPart(searchURL)


    async def runTabControlProcessGenelOto(self, is_tab_active, mainURL, homeURL, searchURL, customer_code_value, user_code_value, password_value):
            self.driver.get(mainURL)
            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                WebDriverWait(self.driver, 2).until(expected_conditions.visibility_of_element_located((By.ID, "CustomerCode")))
                if (self.driver.find_element(By.ID, "CustomerCode")):
                    await self.loginGenelOtoUser(customer_code_value, user_code_value, password_value, searchURL)    
            except:
                self.searchGenelOtoPart(searchURL)
      


    def searchGenelOtoPart(self, searchURL):
        if (self.driver.current_url != searchURL):
            self.driver.get(searchURL)
            # time.sleep(4)
            search_panel = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".panelLoading.search-loading")))
            WebDriverWait(self.driver, 10).until(lambda d: 'search-loading' not in search_panel.get_attribute('class'))
            print('genel redirected to search')
            
        time.sleep(1.5)
        oem_search = self.driver.find_element(By.ID, "txtGeneralSearch")
        oem_search.send_keys(Keys.CONTROL + "a")
        oem_search.send_keys(Keys.DELETE)  
        oem_search.send_keys(self.user_input)
        oem_search.send_keys(Keys.ENTER)
        print('genel search ended')

    def extractGenelOtoPartData(self, data1):
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, "#tbResult tr")

        table_data = self.driver.find_element(By.CSS_SELECTOR, "#tbResult")
        
        row_count = len(dom_elements);

        for i in range(row_count):
            row_index = i + 1
            row_selector = f"tr:nth-child({row_index})"

            selectors = {
                "brand": "td:nth-child(5)",
                "manufacturer_code": "td:nth-child(6)",
                "oem_no": "td:nth-child(7)",
                "product_name": "td:nth-child(8)",
                "desc": "td:nth-child(9)",
                "car_type": "td:nth-child(11)",
                "engine_type": "td:nth-child(12)",
                "list_price": "td:nth-child(16)",
                "tax_included_price": "td:nth-child(17)",
                "stock": "td:nth-child(18) span:nth-child(2)"
            }

            values = []
            for key, selector in selectors.items():
                full_selector = f"{row_selector} {selector}"
                value = table_data.find_elements(By.CSS_SELECTOR, full_selector)[0].text
                values.append(value)

            data1.extend(values)
        return data1;

        


    async def genelOtoSearch(self):
        mainURL, homeURL, searchURL, data1, customer_code_value, user_code_value, password_value = self.getGenelOtoVariables()

        is_tab_active = self.checkIfTabActive(0)

        if (is_tab_active):
            self.searchGenelOtoPart(searchURL)
        else:
            await self.runTabControlProcessGenelOto(is_tab_active, mainURL, homeURL, searchURL, customer_code_value, user_code_value, password_value)
        
        # WAIT FOR DOM TO LOAD
        try: 
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, '#divSearchTable .alert')
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data1.extend(no_record)  
            return data1;      
        except:
            WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#pDataTable tbody td:nth-child(5)")))
            # GET ROW COUNT 
            if (self.driver.find_elements(By.CSS_SELECTOR, "#tbResult tr")):
                data1 = self.extractGenelOtoPartData(data1)
                return data1;