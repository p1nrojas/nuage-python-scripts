from vspk import v6 as vspk
import sys
import inspect
import argparse
session = vspk.NUVSDSession(username=u'csproot', password=u'csproot', enterprise=u'csp', api_url=u'https://10.5.0.211:8443')

### Add arguments to vars
parser = argparse.ArgumentParser()
parser.add_argument(dest='operation', choices=['zonecreate', 'subnetcreate', 'subnetlist' ])
parser.add_argument('-d', '--domain', type=str, help="Domain name" )
parser.add_argument('-s', '--subnet', type=str, help="Subnet name" )
parser.add_argument('-z', '--zone', type=str, help="Zone name" )
parser.add_argument('-a', '--address', type=str, help="IP Address and Mask" )
parser.add_argument('-g', '--gateway', type=str, help="IP Gateway of the subnet" )
parser.add_argument('-n', '--netmask', type=str, help="IP Netmask of the subnet" )
#parser.add_argument('-d', '--domain', type=str, help="Domain Name" )
args = parser.parse_args()

try:
    session.start()
except:
    print ('ERROR: Failed to start the session')
##..

csprootSession = session.user
csprootSession.enterprises.fetch()
mydomain = csprootSession.domains.get_first(filter="name == " + "'" + args.domain + "'")


## List subnets
if args.operation == "list" :
    mysubnets = mydomain.subnets.get()
    for temp in mysubnets:
        print (temp.name)
#..

if args.operation == "zonecreate" :
    myzone = vspk.NUZone(name=args.zone)
    mydomain.create_child(myzone)
    print (myzone)
#..

if args.operation == "subnetcreate" :
    myzone = csprootSession.zones.get_first(filter="name == " + "'" + args.zone + "'")
    mysubnet = vspk.NUSubnet(name=args.subnet, address=args.address, netmask=args.netmask, gateway=args.gateway)
    myzone.create_child(mysubnet)
    print (mysubnet)
  
