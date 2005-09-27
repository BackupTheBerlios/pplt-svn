import PPLT;
import gettext;
import logging;

def InitI18N(BasePath, Lang="en", AltLang="en"):
    logger = logging.getLogger("PPLT");

    logger.debug("Try to find languages (%s,%s) in basepath %s"%(Lang,AltLang,BasePath));
    try:
        tr = gettext.translation("PPLT",BasePath,[Lang,AltLang]);
    except:
        logger.error("No translation found for %s or %s."%(Lang,AltLang));
        tr = gettext.NullTranslations();
    tr.install(unicode=1);
