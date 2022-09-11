"""This is the main script to (almost) automatically write working hours."""
import sys
import os
import json
import time
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from workweek import WorkWeek


def set_arrival(driver: webdriver, t_start: str, t_end: str, t_break: str) -> None:
    """Setting start, end, and break time for the day."""
    pres_cont = driver.find_element(By.ID, "presenceContainer")
    elem_arrive = pres_cont.find_element(By.CSS_SELECTOR, "input[tabindex='41']")
    elem_depart = pres_cont.find_element(By.CSS_SELECTOR, "input[tabindex='61']")
    elem_break = pres_cont.find_element(By.CSS_SELECTOR, "input[tabindex='81']")

    elem_arrive.clear()
    time.sleep(1)
    elem_arrive.send_keys(t_start)

    elem_depart.clear()
    time.sleep(1)
    elem_depart.send_keys(t_end)

    elem_break.clear()
    time.sleep(1)
    elem_break.send_keys(t_break)
    # elem_break.send_keys(Keys.RETURN)
    time.sleep(1)
    safe_button = pres_cont.find_element(By.TAG_NAME, "button")
    safe_button.click()


def set_day(driver: webdriver, day: str) -> None:
    """Selects and sets the date."""
    try:
        WebDriverWait(driver, 4).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "worktime-recording")
                ))
        worktime_recording = driver.find_element(By.CLASS_NAME, "worktime-recording")
    except TimeoutException:
        print('Could not find worktime-recording table!')
        sys.exit()

    input_date = worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='261']")
    input_duration = worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='281']")

    # To make the input invalid, when we press Return, so only the date changes
    input_duration.clear()

    input_date.clear()
    time.sleep(1)
    input_date.send_keys(day)
    time.sleep(1)
    input_date.send_keys(Keys.RETURN)


def set_block(driver: webdriver, block: dict) -> None:
    """Sets project_name, activity, and duration for one block of work"""
    try:
        WebDriverWait(driver, 4).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "worktime-recording")
                ))
        worktime_recording = driver.find_element(By.CLASS_NAME, "worktime-recording")
    except TimeoutException:
        print('Could not find worktime-recording table!')
        sys.exit()

    time.sleep(2)
    projects = worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='341']")
    projects.click()
    time.sleep(1)
    projects.send_keys(block.project_name)
    time.sleep(1)
    projects.send_keys(Keys.DOWN)
    projects.send_keys(Keys.RETURN)

    time.sleep(2)
    activity = worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='381']")
    activity.click()
    time.sleep(1)
    activity.send_keys(block.activity)
    time.sleep(1)
    activity.send_keys(Keys.DOWN)
    activity.send_keys(Keys.RETURN)

    duration = worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='281']")
    duration.click()
    time.sleep(1)
    # Unfortunately the duration needs to be in hours not in minutes
    hours = f'{int(block.duration/60)}:{block.duration%60:02}'
    duration.send_keys(hours)
    time.sleep(1)
    duration.send_keys(Keys.RETURN)

    time.sleep(1)
    worktime_recording.find_element(By.TAG_NAME, "button").click()


def get_project_list_from_dropdown(driver: webdriver) -> list:
    """Extracts the select options from the project name dropdown list."""
    try:
        WebDriverWait(driver, 4).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "worktime-recording")
                ))
        worktime_recording = driver.find_element(By.CLASS_NAME, "worktime-recording")
    except TimeoutException:
        print('Could not find worktime-recording table!')
        sys.exit()

    time.sleep(2)
    worktime_recording.find_element(By.CSS_SELECTOR, "input[tabindex='341']").click()
    time.sleep(1)
    projects_section = driver.find_elements(By.TAG_NAME, "section")[0]
    projects_list = [x.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                    for x in projects_section.find_elements(By.TAG_NAME, "li")
                    if "checked selected" not in x.get_attribute('class')
                    and "disabled" not in x.get_attribute('class')]

    return projects_list


