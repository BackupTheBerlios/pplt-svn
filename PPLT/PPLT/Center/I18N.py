import PPLT;
import gettext;
import logging;

def InitI18N():
	conf = PPLT.Config();
	logger = logging.getLogger("PPLT");

	lang1 = conf.GetLang();
	lang2 = conf.GetAltLang();
	bpath = conf.GetBasePath();

	logger.debug("Try to find languages (%s,%s) in basepath %s"%(lang1,lang2,bpath));
	try:
		tr = gettext.translation("PPLT",bpath,[lang1,lang2]);
	except:
		logger.error("No translation found for %s or %s."%(lang1,lang2));
		tr = gettext.NullTranslations();
	tr.install(unicode=1);
