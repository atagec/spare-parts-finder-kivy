import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class BorusanOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive    

    def getBorusanOtoVariables(self):
        mainURL = 'https://opss.borusanotomotiv.com/'
        searchURL = 'https://opss.borusanotomotiv.com/Purchase/ItemQuery'
        usr_value = 'Mcobanoglu'
        pw_value = '9vtöisi1'
        data5 = ['','','','','','BORUSAN OTO','','','','']

        return mainURL, searchURL, usr_value, pw_value, data5;
    
    async def runTabControlProcessBorusanOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):

            self.driver.execute_script("window.open('about:blank', 'borusanoto');")
            self.driver.switch_to.window("borusanoto")
            self.driver.get(mainURL)

                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            try:
                await self.loginBorusanOtoUser(usr_value, pw_value, searchURL)
            except:
                WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, "divCartBlockPartial")))

                self.searchBorusanOtoPart(searchURL)

    def loginBorusanOtoUser(self, usr_value, pw_value, searchURL):
        WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, 'UserName')))
        username = self.driver.find_element(By.ID, 'UserName') 
        password = self.driver.find_element(By.ID, 'Password') 
        login_button = self.driver.find_element(By.ID, 'btnLogon') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        login_button.click();

        time.sleep(1.25)

    
        self.searchBorusanOtoPart(searchURL)
    
    def searchBorusanOtoPart(self, searchURL):
        if (self.driver.current_url != searchURL):
            self.driver.get(searchURL)
        
         # GO TO SEARCH PAGE
        WebDriverWait(self.driver, 750).until(expected_conditions.visibility_of_element_located((By.ID, "ItemNo_I")))
        # SEARCH PART
        searchbar = self.driver.find_element(By.ID, "ItemNo_I")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

    def checkIfPartExistsBorusanOto(self, data5):
        result_text = self.driver.find_element(By.CSS_SELECTOR, "#divItemResult tbody").text
        alert_text = 'tanımlı değil'
        if (alert_text in result_text):
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data5.extend(no_record)
        
            return data5, False;
        
        return data5, True;


    def extractBorusanOtoPartData(self, data5):
        manufacturer_code = "-"
        desc = '-'
        car_type  = '-'
        engine_type  = '-'

        selectors = {
            "brand": '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(2)',
            "oem_no": '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(2)',
            "product_name": '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(4)',
            "list_price": '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(4)',
            "tax_included_price_value": '#divItemResult table tbody tr:nth-of-type(4) td:nth-of-type(4)',
            "stock": '#divItemResult table tbody tr:nth-of-type(3) td:nth-of-type(2)'
        }

        result = {}
        for key, selector in selectors.items():
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                result[key] = element.text
            except:
                result[key] = None

        # Construct the values list in the required order
        tax_included_price = f"₺{result['tax_included_price_value']}"
        values = [
            result['brand'], None, result['oem_no'], result['product_name'], None,
            None, None, result['list_price'], tax_included_price, result['stock']
        
        ]

        data5.extend(values)
        
        return data5

    async def borusanOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data5 = self.getBorusanOtoVariables();

        is_tab_active = self.checkIfTabActive(2)

        if (is_tab_active):
            self.searchBorusanOtoPart(searchURL)
        else:
            await self.runTabControlProcessBorusanOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)
        
        # WAIT FOR DOM TO LOAD
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "divItemResult")))
        time.sleep(3)

        data5, is_exist = self.checkIfPartExistsBorusanOto(data5)
        if (not is_exist):
            return data5;
    
        data5 = self.extractBorusanOtoPartData(data5)

        return data5;