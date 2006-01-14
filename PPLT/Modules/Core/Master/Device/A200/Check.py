import logging;
import pyDCPU;


def A200Check(Con):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Con, pyDCPU.MasterConnection):
        Logger.error("This is not a valid Connection");
        return(False);

    Con.flush();
    Con.write('%S');

    line = Con.read(2048);
    if line == '%U':
        return(None);
    list = line.split(',');
    return(list);
