from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from functools import cached_property

class BrowserDriver:
    @cached_property
    def driver(self):
        firefox_options = Options();
        firefox_options.add_argument("-profile")
        # CEYHUN
        user_profile_name = "User"
        firefox_options.add_argument("C:/Users/"+ user_profile_name + "/AppData/Roaming/Mozilla/Firefox/Profiles/searchpartuser")
        # ÇOBANOĞLU
        # user_profile_name = "Çobanoğlu"
        # firefox_options.add_argument("C:/Users/"+ user_profile_name + "/AppData/Roaming/Mozilla/Firefox/Profiles/cobanoglu")
       

        return webdriver.Firefox(service=Service('./geckodriver.exe'), options=firefox_options)