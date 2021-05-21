from vspk import v6 as vspk
import sys
import inspect
import argparse
session = vspk.NUVSDSession(username=u'csproot', password=u'csproot', enterprise=u'csp', api_url=u'https://10.5.0.211:8443')

### Add arguments to vars
parser = argparse.ArgumentParser()
parser.add_argument(dest='operation', choices=[ 'update', 'list' ])
parser.add_argument('-e', '--enterprise', type=str, help="Enterprise Name" )
parser.add_argument('-r', '--policy_id', type=str, help="Routing Policy ID" )
parser.add_argument('-a', '--action', type=str, choices=['ACCEPT', 'REJECT'], help="Default action" )
parser.add_argument('-b', '--blob', type=str, help="XML File name with session blob" )
args = parser.parse_args()

try:
    session.start()
except:
    print ('ERROR: Failed to start the session')
##..

try:
    file = open(args.blob)
    blob = file.read().replace("\n", " ")
    file.close()
except:
    print ('ERROR: Failed to open XML file with session blob')

csprootSession = session.user
myent = csprootSession.enterprises.get_first(filter="name == " + "'" + args.enterprise + "'")
print ("Looking into Enterprise: '" + myent.name + "' with ID:" + myent.id)

## List subnets
if args.operation == "list" :
    myrps = myent.routing_policies.get()
    for temp in myrps:
        print (temp.name + " ID: " + temp.id)
#..

if args.operation == "update" :
    myrps = myent.routing_policies.get_first(filter="ID == " + "'" + args.policy_id + "'")
    myrps.default_action=args.action
    myrps.policy_definition=blob
    myrps.save()
    print (myrps.name + " ID:" + myrps.id)
  
#..
