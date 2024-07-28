import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class BasbugOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input 
        self.checkIfTabActive = checkIfTabActive


    def getBasbugOtoVariables(self):
        mainURL = 'https://b2b.basbug.com.tr/'
        searchURL = 'https://b2b.basbug.com.tr/Arama/UrunArama'
        usr_value = '5323925610'
        pw_value = '52727485'
        data4 = ['','','','','','BAŞBUĞ OTO','','','','']

        return mainURL, searchURL, usr_value, pw_value, data4;

    async def runTabControlProcessBasbugOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):
            
            self.driver.execute_script("window.open('about:blank', 'basbugoto');")
            self.driver.switch_to.window("basbugoto")
            self.driver.get(mainURL)

            try:
                await self.loginBasbugOtoUser(searchURL, usr_value, pw_value)
            except:
                self.searchBasbugOtoPart(searchURL)

    async def loginBasbugOtoUser(self, searchURL, usr_value, pw_value):
        # LOGGED IN KONTROLÜ EKLENECEK
        # GET DOM ELEMENTS
        WebDriverWait(self.driver, 6).until(expected_conditions.visibility_of_element_located((By.ID, 'KullaniciAd')))
        time.sleep(0.5)
        username = self.driver.find_element(By.ID, 'KullaniciAd') 
        password = self.driver.find_element(By.ID, 'Sifre') 
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'form .btn.style-danger.btn-raised') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        # password.send_keys("GENELOTO")
        login_button.click();

        self.searchBasbugOtoPart(searchURL)
    
    def searchBasbugOtoPart(self, searchURL):
        if (self.driver.current_url != searchURL):
            self.driver.get(searchURL)
        # SEARCH PART
        print('basbug search started')
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, "txtTumundeAra")))
        searchbar = self.driver.find_element(By.ID, "txtTumundeAra")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        # WAIT FOR DOM TO LOAD
        time.sleep(2)
        print('basbug search ended')

    def extractBasbugOtoPartData(self, data4):
         # GET ROW COUNT 
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, "#grAramaSonuc-body table[id^='tableview']")
        row_count = len(dom_elements);

        table_data = self.driver.find_element(By.CSS_SELECTOR, '#grAramaSonuc-body')

        # CREATE PARTS DATA
        for i in range(row_count):
            brand_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(1)';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text

            oem_no_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(3)';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text


            product_name_selector =  'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(6)';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

            manufacturer_code = "-"
            desc = '-'
            content = '-'

            car_type_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(8)'
            car_type = table_data.find_elements(By.CSS_SELECTOR, car_type_selector)[0].text
            
            engine_type_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(8)'
            engine_type = table_data.find_elements(By.CSS_SELECTOR, engine_type_selector)[0].text
            
            list_price_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(11)'
            list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text

            tax_included_price_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(12)'
            # tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text
            original_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].get_attribute("data-original-title")
            price_value = original_price[original_price.find(':')+1 : original_price.find('TL')]
            tax_included_price =  price_value + 'TL'

            in_stock_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="green"]';
            on_the_way_stock_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="pink"]'
           
            stock = None;
            try:
                if (table_data.find_element(By.CSS_SELECTOR, in_stock_selector)):
                    stock = "VAR"
               
            except:
                pass
            try:
                if (table_data.find_element(By.CSS_SELECTOR, on_the_way_stock_selector) and stock is None ):
                    stock = "YOLDA"
            except:
                if (stock is None):
                    stock = 'YOK'

            
            values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
            data4.extend(values)
    

        return data4;


    async def basbugOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data4 = self.getBasbugOtoVariables()
    
        is_tab_active = self.checkIfTabActive(1)

        if (is_tab_active):
            self.searchBasbugOtoPart(searchURL)
        else:
            await self.runTabControlProcessBasbugOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)
            
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#grAramaSonuc-body table[id^='tableview']")


            data4 = self.extractBasbugOtoPartData(data4)

            return data4;

        except:
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data4.extend(no_record)  
            return data4; 