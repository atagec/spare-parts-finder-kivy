import numpy as np
from asyncio import run

# kivy
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.button import Button

# Scraper
from scrapers import GenelOtoScraper, ArsalOtoScraper, BorusanOtoScraper, MercanlarOtoScraper, BabacanOtoScraper, MotorAsinScraper, BasbugOtoScraper


# BROWSER DRIVER IMPORTS
from browser_driver import BrowserDriver
browser_instance = BrowserDriver()
driver = browser_instance.driver


KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: [10, 10, 10, 10]  # left, top, right, bottom
    
    AnchorLayout:
        size_hint_y: None
        height: dp(60)
        padding: dp(10)
        
        BoxLayout:
            size_hint: None, None
            width: dp(300)
            height: dp(48)
            spacing: dp(10)
            
            MDTextField:
                id: search_field
                hint_text: "OEM No Giriniz"
                mode: "rectangle"
                size_hint: None, None
                width: dp(200)
                height: dp(48)
                on_text_validate: app.on_search_button_press()

            
            MDRectangleFlatButton:
                text: "ARA"
                size_hint: 1, 1
                width: dp(100)
                height: dp(48)
                font_size: "20sp"
                md_bg_color: "#0054ac"
                line_color: "#0054ac"
                text_color: 1, 1, 1, 1
                on_release: app.on_search_button_press()


    BoxLayout:
        id: data_layout
        orientation: 'vertical'
        size_hint: 1, 1
        height: dp(60)
    
    BoxLayout:
        MDLabel:
            id: placeholder
            text: "OEM No Giriniz"
            font_size: "20sp"
            halign: "center"

