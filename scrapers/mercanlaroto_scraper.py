import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException




class MercanlarOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive 


    def getMercanlarOtoVariables(self):
        mainURL = 'https://b2b.mercanlar.com/'
        searchURL = 'https://b2b.mercanlar.com/Home'
        usr_value = 'mcobanoglu7@hotmail.com'
        pw_value = 'Coban1'
        data6 = ['','','','','','MERCANLAR OTO','','','','']

        return mainURL, searchURL, usr_value, pw_value, data6;
    
    async def runTabControlProcessMercanlarOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):
            print('mercanlar search trigger 1')
            self.driver.execute_script("window.open('about:blank', 'mercanlaroto');")
            self.driver.switch_to.window("mercanlaroto")
            self.driver.get(mainURL)

            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            
            if(self.driver.find_element(By.ID, 'LoginEmail')): 
                self.loginMercanlarOtoUser(usr_value, pw_value);
                return;
            print('mercanlar search trigger 2')
            self.searchMercanlarOtoPart()
    
    def loginMercanlarOtoUser(self, usr_value, pw_value):
       
            WebDriverWait(self.driver, 500).until(expected_conditions.visibility_of_element_located((By.ID, 'LoginEmail')))
            username = self.driver.find_element(By.ID, 'LoginEmail') 
            password = self.driver.find_element(By.ID, 'LoginPassword') 
            login_button = self.driver.find_element(By.CSS_SELECTOR, '.login-btn-container .btn.btn-green') 
            # FILL DOM ELEMENTS
            username.send_keys(usr_value)
            password.send_keys(pw_value)
            login_button.click();
    
            # time.sleep(3.5)
            print('mercanlar search trigger 3')
            self.searchMercanlarOtoPart()

    

    def searchMercanlarOtoPart(self):
         # GO TO SEARCH PAGE
        print('mercanlar search started')
        WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "footer-middle-inner")))
        # WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".img-responsive.center-block")))
        # SEARCH PART
        searchbar = self.driver.find_element(By.ID, "spare_part_number")
        print('searchbar', searchbar)
        input_value = searchbar.get_attribute("value")
        if (input_value):
            searchbar.send_keys(Keys.CONTROL + "a")
            searchbar.send_keys(Keys.DELETE)  
        searchbar.send_keys(self.user_input)
        searchbar.submit()



    def checkIfPartExistsMercanlarOto(self, data6):
        WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        result_text = self.driver.find_element(By.CSS_SELECTOR, ".result-container").text
        alert_text = 'önermek'
        if (alert_text in result_text):
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data6.extend(no_record)
        
            return data6, False;

        return data6, True;

    # ##
    def extractMercanlarOtoPartData(self, data6):
        ignored_exceptions=(StaleElementReferenceException)
        time.sleep(2.5)
        WebDriverWait(self.driver, 100, ignored_exceptions).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-item-wrapper")
        row_count = len(dom_elements);

        table_data = self.driver.find_element(By.CSS_SELECTOR, '.result-container')

        time.sleep(4.5)

        for i in range(row_count):
            brand_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(3) .value';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text
            

            oem_no_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(2) .value';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

            product_name_selector =  '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(3) .thumb-list-item-group:nth-of-type(1) .value';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text


            manufacturer_code_selector =  '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(1) .value';
            manufacturer_code = table_data.find_elements(By.CSS_SELECTOR, manufacturer_code_selector)[0].text

            desc = '-'
            content = '-'
            car_type = '-'
            engine_type = '-'

            
            list_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(1) .col-xs-4:nth-of-type(3) .value'
            list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text.strip()

            tax_included_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(2) .total-price'
            tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text.strip()
           

            stock_values_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(5) .thumb-list-item-group .value:nth-of-type(2) ul span';
            stock_values = table_data.find_elements(By.CSS_SELECTOR, stock_values_selector)
            stock_count = len(stock_values)
            stock = 'Yok'
            value_array = []


            for j in range(stock_count):
                stock_value = stock_values[j].get_attribute('class')
                print('stock_value', stock_value)
                if ('in-stock' in stock_value):
                    value_array.append('var')
                elif ('critical' in stock_value):
                    value_array.append('var')
        
                
            if (bool(len(value_array))):
                stock = 'Var'

           
            values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]

            print("values", values)

            data6.extend(values)
        return data6;


    async def mercanlarOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data6 = self.getMercanlarOtoVariables()

        is_tab_active = self.checkIfTabActive(3)

        
        if (is_tab_active):
            print('mercanlar search trigger 1')
            self.searchMercanlarOtoPart()
        else: 
            await self.runTabControlProcessMercanlarOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)

        data6, is_exist = self.checkIfPartExistsMercanlarOto(data6)
        
        if (not is_exist):
            return data6;

       
        data6 = self.extractMercanlarOtoPartData(data6)

        return data6;