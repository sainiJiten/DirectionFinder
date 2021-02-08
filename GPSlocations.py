from bluetooth import *
import math

class LatLong:
    def __init__(self):
        self.uuid = "237ec270-2bcf-46ad-bffe-138659617d87"
        self.R = 6371.0

    def connect(self):
        self.server_sock=BluetoothSocket( RFCOMM )
        self.server_sock.bind(("",PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]
        advertise_service( self.server_sock, "GPSPiServer",service_id = self.uuid,service_classes = [ self.uuid, SERIAL_PORT_CLASS ],profiles = [ SERIAL_PORT_PROFILE ])
        print("Waiting for connection on RFCOMM channel %d" % self.port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)

    
    def values(self):
        try:
            data = self.client_sock.recv(1024)
            s = data.decode("utf-8")
            return s
        except IOError:
            return "Connection failed"

    def disconnect(self):
        self.client_sock.close()
        print("BT Connection closed")
    
    def distance(self,l1,l2):
        lat1 = math.radians(l1[0])
        lon1 = math.radians(l1[1])
        lat2 = math.radians(l2[0])
        lon2 = math.radians(l2[1])
        dlon = lon2 - lon1  
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = self.R * c
        return dist
