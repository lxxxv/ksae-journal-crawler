
import os

import chromecontroller
import utils
import properties

import selenium


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    utils.createFolder(chromedriver_folderpath)
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)
    chromedriver_version = chromecontroller.get_chrome_version()

    print("chromedriver_folderpath : " + chromedriver_folderpath)
    print("chromedriver_filepath : " + chromedriver_filepath)
    print("chromedriver_version : " + chromedriver_version)

    pproperties: properties.Properties = properties.Properties()
    status = pproperties.load_properties(folderpath + "application.properties")
    if (status is None) or (status < 1):
        raise RuntimeError("Error : property load")

    driver: selenium.webdriver.chrome.webdriver.WebDriver = chromecontroller.get_driver(folderpath)
    if (driver == None):
        raise RuntimeError("fail chrome driver file load")


    chromecontroller.do_move_url(driver, pproperties.url, True)

    return 0


if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