def goto_time_mgmt(driver: webdriver) -> None:
    """Navigates to time management form."""
    # Activate Desktop view
    driver.find_element(By.CSS_SELECTOR, "li[data-nav-id='changedevicetype.screen']").click()

    # Open personal area
    driver.find_element(By.CSS_SELECTOR, "li[data-nav-id='WorktimeAccountingWorkflow']").click()

    # Select time management
    try:
        WebDriverWait(driver, 4).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, "li[data-nav-id='53']")
                ))
        driver.find_element(By.CSS_SELECTOR, "li[data-nav-id='53']").click()
    except TimeoutException:
        print('Could not find navigation button!')
        sys.exit()

    # Switch to iframe
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])


def handle_ssl_error(driver: webdriver) -> None:
    """This is a workaround to handle the ssl error
    caused by not importing the appropriate certificate.
    Currently none of the found solutions/fixes seem to work.
    """
    driver.get_element(By.ID, "advancedButton").click()
    driver.get_element(By.ID, "exceptionDialogButton").click()
    driver.send_keys(Keys.RETURN)


def login(driver: webdriver, login_name: str, pswd: str) -> None:
    """Log into the page."""
    elem_name = driver.find_element(By.NAME, "MT_BENUTZERNAME")
    elem_name.clear()
    elem_name.send_keys(login_name)

    elem_pw = driver.find_element(By.NAME, "MT_Kennwort")
    elem_pw.clear()
    elem_pw.send_keys(pswd)
    elem_pw.send_keys(Keys.RETURN)


def submit_data(data: WorkWeek, url: str, name: str, passwd: str = getpass()) -> None:
    """Submits data to the website using Selenium."""
    print(f'{url=}')
    print(f'{name=}')

    # Setting untrusted certs via caps is deprecated and does not work anyway
    # caps = webdriver.DesiredCapabilities().FIREFOX
    # caps['acceptInsecureCerts'] = True
    # driver = webdriver.Firefox(capabilities=caps)

    # Setting options is recommended, but does not seem to work
    # opt = webdriver.FirefoxOptions()
    # opt.accept_insecure_certs = True
    # driver = webdriver.Firefox(options=opt)

    driver = webdriver.Firefox()
    driver.get(f'{url}')

    login(driver, name, passwd)

    # Workaround until setting options actually works
    try:
        WebDriverWait(driver, 4).until(ec.presence_of_element_located((By.ID, "advancedButton")))
        handle_ssl_error(driver)
    except TimeoutException:
        pass

    goto_time_mgmt(driver)

    for day in data.days:
        time.sleep(2)
        set_day(driver, day.date_day)
        time.sleep(2)
        set_arrival(driver, day.start_time, day.end_time, day.break_duration)

        for block in day.blocks:
            set_block(driver, block)
            time.sleep(1)


def load_data(fname: str) -> WorkWeek:
    """Loads data depending on filetype."""
    if filename.split('.')[-1] == 'json':
        return load_data_json(fname=fname)
    if filename.split('.')[-1] == 'xml':
        return load_data_xml(fname=fname)

    return None


def load_data_json(fname: str) -> WorkWeek:
    """Loads data from a json file."""
    work_week = None
    with open(fname, 'r', encoding='utf-8') as fhandle:
        j = json.load(fhandle)
        work_week = WorkWeek(**j['week'])

    return work_week, j['url'], j['name']


def load_data_xml(fname: str) -> WorkWeek:
    """Loads data from an xml file."""
    raise NotImplementedError


def show_menu() -> None:
    """Provides a menu to interactively input values."""
    raise NotImplementedError


if __name__ == "__main__":
    # Just for testing set argument
    if len(sys.argv) == 1:
        sys.argv.append('input.json')

    # Show an interactive menu
    if len(sys.argv) == 1:
        show_menu()

    # Load data from a file
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        ext = filename.split('.')[-1]

        # Accept only json and xml format
        if (ext in ['json', 'xml']) and os.path.isfile(filename):
            submit_data(*load_data(filename))
        else:
            print('If first argument is set, it has to be a json or xml file!')
            sys.exit(1)
    else:
        print('Invalid number of arguments. Use no arguments to show an interactive menu or one as file from which to load data.')
        sys.exit(2)

    print('Script has finished.')
