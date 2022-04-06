
import os
import chromecontroller

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        raise RuntimeError("Error: Creating directory. " + directory)


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    createFolder(chromedriver_folderpath)
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)
    chromedriver_version = chromecontroller.get_chrome_version()

    driver = chromecontroller.get_driver(folderpath)
    if (driver == None):
        raise RuntimeError("fail chrome driver file load")


    return 0


if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

