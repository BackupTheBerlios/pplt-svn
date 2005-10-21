# -*- coding: utf-8 -*-

class BasicException(Exception):
	""" Basic unicode-save exception class """
	def __init__(self, Msg=u""):
		Exception.__init__(self, Msg);
		self.value = Msg;

	def __str__(self): 
		if isinstance(self.value, (str, unicode)): return self.value.decode(errors="replace");
		else: str(self.value);
	def __unicode__(self): 
		if isinstance(self.value, str): return unicode(self.value, errors="replace");
		else: return self.value;


class ImportException(BasicException):
	""" This exception will be raised if a module-list can't be imported. """

class ParseException(BasicException):
	""" This exception will be raised if a imported module-list has the wrong format or
a syntax error. """
