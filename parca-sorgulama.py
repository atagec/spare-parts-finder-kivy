import customtkinter
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from CTkTable import *
import numpy as np
import time
from asyncio import run

# kivy imports
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen



# BROWSER DRIVER IMPORTS
# from browser_driver import BrowserDriver
# browser_instance = BrowserDriver()
# driver = browser_instance.driver



customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class DesktopView(MDScreen):
    pass

class App(MDApp):
    def __init__(self):
        super().__init__()
    def build(self):
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("MARKA.", dp(30)),
                ("ÜRETİCİ KODU", dp(30)),
                ("OEM", dp(60), self.sort_on_signal),
                ("ÜRÜN ADI", dp(30)),
                ("AÇIKLAMA", dp(30)),
                ("ARAÇ TİPİ", dp(30), self.sort_on_schedule),
                ("MOTOR TİPİ", dp(30), self.sort_on_team),
                ("LİSTE FİYAT", dp(30), self.sort_on_team),
                ("STOK", dp(30), self.sort_on_team)
            ],
            row_data=[
                (
                    "1",
                    ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal"),
                    "Astrid: NE shared managed",
                    "Medium",
                    "Triaged",
                    "0:33",
                    "Chase Nguyen",
                    "Chase Nguyen",
                    "Chase Nguyen"
                ),
                (
                    "2",
                    ("alert-circle", [1, 0, 0, 1], "Offline"),
                    "Cosmo: prod shared ares",
                    "Huge",
                    "Triaged",
                    "0:39",
                    "Brie Furman",
                    "Brie Furman",
                    "Brie Furman"
                ),
                (
                    "3",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Phoenix: prod shared lyra-lists",
                    "Minor",
                    "Not Triaged",
                    "3:12",
                    "Jeremy lake",
                    "Jeremy lake",
                    "Jeremy lake"
                ),
                (
                    "4",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Sirius: NW prod shared locations",
                    "Negligible",
                    "Triaged",
                    "13:18",
                    "Angelica Howards",
                    "Angelica Howards",
                    "Angelica Howards"
                ),
                (
                    "5",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Sirius: prod independent account",
                    "Negligible",
                    "Triaged",
                    "22:06",
                    "Diane Okuma",
                    "Diane Okuma",
                    "Diane Okuma"
                ),
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    # Sorting Methods:
    # since the https://github.com/kivymd/KivyMD/pull/914 request, the
    # sorting method requires you to sort out the indexes of each data value
    # for the support of selections.
    #
    # The most common method to do this is with the use of the builtin function
    # zip and enumerate, see the example below for more info.
    #
    # The result given by these funcitons must be a list in the format of
    # [Indexes, Sorted_Row_Data]

    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))

    def sort_on_schedule(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: sum(
                    [
                        int(l[1][-2].split(":")[0]) * 60,
                        int(l[1][-2].split(":")[1]),
                    ]
                ),
            )
        )

    def sort_on_team(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][-1]))
    # def __init__(self):
    #     super().__init__()

        # configure window
        # self.title("Çobanoğlu Parça Sorgulama")
        # self.geometry(f"{1100}x{580}")

        # Grid configuration
        # self.configure_grid()

        # Create frame
        # self.create_frame()

        # Create entry and search button
        # self.create_entry_and_button()

       

    def configure_grid(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=0)

    def create_frame(self):
        # Create frame
        self.frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=1)

    def create_entry_and_button(self):
        # Create entry and search button
        self.entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="OEM NO")
        self.entry.grid(row=0, column=1, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", command=self.searchPart)

        self.search_button = customtkinter.CTkButton(master=self.frame, text="ARA", width=90, command=self.searchPart, fg_color="#0054ac")
        self.search_button.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)



    # @cached_property
    # def driver(self):
    #     firefox_options = Options();
    #     firefox_options.add_argument("-profile")
    #     # user_profile
    #     user_profile_name = "User"
    #     # user_profile_name = "dbura"
    #     firefox_options.add_argument("C:/Users/"+ user_profile_name + "/AppData/Roaming/Mozilla/Firefox/Profiles/searchpartuser")
       

    #     return webdriver.Firefox(service=Service('./geckodriver.exe'), options=firefox_options)

    def checkIfTabActive(self, index):
        parent_handle = driver.current_window_handle
        all_handles = driver.window_handles
        print("parent handle", parent_handle)
        print("all_handles", all_handles)
       
        if (len(all_handles) < index + 1):
            return False;
    
        for handle in all_handles:
            if handle != parent_handle:
                tab_id = all_handles[index]
                driver.switch_to.window(tab_id)
                return True
                break
    

    def getGenelOtoVariables(self):
        mainURL = "https://b4b.geneloto.com.tr/"
        homeURL = "https://b4b.geneloto.com.tr/Home"
        searchURL = "https://b4b.geneloto.com.tr/Search";
        data1 = ['','','','','','GENEL OTO','','','','']
        customer_code_value = 'G3600';
        user_code_value = 'G3600'
        password_value = 'GENELOTO'

        return mainURL, homeURL, searchURL, data1, customer_code_value, user_code_value, password_value;


    async def loginGenelOtoUser(self, customer_code_value, user_code_value, password_value, searchURL):
        customer_code = driver.find_element(By.ID, "CustomerCode") 
        user_code = driver.find_element(By.ID, "UserCode") 
        password = driver.find_element(By.ID, "Password") 
        login_button = driver.find_element(By.ID, "btnLogin") 
        # FILL DOM ELEMENTS
        customer_code.send_keys(customer_code_value)
        user_code.send_keys(user_code_value)
        password.send_keys(password_value)
        login_button.click();
        print('logged in')

        self.searchGenelOtoPart(searchURL)

    
    async def runTabControlProcessGenelOto(self, is_tab_active, mainURL, homeURL, searchURL, customer_code_value, user_code_value, password_value):
            # if (self.driver.current_url != homeURL or self.driver.current_url != searchURL):
            driver.get(mainURL)
            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.ID, "CustomerCode")))
                if (driver.find_element(By.ID, "CustomerCode")):
                    await self.loginGenelOtoUser(customer_code_value, user_code_value, password_value, searchURL)    
            except:
                self.searchGenelOtoPart(searchURL)
            
            # GO TO SEARCH PAGE
            # if(self.driver.current_url != searchURL):
            #     self.driver.get(searchURL)
                # WAIT FOR DOM TO LOAD
    

    def searchGenelOtoPart(self, searchURL):
        if (driver.current_url != searchURL):
            driver.get(searchURL)
            # time.sleep(4)
            search_panel = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".panelLoading.search-loading")))
            WebDriverWait(driver, 10).until(lambda d: 'search-loading' not in search_panel.get_attribute('class'))
            print('genel redirected to search')
            
        time.sleep(1.5)
        oem_search = driver.find_element(By.ID, "txtGeneralSearch")
        oem_search.send_keys(Keys.CONTROL + "a")
        oem_search.send_keys(Keys.DELETE)  
        oem_search.send_keys(self.user_input)
        oem_search.send_keys(Keys.ENTER)
        print('genel search ended')

    def extractGenelOtoPartData(self, data1):
        dom_elements = driver.find_elements(By.CSS_SELECTOR, "#tbResult tr")

        table_data = driver.find_element(By.CSS_SELECTOR, "#tbResult")
       
        row_count = len(dom_elements);

        # for i in range(row_count):

            
        #     brand_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(5)';
        #     brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text

        #     manufacturer_code_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(6)';
        #     manufacturer_code = table_data.find_elements(By.CSS_SELECTOR, manufacturer_code_selector)[0].text

        #     oem_no_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(7)';
        #     oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

        #     product_name_selector =  'tr:nth-child(' + str(i + 1) + ') td:nth-child(8)';
        #     product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

        #     desc_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(9)';
        #     desc = table_data.find_elements(By.CSS_SELECTOR, desc_selector)[0].text

        #     content_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(10)';
        #     content = table_data.find_elements(By.CSS_SELECTOR, content_selector)[0].text

        #     car_type_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(11)';
        #     car_type = table_data.find_elements(By.CSS_SELECTOR, car_type_selector)[0].text

        #     engine_type_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(12)';
        #     engine_type = table_data.find_elements(By.CSS_SELECTOR, engine_type_selector)[0].text

        #     list_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(16)';
        #     list_price = table_data.find_elements(By.CSS_SELECTOR, list_price_selector)[0].text

        #     tax_included_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(17)'
        #     tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text

        #     stock_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(18) span:nth-child(2)';
        #     stock = table_data.find_elements(By.CSS_SELECTOR, stock_selector)[0].text
            
        #     values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
        #     data1.extend(values)
            
        # return data1;

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
            driver.find_element(By.CSS_SELECTOR, '#divSearchTable .alert')
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data1.extend(no_record)  
            return data1;      
        except:
            WebDriverWait(driver, 1000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#pDataTable tbody td:nth-child(5)")))
            # GET ROW COUNT 
            if (driver.find_elements(By.CSS_SELECTOR, "#tbResult tr")):
                data1 = self.extractGenelOtoPartData(data1)
                return data1;


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

            # if ('search' not in self.driver.current_url):
            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                await self.loginMotorAsinUser(usr_value, pw_value)
            except:
                self.searchMotorAsinPart()
    


    def searchMotorAsinPart(self):
        print('aşin search started')
        WebDriverWait(self.driver, 400).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".td-item.td-product")))
        # WebDriverWait(self.driver, 400).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="text"].searchInput')))
        print('aşin search middle')
        self.driver.find_element(By.CSS_SELECTOR, ".td-item.td-product")
        oem_search = self.driver.find_element(By.CLASS_NAME, "searchInput")
        oem_search.send_keys(Keys.CONTROL + "a")
        oem_search.send_keys(Keys.DELETE)   
        oem_search.send_keys(self.user_input)
        oem_search.send_keys(Keys.ENTER)

        print('aşin search ended')

    def extractMotorAsinPartData(self, data2):
        # time.sleep(3.5)
        WebDriverWait(self.driver, 300).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")))
        # WebDriverWait(self.driver, 4000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "mark")))
        # alert = self.driver.find_element(By.CSS_SELECTOR, '.table-products tbody:nth-of-type(2) > tr td')
        
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2) > tr")

        table_data = self.driver.find_element(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")
        # GET ROW COUNT 
        row_count = len(dom_elements);

        print('create aşin data')
    
        for i in range(row_count):
            print('aşin', i)
            brand_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(6) span span';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text

            print('aşin 2', brand)
            
            manufacturer_code_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(7) span';
            manufacturer_code = table_data.find_elements(By.CSS_SELECTOR, manufacturer_code_selector)[0].text

            print('aşin 3',  manufacturer_code)

            oem_no_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(4) span';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

            print('aşin 4', oem_no)

            product_name_selector =  'tr:nth-child(' + str(i + 1) + ') td:nth-child(5) span';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

            print('aşin 5', product_name)
            desc = 'YOK'
            content = 'YOK'
            car_type = 'YOK'
            engine_type = 'YOK'


            list_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(8) span font:not(.ng-hide)';
            list_price = table_data.find_elements(By.CSS_SELECTOR, list_price_selector)[0].text
            print('aşin 6', list_price)
            tax_included_price_selector = 'tr:nth-child(' + str(i + 1) + ') td:nth-child(10) span span:not(.ng-hide)'
            tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text
            print('aşin 7',  tax_included_price)
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


            # if (self.driver.current_url != searchURL):
            #     self.driver.get(mainURL)
                
            try:
                await self.loginArsalOtoUser(usr_value, pw_value)
            except:
                self.searchArsalOtoPart()
                # time.sleep(3)

                # GO TO SEARCH PAGE
                # self.driver.get(searchURL)
                # WebDriverWait(self.driver, 500).until(expected_conditions.visibility_of_element_located((By.ID, "searchbar")))

    def searchArsalOtoPart(self):
        time.sleep(2)
        # SEARCH PART
        searchbar = self.driver.find_element(By.ID, "searchbar")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        
        # WAIT FOR DOM TO LOAD
        # time.sleep(5)
    
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-table")))
    
    def extractArsalOtoPartData(self, data3):
        time.sleep(4.5)
        # GET ROW COUNT 
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".place-self-center .p-datatable-tbody tr")
    
        row_count = len(dom_elements);

        table_data = self.driver.find_element(By.CSS_SELECTOR, ".place-self-center")

        print('create arsal data')
        for i in range(row_count):
            brand_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(3) span';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[1].text
            

            oem_no_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(5)';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

            product_name_selector =  '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(3) span';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

            manufacturer_code = "-"
            desc = '-'
            content = '-'
            car_type = '-'
            engine_type = '-'
            list_price = "-"

            tax_included_price_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(8)'
            tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text

            stock_selector = '.table-products tbody:nth-of-type(2) tr:nth-child(' + str(i + 1) + ') td:nth-child(11)';

            try:
                if (table_data.find_element(By.CSS_SELECTOR, '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(7) img[alt*="Var"]')):
                    stock = 'VAR'
                if (table_data.find_element(By.CSS_SELECTOR, '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(7) svg.fill-blue-500')):
                    stock = "YOLDA"
            except:
                stock = 'YOK'

            values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
            data3.extend(values)

        return data3;

    # def checkIfPartExistsArsalOto(self, data3):
    #     WebDriverWait(self.driver, 4).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-emptymessage")))
    #     result_message = self.driver.find_element(By.CSS_SELECTOR, ".p-datatable-emptymessage div")
    #     if (alert_text in result_text):
    #         no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
    #         data6.extend(no_record)
        
    #         return data6, False;

    #     return data6, True;
    
    async def arsalOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data3 = self.getArsalOtoVariables()

        is_tab_active = self.checkIfTabActive(2)

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
        print('login started')
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

        print('login ended')
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



        print('create basbug data')
        # CREATE PARTS DATA
        for i in range(row_count):
            print(i)
            brand_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(1)';
            brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text
            print("basbug 1")

            oem_no_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(3)';
            oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text


            print("basbug 2")
            product_name_selector =  'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(6)';
            product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

            print("basbug 3")
            manufacturer_code = "-"
            desc = '-'
            content = '-'

            car_type_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(8)'
            car_type = table_data.find_elements(By.CSS_SELECTOR, car_type_selector)[0].text
            
            print("basbug 4")
            engine_type_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(8)'
            engine_type = table_data.find_elements(By.CSS_SELECTOR, engine_type_selector)[0].text
            
            print("basbug 5")
            list_price_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(11)'
            list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text

            print("basbug 6")
            tax_included_price_selector = 'table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(12)'
            # tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text
            original_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].get_attribute("data-original-title")
            price_value = original_price[original_price.find(':')+1 : original_price.find('TL')]
            tax_included_price =  price_value + 'TL'

            print("basbug 7")
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

            print("basbug 8")
            
            values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
            data4.extend(values)
    

        return data4;


    async def basbugOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data4 = self.getBasbugOtoVariables()
    
        is_tab_active = self.checkIfTabActive(3)

        if (is_tab_active):
            print('is basbug tab active', is_tab_active)
            self.searchBasbugOtoPart(searchURL)
        else:
            await self.runTabControlProcessBasbugOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)
            
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#grAramaSonuc-body table[id^='tableview']")


            print('basbug try 2')
            data4 = self.extractBasbugOtoPartData(data4)

            return data4;

        except:
            print('no record basbug')
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data4.extend(no_record)  
            return data4;  

    
       

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

            # if (searchURL not in self.driver.current_url):

                # self.driver.get(mainURL)
                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            try:
                await self.loginBorusanOtoUser(usr_value, pw_value, searchURL)

                # self.driver.get(searchURL)
            except:
                WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, "divCartBlockPartial")))
                # self.driver.get(searchURL)

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
        brand_selector = '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(2)';
        brand = self.driver.find_elements(By.CSS_SELECTOR, brand_selector)[0].text

        oem_no_selector = '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(2)';
        oem_no = self.driver.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

        product_name_selector =  '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(4)';
        product_name = self.driver.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text


        manufacturer_code = "-"
        desc = '-'
        content = '-'
        car_type  = '-'
        engine_type  = '-'

        
        list_price_selector = '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(4)'
        list_price = self.driver.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text

        tax_included_price_selector = '#divItemResult table tbody tr:nth-of-type(4) td:nth-of-type(4)'
        tax_included_price_value = self.driver.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text
        tax_included_price = "₺" + tax_included_price_value

        # in_stock_selector = '#grAramaSonuc-body table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="green"]';
        # on_the_way_stock_selector = '#grAramaSonuc-body table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="pink"]'
        
        stock_selector = '#divItemResult table tbody tr:nth-of-type(3) td:nth-of-type(2)';
        stock = self.driver.find_elements(By.CSS_SELECTOR, stock_selector)[0].text

        values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
        data5.extend(values)
        return data5;

    async def borusanOtoSearch(self):
        mainURL, searchURL, usr_value, pw_value, data5 = self.getBorusanOtoVariables();

        is_tab_active = self.checkIfTabActive(4)

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
        
       
    def getMercanlarOtoVariables(self):
        mainURL = 'https://b2b.mercanlar.com/'
        searchURL = 'https://b2b.mercanlar.com/Home'
        usr_value = 'mcobanoglu7@hotmail.com'
        pw_value = 'Coban1'
        data6 = ['','','','','','MERCANLAR OTO','','','','']

        return mainURL, searchURL, usr_value, pw_value, data6;
    
    async def runTabControlProcessMercanlarOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):

            self.driver.execute_script("window.open('about:blank', 'mercanlaroto');")
            self.driver.switch_to.window("mercanlaroto")
            self.driver.get(mainURL)

            # if (searchURL not in self.driver.current_url):
            #     self.driver.get(mainURL)
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
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)  
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        print('mercanlar search ended')
        # time.sleep(3)

        # # WAIT FOR DOM TO LOAD
        # WebDriverWait(self.driver, 1000).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "result-container")))

    def checkIfPartExistsMercanlarOto(self, data6):
        WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        result_text = self.driver.find_element(By.CSS_SELECTOR, ".result-container").text
        alert_text = 'önermek'
        if (alert_text in result_text):
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data6.extend(no_record)
        
            return data6, False;

        return data6, True;

    def extractMercanlarOtoPartData(self, data6):
        ignored_exceptions=(StaleElementReferenceException)
        time.sleep(2.5)
        WebDriverWait(self.driver, 100, ignored_exceptions).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        dom_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-item-wrapper")
        row_count = len(dom_elements);

        table_data = self.driver.find_element(By.CSS_SELECTOR, '.result-container')

        # time.sleep(4.5)

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

            
            list_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(1) .col-xs-4:nth-of-type(2) .value'
            list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text.strip()

            tax_included_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(2) .total-price'
            tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text.strip()
           
            # price_value = original_price[original_price.find(':')+1 : original_price.find('TL')]
            # tax_included_price =  price_value + 'TL'

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

        is_tab_active = self.checkIfTabActive(5)

        
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
        # if (not is_tab_active):
            self.driver.execute_script("window.open('about:blank', 'babacanoto');")
            self.driver.switch_to.window("babacanoto")
            self.driver.get(mainURL)

            # if (searchURL not in self.driver.current_url):
                # self.driver.get(mainURL)

                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            time.sleep(1.5)
            try:
                await self.loginBabacanOtoUser(cst_value, usr_value, pw_value, searchURL)
                
            
            except:
                # search_button = self.driver.find_element(By.CSS_SELECTOR, '.has-sub.m-img-search a') 
                # search_button.click()
                self.searchBabacanOtoPart(searchURL)
                # self.driver.get(searchURL)

    def loginBabacanOtoUser(self, cst_value, usr_value, pw_value, searchURL):
        if (self.driver.find_element(By.ID, 'txtCustomerB2bCode')):
            customer_code = self.driver.find_element(By.ID, 'txtCustomerB2bCode') 
            user_code = self.driver.find_element(By.ID, 'txtCustomerUserCode') 
            password = self.driver.find_element(By.ID, 'txtCustomerPassword') 
            login_button = self.driver.find_element(By.ID, 'btnLogin') 
            # FILL DOM ELEMENTS
            customer_code.send_keys(cst_value)
            user_code.send_keys(usr_value)
            password.send_keys(pw_value)
            login_button.click();
            # self.driver.get(defaultURL)
            search_button = self.driver.find_element(By.CSS_SELECTOR, '.has-sub.m-img-search a') 
            search_button.click()

            self.searchBabacanOtoPart(searchURL)

    def searchBabacanOtoPart(self, searchURL):
        if (self.driver.current_url != searchURL):
            self.driver.get(searchURL)
        # GO TO SEARCH PAGE
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



            for i in range(row_count):
                print('babacan data', i)
                brand_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(5)';
                brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text
                

                oem_no = '-'

                product_name_selector =  '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(3)';
                product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text


                car_type_selector =  '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(4)';
                car_type = table_data.find_elements(By.CSS_SELECTOR, car_type_selector)[0].text

                desc = '-'
                content = '-'
                manufacturer_code = '-'
                engine_type = '-'
                tax_included_price = 'SİTEYE BAKINIZ'

                
                list_price_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(8)'
                list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text.strip()

            
                in_stock_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(6) img[src*="green"]';
                out_of_stock_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(6) img[src*="red"]';
            
                stock = None;
                try:
                    if (table_data.find_element(By.CSS_SELECTOR, in_stock_selector)):
                        stock = "VAR"
                except:
                    if (stock is None):
                        stock = "YOK"

                

                values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
                data7.extend(values)

            return data7;

    async def babacanOtoSearch(self):
        mainURL, searchURL, defaultURL, cst_value, usr_value, pw_value, data7 = self.getBabacanOtoVariables()

        is_tab_active = self.checkIfTabActive(6)

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

    
    def findStockValues(self, nums, nth):
        start_index = nth - 1
        return nums[start_index::nth]
    
    def findStockIndexes(self, stock_values):
        # check_value = "Var"
        np_array = np.array(stock_values)
        stock_indexes = np.where((np_array == 'Var') | (np_array == 'VAR'))

        return stock_indexes[0]
    
    def showLoader(self):
        self.loading_label = customtkinter.CTkLabel(master=self, text="Yükleniyor...")
        self.loading_label.place(relx=0.5, rely=0.5)
        self.loading_label.update_idletasks()
    
    def hideLoader(self):
        self.loading_label.place_forget()

    def hideTable(self):
        try:
            print(self.table)
            self.table.destroy()
            print('true')
        except:
            print('false')
            return False


    def searchPart(self, event):
        # self.hideTable()
        # self.showLoader()

        self.data = ["MARKA", "ÜRETİCİ KODU ", "OEM", "ÜRÜN ADI", "AÇIKLAMA", "ARAÇ TİPİ", "MOTOR TİPİ", "LİSTE FİYAT", "KDV'Lİ MALİYET", "STOK"]
        column_count = len(self.data)

        self.user_input = self.entry.get().strip();

        header_indexes = []

        data1 = run(self.genelOtoSearch()) 

        # data2 = run(self.motorAsinSearch()); 
        
        # data3 = run(self.arsalOtoSearch()); 

        # data4 = run(self.basbugOtoSearch()) 

        # data5 = run(self.borusanOtoSearch()) 
        
        # data6 = run(self.mercanlarOtoSearch()) 

        # data7 = run(self.babacanOtoSearch())

        print('GENEL OTO')
        print(data1)
        # print('MOTOR AŞİN')
        # print(data2)
        # print('ARSAL OTO')
        # print(data3)
        # print('BAŞBUĞ OTO')
        # print(data4)
        # print('BORUSAN OTO')
        # print(data5)
        # print('MERCANLAR OTO')
        # print(data6)
        # print('BABACAN OTO')
        # print(data7)

        # CTK destroy table widget
        # tksheet
       

        # 22116768800
        # 63117240248
        # 31306852158
        # 34411162005
        # 51117293030
        # 11417600466


        self.data += data1;
        header_indexes.append(1)

       
        # index2 = int(len(self.data) / 10);
        # header_indexes.append(index2)
        # self.data += data2;

        # index3 = int(len(self.data) / 10);
        # header_indexes.append(index3)
        # self.data += data3;


        # index4 = int(len(self.data) / 10);
        # header_indexes.append(index4)
        # self.data += data4;


        # index5 = int(len(self.data) / 10);
        # header_indexes.append(index5)
        # self.data += data5;


        # index6 = int(len(self.data) / 10);
        # header_indexes.append(index6)
        # self.data += data6;


        # index7 = int(len(self.data) / 10);
        # header_indexes.append(index7)
        # self.data += data7;

        print("data", self.data)


        
        stock_values = self.findStockValues(self.data, 10)
        stock_indexes = self.findStockIndexes(stock_values)

       
        # # ROW COUNT DİNAMİK YAPILACAK
        row_count = int(len(self.data) / 10);


        
        self.data = np.reshape(self.data, [row_count, column_count])
        self.data = list(self.data)

        # self.hideLoader()
        
        self.table = CTkTable(self, row=row_count, column=column_count, values=self.data, header_color="#90290a", font=('Calibri', 18))
        self.table.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="wens", padx=(0, 0), pady=(0, 0))




        for j in list(header_indexes):
            self.table.edit_row(j, font=(None, 25), fg_color="#202020")
        

        for i in list(stock_indexes):
            self.table.edit_row(i, fg_color="green")
            # self.table.select(i, 10).edit(fg_color="green")



if __name__ == "__main__":
    app = App()
    app.run()
    # app.mainloop()


  