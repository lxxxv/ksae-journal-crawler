
import os

import chromecontroller
import utils
import properties

import selenium
import selenium.webdriver
import selenium.webdriver.chrome.webdriver
import selenium.webdriver.remote.webelement

def init(folderpath):
    pproperties: properties.Properties = properties.Properties()
    status = pproperties.load_properties(folderpath + "application.properties")
    if (status is None) or (status < 1):
        raise RuntimeError("Error : property load")

    driver: selenium.webdriver.chrome.webdriver.WebDriver = chromecontroller.get_driver(folderpath)
    if driver is None:
        raise RuntimeError("fail chrome driver file load")

    return pproperties, driver


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    utils.createFolder(chromedriver_folderpath)
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)
    chromedriver_version = chromecontroller.get_chrome_version()

    print("chromedriver_folderpath : " + chromedriver_folderpath)
    print("chromedriver_filepath : " + chromedriver_filepath)
    print("chromedriver_version : " + chromedriver_version)

    pproperties, driver = init(folderpath)

    url: str = chromecontroller.do_move_url(driver, pproperties.url + pproperties.param, True)

    el: selenium.webdriver.remote.webelement.WebElement = chromecontroller.get_element_by_xpath(driver, "/html/body/div[2]/div[2]/div/div/div[3]/ul/li[3]/a/div/p", -1)
    if el is None:
        print("111")


    return 0



if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

