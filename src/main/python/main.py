
import os
import chromecontroller


def main(folderpath):
    chromedriver_folderpath = folderpath + "chromedriver/"
    chromedriver_filepath = chromecontroller.init(chromedriver_folderpath)

    print(chromedriver_filepath)
    return 0


if __name__ == '__main__':
    folderpath = os.path.dirname(os.path.abspath(__file__)) + "\\"
    folderpath = folderpath.replace("src\\main\\python\\", "")
    folderpath = folderpath.replace("\\", "/")
    main(folderpath)

