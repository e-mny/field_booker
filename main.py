import time
from datetime import date, timedelta
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions
load_dotenv()
TIMEOUT_CONSTANT = 10

# mainfield; lowerfieldarch; lowerfieldspec

"""
Locations: (copy name to variable "location_to_book")
1) mainfield
2) lowerfieldarch
3) lowerfieldspec

Field number: 1, 2, 3, 4

Time slots:
1 = 0830H - 1000H
2 = 1000H - 1130H
3 = 1130H - 1300H
4 = 1300H - 1430H
5 = 1430H - 1600H
6 = 1600H - 1730H
7 = 1730H - 1900H

"""

location_to_book = "mainfield"
field_num = 1
timeslot = 1



starttime = time.time()


LOCATIONS_DICT = {
    'mainfield': [
        "1MF24",
        "1MF2MF"
    ],
    'lowerfieldarch': [
        "1F124",
        "1F12F1"
    ],
    'lowerfieldspec': [
        "1F224",
        "1F22F2"
    ]
}

username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
# print(username, password)

options = FirefoxOptions()
options.add_argument("--start-maximized")
options.set_preference("print.always_print_silent", True)
options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
options.set_preference("print_printer", "Mozilla Save to PDF")

browser = webdriver.Firefox(options=options)
browser.get("https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg=")

# Username
# username_input = browser.find_element_by_name("UserName")
# username_input.send_keys(username)
# username_input.submit()
# time.sleep(2)
username_input = WebDriverWait(browser, TIMEOUT_CONSTANT).until(EC.presence_of_element_located((By.NAME, "UserName")))
username_input.send_keys(username)
username_input.submit()


# Password
# password_input = browser.find_element_by_name("PIN")
# password_input.send_keys(password)
# password_input.submit()
# time.sleep(2)
password_input = WebDriverWait(browser, TIMEOUT_CONSTANT).until(EC.presence_of_element_located((By.NAME, "PIN")))
password_input.send_keys(password)
password_input.submit()


# Choose Location_id
# location_id = "1MF24" # (Main field)
# location_id = "1F124" # (Lower field archery side)
# location_id = "1F224" # (Lower field H6 side)

location_id = LOCATIONS_DICT[location_to_book][0]
# print(location_id)

# Choose location
WebDriverWait(browser, TIMEOUT_CONSTANT).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{location_id}']"))).click()


# Choose slots
"""
Slot string example = 1MF2MF0117-Jan-20231
Slot string format {(custom field ID)(field slot number)(date)(timeslot)}

Field ID:
Main Field = 1MF2MF
Archery side Lower Field = 1F12F1
H6 side Lower Field = 1F22F2


"""

today_date = date.today()
booking_date = today_date + timedelta(days=7) # Booking 7 days later
booking_date = booking_date.strftime("%d-%b-%Y")
print(f"Date to book: {booking_date}")
print(f"Booking location at {location_to_book}")
location_id_2 = LOCATIONS_DICT[location_to_book][1]
slot_string = location_id_2 + "0" + str(field_num) + booking_date + str(timeslot)
# print(slot_string)

# Book slots
# slot_button = browser.find_element_by_xpath(f"//input[@value='{slot_string}']").click()
# time.sleep(5)
WebDriverWait(browser, TIMEOUT_CONSTANT).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{slot_string}']"))).click()



# Confirm
# confirm_button = browser.find_element_by_xpath("//input[@value='Confirm']").click()
# time.sleep(2)
WebDriverWait(browser, TIMEOUT_CONSTANT).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm']"))).click()



# Print
browser.execute_script("window.print();")
time.sleep(2)  # Found that a little wait is needed for the print to be rendered otherwise the file will be corrupted


browser.close()

endtime = time.time()
print(f"Time taken: {(endtime - starttime):.2f}s")