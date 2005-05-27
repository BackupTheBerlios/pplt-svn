# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
# communication.                                                               # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 # 
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    # 
# ############################################################################ # 

# Changelog:
# 2005-05-27:
#	Release as version 0.2.0


import logging;
import sys;

def Logger(Level,File,SysLog):
    
    Logger = logging.getLogger("PPLT");

    if not Level == 'off':
        if SysLog:
            if sys.platform == 'linux2':
                try:
                    LogHndl = logging.SysLogHandler();
                except:
                    LogHndl = logging.StreamHandler(sys.stderr);
            else:
                try:
                    LogHndl = NTEventLogHandler('PPLT');
                except:
                    LogHndl = logging.StreamHandler(sys.stderr);
        elif File:
            LogHndl = logging.FileHandler(File);
        else:
            LogHndl = logging.StreamHandler(sys.stderr);
            
        LogFmt = logging.Formatter('PPLT: %(asctime)s %(levelname)s: %(filename)s('
                               '%(lineno)d): %(message)s');
        LogHndl.setFormatter(LogFmt);
        Logger.addHandler(LogHndl);
        if Level == 'debug':
            Logger.setLevel(logging.DEBUG);
        elif Level == 'info':
            Logger.setLevel(logging.INFO);
        elif Level == 'warning':
            Logger.setLevel(logging.WARNING);
        elif Level == 'error':
            Logger.setLevel(logging.ERROR);
        else:
            #default level: error;
            Logger.setLevel(logging.ERROR);
    Logger.info("Start logging");
    return(Logger);
