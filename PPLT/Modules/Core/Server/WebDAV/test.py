#!/usr/bin/python
import pyDCPU
import PPLT
from twisted.application import internet, service
from twisted.web import static
from akadav.davserver import Site
from twisted.web import static


core = pyDCPU.Core(UserDBFile="/usr/PPLT/UserDB.xml");

rand = core.MasterTreeAdd(None, "Master.Debug.Random", None, {});
rand_slot = core.MasterTreeAttachSymbolSlot(rand, "DWord", "DWord");

core.SymbolTreeCreateSymbol("/test",rand_slot);
print "TEST: %s"%str(core.SymbolTreeGetValue("/test"));


APP_ARG = {};
APP_ARG.update( {"uid":500} );
APP_ARG.update( {"gid":100} );

SITE_ARGS = {"logPath":"/home/hannes/PPLT/test.log"};


application = service.Application("pyDCPU");
serviceCollection = service.IServiceCollection(application);

root = static.Data("""<html><head></head><body>Test</body></html>""","text/html");

site = Site(root,**SITE_ARGS);
server = internet.TCPServer(4711,site);
server.setServiceParent(serviceCollection);
#server.startService();

while True:
	pass;
