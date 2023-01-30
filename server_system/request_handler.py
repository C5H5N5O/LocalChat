import json

# обрабатывает измениеия касающиеся групп
class ModificationHandler():

    requests = {
    #key: запрос, #value: метод, обрабатывающий такие запросы
        
    }

    def handle(self, data):
        pass
    


# обрабатывает запросы связанные с отправкой каких-либо сообщений, добавления эмодзи и т д
class MassageHandler():

    requests = {
        #key: запрос, #value: метод, обрабатывающий такие запросы
        
    }

    def handle(self, data):
        pass

     
class InfoRequestHendler():

    requests = {
        #key: запрос, #value: метод, обрабатывающий такие запросы
        
    }

    def handle(self, data):
        pass


class RequestHendler():

    requests_tipes = {
        #key: тип запроса, #value: класс, обрабатывающий такие типы запросов
        "massage"     : MassageHandler(),
        "modification": ModificationHandler(),
        "info_request": InfoRequestHendler()
    }
    
    def handle(self, data):
        #self.requests_tipes[data[0]].handle(data[1])

        print(data)
