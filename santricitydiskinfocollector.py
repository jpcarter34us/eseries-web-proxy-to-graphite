import requests
#import pprint
from pprint import pprint
import json
#from datatime import datetime
import calendar
import time
from socket import socket

server_root_url = 'http://localhost:8080'
api_version = 2
api_path = '/devmgr/v{version}'.format(version=api_version)

#CARBON Session Establishment
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
#delay = 25
delay = 15
sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

session = requests.Session()
session.verify = False
session.headers.update({'Content-type' : 'application/json'})
session.headers.update({'Accept' : 'application/json'})
while True:
        base_auth_url = server_root_url + '/devmgr/utils/login?uid=ro&pwd=ro'

        session.get(base_auth_url)

        storage_systems_url = server_root_url + api_path + '/storage-systems'
        san_controllers = session.get(storage_systems_url).json()
        lines = []
        for san_controller in san_controllers:
                now = int( time.time() )
                sc_id = san_controller['id']
                sc_hostname = san_controller['name']
                sc_disk_analysis_url = server_root_url + api_path + '/storage-systems/' + sc_id + '/analysed-drive-statistics'
                #print sc_vol_analysis_url
                analysed_disks = session.get(sc_disk_analysis_url).json()
                for adisk in analysed_disks:
                        #print '--------------VOL--------------'
                        diskName =  adisk['diskId']
                        rawObsTime = adisk['observedTime']
                        #print rawObsTime
                        for stat in adisk:
                                if stat <> 'observedTime' and stat <> 'diskId' and stat <> 'volumeId':
                                        #print stat
                                        #print avol[stat]
                                        #print sc_hostname + '.volumes.' + volName + '.' + stat + ' ' + str(avol[stat]) + ' ' + str(now)
                                        lines.append(sc_hostname + '.disks.' + diskName + '.' + stat + ' ' + str(adisk[stat]) + ' ' + str(now))
                                        #print '------stat------'
                        #print '-------------End VOL-----------'
                #print '--------------------------------'
        message = '\n'.join(lines) + '\n' #all lines must end in a newline
        print "sending message\n"
        print '-' * 80
        print message
        print
        sock.sendall(message)
        time.sleep(delay)
