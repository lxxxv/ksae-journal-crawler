
import utils

class Properties:
    def __init__(self):
        self.url: str = ""
        self.param: str = ""
        self.botContentListXpath: str = ""
        self.botContentListLiXpath: str = ""
        self.pagingXpath: str = ""
        self.pagebodyxpath: str = ""
        self.invalidUrl: str = ""
        self.maxB: int = 0


    def load_properties(self, filepath):
        status = 0
        if utils.isfileexists(filepath):
            file_config = open(filepath, mode='r', encoding='utf8')
            while 1:
                temp_line: str = file_config.readline()
                try:
                    escape = temp_line.index("\n")
                except:
                    escape = len(temp_line)

                try:
                    if temp_line:
                        str_config = temp_line[0:escape].strip()
                        if str_config.find("#") == 0:
                            pass
                        else:
                            if str_config.strip() == '':
                                pass
                            else:
                                if str_config.find("url=") == 0:
                                    self.url = str_config.replace("url=", "").strip()
                                    status = status + 1
                                elif str_config.find("param=") == 0:
                                    self.param = str_config.replace("param=", "").strip()
                                    status = status + 1
                                elif str_config.find("botContentListxpath=") == 0:
                                    self.botContentListXpath = str_config.replace("botContentListxpath=", "").strip()
                                    status = status + 1
                                elif str_config.find("botContentListlixpath=") == 0:
                                    self.botContentListLiXpath = str_config.replace("botContentListlixpath=", "").strip()
                                    status = status + 1
                                elif str_config.find("pagingxpath=") == 0:
                                    self.pagingXpath = str_config.replace("pagingxpath=", "").strip()
                                    status = status + 1
                                elif str_config.find("pagebodyxpath=") == 0:
                                    self.pagebodyxpath = str_config.replace("pagebodyxpath=", "").strip()
                                    status = status + 1
                                elif str_config.find("invalidurl=") == 0:
                                    self.invalidUrl = str_config.replace("invalidurl=", "").strip()
                                    status = status + 1
                                elif str_config.find("maxbidx=") == 0:
                                    self.maxB = int(str_config.replace("maxbidx=", "").strip())
                                    status = status + 1
                    else:
                        break
                except Exception as e:
                    raise RuntimeError("adQ8b5FLEuzAJzTt " + e)
            file_config.close()
            return status
        else:
            raise RuntimeError("Error: application.properties file not exists " + filepath)
