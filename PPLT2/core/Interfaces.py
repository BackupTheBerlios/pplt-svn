

class IDisposable:
    def notify_data(self):
        raise NotImplemented("The notify_data() method have to be implemented!");


class IStreamModule:
    def connect(self, address, child = none):
        raise NotImplemented("This connect() method have to be implemented!");

    def read(self, con_id, length):
        raise NotImplemented("This read() method have to be implemented!");

    def write(self, con_id, data):
        raise NotImplemented("This read() method have to be implemented!");

    def disconnect(self, con_id):
        raise NotImplemented("This read() method have to be implemented!");
        
