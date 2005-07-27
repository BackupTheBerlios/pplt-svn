import ZSI;
import ReplyBase;
import BrowseElement;
import OPCError;



class BrowseResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'BrowseResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._BrowseResult = None
		self._Elements = None
		self._Errors = None
		self._ContinuationPoint = None;
		self._MoreElements = False;


		TClist = [	ReplyBase.ReplyBase_Def(name="BrowseResult", ns=ns, optional=1),
					BrowseElement.BrowseElement_Def(name="Elements", ns=ns, repeatable=1, optional=1),
					OPCError.OPCError_Def(name="Errors", ns=ns, repeatable=1, optional=1), 
					ZSI.TC.String(pname="ContinuationPoint", aname="_ContinuationPoint"),
					ZSI.TC.Boolean(pname="MoreElements", aname="_MoreElements"),	];

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
	def Get_BrowseResult(self):
		return self._BrowseResult

	def Set_BrowseResult(self,_BrowseResult):
		self._BrowseResult = _BrowseResult

	def Get_Elements(self):
		return self._Elements

	def Set_Elements(self,_Elements):
		self._Elements = _Elements

	def Get_Errors(self):
		return self._Errors

	def Set_Errors(self,_Errors):
		self._Errors = _Errors

