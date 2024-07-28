import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class MotorAsinScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive

    def getMotorAsinVariables(self):
            mainURL = 'https://b4b.motorasin.com';
            usr_value = "BPR.034.212"
            pw_value = "6322612"
            data2 = ['','','','','','MOTOR AŞİN','','','','']

            return mainURL, data2, usr_value, pw_value;

    async def loginMotorAsinUser(self, usr_value, pw_value):
        print('login motor aşin')
        WebDriverWait(self.driver, 2).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "txtUserName")))
        username = self.driver.find_element(By.CLASS_NAME, "txtUserName") 
        password = self.driver.find_element(By.CLASS_NAME, "txtPassword") 
        login_button = self.driver.find_element(By.ID, 'login')
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
       
        login_button.click();
    
        self.searchMotorAsinPart()


    async def runTabControlProcessMotorAsin(self, is_tab_active, mainURL,  usr_value, pw_value):
            self.driver.execute_script("window.open('about:blank', 'motorasin');")
            self.driver.switch_to.window("motorasin")
            self.driver.get(mainURL)

            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                await self.loginMotorAsinUser(usr_value, pw_value)
            except:
                self.searchMotorAsinPart()
    


    def searchMotorAsinPart(self):
        print('aşin search started')
        WebDriverWait(self.driver, 400).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".td-item.td-product")))
        print('aşin search middle')
        self.driver.find_element(By.CSS_SELECTOR, ".td-item.td-product")
        oem_search = self.driver.find_element(By.CLASS_NAME, "searchInput")
        oem_search.send_keys(Keys.CONTROL + "a")
        oem_search.send_keys(Keys.DELETE)   
        oem_search.send_keys(self.user_input)
        oem_search.send_keys(Keys.ENTER)

        print('aşin search ended')

    def extractMotorAsinPartData(self, data2):
        WebDriverWait(self.driver, 300).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")))
        
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2) > tr")

        table_data = self.driver.find_element(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")
        # GET ROW COUNT 
        row_count = len(dom_elements);

    
        for i in range(row_count):
            brand_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(6) span span';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text
            
            manufacturer_code_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(7) span';
            manufacturer_code = table_data.find_elements(By.CSS_SELECTOR, manufacturer_code_selector)[0].text

            oem_no_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(4) span';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

            product_name_selector =  'tr:nth-child(' + str(i + 1) + ') td:nth-child(5) span';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

            desc = 'YOK'
            content = 'YOK'
            car_type = 'YOK'
            engine_type = 'YOK'


            list_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(8) span font:not(.ng-hide)';
            list_price = table_data.find_elements(By.CSS_SELECTOR, list_price_selector)[0].text

            tax_included_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(10) span span:not(.ng-hide)'
            tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text

            try:
                if (table_data.find_element(By.CSS_SELECTOR, 'tr:nth-child(' + str(i + 1) + ') td:nth-child(11) .table-stock .stock-column .fa-check') or
                    table_data.find_element(By.CSS_SELECTOR, 'tr:nth-child(' + str(i + 1) + ') td:nth-child(11) .table-stock .stock-column .fa-exclamation-triangle')):
                    stock = 'VAR'
            except:
                stock = 'YOK'

            values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
            data2.extend(values)
        return data2;
    

    async def motorAsinSearch(self):
            mainURL, data2, usr_value, pw_value = self.getMotorAsinVariables()
            print('data2 aşin start', data2)

            is_tab_active = self.checkIfTabActive(1)

            if (is_tab_active):
                self.searchMotorAsinPart()
            else:
                await self.runTabControlProcessMotorAsin(is_tab_active, mainURL, usr_value, pw_value)


            try: 
                time.sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, '.table-products tbody:nth-of-type(2) > tr')
                data2 = self.extractMotorAsinPartData(data2)


                return data2;
            except:
                no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
                data2.extend(no_record)
            
                return data2;