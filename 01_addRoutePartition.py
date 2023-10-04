"""AXL <addPhone> sample script, using the zeep library

__author__  = "Ilker MANSUR"
__version__ = "1.0"

"""

from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from requests.auth import HTTPBasicAuth

disable_warnings(InsecureRequestWarning)

username = 'axluser'
password = '1Qaz2Wsx'
fqdn = '198.18.133.3'
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'axlsqltoolkit/schema/current/AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
axl = client.create_service(binding, address)

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))     


try:
    add_partition = axl.addRoutePartition (routePartition= {'name' : 'Local_PT',
                                                            'description' : 'Test Partition'})

except:
    show_history()