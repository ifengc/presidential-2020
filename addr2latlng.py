"""convert address to latitude and longitude"""
import os
import sys
import time
import functools
from typing import Tuple

from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument("headless")


def retry_func(func):
    """retry function"""

    @functools.wraps(func)
    def warp_func(*args, **kargs):
        for _ in range(3):
            try:
                func_result = func(*args, **kargs)
            except Exception as e:
                print("Retry [function: {}], {}".format(func.__name__, e))
                time.sleep(5)
            else:
                return func_result
        else:
            raise Exception("Retry timeout")
    return warp_func


@retry_func
def get_coordinate(addr: str) -> Tuple[str, str]:
    """get latitude and longitude
    Ref: medium Geocoding - 批量處理地址轉換經緯度
    """
    browser = webdriver.Chrome(executable_path='chromedriver', options=options)
    browser.get("http://www.map.com.tw/")
    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(2)
    iframe = browser.find_elements_by_tag_name("iframe")[1]
    browser.switch_to.frame(iframe)
    xpath = "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]"
    coor_btn = browser.find_element_by_xpath(xpath)
    coor_btn.click()
    coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    lng = coor[0].split("：")[-1]
    browser.quit()
    return (lat, lng)


def main():
    """main function"""
    input_f_name = sys.argv[1].strip()
    output_f_name = input_f_name + "_latlng.csv"

    prev_set = set()
    if os.path.exists(output_f_name):
        f_prev = open(output_f_name, "r")
        prev_set = {line.strip().split(",")[0] for line in f_prev}
        f_prev.close()

    f_writer = open(output_f_name, "a")
    with open(input_f_name, "r") as f_reader:
        for i, line in enumerate(f_reader):
            line = line.strip()
            if line in prev_set:
                continue

            latlng = get_coordinate(line)
            print(i, line, latlng)
            f_writer.write(f"{line},{latlng[0]},{latlng[1]}\n")
    f_writer.close()


if __name__ == "__main__":
    main()
