import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Driver path
path = 'path_to_driver'
driver = webdriver.Chrome(path)

# Maximize Window
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(5)

# Enter to the site
driver.get('https://www.linkedin.com/login')
time.sleep(3)

# Accept cookies
driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div/section/div/div[2]/button[1]").click()
time.sleep(3)

user_name = 'username'
password = 'password'
send_usr = driver.find_element(By.ID, "username")
send_usr.clear()
send_usr.send_keys(user_name)
time.sleep(3)

send_psw = driver.find_element(By.ID, "password")
send_psw.clear()
send_psw.send_keys(password)
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

# Login button
driver.implicitly_wait(20)
driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
driver.implicitly_wait(30)
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3344813886&f_E=1%2C2%2C3%2C4%2C5&f_JT=F%2CP%2CC%2CT%2CI%2CO"
    "&geoId=105072130&keywords=project%20manager&location=Poland")
time.sleep(3)

links = []

for page in range(2, 40):
    time.sleep(5)
    jobs_block = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/div')
    job_list = jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')

    for job in job_list:
        all_links = job.find_elements(By.TAG_NAME, 'a')

        for a in all_links:
            if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute(
                    'href') not in links:
                links.append(a.get_attribute('href'))
            else:
                pass
        driver.execute_script("arguments[0].scrollIntoView();", job)

    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, f'//button[@aria-label="Page {page}"]').click()
    print(f'Collecting the links in the page: {page - 1}')
    # go to next page:
    time.sleep(3)

for i in range(len(links)):
    main_data = []
    driver.get(links[i])

    time.sleep(5)
    driver.implicitly_wait(10)
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")
    print(links[i])

    if soup.title:
        company_name = soup.title.text.split(' | ')[1]
    else:
        company_name = soup.title.text.split(' | ')[0]

    if len(soup.find('li', {'class': 'jobs-unified-top-card__job-insight'}).find("span").text.strip().split(
            ' · ')) > 1:
        level = \
            soup.find('li', {'class': 'jobs-unified-top-card__job-insight'}).find("span").text.strip().split(' · ')[
                1]
    else:
        level = 'Not specified'

    job_type = \
        soup.find('li', {'class': 'jobs-unified-top-card__job-insight'}).find('span').text.strip().split(' · ')[0]

    if soup.find("div", class_='t-14 mt5'):
        if '\n' in soup.find("div", class_='t-14 mt5').text.strip():
            depart = soup.find("div", class_='t-14 mt5').text.strip().replace('\n', '').split('                  ')[
                0]
        else:
            depart = soup.find("div", class_='t-14 mt5').text.strip()
    else:
        depart = 'Not specified'

    position = soup.title.text.split(' | ')[0]

    if ', ' in soup.find("span", {"class": "jobs-unified-top-card__bullet"}).text.strip():
        location = soup.find("span", {"class": "jobs-unified-top-card__bullet"}).text.strip().split(', ')[0]
    else:
        location = soup.find("span", {"class": "jobs-unified-top-card__bullet"}).text.strip().split(' ')[0]

    if soup.find("span", {'class': 'jobs-unified-top-card__posted-date'}):
        created_at = soup.find("span", {'class': 'jobs-unified-top-card__posted-date'}).text.strip()
    else:
        created_at = 'Not specified'

    main_data.append({'company_name': company_name,
                      'level': level,
                      'job_type': job_type,
                      'department': depart,
                      'position': position,
                      'location': location,
                      'date_posted': created_at,
                      'link_job': str(links[i])})

    df = pd.DataFrame(main_data)

    if i == 0:
        df.to_csv('linkedin_jobs.csv', index=False, header=True, mode='w')
    else:
        df.to_csv('linkedin_jobs.csv', index=False, header=False, mode='a')
