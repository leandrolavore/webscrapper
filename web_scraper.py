from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup



url = 'https://www.amazon.com.au/'

browser = webdriver.Chrome('C:\\Users\Leandro\Downloads\chromedriver.exe')
browser.get(url)

search = browser.find_element_by_name('field-keywords')
search.send_keys("Laptop Lenovo")
search.send_keys(Keys.ENTER)

browser.implicitly_wait(15)
#passing my url from selenium to bs4
new_url = browser.current_url
client = ureq(new_url)
html_scrap = client.read()
client.close()
html_soup = soup(html_scrap, "html.parser")

containers = html_soup.findAll("div", {"class": "s-include-content-margin s-border-bottom"})
page = containers[0]

title_tag = page.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
title = title_tag.text
price_tag = page.find("span", {"class": "a-offscreen"})
price = price_tag.text


filename = "portfolio-scraper.csv"
file = open(filename, "w")
headers = "Model, Price""\n"
file.write(headers)


def get_next_page():
    browser.find_element_by_partial_link_text("Next").click()
    browser.implicitly_wait(15)

    new_url = browser.current_url
    client = ureq(new_url)
    html_scrap = client.read()
    client.close()
    html_soup = soup(html_scrap, "html.parser")
    containers = html_soup.findAll("div", {"class": "s-include-content-margin s-border-bottom"})
    scrap_html(containers)


def scrap_html(containers):
    for container in containers:
        title_tag = container.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
        try:
            title = title_tag.text
        except:
            title = "no model available"


        price_tag = container.find("span", {"class": "a-offscreen"})
        try:
            price = price_tag.text
        except:
            price = "no price available"

        xls = title + "," + price + "\n"
        file.write(xls)


scrap_html(containers)
get_next_page()
browser.implicitly_wait(10)
get_next_page()
browser.implicitly_wait(10)
file.close()


# click_next = browser.find_element_by_partial_link_text("Next").click()
# browser.implicitly_wait(15)
#
# new_url = browser.current_url
# client = ureq(new_url)
# html_scrap = client.read()
# client.close()
# html_soup = soup(html_scrap, "html.parser")
# containers = html_soup.findAll("div", {"class": "s-include-content-margin s-border-bottom"})
#
# scrap_html(containers)