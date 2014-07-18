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
		#add some extra san information
		lines.append(sc_hostname + '.info.driveCount ' + str(san_controller['driveCount']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.freePoolSpace ' + str(san_controller['freePoolSpace']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.hotSpareCount ' + str(san_controller['hotSpareCount']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.hotSpareSize ' + str(san_controller['hotSpareSize']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.trayCount ' + str(san_controller['trayCount']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.unconfiguredSpace ' + str(san_controller['unconfiguredSpace']) + ' ' + str(now))
		lines.append(sc_hostname + '.info.usedPoolSpace ' + str(san_controller['usedPoolSpace']) + ' ' + str(now))
		#end extran san information
		sc_vol_analysis_url = server_root_url + api_path + '/storage-systems/' + sc_id + '/analysed-volume-statistics'
		#print sc_vol_analysis_url
		analysed_vols = session.get(sc_vol_analysis_url).json()
		#pprint(analysed_vols)
		#pprint(analysed_vol_statistics)
		for avol in analysed_vols:
			#print '--------------VOL--------------'
			volName =  avol['volumeName']
			rawObsTime = avol['observedTime']
			#print rawObsTime	
			for stat in avol:
				if stat <> 'observedTime' and stat <> 'volumeName' and stat <> 'volumeId':
					#print stat
					#print avol[stat]
					#print sc_hostname + '.volumes.' + volName + '.' + stat + ' ' + str(avol[stat]) + ' ' + str(now)
					lines.append(sc_hostname + '.volumes.' + volName + '.' + stat + ' ' + str(avol[stat]) + ' ' + str(now))
					#print '------stat------'
			#print '-------------End VOL-----------'
		#print '--------------------------------'
		sc_thin_vols_url = server_root_url + api_path + '/storage-systems/' + sc_id + '/thin-volumes/'
		thin_vols = session.get(sc_thin_vols_url).json()
		for thin_vol in thin_vols:
			volName = thin_vol['name']
			
			#will manually grab the stats that I want for the thin volume.
			tvolprefix = sc_hostname +'.volumes.thin_volumes.' + volName + '.'
			lines.append(tvolprefix + 'capacity ' + str(thin_vol['capacity']) + ' ' + str(now))
			lines.append(tvolprefix + 'currentProvisionedCapacity ' + str(thin_vol['currentProvisionedCapacity']) + ' ' + str(now))
			lines.append(tvolprefix + 'initialProvisionedCapacity ' + str(thin_vol['initialProvisionedCapacity']) + ' ' + str(now))
			lines.append(tvolprefix + 'maxVirtualCapacity ' + str(thin_vol['maxVirtualCapacity']) + ' ' + str(now))
			lines.append(tvolprefix + 'provisionedCapacityQuota' + str(thin_vol['provisionedCapacityQuota']) + ' ' + str(now))
			lines.append(tvolprefix + 'totalSizeInBytes' + str(thin_vol['totalSizeInBytes']) + ' ' + str(now))			
	message = '\n'.join(lines) + '\n' #all lines must end in a newline
	print "sending message\n"
	print '-' * 80
	print message
	print
	sock.sendall(message)
	time.sleep(delay)
