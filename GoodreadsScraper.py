from selenium import webdriver
from selenium.webdriver.common import keys
import csv
import time
import argparse
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options

# from pyvirtualdisplay import Display
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select

# import json
driver = ''


def create_csv_file(output_file):
    header = ['Title', 'URL']
    with open(output_file, 'w+') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(header)

def read_from_txt_file(input_file):
    lines = [line.rstrip('\n') for line in open(input_file, 'r')]
    return lines

def write_into_csv_file(output_file, vendor):
   with open(output_file, 'a') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(vendor)

def search_for_title(title):
    driver.get('https://www.goodreads.com/search?q=')
    time.sleep(2)
    search_field = driver.find_element_by_name('q')
    search_field.clear()
    search_field.send_keys(title)
    search_field.send_keys(keys.Keys.RETURN) # you missed this part
    try:
        url = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a')
        print(url.get_attribute('href'))
        return True
    except:
        return False

def scrape_url():
    try:
        url = driver.find_element_by_css_selector('a.bookTitle').get_attribute('href')
    except:
        url = "N/A"
    return url


def main(input_file, output_file):
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized") 
    options.add_argument("headless") 
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option('useAutomationExtension', False)
    global driver
    driver = webdriver.Chrome(options=options) #Comment this line and use the second option if you need to provide executable webdriver path
    # driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

    driver.get('https://www.goodreads.com')
    time.sleep(5)
    create_csv_file(output_file)
    titles = read_from_txt_file(input_file)    

    for title in titles:
        if search_for_title(title):
            url = scrape_url()
        else:
            url = "N/A"
        write_into_csv_file(output_file, [title, url])
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='add, modify and delete upstream nodes')
    ap = argparse.ArgumentParser(prog='GoodreadsScraper.py',
                                    usage='%(prog)s [options] --input ./booktitle.txt --output output.csv',
                                    description='Start scrapping of the input .txt file and store in output .csv file')
    ap.add_argument( '-i','--input',type=str,action='store', required=True, help='input txt file path(default:current path)')
    ap.add_argument( '-o','--output' ,type=str, action='store',required=True,help='output csv fiel path(defualt: current path)')
    args = ap.parse_args()
    input_file = args.input
    output_file = args.output
    print('reading book title..')
    main(input_file, output_file)