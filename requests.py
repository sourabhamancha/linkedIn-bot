from selenium import webdriver
from time import sleep
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import date
from selenium.webdriver.common.keys import Keys

class LinkedInBot():
  
  def __init__(self):
    self.driver = webdriver.Chrome("/Users/sourabhamancha/Documents/Projects/linkedin_bot/chromedriver")
  
  def login(self, username, password):
    self.driver.get('https://www.linkedin.com/login') #Open LinkedIn login page
    self.username = username
    self.password = password

    sleep(2)

    email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
    email_in.send_keys(self.username)

    pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
    pw_in.send_keys(self.password)


    sign_in_btn = self.driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_btn.click()
    sleep(5)

    try:
      not_now_btn = self.driver.find_element_by_xpath('//*[@class="btn__secondary--large-muted"]')
      not_now_btn.click()
      sleep(5)
    except Exception:
      print("There is no 'Remember me' section this time!")
  
  def search(self, keyword):
    self.keyword = keyword
    self.driver.find_element_by_xpath('//*[@class="search-global-typeahead   global-nav__search-typeahead"]').click()
    search_input = self.driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
    search_input.send_keys(self.keyword)
    search_input.send_keys(Keys.ENTER) 
    sleep(5)
    self.driver.find_element_by_xpath('//*[@aria-label="People"]').click()

  def send_requests(self, num):
    total = 0
    while total <= num:
      count = 0
      while count <= 7:
        try: 
          sleep(2)
          self.driver.find_element_by_xpath('//*[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]').click()
          sleep(2)
          title = self.driver.find_element_by_xpath('//*[@id="send-invite-modal"]').text
          if title == "Connect":
            sleep(2)
            self.driver.find_element_by_xpath('//*[@aria-label="Dismiss"]').click()
            count = count + 7
            break
          sleep(2)
          self.driver.find_element_by_xpath('//*[@aria-label="Send now"]').click() 
          count = count + 1
          total = total + 1
          print("Total requests sent: {}".format(total))
        except Exception:
          print("Exception")
          count = count + 1
          continue
      sleep(2)
      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      sleep(2)
      next_button = self.driver.find_element_by_xpath('//*[@aria-label="Next"]')
      next_button.click()



bot = LinkedInBot()

# #Logging in to LinkedIn
bot.login(<username>, <password>)  #Provide LinkedIn username and password

# Searching for people
bot.search("recruiter at apple") # Provide the keyword for search

# Sending requests
bot.send_requests(10) # Provide the total requests to be sent as an attribute

bot.driver.quit()