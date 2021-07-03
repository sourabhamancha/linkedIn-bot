from selenium import webdriver
from time import sleep
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import date


class LinkedInBot:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self, username, password):
        self.driver.get('https://www.linkedin.com/login')  # Open LinkedIn login page
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

    def nav_to_jobs(self):  # Navigates to the jobs page in LinkedIn
        jobs_menu = self.driver.find_element_by_xpath('//*[@id="jobs-nav-item"]')
        jobs_menu.click()
        sleep(5)

    def nav_to_net(self):  # Navigates to the networks page in LinkedIn
        self.driver.find_element_by_xpath('//*[@id="mynetwork-nav-item"]').click()
        sleep(5)

    def get_job_results(self, role, location):
        self.role = role
        self.location = location

        self.driver.find_element_by_xpath('//*[@aria-label="Search by title, skill, or company"]').send_keys(self.role)
        self.driver.find_element_by_xpath('//*[@aria-label="City, state, or zip code"]').send_keys(self.location)
        self.driver.find_element_by_xpath('//*[@type="submit"]').click()
        sleep(5)

        jobs_df = pd.DataFrame(columns=['Company_Name', 'Role', 'Posted_Date', 'Job_Link'])  # Create a new dataframe

        jobs = self.driver.find_elements_by_xpath(
            '//*[@class="job-card-search__link-wrapper js-focusable disabled ember-view"]')  # Get all the jobs

        for job in jobs:
            job.click()
            sleep(2)
            job_link_linkedin = job.get_attribute("href")
            role_name = self.driver.find_element_by_xpath(
                '//*[@class="jobs-details-top-card__job-title t-20 t-black t-normal"]').text
            company_name = self.driver.find_element_by_xpath(
                '//*[@class="jobs-details-top-card__company-url ember-view"]').text
            posted_deets = self.driver.find_element_by_xpath(
                '//*[@class="jobs-details-top-card__job-info t-14 t-black--light t-normal"]').text
            posted_deets_list = posted_deets.split()
            if (len(posted_deets_list) == 12):
                posted_date = posted_deets_list[3] + ' ' + posted_deets_list[4] + ' ' + posted_deets_list[5]
            else:
                posted_date = posted_deets_list[2] + ' ' + posted_deets_list[3] + ' ' + posted_deets_list[4]

            jobs_df = jobs_df.append({'Company_Name': company_name, 'Role': role_name, 'Posted_Date': posted_date,
                                      'Job_Link': job_link_linkedin},
                                     ignore_index=True)  # Append fields to the dataframe object

        return jobs_df

    def send_requests(self, num):
        self.num = num

        nets = self.driver.find_elements_by_xpath('//*[@data-control-name="people_connect"]')
        total_reqs = len(nets)

        if self.num > total_reqs:
            self.num = total_reqs
            print("Exceeded maximun value. Sending only {} requests".format(total_reqs))

        for i in range(self.num):
            nets[i].click()

    def email(self, df):
        self.df = df

        Date = date.today().strftime("%m/%d/%Y")

        table_header = ''
        for column in self.df.columns:
            table_header = table_header + '<th>' + column + '</th>'

        table_data = ''
        for row in range(len(self.df.index)):
            table_data = table_data + '<tr>'
            for col in range(len(self.df.columns)):
                table_data = table_data + '<td>' + str(self.df.iloc[row, col]) + '</td>'
            table_data = table_data + '<tr>'

        HTML = """
          <!DOCTYPE html>
          <html>
            <head>
              <meta charset="utf-8" />
                  <style type="text/css">
                table {
                  background: white;
                  border-radius:3px;
                  border-collapse: collapse;
                  height: auto;
                  max-width: 900px;
                  padding:5px;
                  width: 100%;
                  animation: float 5s infinite;
                }
                th {
                  color:#D5DDE5;;
                  background:#1b1e24;
                  border-bottom: 4px solid #9ea7af;
                  font-size:14px;
                  font-weight: 300;
                  padding:10px;
                  text-align:center;
                  vertical-align:middle;
                }
                tr {
                  border-top: 1px solid #C1C3D1;
                  border-bottom: 1px solid #C1C3D1;
                  border-left: 1px solid #C1C3D1;
                  color:#666B85;
                  font-size:16px;
                  font-weight:normal;
                }
                tr:hover td {
                  background:#4E5066;
                  color:#FFFFFF;
                  border-top: 1px solid #22262e;
                }
                td {
                  background:#FFFFFF;
                  padding:10px;
                  text-align:left;
                  vertical-align:middle;
                  font-weight:300;
                  font-size:13px;
                  border-right: 1px solid #C1C3D1;
                }
              </style>
            </head>
            <body>
              Hello Sourabh,<br> <br>
              Please find the jobs data below from the script you just ran:<br><br>
              <table>
                <thead>
                  <tr style="border: 1px solid #1b1e24;">
                  """ + table_header + """
                  </tr>
                </thead>
                <tbody>
                  """ + table_data + """
                </tbody>
              </table>
              <br><br>
              For more assistance, please get in touch with yourself :p -
              <a href='mailto:sourabh.amancha@gmail.com'>sourabh.amancha@gmail.com</a>.<br> <br>
              Thank you!
            </body>
          </html>
          """

        def sendEmail(_from, _to, _subj, _body):
            msg = MIMEMultipart("alternative", None, [MIMEText(HTML, 'html')])
            # msg = MIMEText(str(_body))
            msg['Subject'] = _subj
            msg['From'] = _from
            msg['To'] = _to

            s = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP gmail server and port
            s.ehlo()
            s.starttls()
            s.login('username', 'password')  # Sender gmail username and password
            s.sendmail(_from, [_to], msg.as_string())
            s.quit()

        if len(self.df.index) > 0:
            sendEmail('sourabh.amancha@gmail.com', 'sourabh.amancha@gmail.com', 'Jobs Data - ' + Date, '')


bot = LinkedInBot()

# Logging in to LinkedIn
bot.login('username', 'password')  # Provide LinkedIn username and password

# Getting job results as an email
bot.nav_to_jobs()
df = bot.get_job_results('software engineer', 'hyderabad')  # Provide role and location to search in LinkedIn jobs
print(df)
bot.email(df)

# Sending 'n' requests of a max of 40 requests
bot.nav_to_net()
bot.send_requests(10)

bot.driver.quit()
