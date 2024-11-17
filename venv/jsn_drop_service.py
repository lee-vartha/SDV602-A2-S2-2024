import requests
import json

class jsnDrop(object):
    def __init__(self, tok = None, url = None) -> None:
        self.tok = tok
        self.url = url
        self.jsnStatus = ""
        self.jsnResult = {}

        self.decode = json.JSONDecoder().decode
        self.encode = json.JSONEncoder().encode

        self.jsnDropRecord = self.decode('{"tok":"","cmd":{}}')
        self.jsnDropCreate = self.decode('{"CREATE":"aTableName","EXAMPLE":{}}')
        self.jsnDropStore  = self.decode('{"STORE":"aTableName","VALUE":[]}')
        self.jsnDropDrop   = self.decode('{"DROP":"aTableName"}')
        self.jsnDropAll    = self.decode('{"ALL":"aTableName"}')
        self.jsnDropSelect = self.decode('{"SELECT":"aTableName","WHERE":"aField = b"}')
        self.jsnDropDelete = self.decode('{"DELETE":"aTableName","WHERE":"aField = b"}')

    def jsnDropApi(self, command):
        api_call = self.jsnDropRecord
        api_call["tok"] = self.tok
        api_call["cmd"] = command
        payload = {'tok': self.encode(api_call)}

        print (f"API CALL PAYLOAD = {payload}")

        r = requests.get(self.url, payload)

        jsnResponse = r.json()
        self.jsnStatus = jsnResponse["JsnMsg"]
        self.jsnResult = jsnResponse["Msg"]

        print(f"Status = {self.jsnStatus}, Result = {self.jsnResult}")
        return self.jsnResult


    
    def create(self,table_name, example):
        command = self.jsnDropCreate
        command["CREATE"] = table_name
        command["EXAMPLE"] = example
        return self.jsnDropApi(command)
        
    def store(self, table_name, value_list):
        command = self.jsnDropStore
        command["STORE"] = table_name
        command["VALUE"] = value_list
        return self.jsnDropApi(command)
    
    def drop(self,table_name):
        command = self.jsnDropDrop
        command["DROP"] = table_name
        return self.jsnDropApi(command)


    def all(self, table_name):
        command = self.jsnDropAll
        command["ALL"] = table_name
        return self.jsnDropApi(command)

    def select(self, table_name, where):
        command = self.jsnDropSelect
        command["SELECT"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)

    def delete(self,table_name, where):
        command = self.jsnDropDelete
        command["DELETE"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)


    

class jsnTable(object):

    def __init__(self, table_name, jsnDrop) -> None:
        self.table_name = table_name
        self.jsnDrop = jsnDrop
        self.jsnResult = {}
        self.jsnStatus = ""

    def create(self, example):
        return self.jsnDrop.create(self.table_name, example)

    def store(self, value_list):
        return self.jsnDrop.store(self.table_name, value_list)

    def drop(self):
        return self.jsnDrop.drop(self.table_name)

    def all(self):
        return self.jsnDrop.all(self.table_name)

    def select(self, where):
        return self.jsnDrop.select(self.table_name, where)

    def delete(self, where):
        return self.jsnDrop.delete(self.table_name, where)

    def __str__(self) -> str:
        return f"Table Name: {self.table_name}, Status: {self.jsnStatus}, Result: {self.jsnResult}"

