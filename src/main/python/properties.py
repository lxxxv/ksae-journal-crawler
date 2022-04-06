
import utils

class Properties:
    def __init__(self):
        self.url = ""


    def load_properties(self, filepath):
        status = 0
        if utils.isfileexists(filepath):
            file_config = open(filepath, mode='r', encoding='utf8')
            while 1:
                temp_line = file_config.readline()
                try:
                    escape = temp_line.index("\n")
                except:
                    escape = len(temp_line)

                if temp_line:
                    str_config = temp_line[0:escape]
                    if str_config.find("#")>= 0:
                        pass
                    else:
                        if str_config.strip() == '':
                            pass
                        else:
                            if str_config.find("url=")>= 0:
                                self.url = str_config.replace("url=", "").strip()
                                status = status + 1
                else:
                    break
            file_config.close()
            return status
        else:
            raise RuntimeError("Error: application.properties file not exists " + filepath)
