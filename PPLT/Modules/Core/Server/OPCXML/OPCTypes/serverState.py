import ZSI;
import __init__ as ns1;

class serverState_Def(ZSI.TC.String):
	tag = "tns:serverState"
	def __init__(self, name=None, ns=None, **kw):
		aname = None
		if name:
			kw["pname"] = name
			kw["aname"] = "_%s" % name
			kw["oname"] = '%s xmlns:tns="%s"' %(name,ns1.targetNamespace)
		ZSI.TC.String.__init__(self, **kw)

