import sys
import socket
from lru_cache import lru_cache
from bloom_filter import BloomFilter
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT,serialize_DELETE
from node_ring import NodeRing


BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()
    
    def put(self,value):

      client_ring = NodeRing(NODES)
      data_bytes, key = serialize_PUT(value)
      server = client_ring.get_node(key)
      udp_client.host = server['host']
      udp_client.port = server['port']
      response = udp_client.send(data_bytes)
      return key
    
    @lru_cache(5)
    def get(self,key):
      client_ring = NodeRing(NODES)
      data_bytes, key = serialize_GET(key)
      server = client_ring.get_node(key)
      udp_client.host = server['host']
      udp_client.port = server['port']
      response = udp_client.send(data_bytes)
         
      return response
    
    def delete(self,key):
      client_ring = NodeRing(NODES)
      data_bytes, key = serialize_DELETE(key)
      server = client_ring.get_node(key)
      udp_client.host = server['host']
      udp_client.port = server['port']
      response = udp_client.send(data_bytes)
      return response


bloomfilter = BloomFilter(20,0.05)

@lru_cache(5)
def get(key):
    global bloomfilter
    
    if bloomfilter.is_member(key):
        return udp_client.get(key)
    else:
        return None
        
def put(value):
    global bloomfilter
    key = udp_client.put(value)
    bloomfilter.add(key)
    return key

def delete(key):
    global bloomfilter
    if bloomfilter.is_member(key):
        return udp_client.delete(key)
    else:
        return None




if __name__ == "__main__":
    
    udp_client = UDPClient(0,0)
    hash_codes = set()
    
    #PUT all users
    for u in USERS:
        key = put(u)
        print(key)
        hash_codes.add(key)
    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    #DELETE key
    print(delete('4cc00164086b6002dcfe67b2e82d465f'))

    #GET key
    print(get('77086357f450285ec1afdcfd00741755'))

    #Try to GET the deleted key --> failed
    print(get('4cc00164086b6002dcfe67b2e82d465f'))





    

    