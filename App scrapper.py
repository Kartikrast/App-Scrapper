import re
import time
import numpy as np
import pandas as pd
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By


class Instagram_data:

    def __init__(self, version, adb_name, target, searchtag):
        self.user_names = None
        self.followers = None
        self.following = None
        self.email = None
        self.ph_number = None
        self.post = None
        self.version = version
        self.adb_name = adb_name
        self.target = target
        self.searchtag = searchtag
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': str(self.adb_name),  # Replace with your device name
            'udid': str(self.adb_name),  # Replace with your device UDID
            'platformVersion': str(self.version),  # Replace with your Android version (e.g., 11)
            'appPackage': 'com.instagram.android',
            'appActivity': '.activity.MainTabActivity',
            'automationName': 'UiAutomator2',  # Use UiAutomator2 for Android
            'noReset': True,  # Keeps the app data between sessions
            'newCommandTimeout': 6000,  # Timeout for new commands to the server
            'adbExecTimeout': 20000,  # Timeout for ADB commands (adjust as needed)
            'autoGrantPermissions': True,  # Grant necessary permissions automatically
            'disableWindowAnimation': True,  # Disable window animations for faster test execution
            'unicodeKeyboard': True,  # Enable Unicode input (if needed)
            'resetKeyboard': True,  # Reset keyboard after test (if needed)
            "appium:ensureWebviewsHavePages": True
        }
        options = UiAutomator2Options().load_capabilities(caps=desired_caps)
        return webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)

    def search(self):
        search_button = self.driver.find_element(By.XPATH,
                                                 '(//android.widget.ImageView[@resource-id="com.instagram.android:id/tab_icon"])[3]')
        search_button.click()
        time.sleep(2)
        box_button = self.driver.find_element(By.XPATH,
                                              '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/action_bar_textview_custom_title_container"]')
        box_button.click()
        search_box = self.driver.find_element(By.XPATH,
                                              '//android.widget.EditText[@resource-id="com.instagram.android:id/action_bar_search_edit_text"]')
        search_box.send_keys(self.searchtag)
        time.sleep(1)
        search_box.click()
        time.sleep(2)
        first_result = self.driver.find_element(By.XPATH,
                                                f"//android.widget.TextView[@content-desc='{self.searchtag}']")
        first_result.click()
        time.sleep(2)

    def swipe(self):
        screen_size = self.driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']
        start_x = screen_width // 2
        start_y = int(screen_height * 0.9)  # Start swipe from 90% of the screen height
        end_x = screen_width // 2
        end_y = int(screen_height * 0.1)
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)

    def extractor(self):
        self.user_names = []
        self.followers = []
        self.following = []
        self.post = []
        self.email = []
        self.ph_number = []
        self.search()
        time.sleep(2)
        try:
            posts = self.driver.find_elements(by='id', value='com.instagram.android:id/image_button')
            while len(self.user_names) < self.target:
                for i in range(5):
                    posts = self.driver.find_elements(by='id', value='com.instagram.android:id/image_button')
                    posts[i].click()
                    try:
                        account = self.driver.find_element(by='id',
                                                           value='com.instagram.android:id/row_feed_photo_profile_name')
                        account.click()
                        user_name = self.driver.find_element(by='id',
                                                             value='com.instagram.android:id/action_bar_title').text

                        if user_name in self.user_names:
                            self.driver.back()
                            self.driver.back()
                            continue
                        else:
                            self.user_names.append(user_name)
                        self.followers.append(self.driver.find_element(by='id',
                                                                       value='com.instagram.android:id/row_profile_header_textview_followers_count').text)
                        self.following.append(self.driver.find_element(by='id',
                                                                       value='com.instagram.android:id/row_profile_header_textview_following_count').text)
                        try:
                            contact_button = self.driver.find_element(By.XPATH,
                                                                      "//android.widget.TextView[@text='Contact']")
                            contact_button.click()
                            contacts = self.driver.find_elements(by='id',
                                                                 value='com.instagram.android:id/contact_option_sub_text')
                            email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
                            phone_pattern = re.compile(r'^\+1[\d -]{10,}$')
                            email_id = []
                            p_num = []
                            for contact in contacts:
                                text = contact.text
                                if email_pattern.match(text):
                                    email_id.append(text)
                                    self.email.append(text)
                                elif phone_pattern.match(text):
                                    p_num.append(text)
                                    self.ph_number.append(text)
                                else:
                                    continue
                            if len(email_id) == 0:
                                self.email.append(np.nan)
                            if len(p_num) == 0:
                                self.ph_number.append(np.nan)
                        except:
                            message_button = self.driver.find_element(By.XPATH,
                                                                      '//android.widget.Button[@content-desc="Message"]')
                            message_button.click()
                            self.email.append(np.nan)
                        self.driver.back()
                        self.driver.back()
                        self.driver.back()
                        time.sleep(1)
                    except:
                        self.driver.back()
                self.swipe()
                self.swipe()
                self.swipe()
                time.sleep(1)
        except:
            print('Scrapping Completed')

    def dataframe(self):
        self.extractor()
        if self.searchtag in self.user_names:
            index = self.user_names.index(self.searchtag)
            del (self.user_names[index])
        data = pd.DataFrame({
            'Usernames': self.user_names,
            'Followers': self.followers,
            'Following': self.following,
            'Email': self.email,
        })
        data.to_excel('leads.xlsx', index=False)
        self.driver.quit()