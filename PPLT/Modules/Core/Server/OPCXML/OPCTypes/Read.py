import ZSI;
import RequestOptions;
import ReadRequestItemList;

class Read_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'Read'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._Options = None
		self._ItemList = None

		TClist = [	RequestOptions.RequestOptions_Def(name="Options", ns=ns, optional=1),
					ReadRequestItemList.ReadRequestItemList_Def(name="ItemList", ns=ns, optional=1),	];

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
	def Get_Options(self):
		return self._Options

	def Set_Options(self,_Options):
		self._Options = _Options

	def Get_ItemList(self):
		return self._ItemList

	def Set_ItemList(self,_ItemList):
		self._ItemList = _ItemList

