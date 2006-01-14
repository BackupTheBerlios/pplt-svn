import ZSI;
import SubscribeRequestItem;

class SubscribeRequestItemList_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'SubscribeRequestItemList'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Items = None

		TClist = [	SubscribeRequestItem.SubscribeRequestItem_Def(name="Items", ns=ns, repeatable=1, optional=1), ]

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
										hasextras=1, **kw)

	def Get_Items(self):
		return self._Items

	def Set_Items(self,_Items):
		self._Items = _Items


