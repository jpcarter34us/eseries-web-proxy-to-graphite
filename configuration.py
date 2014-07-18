import requests

#Parameters
server_root_url = 'http://localhost:8080'
api_version = 2
api_path = '/devmgr/v{version}'.format(version=api_version)

#Specify username and password for the api here. User should have read/write access.
auth = ('rw', 'rw')

#Create a persistent session with the follow settings
session = requests.Session()
session.verify = False # Verify SSL certificate
session.auth = auth  # Configure HTTP Authentication
session.headers.update({'Content-type': 'application/json'}) #Input for PUT/POST is always json
session.headers.update({'Accept': 'application/json'}) #Always expect to receive a json

base_url = server_root_url + api_path

#resource paths
resources = {
'storage-systems': '/storage-systems',
'storage-system': "/storage-systems/{array_id}",
'pools': "/storage-systems/{array_id}/storage-pools",
'pool': "/storage-systems/{array_id}/storage-pools/{id}",
'drives': "/storage-systems/{array_id}/drives",
'drive': "/storage-systems/{array_id}/drives/{id}",
'volumes': "/storage-systems/{array_id}/volumes",
'volume': "/storage-systems/{array_id}/volumes/{id}",
'thin_volumes' : "/storage-systems/{array_id}/thin-volumes",
'thin_volume' : "/storage-systems/{array_id}/thin-volume/{id}",
'snapshot_groups': "/storage-systems/{array_id}/snapshot-groups",
'snapshot_group': "/storage-systems/{array_id}/snapshot-groups/{id}",
'snapshot_views': "/storage-systems/{array_id}/snapshot-volumes",
'snapshot_view': "/storage-systems/{array_id}/snapshot-volumes/{id}",
'snapshots': "/storage-systems/{array_id}/snapshot-images",
'snapshot': "/storage-systems/{array_id}/snapshot-images/{id}",
'volume_copies' : "/storage-systems/{array_id}/volume-copy-jobs",
'volume_copy' : "/storage-systems/{array_id}/volume-copy-jobs/{id}",
'volume_copy_control' : "/storage-systems/{array_id}/volume-copy-jobs-control/{id}",
'analysed_volume_statistics': "/storage-systems/{array_id}/analysed-volume-statistics",
'volume_statistics': "/storage-systems/{array_id}/volume-statistics",
'volume_statistic' : '/storage-systems/{array_id}/volume-statistics/{id}',
'analysed-drive_statistics': "/storage-systems/{array_id}/analysed-drive-statistics",
'drive_statistics': "/storage-systems/{array_id}/drive-statistics",
'drive_statistic' : '/storage-systems/{array_id}/drive-statistics/{id}',
'volume_mappings': "/storage-systems/{array_id}/volume-mappings",
'volume_mapping': "/storage-systems/{array_id}/volume-mappings/{id}",
'host_groups': '/storage-systems/{array_id}/host-groups',
'host_group': '/storage-systems/{array_id}/host-groups/{id}',
'hosts': '/storage-systems/{array_id}/hosts',
'host': '/storage-systems/{array_id}/hosts/{id}',
'host_ports' : '/storage-systems/{array_id}/host-ports',
'host_port' : '/storage-systems/{array_id}/host-ports/{id}',
'host_types' : '/storage-systems/{array_id}/host-types',
'events' : "/storage-systems/{array_id}/mel-events?count=8192",
'critical_events' : "/storage-systems/{array_id}/mel-events?critical=true",
'hardware' : "/storage-systems/{array_id}/hardware-inventory/",
'graph' : "/storage-systems/{array_id}/graph/",
'symbol': "/storage-systems/{array_id}/symbol/{command}/"
}