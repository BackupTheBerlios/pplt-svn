import ZSI;
import ItemValue;

class SubscribeItemValue_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'SubscribeItemValue'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._ItemValue = None
		self._RevisedSamplingRate = None;

		TClist = [	ItemValue.ItemValue_Def(name="ItemValue", ns=ns, optional=1),
					ZSI.TC.Iint(pname="RevisedSamplingRate", aname="_RevisedSamplingRate"),	];

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

	def Get_ItemValue(self):
		return self._ItemValue

	def Set_ItemValue(self,_ItemValue):
		self._ItemValue = _ItemValue


