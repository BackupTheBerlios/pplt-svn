import ZSI;
import ReadRequestItem;
from ZSIPatch import Struct

class ReadRequestItemList_Def(Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ReadRequestItemList'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Items = None
		self._ItemPath = None;
		self._ReqType = None;
		self._MaxAge = None;


		TClist =	[ReadRequestItem.ReadRequestItem_Def(name="Items", ns=ns, repeatable=1, optional=1), ];

		AttrList =	[ZSI.TC.String(pname="ItemPath", aname="_ItemPath", optional=0),
					ZSI.TC.QName(pname="ReqType", aname="_ReqType"),
					ZSI.TC.Iint(pname="MaxAge", aname="_MaxAge"), ]

		oname = name

		if name:
			aname = '_%s' % name
			if ns:
				oname += ' xmlns="%s"' % ns
			else:
				oname += ' xmlns="%s"' % self.__class__.schema
		else:
			aname = None

		Struct.__init__(	self, self.__class__, TClist, AttrList,
							pname=name, inorder=0,
							aname=aname, oname=oname,
							hasextras=1, **kw)



	def Get_Items(self): return self._Items;
	def Set_Items(self,_Items): self._Items = _Items;
	def Get_ItemPath(self): return(self._ItemPath);
	def Set_ItemPath(self, Path): self._ItemPath = Path;
	def Get_ReqType(self): return(self._ReqType);
	def Set_ReqType(self, Type): self._ReqType = Type;
	def Get_MaxAge(self): return(self._MaxAge);
	def Set_MaxAge(self, Age): self._MaxAge = Age;


	
