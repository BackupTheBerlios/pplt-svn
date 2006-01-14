import ZSI;
import ItemProperty;

class PropertyReplyList_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'PropertyReplyList'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Properties = None
		self._ItemPath = None;
		self._ItemName = None;
		self._ResultID = None;

		TClist = [	ItemProperty.ItemProperty_Def(name="Properties", ns=ns, repeatable=1, optional=1),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),
					ZSI.TC.QName(pname="ResultID", aname="_ResultID"),	];

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
										hasextras=1, **kw);

	def Get_Properties(self):
		return self._Properties

	def Set_Properties(self,_Properties):
		self._Properties = _Properties


