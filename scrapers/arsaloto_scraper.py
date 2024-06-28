import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class ArsalOtoScraper:
    def __init__(self, driver, user_input, checkIfTabActive):
        self.driver = driver
        self.user_input = user_input
        self.checkIfTabActive = checkIfTabActive 

    def getArsalOtoVariables(self):
            mainURL = 'https://bayi.arsalotomotiv.com';
            searchURL = "https://bayi.arsalotomotiv.com/search"
            usr_value = "M0101024"
            pw_value = "07EA13"
            data3 = ['','','','','','ARSAL OTO','','','','']

            return mainURL, searchURL, usr_value, pw_value, data3;

    def loginArsalOtoUser(self, usr_value, pw_value):
        WebDriverWait(self.driver, 2000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.inputfrm[type="text"]')))
        # GET DOM ELEMENTS
        username = self.driver.find_element(By.CSS_SELECTOR, '.inputfrm[type="text"]') 
        password = self.driver.find_element(By.CSS_SELECTOR, '.inputfrm[type="password"]') 
        login_button = self.driver.find_element(By.ID, 'login_button') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        login_button.click();
    
        self.searchArsalOtoPart()

    async def runTabControlProcessArsalOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):
            self.driver.execute_script("window.open('about:blank', 'arsaloto');")
            self.driver.switch_to.window("arsaloto")
            self.driver.get(mainURL)
                
            try:
                await self.loginArsalOtoUser(usr_value, pw_value)
            except:
                self.searchArsalOtoPart()
               

    def searchArsalOtoPart(self):
        time.sleep(2)
        # SEARCH PART
        searchbar = self.driver.find_element(By.ID, "searchbar")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)
    
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-table")))
    
    def extractArsalOtoPartData(self, data3):
        time.sleep(4.5)
        # GET ROW COUNT 
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".place-self-center .p-datatable-tbody tr")
    
        row_count = len(dom_elements);

        table_data = self.driver.find_element(By.CSS_SELECTOR, ".place-self-center")

        for i in range(row_count):
                row_selector = f'.p-datatable-tbody tr:nth-of-type({i + 1})'

                print('wow', f'{row_selector} td:nth-of-type(3) span')

                # Old brand
                # brand = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(3) span')[1].text
                brand = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(2) span')[1].text
                oem_no = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(5)')[0].text
                # Old product name
                # product_name = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(3) span')[0].text
                product_name = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(2) span')[0].text

                tax_included_price = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(8)')[0].text

                stock = 'YOK'
                if table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(7) img[alt*="Var"]'):
                    stock = 'VAR'
                elif table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(7) svg.fill-blue-500'):
                    stock = 'YOLDA'

                values = [brand, "-", oem_no, product_name, "-", "-", "-", "-", tax_included_price, stock]
                data3.extend(values)

        return data3;



    
    async def arsalOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data3 = self.getArsalOtoVariables()

        is_tab_active = self.checkIfTabActive(1)

        if (is_tab_active):
           self.searchArsalOtoPart()
        else:
           await self.runTabControlProcessArsalOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)
       
        
        try: 

            data3 = self.extractArsalOtoPartData(data3)
            return data3;
           
    
        except:
             # time.sleep(2.5)
            WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-emptymessage")))
            alert = self.driver.find_element(By.CSS_SELECTOR, '.p-datatable-emptymessage')
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data3.extend(no_record)
            
            return data3;
           