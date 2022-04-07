
import os

import chromecontroller
import utils
import properties

import selenium
import selenium.webdriver
import selenium.webdriver.chrome.webdriver
import selenium.webdriver.remote.webelement

def init(folderpath: str):
    try:
        pproperties: properties.Properties = properties.Properties()
        status = pproperties.load_properties(folderpath + "application.properties")
        if (status is None) or (status < 1):
            raise RuntimeError("HxVwJ8mFPd5fnEmh " + folderpath)

        driver: selenium.webdriver.chrome.webdriver.WebDriver = chromecontroller.get_driver(folderpath)
        if driver is None:
            raise RuntimeError("MEpbaPKTa3RdzmNr")
    except Exception as e:
        raise RuntimeError("hRAV2LJX4YArdFfT " + e)


    return pproperties, driver


def start(pproperties: properties.Properties, driver: selenium.webdriver.chrome.webdriver.WebDriver):
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


def load_volume_xpath(pproperties: properties.Properties, driver: selenium.webdriver.chrome.webdriver.WebDriver, volume_xpath_list):
    try:
        el_group: selenium.webdriver.remote.webelement.WebElement = chromecontroller.get_element_by_xpath(driver, pproperties.botContentListXpath, -1)
        if el_group is None:
            raise RuntimeError("s7dBjGWjb2cjtBG6 " + driver.current_url + pproperties.botContentListXpath)

        el_list: selenium.webdriver.remote.webelement.WebElement = el_group.find_elements_by_tag_name("li")
        if el_list is None:
            raise RuntimeError("cnVZGL7b7SFe3Rhd " + driver.current_url + pproperties.botContentListXpath)

        list_count: int = len(el_list)

        idx: int = 0
        while idx < list_count:
            volume_xpath_list.append(pproperties.botContentListLiXpath.format(idx=idx+1))
            idx = idx + 1

    except Exception as e:
        raise RuntimeError("4vRPqEsskgDgjXbq " + e)

    return len(volume_xpath_list)


def load_page_xpath(pproperties: properties.Properties, driver: selenium.webdriver.chrome.webdriver.WebDriver, page_xpath_list):
    try:
        el_group: selenium.webdriver.remote.webelement.WebElement = chromecontroller.get_element_by_xpath(driver, pproperties.pagingXpath, -1)
        if el_group is None:
            raise RuntimeError("4xMwDPdJZDQ767Bf " + driver.current_url + pproperties.pagingXpath)

        el_list: selenium.webdriver.remote.webelement.WebElement = el_group.find_elements_by_tag_name("a")
        if el_list is None:
            raise RuntimeError("Q79F6EQYpMrRtQy2 " + driver.current_url + pproperties.pagingXpath)

        list_count: int = len(el_list)

        idx: int = 0
        while idx < list_count:
            classname = el_list[idx].get_attribute("class").strip()
            if classname.find("num") >= 0:
                page_xpath_list.append(pproperties.pagebodyxpath.format(idx=idx+1))
            else:
                if classname.find("next") >= 0:
                    page_xpath_list.append(pproperties.pagebodyxpath.format(idx=idx+1))
                    chromecontroller.do_element_click(driver, el_list[idx])
                    load_page_xpath(pproperties, driver, page_xpath_list)
            idx = idx + 1

    except Exception as e:
        raise RuntimeError("4vRPqEsskgDgjXbq " + e)

    return len(page_xpath_list)


def main(folderPath):
    try:
        volume_xpath_list = []
        page_xpath_list = []

        chromedriver_FolderPath = folderPath + "chromedriver/"
        utils.createFolder(chromedriver_FolderPath)
        chromedriver_filepath = chromecontroller.init(chromedriver_FolderPath)

        print("chromedriver_FolderPath : " + chromedriver_FolderPath)
        print("chromedriver_filepath : " + chromedriver_filepath)
        print("chromedriver_version : " + chromecontroller.get_chrome_version())

        pproperties, driver = init(folderPath)

        chromecontroller.do_move_url(driver, pproperties.url + pproperties.param, True)
        load_volume_xpath(pproperties, driver, volume_xpath_list)
        chromecontroller.do_move_url(driver, pproperties.url + pproperties.param, True)
        load_page_xpath(pproperties, driver, page_xpath_list)

    except Exception as e:
        raise RuntimeError("2UAqPeu4xAHBHM4W " + e)

    return 0



if __name__ == '__main__':
    folderPath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderPath = folderPath.replace("src\\main\\python\\", "")
    folderPath = folderPath.replace("\\", "/")
    main(folderPath)

