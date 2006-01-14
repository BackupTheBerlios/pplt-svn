import ZSI;
import time;
from ZSI import _copyright, _children, _child_elements, \
        _inttypes, _stringtypes, _seqtypes, _find_arraytype, _find_href, \
        _find_type, \
        EvaluateException
from ZSI.TC import TypeCode, Any, _get_object_id
from ZSI.wstools.Namespaces import SCHEMA, SOAP
import re, types

_find_arrayoffset = lambda E: E.getAttributeNS(SOAP.ENC, "offset")
_find_arrayposition = lambda E: E.getAttributeNS(SOAP.ENC, "position")

_offset_pat = re.compile(r'\[[0-9]+\]')
_position_pat = _offset_pat


def _check_typecode_list(ofwhat, tcname):
    '''Check a list of typecodes for compliance with Struct or Choice
    requirements.'''
    for o in ofwhat:
        if not isinstance(o, TypeCode):
            raise TypeError(
                tcname + ' ofwhat outside the TypeCode hierarchy, ' +
                str(o.__class__))
        if o.pname is None:
            raise TypeError(tcname + ' element ' + str(o) + ' has no name')


class Struct(ZSI.TCcompound.Struct):
	def __init__(self, ClassName, TCList, AttrList, **kw):
		self.AttributeList = AttrList;
		ZSI.TCcompound.Struct.__init__(self, ClassName, TCList, **kw);

	def parse(self, elm, ps):
		ret = ZSI.TCcompound.Struct.parse(self, elm, ps);
		for attr in self.AttributeList:
			if not elm.hasAttribute(attr.pname):
				#FIXME: check if optional, else -> exception!
				continue;

			value = elm.getAttribute(attr.pname);

			if isinstance(attr, ZSI.TC.String) or isinstance(attr, ZSI.TC.QName):
				setattr(ret,attr.aname, value);
			elif isinstance(attr, ZSI.TC.gDateTime):
				setattr(ret, attr.aname, int(value));
			elif isinstance(attr, ZSI.TC.Boolean):
				if value == "true":
					setattr(ret, attr.aname, 1);
				else:
					setattr(ret, attr.aname, 0);
			elif isinstance(attr, ZSI.TC.Integer):
				setattr(attr, attr.aname, int(value));
			elif isinstance(attr, ZSI.TC.Decimal):
				setattr(attr, attr.aname, float(value));
			else:
				print "Unknown Type: %s"%str(type(attr));
				#FIXME: raise exception
		return(ret);
				
	def serializeAttr(self, pyobj):
		attrtext="";
		for attr in pyobj.AttributeList:
			pname = attr.pname;
			value = getattr(pyobj, attr.aname, None);
			if value != None:
				if isinstance(attr, ZSI.TC.gDateTime):
					if isinstance(value, int):
						value = time.strftime("%Y-%m-%dT%H:%M:%S.000000-01:00",time.localtime(value))
				attrtext += "%s=\"%s\" "%(pname, value);
			else:
				print "Attr. %s doesn't exists or is None."%attr.aname;
			#FIXME: check optionality, defautls, ...
		return(attrtext.strip());

	def serialize(self, sw, pyobj, inline=None, name=None, attrtext='', **kw):
		if inline or self.inline:
			self.cb(sw, pyobj, name=name, **kw)
		else:
			objid = _get_object_id(pyobj)
			n = name or self.oname or ('E' + objid)
			print >>sw, '<%s%s %s href="#%s"/>' % (n, attrtext, self.serializeAttr(pyobj), objid)
			sw.AddCallback(self.cb, pyobj)

	def cb(self, sw, pyobj, name=None, **kw):
		if not self.mutable and sw.Known(pyobj): return
		objid = _get_object_id(pyobj)
		n = name or self.oname or ('E' + objid)
		if self.inline:
			print >>sw, '<%s %s>' % (n, self.serializeAttr(pyobj));
		else:
			if kw.get('typed', self.typed):
				attrtext = ' xmlns="%s" xsi:type="%s" ' % (self.type[0], self.type[1])
			else:
				attrtext = ''
			print >>sw, '<%s %sid="%s" %s>' % (n, attrtext, objid, self.serializeAttr(pyobj))
		if self.pyclass:
			d = pyobj.__dict__
		else:
			d = pyobj
			if TypeCode.typechecks and type(d) != types.DictType:
				raise TypeError("Classless struct didn't get dictionary")
		for what in self.ofwhat:
			v = d.get(what.aname)
			if v is None:
				v = d.get(what.aname.lower())
			if what.optional and v is None: continue
			try:
				if what.repeatable and type(v) in _seqtypes:
					for v2 in v: what.serialize(sw, v2)
				else:
					what.serialize(sw, v)
			except Exception, e:
				raise Exception('Serializing %s.%s, %s %s' %
					(n, what.aname or '?', e.__class__.__name__, str(e)))

        # ignore the xmlns if it was explicitly stated
		i = n.find('xmlns')
		if i > 0:
			print >>sw, '</%s>' % n[:i - 1]
		else:
			print >>sw, '</%s>' % n

	