'''


class App(MDApp):
    def __init__(self):
        super().__init__()

    def build(self):
        # Old layout
        # # Create the input field
        # self.layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # # Create the input field layout
        # input_layout = MDBoxLayout( orientation='horizontal',size_hint=(None, None), width=200, height="40dp")

        # # Create the input field
        # self.input_field = MDTextField(
        #     hint_text="OEM No",
        #     size_hint_x=None,
        #     width=input_layout.width
        # )

        # # Create table placeholder field
        # self.table_placeholder = Button(text='OEM NO Giriniz', color="black", size_hint=(1, 1), background_color="#c5d5c500")
        # # Create the submit button
        # submit_button = MDRectangleFlatIconButton(
        #     text="ARA",
        #     md_bg_color="blue",
        #     text_color= "white",
        #     line_color= "blue"
        # )

        # submit_button.bind(on_release=self.searchPart)

        # input_layout.add_widget(self.input_field)
        # input_layout.add_widget(submit_button)

        # self.layout.add_widget(input_layout)
        # self.layout.add_widget(self.table_placeholder)
        # # self.layout.add_widget(self.data_tables)
        # return self.layout

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        return Builder.load_string(KV)

    def on_search_button_press(self):
        self.searchPart(self.input_field.text)

    @property
    def input_field(self):
        return self.root.ids.search_field

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

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
            return False

        for handle in all_handles:
            if handle != parent_handle:
                tab_id = all_handles[index]
                driver.switch_to.window(tab_id)
                return True
                break

    # ---- 1 ----#
    # GENEL OTO START
    # GENEL OTO END

    # ---- 2 ----#
    # MOTOR ASİN START
    # MOTOR ASİN END

    # ---- 3 ----#
    # ARSAL OTO START
    # ARSAL OTO END

    # ---- 4 ----#
    # BASBUG OTO START
    # BASBUG OTO END

    # ---- 5 ----#
    # BORUSAN OTO START
    # BORUSAN OTO END

    # ---- 6 ----#
    # MERCANLAR OTO START
    # MERCANLAR OTO END

    # ---- 7 ----#
    # BABACAN OTO START
    # BABACAN OTO END

    def findStockValues(self, nums, nth):
        start_index = nth - 1
        return nums[start_index::nth]

    def findStockIndexes(self, stock_values):
        # check_value = "Var"
        np_array = np.array(stock_values)
        stock_indexes = np.where((np_array == 'Var') | (np_array == 'VAR'))

        return stock_indexes[0]

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

    def hidePlaceholderText(self):
        # Hide the placeholder label
        placeholder = self.root.ids.placeholder
        placeholder.height = 0
        placeholder.opacity = 0
        # self.root.remove_widget(placeholder)

    def searchPart(self, event):
        # C
        # self.hideTable()

        # self.data = ["MARKA", "ÜRETİCİ KODU ", "OEM", "ÜRÜN ADI", "AÇIKLAMA", "ARAÇ TİPİ", "MOTOR TİPİ", "LİSTE FİYAT", "KDV'Lİ MALİYET", "STOK"]
        self.data = []

        column_count = 10

        self.user_input = self.input_field.text.strip()

        header_indexes = []

        # Scrapers start
        scraper1 = GenelOtoScraper(
            driver, self.user_input, self.checkIfTabActive)
        data1 = run(scraper1.genelOtoSearch())

        scraper3 = ArsalOtoScraper(driver, self.user_input, self.checkIfTabActive)
        data3 = run(scraper3.arsalOtoSearch())

        scraper5 = BorusanOtoScraper(driver, self.user_input, self.checkIfTabActive)
        data5 = run(scraper5.borusanOtoSearch())

        scraper6 = MercanlarOtoScraper(driver, self.user_input, self.checkIfTabActive)
        data6 = run(scraper6.mercanlarOtoSearch())

        scraper7 = BabacanOtoScraper(driver, self.user_input, self.checkIfTabActive)
        data7 = run(scraper7.babacanOtoSearch())

        # scraper2 = MotorAsinScraper(driver, self.user_input, self.checkIfTabActive)
        # data2 = run(scraper2.motorAsinSearch())

        # scraper4 = BasbugOtoScraper(driver, self.user_input, self.checkIfTabActive)
        # data4 = run(scraper4.basbugOtoSearch())

        # Scrapers end

        # data1 = run(self.genelOtoSearch())

        # data2 = run(self.motorAsinSearch());

        # data3 = run(self.arsalOtoSearch());

        # data4 = run(self.basbugOtoSearch())

        # data5 = run(self.borusanOtoSearch())

        # data6 = run(self.mercanlarOtoSearch())

        # data7 = run(self.babacanOtoSearch())

        # print('MOTOR AŞİN')
        # print(data2)

        # print('BAŞBUĞ OTO')
        # print(data4)

        print('GENEL OTO')
        print(data1)

        print('ARSAL OTO')
        print(data3)

        print('BORUSAN OTO')
        print(data5)

        print('MERCANLAR OTO')
        print(data6)

        print('BABACAN OTO')
        print(data7)

        # 22116768800
        # 63117240248
        # 31306852158
        # 34411162005
        # 51117293030
        # 11417600466

        # index2 = int(len(self.data) / 10);
        # header_indexes.append(index2)
        # self.data += data2;

        # index4 = int(len(self.data) / 10);
        # header_indexes.append(index4)
        # self.data += data4;

        self.data += data1
        header_indexes.append(1)

        index3 = int(len(self.data) / 10);
        header_indexes.append(index3)
        self.data += data3;

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

        # ROW COUNT DİNAMİK YAPILACAK
        row_count = int(len(self.data) / 10)

        self.data = np.reshape(self.data, [row_count, column_count])
        self.data = list(self.data)

        print('final data', self.data)

        self.hidePlaceholderText()

        self.data_tables = MDDataTable(
            use_pagination=True,
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
            rows_num=10,
            size_hint_y=1,
            # C
        )

        # Calculate height dynamically
        # data_height = row_count * 48  # Assuming each row is 48dp high
        # self.data_tables.height = data_height

        # Add the MDDataTable to the layout
        data_layout = self.root.ids.data_layout
        data_layout.clear_widgets()
        data_layout.add_widget(self.data_tables)

        # C
        # self.layout.add_widget(self.data_tables)


if __name__ == "__main__":
    app = App()
    app.run()
