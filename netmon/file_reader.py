import json
import os

class FileReader:
    def __init__(self,filename):
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', filename)
        with open(filepath, 'r') as file:
            self.ip_data_json = json.load(file)
        self.Lines = []
        self.read()

    def read(self):
        for index in range(0, len(self.ip_data_json)):
            self.Lines.append("{},{}".format(
                    self.ip_data_json[index]['name'],
                    self.ip_data_json[index]['ip']
                )
            )
