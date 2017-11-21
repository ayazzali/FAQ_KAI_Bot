import configparser
import os

class Config:

    def getToken(path= "settings.ini"):
        """
        Create, read, update, delete config
        """
        if not os.path.exists(path):
            createConfig(path)
        
        config = configparser.ConfigParser()
        config.read(path)
        
        # Читаем некоторые значения из конфиг. файла.
        token = config.get("Settings", "token")
        return token

    def createConfig(path):
        """
        Create a DEFAULT config file
        """
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "DB_NAME", "db_001.db")
        config.set("Settings", "table_name", "T_Question_Answer")
        
        config.set("Settings", "test2", "You are using %(font)s at %(font_size)s pt")
        
        with open(path, "w") as config_file:
            config.write(config_file)

    
    def getConfig(path):
        """
        Create, read, update, delete config
        """
        if not os.path.exists(path):
            createConfig(path)
        
        config = configparser.ConfigParser()
        config.read(path)
        
        # Читаем некоторые значения из конфиг. файла.
        font = config.get("Settings", "font")
        font_size = config.get("Settings", "font_size")
        return self

if __name__ == "__main__":
    path = "settings.ini"
    getToken()
    #createConfig(path)