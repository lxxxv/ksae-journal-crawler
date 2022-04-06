
import os

import chromecontroller
import utils


def load_properties(filepath):
    if utils.isfileexists(filepath):
        pass
    else:
        raise RuntimeError("Error: application.properties file not exists " + filepath)


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    utils.createFolder(chromedriver_folderpath)
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)
    chromedriver_version = chromecontroller.get_chrome_version()

    print("chromedriver_folderpath : " + chromedriver_folderpath)
    print("chromedriver_filepath : " + chromedriver_filepath)
    print("chromedriver_version : " + chromedriver_version)

    load_properties(folderpath + "application.properties1")

    driver = chromecontroller.get_driver(folderpath)
    if (driver == None):
        raise RuntimeError("fail chrome driver file load")


    return 0


if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

