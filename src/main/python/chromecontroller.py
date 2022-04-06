
import sys
import os
import subprocess
import urllib.request
import urllib.error
import zipfile
import xml.etree.ElementTree as elemTree
import logging
import re
import shutil

import time
import random

from io import BytesIO
from typing import Optional, AnyStr

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


m_longint_sleep:int = 2


def get_chromedriver_filename():
    if sys.platform.startswith("win"):
        return "chromedriver.exe"
    return "chromedriver"


def get_variable_separator():
    if sys.platform.startswith("win"):
        return ";"
    return ":"


def get_platform_architecture():
    if sys.platform.startswith("linux") and sys.maxsize > 2 ** 32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        architecture = "64"
    elif sys.platform.startswith("win"):
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError("Could not determine chromedriver download URL for this platform.")
    return platform, architecture


def get_chromedriver_url(version):
    base_url = "https://chromedriver.storage.googleapis.com/"
    platform, architecture = get_platform_architecture()
    return base_url + version + "/chromedriver_" + platform + architecture + ".zip"


def find_binary_in_path(filename):
    if "PATH" not in os.environ:
        return None
    for directory in os.environ["PATH"].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, "-v"])
        version = re.match(r".*?([\d.]+).*?", version.decode("utf-8"))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chrome_version():
    platform, _ = get_platform_architecture()
    if platform == "linux":
        path = get_linux_executable_path()
        with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode("utf-8").replace("Chromium", "").replace("Google Chrome", "").strip()
    elif platform == "mac":
        process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
    elif platform == "win":
        process = subprocess.Popen(
            ["reg", "query", "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon", "/v", "version"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        output = process.communicate()
        if output:
            version = output[0].decode("UTF-8").strip().split()[-1]
        else:
            process = subprocess.Popen(
                ["powershell", "-command", "$(Get-ItemProperty -Path Registry::HKEY_CURRENT_USER\\Software\\Google\\chrome\\BLBeacon).version"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            version = process.communicate()[0].decode("UTF-8").strip()
    else:
        return
    return version


def get_linux_executable_path():
    for executable in (
            "google-chrome",
            "google-chrome-stable",
            "google-chrome-beta",
            "google-chrome-dev",
            "chromium-browser",
            "chromium",
    ):
        path = shutil.which(executable)
        if path is not None:
            return path
    raise ValueError("No chrome executable found on PATH")


def get_major_version(version):
    return version.split(".")[0]


def get_matched_chromedriver_version(version):
    doc = urllib.request.urlopen("https://chromedriver.storage.googleapis.com").read()
    root = elemTree.fromstring(doc)
    for k in root.iter("{http://doc.s3.amazonaws.com/2006-03-01}Key"):
        if k.text.find(get_major_version(version) + ".") == 0:
            return k.text.split("/")[0]
    return


def get_chromedriver_path():
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    print(get_chromedriver_path())


def download_chromedriver(path: Optional[AnyStr] = None):
    chrome_version = get_chrome_version()
    if not chrome_version:
        logging.debug("Chrome is not installed.")
        return
    chromedriver_version = get_matched_chromedriver_version(chrome_version)
    if not chromedriver_version:
        logging.warning("Can not find chromedriver for currently installed chrome version.")
        return
    major_version = get_major_version(chromedriver_version)

    if path:
        if not os.path.isdir(path):
            raise ValueError(f"Invalid path: {path}")
        chromedriver_dir = os.path.join(
            os.path.abspath(path),
            major_version
        )
    else:
        chromedriver_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            major_version
        )
    chromedriver_filename = get_chromedriver_filename()
    chromedriver_filepath = os.path.join(chromedriver_dir, chromedriver_filename)
    if not os.path.isfile(chromedriver_filepath) or \
            not check_version(chromedriver_filepath, chromedriver_version):
        logging.info(f"Downloading chromedriver ({chromedriver_version})...")
        if not os.path.isdir(chromedriver_dir):
            os.makedirs(chromedriver_dir)
        url = get_chromedriver_url(version=chromedriver_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError("Not Found")
        except urllib.error.URLError:
            raise RuntimeError(f"Failed to download chromedriver archive: {url}")
        archive = BytesIO(response.read())
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extract(chromedriver_filename, chromedriver_dir)
    else:
        logging.info("Chromedriver is already installed.")
    if not os.access(chromedriver_filepath, os.X_OK):
        os.chmod(chromedriver_filepath, 0o744)
    return chromedriver_filepath


def init(folderpath):
    chromedriver_filepath = download_chromedriver(folderpath)
    if not chromedriver_filepath:
        logging.debug("Can not download chromedriver.")
        return
    chromedriver_dir = os.path.dirname(chromedriver_filepath)
    if "PATH" not in os.environ:
        os.environ["PATH"] = chromedriver_dir
    elif chromedriver_dir not in os.environ["PATH"]:
        os.environ["PATH"] = chromedriver_dir + get_variable_separator() + os.environ["PATH"]
    return chromedriver_filepath


def get_driver(download_folderpath):
    driver = None
    x = -5000
    y = -5000
    width = 1300
    height = 900

    try:
        print("check web driver")

        if (download_folderpath == ""):
            driver: selenium.webdriver.chrome.webdriver.WebDriver = webdriver.Chrome()
        else:
            options: selenium.webdriver.chrome.options.Options = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : download_folderpath}
            options.add_experimental_option("prefs", prefs)
            driver: selenium.webdriver.chrome.webdriver.WebDriver = webdriver.Chrome(chrome_options=options)

        print("ready to web driver")
        driver.set_window_position(x, y)
        driver.set_window_size(width, height)

        return driver
    except Exception as e:
        print(e)
        return None


def get_elements_by_xpath(_driver, _str_path, _max_check_count):
    try:
        element = None
        if _max_check_count < 0:
            while (1):
                element = _driver.find_elements_by_xpath(_str_path)
                if len(element)> 0:
                    break
            return element
        else:
            counter = 0
            while (counter < _max_check_count):
                element = _driver.find_elements_by_xpath(_str_path)
                if len(element)> 0:
                    break
                else:
                    counter = counter + 1
            return element
    except Exception as e:
        print(e)
        return None


def get_element_by_xpath(_driver, _str_path, _max_check_count):
    try:
        element = None
        if _max_check_count < 0:
            while (1):
                element = _driver.find_element_by_xpath(_str_path)
                if element is None:
                    pass
                else:
                    break
            return element
        else:
            counter = 0
            while (counter < _max_check_count):
                element = _driver.find_element_by_xpath(_str_path)
                if element is None:
                    counter = counter + 1
                else:
                    break
            return element
    except Exception as e:
        print(e)
        return None


def do_move_url(_driver: selenium.webdriver.chrome.webdriver.WebDriver, _url, _is_loop):
    try:
        _driver.get(_url)
        time.sleep(random.randrange(1, m_longint_sleep))
    except Exception as e:
        if (_is_loop == True):
            do_move_url(_driver, _url, _is_loop)
        else:
            raise RuntimeError("Error: move url : " + _url)
    return _driver.current_url


def do_elements_click(_driver, _element):
    _element[0].click()
    time.sleep(random.randrange(1, m_longint_sleep))
    return 1


def do_element_click(_driver, _element):
    _element.click()
    time.sleep(random.randrange(1, m_longint_sleep))
    return 1


def do_switch_iframe(_driver, _iframe_url):
    try:
        element_iframe = get_elements_by_xpath(_driver, _iframe_url, -1)
        if (not element_iframe is None):
            _driver.switch_to.frame(element_iframe[0])
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
    return 1



