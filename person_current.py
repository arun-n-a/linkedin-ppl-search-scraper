import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("/home/arun/Downloads/chromedriver")
driver.maximize_window()
driver.get("https://www.linkedin.com/")
# sleep(5)

email = ""  # add your linkedin email address
password = ""  # add your linkedin password

driver.find_element_by_xpath("/html/body/nav/a[3]").click()
sleep(2)
driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(email)  # textbox user email
driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(password)  # textbox for assword
try:
    # submit button div id of button may vary 3 or 4
    driver.find_element_by_xpath("""//*[@id="app__container"]/main/div[2]/form/div[3]/button""").click()
except:
    driver.find_element_by_xpath("""//*[@id="app__container"]/main/div[2]/form/div[4]/button""").click()
sleep(2)
driver.get("https://www.linkedin.com/search/results/people/")
sleep(2)
driver.find_element_by_xpath("""/html/body/div[5]/div[3]/div[3]/div/div[1]/header/div/div/div[2]/button""").click()
sleep(2)
driver.find_element_by_xpath("""//*[@id="locations-facet-values"]/fieldset/ol/li[3]/label""").click()
sleep(2)
driver.find_element_by_xpath("""//*[@id="industries-facet-values"]/fieldset/ol/li[4]/label""").click()
sleep(2)
driver.find_element_by_xpath("""//*[@id="search-advanced-title"]""").send_keys("CEO")
sleep(2)
driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[1]/div/div[2]/button[2]""").click()
result = []
sleep(2)
for j in range(2):
    for i in range(2):
        driver.find_element_by_tag_name("html").send_keys(Keys.SPACE)
        sleep(1)
    soup = BeautifulSoup(driver.page_source)
    search_results = soup.findAll("div", {"class": "search-result__wrapper"})
    for page, search_result in enumerate(search_results):
        data = {}
        name = search_result.find("div", {"class": "visually-hidden"}).text
        job_title = search_result.find_all("p")[0].text.split(" at ")[0].strip()
        try:
            organization = search_result.find_all("p")[0].text.split(" at ")[1].strip()
        except:
            organization = ""
        try:
            location = search_result.find_all("p")[1].text.strip()
        except:
            location = ""
        result.append({"Name": name, "Location": location, "Job Title": job_title, "Organization": organization})
        try:
            driver.find_element_by_xpath(
                f"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/ul/li[{page + 1}]").click()
        except:
            pass
driver.quit()
opcsv = open("output.csv", "w")
writer = csv.DictWriter(opcsv, fieldnames=["Name", "Location", "Job Title", "Organization"])
writer.writeheader()
for row in result:
    writer.writerow(row)
opcsv.close()
