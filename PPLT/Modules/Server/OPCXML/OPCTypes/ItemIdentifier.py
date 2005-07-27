import ZSI;

class ItemIdentifier_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ItemIdentifier'

	def __init__(self, name=None, ns=None, **kw):

		self._ItemPath = None;
		self._ItemName = None;

		TClist = [	ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),	];

		oname = name

		if name:
			aname = '_%s' % name
			if ns:
				oname += ' xmlns="%s"' % ns
			else:
				oname += ' xmlns="%s"' % self.__class__.schema
		else:
			aname = None

		ZSI.TCcompound.Struct.__init__(	self, self.__class__, TClist,
										pname=name, inorder=0,
										aname=aname, oname=oname,
										**kw)

