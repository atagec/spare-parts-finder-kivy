import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class BabacanOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive 

    def getBabacanOtoVariables(self):
        mainURL = 'https://b2b.babacandisticaret.com/login.aspx';
        searchURL = 'https://b2b.babacandisticaret.com/Search.aspx';
        defaultURL = 'https://b2b.babacandisticaret.com/Default.aspx';
        cst_value = '120.34.079';
        usr_value = '120.34.079';
        pw_value = '6322612';

        data7 = ['','','','','','BABACAN OTO','','','','']

        return mainURL, searchURL, defaultURL, cst_value, usr_value, pw_value, data7;

    async def runTabControlProcessBabacanOto(self, is_tab_active, mainURL, searchURL, cst_value, usr_value, pw_value):
        self.driver.execute_script("window.open('about:blank', 'babacanoto');")
        self.driver.switch_to.window("babacanoto")
        self.driver.get(mainURL)
        # LOGGED IN KONTROLÜ EKLENECEK
        # GET DOM ELEMENTS
        try:
            await self.loginBabacanOtoUser(cst_value, usr_value, pw_value, searchURL)
        except:
            self.searchBabacanOtoPart(searchURL)
               

    
    def loginBabacanOtoUser(self, cst_value, usr_value, pw_value, searchURL):
        time.sleep(4)
        if (self.driver.find_element(By.ID, 'txtCustomerB2bCode')):
        # if (WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, "txtCustomerB2bCode")))):
            customer_code = self.driver.find_element(By.ID, 'txtCustomerB2bCode') 
            user_code = self.driver.find_element(By.ID, 'txtCustomerUserCode') 
            password = self.driver.find_element(By.ID, 'txtCustomerPassword') 
            login_button = self.driver.find_element(By.ID, 'btnLogin') 
    
            customer_code.clear()
            user_code.clear()
            password.clear()

            customer_code.send_keys(cst_value)
            user_code.send_keys(usr_value)
            password.send_keys(pw_value)
            login_button.click();
            # self.driver.get(defaultURL)
            search_button = self.driver.find_element(By.CSS_SELECTOR, '.has-sub.m-img-search a') 
            search_button.click()
            print('search babacan oto part')
            self.searchBabacanOtoPart(searchURL)

    def searchBabacanOtoPart(self, searchURL):
        if (self.driver.current_url != searchURL):
            self.driver.get(searchURL)
        # GO TO SEARCH PAGE
        print('search babacan oto part 2')
        WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, "txtGeneralSearch")))
        # SEARCH PART
        searchbar = self.driver.find_element(By.ID, "txtGeneralSearch")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        time.sleep(3)

    def extractBabacanOtoPartData(self, data7):
            print('extract babacan oto part')
            dom_elements = self.driver.find_elements(By.CSS_SELECTOR, "#gvResult .Row")
            row_count = len(dom_elements);

            table_data = self.driver.find_element(By.CSS_SELECTOR, "#gvResult")

            # ----------  
            # Iterate through the rows
            for i, row in enumerate(dom_elements):
                # Use relative selectors to find the cells within the current row
                cells = row.find_elements(By.CSS_SELECTOR, '.Cell')

                brand = cells[4].text
                oem_no = '-'
                product_name = cells[2].text
                car_type = cells[3].text
                desc = '-'
                content = '-'
                manufacturer_code = '-'
                engine_type = '-'
                tax_included_price = 'SİTEYE BAKINIZ'
                list_price = cells[7].text.strip()

                # Check stock status
                stock = "YOK"
                try:
                    if cells[5].find_element(By.CSS_SELECTOR, 'img[src*="green"]'):
                        stock = "VAR"
                except:
                    pass

                # Collect values in the desired order
                values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]

                data7.extend(values)

            return data7

    async def babacanOtoSearch(self):
        mainURL, searchURL, defaultURL, cst_value, usr_value, pw_value, data7 = self.getBabacanOtoVariables()

        is_tab_active = self.checkIfTabActive(4)

        if (is_tab_active):
            self.searchBabacanOtoPart(searchURL)
        else:
            await self.runTabControlProcessBabacanOto(is_tab_active, mainURL, searchURL, cst_value, usr_value, pw_value)


        
        # time.sleep(4)

        try:
            if(self.driver.find_element(By.CSS_SELECTOR, '#gvResult .Row')):

                data7 = self.extractBabacanOtoPartData(data7)

                return data7;
               
        except:    
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data7.extend(no_record)

            return data7;