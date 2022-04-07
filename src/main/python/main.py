
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
        raise RuntimeError("HxVwJ8mFPd5fnEmh " + folderpath)

    driver: selenium.webdriver.chrome.webdriver.WebDriver = chromecontroller.get_driver(folderpath)
    if driver is None:
        raise RuntimeError("MEpbaPKTa3RdzmNr")

    return pproperties, driver


def start(pproperties, driver):
    url: str = driver.current_url

    chromecontroller.do_move_url(driver, url, True)

    el_botContentbody: selenium.webdriver.remote.webelement.WebElement = chromecontroller.get_element_by_xpath(driver, pproperties.botContentList, -1)
    if el_botContentbody is None:
        raise RuntimeError("s7dBjGWjb2cjtBG6 " + driver.current_url + pproperties.botContentList)

    el_li_list = el_botContentbody.find_elements_by_tag_name("li")
    if el_li_list is None:
        raise RuntimeError("cnVZGL7b7SFe3Rhd " + driver.current_url + pproperties.botContentList)

    list_count: int = len(el_li_list)
    #
    # li 에 있는 값을 루프 돌면서 선택하여 페이지 전환을 한다.
    #
    for el_li in el_li_list:
        el_a = el_li.find_element_by_tag_name("a")
        if el_a is None:
            raise RuntimeError("HhsjNaKvHq28CwWx " + driver.current_url + pproperties.botContentList)

        chromecontroller.do_element_click(driver, el_a)

        print(el_li.text)

    return 0


def checkurls(pproperties, driver):
    # idx: int = 0
    # while idx < 1000:
    #     url = "http://journal.ksae.org/_common/do.php?a=full&b=22&bidx={bidx}".format(bidx=idx)
    #     chromecontroller.do_move_url(driver, url, True)
    return 0


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    utils.createFolder(chromedriver_folderpath)
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)

    print("chromedriver_folderpath : " + chromedriver_folderpath)
    print("chromedriver_filepath : " + chromedriver_filepath)
    print("chromedriver_version : " + chromecontroller.get_chrome_version())

    pproperties, driver = init(folderpath)

    checkurls(pproperties, driver)



    url: str = chromecontroller.do_move_url(driver, pproperties.url + pproperties.param, True)


    start(pproperties, driver)

    return 0



if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

