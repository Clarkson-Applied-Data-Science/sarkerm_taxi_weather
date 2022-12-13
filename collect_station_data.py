from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime,csv,time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

tries = 0
host = 'https://www.wunderground.com/history/daily/us/ny/new-york-city'

#driver = webdriver.Chrome('/home/baset/chromedriver_linux64/chromedriver')
caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "normal"  #  Waits for full page load
caps["pageLoadStrategy"] = "none"   # Do not wait for full page load


def save_history_data_in_csv(station_row, formated_date,h_list):
    arr = []
    arr.append(formated_date)
    h_list = station_row + arr + h_list
    with open('station_data/'+station_row[0]+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(h_list)



def get_history_data(url,station_row, formated_date):
    global tries
    print(url)
    try:
        driver = webdriver.Chrome(desired_capabilities=caps, executable_path='/home/baset/chromedriver_linux64/chromedriver')
        driver.get(url)
        histories = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements_by_xpath("//table[@aria-labelledby='History observation']//tr//td[@role='gridcell']"))
        
        n = 1
        h_list = []
        for p in histories:
            h_list.append(p.text)
            if n == 10:
                #print(p.text)
                #print("\n")
                save_history_data_in_csv(station_row, formated_date,h_list)
                h_list = []
                n = 0
            n += 1
        tries = 0
        driver.close()
        driver.quit()
    except Exception as e:
        print("Error",e)
        driver.close()
        driver.quit()
        
        if tries < 20:
            print("try again",tries)
            tries += 1
            get_history_data(url,station_row, formated_date)
        else:
            print("stop at",url)
            with open("errorlog.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([url])
        





d1 = datetime.date(2015, 1, 1)
d2 = datetime.date(2015, 12, 31)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]


with open('stations.csv', 'r',) as file:
    reader = csv.reader(file, delimiter = ',')


    for i,station_row in enumerate(reader):
        if i == 0:
            continue

        for day in days:
            url = host+'/'+station_row[0] + '/date/' + day.strftime('%Y-%m-%d')   
            formated_date = day.strftime('%Y-%m-%d') 

            if tries < 20:
                get_history_data(url,station_row, formated_date)
            else:
                print("stop at",url)
                with open("log/errorlog.csv", 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([url])
                exit()



            
