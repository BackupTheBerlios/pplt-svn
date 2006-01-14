import ZSI;
import QualityBits;
import LimitBits;



class OPCQuality_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'OPCQuality'

	def __init__(self, name=None, ns=None, **kw):
		self._QualityField = "good";
		self._LimitField = "none";
		self._VendorField = 0;

		TClist = [	QualityBits.qualityBits_Def(name="QualityField"),
					LimitBits.limitBits_Def(name="LimitField"),
					ZSI.TC.IunsignedByte(pname="VendorField", aname="_VendorField"),	];

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

