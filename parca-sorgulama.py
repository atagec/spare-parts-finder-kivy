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
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.button import Button






# https://www.youtube.com/watch?v=dVVPOPuPPc0


# BROWSER DRIVER IMPORTS
from browser_driver import BrowserDriver
browser_instance = BrowserDriver()
driver = browser_instance.driver



class App(MDApp):
    def __init__(self):
        super().__init__()
    def build(self):
        # Create the input field
        self.layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))


        # Create the input field layout
        input_layout = MDBoxLayout( orientation='horizontal',size_hint=(None, None), width=200, height="40dp")

  
        # input_layout.add_widget(MDBoxLayout(size_hint_x=None, width=1))
        # Create the input field
        self.input_field = MDTextField(
            hint_text="OEM No",
            size_hint_x=None,
            width=input_layout.width
        )

        # Create table placeholder field
        self.table_placeholder = Button(text='OEM NO Giriniz', color="black", size_hint=(1, 1), background_color="#c5d5c500")
        # Create the input field
        # self.input_field = MDTextField(
        #     hint_text="Enter data",
        #     size_hint_y=None,
        #     width=200,
        #     height="40dp"
        # )

        # Create the submit button
        submit_button = MDRectangleFlatIconButton(
            text="ARA",
            md_bg_color="blue",
            text_color= "white",
            line_color= "blue"
        )

        submit_button.bind(on_release=self.searchPart)


        input_layout.add_widget(self.input_field)
        input_layout.add_widget(submit_button)

        
        
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
        # self.data_tables.bind(on_row_press=self.on_row_press)
        # self.data_tables.bind(on_check_press=self.on_check_press)
        # screen = MDScreen()
        # screen.add_widget(input_field)
        # screen.add_widget(self.data_tables)
        self.layout.add_widget(input_layout)
        self.layout.add_widget(self.table_placeholder)
        # self.layout.add_widget(self.data_tables)
        return self.layout

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
            driver.get(mainURL)
            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.ID, "CustomerCode")))
                if (driver.find_element(By.ID, "CustomerCode")):
                    await self.loginGenelOtoUser(customer_code_value, user_code_value, password_value, searchURL)    
            except:
                self.searchGenelOtoPart(searchURL)
     
    

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
        WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "txtUserName")))
        username = driver.find_element(By.CLASS_NAME, "txtUserName") 
        password = driver.find_element(By.CLASS_NAME, "txtPassword") 
        login_button = driver.find_element(By.ID, 'login')
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
       
        login_button.click();
    
        self.searchMotorAsinPart()


    async def runTabControlProcessMotorAsin(self, is_tab_active, mainURL,  usr_value, pw_value):
            driver.execute_script("window.open('about:blank', 'motorasin');")
            driver.switch_to.window("motorasin")
            driver.get(mainURL)

            # if ('search' not in driver.current_url):
            # LOGGED IN KONTROLÜ EKLENECEK
            # GET DOM ELEMENTS
            try:
                await self.loginMotorAsinUser(usr_value, pw_value)
            except:
                self.searchMotorAsinPart()
    


    def searchMotorAsinPart(self):
        print('aşin search started')
        WebDriverWait(driver, 400).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".td-item.td-product")))
        # WebDriverWait(driver, 400).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="text"].searchInput')))
        print('aşin search middle')
        driver.find_element(By.CSS_SELECTOR, ".td-item.td-product")
        oem_search = driver.find_element(By.CLASS_NAME, "searchInput")
        oem_search.send_keys(Keys.CONTROL + "a")
        oem_search.send_keys(Keys.DELETE)   
        oem_search.send_keys(self.user_input)
        oem_search.send_keys(Keys.ENTER)

        print('aşin search ended')

    def extractMotorAsinPartData(self, data2):
        # time.sleep(3.5)
        WebDriverWait(driver, 300).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")))
        # WebDriverWait(driver, 4000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "mark")))
        # alert = driver.find_element(By.CSS_SELECTOR, '.table-products tbody:nth-of-type(2) > tr td')
        
        dom_elements = driver.find_elements(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2) > tr")

        table_data = driver.find_element(By.CSS_SELECTOR, ".table-products tbody:nth-of-type(2)")
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
                driver.find_element(By.CSS_SELECTOR, '.table-products tbody:nth-of-type(2) > tr')
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
        WebDriverWait(driver, 2000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.inputfrm[type="text"]')))
        # GET DOM ELEMENTS
        username = driver.find_element(By.CSS_SELECTOR, '.inputfrm[type="text"]') 
        password = driver.find_element(By.CSS_SELECTOR, '.inputfrm[type="password"]') 
        login_button = driver.find_element(By.ID, 'login_button') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        login_button.click();
    
        self.searchArsalOtoPart()

    async def runTabControlProcessArsalOto(self, is_tab_active, mainURL, searchURL, usr_value, pw_value):
            driver.execute_script("window.open('about:blank', 'arsaloto');")
            driver.switch_to.window("arsaloto")
            driver.get(mainURL)


            # if (driver.current_url != searchURL):
            #     driver.get(mainURL)
                
            try:
                await self.loginArsalOtoUser(usr_value, pw_value)
            except:
                self.searchArsalOtoPart()
                # time.sleep(3)

                # GO TO SEARCH PAGE
                # driver.get(searchURL)
                # WebDriverWait(driver, 500).until(expected_conditions.visibility_of_element_located((By.ID, "searchbar")))

    def searchArsalOtoPart(self):
        time.sleep(2)
        # SEARCH PART
        searchbar = driver.find_element(By.ID, "searchbar")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        
        # WAIT FOR DOM TO LOAD
        # time.sleep(5)
    
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-table")))
    
    def extractArsalOtoPartData(self, data3):
        time.sleep(4.5)
        # GET ROW COUNT 
        dom_elements = driver.find_elements(By.CSS_SELECTOR, ".place-self-center .p-datatable-tbody tr")
    
        row_count = len(dom_elements);

        table_data = driver.find_element(By.CSS_SELECTOR, ".place-self-center")

        # print('create arsal data')
        # for i in range(row_count):
        #     brand_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(3) span';
        #     brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[1].text
            

        #     oem_no_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(5)';
        #     oem_no = table_data.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

        #     product_name_selector =  '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(3) span';
        #     product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text

        #     manufacturer_code = "-"
        #     desc = '-'
        #     car_type = '-'
        #     engine_type = '-'
        #     list_price = "-"

        #     tax_included_price_selector = '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(8)'
        #     tax_included_price = table_data.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text


        #     try:
        #         if (table_data.find_element(By.CSS_SELECTOR, '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(7) img[alt*="Var"]')):
        #             stock = 'VAR'
        #         if (table_data.find_element(By.CSS_SELECTOR, '.p-datatable-tbody tr:nth-of-type(' +  str(i + 1)  +') td:nth-of-type(7) svg.fill-blue-500')):
        #             stock = "YOLDA"
        #     except:
        #         stock = 'YOK'

        #     values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
        #     data3.extend(values)

        # return data3;
        print('create arsal data')
        for i in range(row_count):
                row_selector = f'.p-datatable-tbody tr:nth-of-type({i + 1})'

                brand = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(3) span')[1].text
                oem_no = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(5)')[0].text
                product_name = table_data.find_elements(By.CSS_SELECTOR, f'{row_selector} td:nth-of-type(3) span')[0].text

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
            WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".p-datatable-emptymessage")))
            alert = driver.find_element(By.CSS_SELECTOR, '.p-datatable-emptymessage')
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
            
            driver.execute_script("window.open('about:blank', 'basbugoto');")
            driver.switch_to.window("basbugoto")
            driver.get(mainURL)

            try:
                await self.loginBasbugOtoUser(searchURL, usr_value, pw_value)
            except:
                self.searchBasbugOtoPart(searchURL)

    async def loginBasbugOtoUser(self, searchURL, usr_value, pw_value):
        # LOGGED IN KONTROLÜ EKLENECEK
        # GET DOM ELEMENTS
        print('login started')
        WebDriverWait(driver, 6).until(expected_conditions.visibility_of_element_located((By.ID, 'KullaniciAd')))
        time.sleep(0.5)
        username = driver.find_element(By.ID, 'KullaniciAd') 
        password = driver.find_element(By.ID, 'Sifre') 
        login_button = driver.find_element(By.CSS_SELECTOR, 'form .btn.style-danger.btn-raised') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        # password.send_keys("GENELOTO")
        login_button.click();

        print('login ended')
        self.searchBasbugOtoPart(searchURL)
    
    def searchBasbugOtoPart(self, searchURL):
        if (driver.current_url != searchURL):
            driver.get(searchURL)
        # SEARCH PART
        print('basbug search started')
        WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, "txtTumundeAra")))
        searchbar = driver.find_element(By.ID, "txtTumundeAra")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        # WAIT FOR DOM TO LOAD
        time.sleep(2)
        print('basbug search ended')

    def extractBasbugOtoPartData(self, data4):
         # GET ROW COUNT 
        dom_elements = driver.find_elements(By.CSS_SELECTOR, "#grAramaSonuc-body table[id^='tableview']")
        row_count = len(dom_elements);

        table_data = driver.find_element(By.CSS_SELECTOR, '#grAramaSonuc-body')



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
    
        is_tab_active = self.checkIfTabActive(1)

        if (is_tab_active):
            print('is basbug tab active', is_tab_active)
            self.searchBasbugOtoPart(searchURL)
        else:
            await self.runTabControlProcessBasbugOto(is_tab_active, mainURL, searchURL, usr_value, pw_value)
            
        try:
            driver.find_element(By.CSS_SELECTOR, "#grAramaSonuc-body table[id^='tableview']")


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

            driver.execute_script("window.open('about:blank', 'borusanoto');")
            driver.switch_to.window("borusanoto")
            driver.get(mainURL)

            # if (searchURL not in driver.current_url):

                # driver.get(mainURL)
                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            try:
                await self.loginBorusanOtoUser(usr_value, pw_value, searchURL)

                # driver.get(searchURL)
            except:
                WebDriverWait(driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, "divCartBlockPartial")))
                # driver.get(searchURL)

                self.searchBorusanOtoPart(searchURL)

    def loginBorusanOtoUser(self, usr_value, pw_value, searchURL):
        WebDriverWait(driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, 'UserName')))
        username = driver.find_element(By.ID, 'UserName') 
        password = driver.find_element(By.ID, 'Password') 
        login_button = driver.find_element(By.ID, 'btnLogon') 
        # FILL DOM ELEMENTS
        username.send_keys(usr_value)
        password.send_keys(pw_value)
        login_button.click();

        time.sleep(1.25)

    
        self.searchBorusanOtoPart(searchURL)
    
    def searchBorusanOtoPart(self, searchURL):
        if (driver.current_url != searchURL):
            driver.get(searchURL)
        
         # GO TO SEARCH PAGE
        WebDriverWait(driver, 750).until(expected_conditions.visibility_of_element_located((By.ID, "ItemNo_I")))
        # SEARCH PART
        searchbar = driver.find_element(By.ID, "ItemNo_I")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

    def checkIfPartExistsBorusanOto(self, data5):
        result_text = driver.find_element(By.CSS_SELECTOR, "#divItemResult tbody").text
        alert_text = 'tanımlı değil'
        if (alert_text in result_text):
            no_record = ['','','','','','KAYIT BULUNAMADI','','','','']
            data5.extend(no_record)
        
            return data5, False;
        
        return data5, True;


    def extractBorusanOtoPartData(self, data5):
           # in_stock_selector = '#grAramaSonuc-body table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="green"]';
        # on_the_way_stock_selector = '#grAramaSonuc-body table[id^="tableview"]:nth-of-type(' + str( i + 1 ) +') td:nth-of-type(15) img[src*="pink"]'
        manufacturer_code = "-"
        desc = '-'
        car_type  = '-'
        engine_type  = '-'

        # brand_selector = '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(2)';
        # brand = driver.find_elements(By.CSS_SELECTOR, brand_selector)[0].text

        # oem_no_selector = '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(2)';
        # oem_no = driver.find_elements(By.CSS_SELECTOR, oem_no_selector)[0].text

        # product_name_selector =  '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(4)';
        # product_name = driver.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text     

        
        # list_price_selector = '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(4)'
        # list_price = driver.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text

        # tax_included_price_selector = '#divItemResult table tbody tr:nth-of-type(4) td:nth-of-type(4)'
        # tax_included_price_value = driver.find_elements(By.CSS_SELECTOR, tax_included_price_selector)[0].text
        # tax_included_price = "₺" + tax_included_price_value

     
        
        # stock_selector = '#divItemResult table tbody tr:nth-of-type(3) td:nth-of-type(2)';
        # stock = driver.find_elements(By.CSS_SELECTOR, stock_selector)[0].text

        # values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
        # data5.extend(values)
        # return data5;

        selectors = {
            "brand": '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(2)',
            "oem_no": '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(2)',
            "product_name": '#divItemResult table tbody tr:nth-of-type(1) td:nth-of-type(4)',
            "list_price": '#divItemResult table tbody tr:nth-of-type(2) td:nth-of-type(4)',
            "tax_included_price_value": '#divItemResult table tbody tr:nth-of-type(4) td:nth-of-type(4)',
            "stock": '#divItemResult table tbody tr:nth-of-type(3) td:nth-of-type(2)'
        }

        elements = driver.find_elements(By.CSS_SELECTOR, ', '.join(selectors.values()))
       

        # brand = elements[0].text
        # oem_no = elements[1].text
        # product_name = elements[2].text
        # list_price = elements[3].text
        # tax_included_price_value = elements[4].text
        # stock = elements[5].text
        # tax_included_price = "₺" + tax_included_price_value


        # values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
        # data5.extend(values)

            # Create a dictionary mapping each selector to its corresponding element text
        result = {}
        for key, selector in selectors.items():
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
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
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "divItemResult")))
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
            print('mercanlar search trigger 1')
            driver.execute_script("window.open('about:blank', 'mercanlaroto');")
            driver.switch_to.window("mercanlaroto")
            driver.get(mainURL)

            # if (searchURL not in driver.current_url):
            #     driver.get(mainURL)
                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            
            if(driver.find_element(By.ID, 'LoginEmail')): 
                self.loginMercanlarOtoUser(usr_value, pw_value);
                return;
            print('mercanlar search trigger 2')
            self.searchMercanlarOtoPart()
    
    def loginMercanlarOtoUser(self, usr_value, pw_value):
       
            WebDriverWait(driver, 500).until(expected_conditions.visibility_of_element_located((By.ID, 'LoginEmail')))
            username = driver.find_element(By.ID, 'LoginEmail') 
            password = driver.find_element(By.ID, 'LoginPassword') 
            login_button = driver.find_element(By.CSS_SELECTOR, '.login-btn-container .btn.btn-green') 
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
        WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "footer-middle-inner")))
        # WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".img-responsive.center-block")))
        # SEARCH PART
        searchbar = driver.find_element(By.ID, "spare_part_number")
        print('searchbar', searchbar)
        input_value = searchbar.get_attribute("value")
        if (input_value):
            searchbar.send_keys(Keys.CONTROL + "a")
            searchbar.send_keys(Keys.DELETE)  
        searchbar.send_keys(self.user_input)
        searchbar.submit()
        # searchbar.send_keys(Keys.ENTER)

        # print('mercanlar search ended')
        # time.sleep(3)

        # # WAIT FOR DOM TO LOAD
        # WebDriverWait(driver, 1000).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "result-container")))

    def checkIfPartExistsMercanlarOto(self, data6):
        WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        result_text = driver.find_element(By.CSS_SELECTOR, ".result-container").text
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
        WebDriverWait(driver, 100, ignored_exceptions).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".result-container")))
        dom_elements = driver.find_elements(By.CSS_SELECTOR, ".product-item-wrapper")
        row_count = len(dom_elements);

        table_data = driver.find_element(By.CSS_SELECTOR, '.result-container')

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

            
            # list_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(1) .col-xs-4:nth-of-type(2) .value'
            list_price_selector = '.product-item-wrapper:nth-of-type(' + str( i + 1 ) +') .css-table .col:nth-of-type(6) .row:nth-of-type(1) .col-xs-4:nth-of-type(3) .value'
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

        # NEW SCRIPT
        # selectors = {
        #     "brand": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(3) .value",
        #     "oem_no": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(2) .value",
        #     "product_name": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(3) .thumb-list-item-group:nth-of-type(1) .value",
        #     "manufacturer_code": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(2) .thumb-list-item-group:nth-of-type(1) .value",
        #     "list_price": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(6) .row:nth-of-type(1) .col-xs-4:nth-of-type(3) .value",
        #     "tax_included_price": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(6) .row:nth-of-type(2) .total-price",
        #     "stock": ".product-item-wrapper:nth-of-type({}) .css-table .col:nth-of-type(5) .thumb-list-item-group .value:nth-of-type(2) ul span"
        # }


        # for i in range(row_count):
        #     values = []
        #     selector_list = [selector.format(i + 1) for selector in selectors.values()]
        #     combined_selector = "\n".join(selector_list)  # Join selectors with newline

        #     elements = table_data.find_elements(By.CSS_SELECTOR, combined_selector)
        #     for element, key in zip(elements, selectors):
        #         # Handle potential exceptions
        #         try:
        #             value = element.text.strip()
        #         except:
        #             value = "-"
        #         values.append(value)

        #     # Stock check using list comprehension and conditional expression
        #     stock_values = [span.get_attribute("class") for span in table_data.find_elements(By.CSS_SELECTOR, selectors["stock"].format(i + 1))]
        #     stock = "Yok"
        #     if any("in-stock" in stock_value for stock_value in stock_values):
        #         stock = "Var"

        #     values.append(stock)
        #     data6.extend(values)
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
            driver.execute_script("window.open('about:blank', 'babacanoto');")
            driver.switch_to.window("babacanoto")
            driver.get(mainURL)

            # if (searchURL not in driver.current_url):
                # driver.get(mainURL)

                # LOGGED IN KONTROLÜ EKLENECEK
                # GET DOM ELEMENTS
            # time.sleep(3)
            print('babacan 1')
            try:
                await self.loginBabacanOtoUser(cst_value, usr_value, pw_value, searchURL)
                
            
            except:
                print('babacan 2')
                # search_button = driver.find_element(By.CSS_SELECTOR, '.has-sub.m-img-search a') 
                # search_button.click()
                self.searchBabacanOtoPart(searchURL)
                # driver.get(searchURL)


    def clearInputFields(elements):
        for element in elements:
            try:
                element.clear()
            except Exception as e:
                print(f"Could not clear field: {e}")
    
    def loginBabacanOtoUser(self, cst_value, usr_value, pw_value, searchURL):
        time.sleep(4)
        if (driver.find_element(By.ID, 'txtCustomerB2bCode')):
        # if (WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, "txtCustomerB2bCode")))):
            customer_code = driver.find_element(By.ID, 'txtCustomerB2bCode') 
            user_code = driver.find_element(By.ID, 'txtCustomerUserCode') 
            password = driver.find_element(By.ID, 'txtCustomerPassword') 
            login_button = driver.find_element(By.ID, 'btnLogin') 
    
            customer_code.clear()
            user_code.clear()
            password.clear()
            # self.clearInputFields([customer_code, user_code, password])

            customer_code.send_keys(cst_value)
            user_code.send_keys(usr_value)
            password.send_keys(pw_value)
            login_button.click();
            # driver.get(defaultURL)
            search_button = driver.find_element(By.CSS_SELECTOR, '.has-sub.m-img-search a') 
            search_button.click()
            print('search babacan oto part')
            self.searchBabacanOtoPart(searchURL)

    def searchBabacanOtoPart(self, searchURL):
        if (driver.current_url != searchURL):
            driver.get(searchURL)
        # GO TO SEARCH PAGE
        print('search babacan oto part 2')
        WebDriverWait(driver, 1000).until(expected_conditions.visibility_of_element_located((By.ID, "txtGeneralSearch")))
        # SEARCH PART
        searchbar = driver.find_element(By.ID, "txtGeneralSearch")
        searchbar.send_keys(Keys.CONTROL + "a")
        searchbar.send_keys(Keys.DELETE)     
        searchbar.send_keys(self.user_input)
        searchbar.send_keys(Keys.ENTER)

        time.sleep(3)

    def extractBabacanOtoPartData(self, data7):
            print('extract babacan oto part')
            dom_elements = driver.find_elements(By.CSS_SELECTOR, "#gvResult .Row")
            row_count = len(dom_elements);

            table_data = driver.find_element(By.CSS_SELECTOR, "#gvResult")

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
    
            # ----------  



            # for i in range(row_count):
            #     brand_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(5)';
            #     brand = table_data.find_elements(By.CSS_SELECTOR, brand_selector)[0].text
                

            #     oem_no = '-'

            #     product_name_selector =  '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(3)';
            #     product_name = table_data.find_elements(By.CSS_SELECTOR, product_name_selector)[0].text


            #     car_type_selector =  '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(4)';
            #     car_type = table_data.find_elements(By.CSS_SELECTOR, car_type_selector)[0].text

            #     desc = '-'
            #     content = '-'
            #     manufacturer_code = '-'
            #     engine_type = '-'
            #     tax_included_price = 'SİTEYE BAKINIZ'

                
            #     list_price_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(8)'
            #     list_price = table_data.find_elements(By.CSS_SELECTOR,  list_price_selector)[0].text.strip()

            
            #     in_stock_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(6) img[src*="green"]';
            #     out_of_stock_selector = '.Row:nth-of-type('+ str( i + 1)  +') .Cell:nth-of-type(6) img[src*="red"]';
            
            #     stock = None;
            #     try:
            #         if (table_data.find_element(By.CSS_SELECTOR, in_stock_selector)):
            #             stock = "VAR"
            #     except:
            #         if (stock is None):
            #             stock = "YOK"

                

            #     values = [brand, manufacturer_code, oem_no, product_name, desc, car_type, engine_type, list_price, tax_included_price, stock]
            #     data7.extend(values)

            # return data7;

    async def babacanOtoSearch(self):
        mainURL, searchURL, defaultURL, cst_value, usr_value, pw_value, data7 = self.getBabacanOtoVariables()

        is_tab_active = self.checkIfTabActive(4)

        if (is_tab_active):
            self.searchBabacanOtoPart(searchURL)
        else:
            await self.runTabControlProcessBabacanOto(is_tab_active, mainURL, searchURL, cst_value, usr_value, pw_value)


        
        # time.sleep(4)

        try:
            if(driver.find_element(By.CSS_SELECTOR, '#gvResult .Row')):

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
            self.layout.remove_widget(self.data_tables)
            self.table.destroy()
            print('true')
        except:
            self.layout.remove_widget(self.table_placeholder)
            print('false')
            return False
        


    def searchPart(self, event):

        print('START')
        
        self.hideTable()
        # self.showLoader()

        # self.data = ["MARKA", "ÜRETİCİ KODU ", "OEM", "ÜRÜN ADI", "AÇIKLAMA", "ARAÇ TİPİ", "MOTOR TİPİ", "LİSTE FİYAT", "KDV'Lİ MALİYET", "STOK"]
        self.data = []

        column_count = 10;

        self.user_input = self.input_field.text.strip();

        header_indexes = []

        data1 = run(self.genelOtoSearch()) 

        # data2 = run(self.motorAsinSearch()); 
        
        data3 = run(self.arsalOtoSearch()); 

        # data4 = run(self.basbugOtoSearch()) 

        data5 = run(self.borusanOtoSearch()) 
        
        data6 = run(self.mercanlarOtoSearch()) 

        data7 = run(self.babacanOtoSearch())

        print('GENEL OTO')
        print(data1)
        # print('MOTOR AŞİN')
        # print(data2)
        print('ARSAL OTO')
        print(data3)
        # print('BAŞBUĞ OTO')
        # print(data4)
        print('BORUSAN OTO')
        print(data5)
        print('MERCANLAR OTO')
        print(data6)
        print('BABACAN OTO')
        print(data7)

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

        index3 = int(len(self.data) / 10);
        header_indexes.append(index3)
        self.data += data3;


        # index4 = int(len(self.data) / 10);
        # header_indexes.append(index4)
        # self.data += data4;


        index5 = int(len(self.data) / 10);
        header_indexes.append(index5)
        self.data += data5;


        index6 = int(len(self.data) / 10);
        header_indexes.append(index6)
        self.data += data6;


        index7 = int(len(self.data) / 10);
        header_indexes.append(index7)
        self.data += data7;

        print("data", self.data)


        
        stock_values = self.findStockValues(self.data, 10)
        stock_indexes = self.findStockIndexes(stock_values)

       
        # # ROW COUNT DİNAMİK YAPILACAK
        row_count = int(len(self.data) / 10);


        
        self.data = np.reshape(self.data, [row_count, column_count])
        self.data = list(self.data)

        print('final data', self.data)

        # self.hideLoader()

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
                ("KDV'Lİ MALİYET", dp(30), self.sort_on_team),
                ("STOK", dp(30), self.sort_on_team)
            ],
            row_data=self.data,
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
            rows_num=10
        )

        self.layout.add_widget(self.data_tables)
        
        # self.table = CTkTable(self, row=row_count, column=column_count, values=self.data, header_color="#90290a", font=('Calibri', 18))
        # self.table.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="wens", padx=(0, 0), pady=(0, 0))




        # for j in list(header_indexes):
        #     self.table.edit_row(j, font=(None, 25), fg_color="#202020")
        

        # for i in list(stock_indexes):
        #     self.table.edit_row(i, fg_color="green")



if __name__ == "__main__":
    app = App()
    app.run()
    # app.mainloop()


  