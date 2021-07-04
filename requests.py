# MARK:- weBDriver
from selenium import webdriver
# MARK:- Time
from time import sleep
from selenium.webdriver.common.keys import Keys

# MARK:- Credential manger
from Cred import Cred


class LinkedInBotMain:
    # MARK:- Username and password for linked in account 
    username = "nan"
    password = "nan"
    requestCnt = 10
    sleepCnt2Second = 2
    sleepCnt5Second = 5

    def __init__(self):
        self.driver = webdriver.Firefox()

    # MARK:- login and open account page

    def login(self, username, password):
        self.driver.get('https://www.linkedin.com/login')  # Open LinkedIn login page
        self.username = username
        self.password = password

        sleep(self.sleepCnt2Second)

        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys(self.username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys(self.password)

        sign_in_btn = self.driver.find_element_by_xpath('//*[@type="submit"]')
        sign_in_btn.click()
        sleep(self.sleepCnt5Second)

        try:
            not_now_btn = self.driver.find_element_by_xpath('//*[@class="btn__secondary--large-muted"]')
            not_now_btn.click()
            sleep(self.sleepCnt5Second)
        except Exception:
            print("There is no 'Remember me' section this time!")

    # MARK:- search for what ever

    def search(self, keyword):
        self.keyword = keyword 
        self.driver.find_element_by_xpath(
            '//*[@class="search-global-typeahead   global-nav__search-typeahead"]').click()
        search_input = self.driver.find_element_by_xpath(
            '//*[@class="search-global-typeahead__input always-show-placeholder"]')
        search_input.send_keys(self.keyword)
        search_input.send_keys(Keys.ENTER)
        sleep(self.sleepCnt5Second)
        self.driver.find_element_by_xpath('//*[@aria-label="People"]').click()

    # MARK:- send requests to what ever you want

    def send_requests(self):
        num = self.requestCnt
        total = 0
        while total <= num:
            count = 0
            while count <= 7:
                try:
                    sleep(self.sleepCnt2Second)
                    self.driver.find_element_by_xpath(
                        '//*[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]').click()
                    sleep(self.sleepCnt2Second)
                    title = self.driver.find_element_by_xpath('//*[@id="send-invite-modal"]').text
                    if title == "Connect":
                        sleep(self.sleepCnt2Second)
                        self.driver.find_element_by_xpath('//*[@aria-label="Dismiss"]').click()
                        count = count + 7
                        break
                    sleep(self.sleepCnt2Second)
                    self.driver.find_element_by_xpath('//*[@aria-label="Send now"]').click()
                    count = count + 1
                    total = total + 1
                    print("Total requests sent: {}".format(total))
                except Exception as exc:
                    print("Exception", exc.__str__())
                    count = count + 1
                    continue
            sleep(self.sleepCnt2Second)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(self.sleepCnt2Second)
            next_button = self.driver.find_element_by_xpath('//*[@aria-label="Next"]')
            next_button.click()


bot = LinkedInBotMain()
# #Logging in to LinkedIn
bot.login(Cred.getuser_name(), Cred.getuser_password())  # Provide LinkedIn username and password
# Searching for people
bot.search("recruiter ")  # Provide the keyword for search
# Sending requests
bot.send_requests()  # Provide the total requests to be sent as an attribute
bot.driver.quit()
