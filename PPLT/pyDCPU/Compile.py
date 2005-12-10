# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
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

import zipfile;
import imp;
import marshal;
import time;

def Compile(ZipFile):
    """ This function compiles all python files inside a ZIP archive. """
    ZIP = zipfile.PyZipFile(ZipFile, mode="a");
    Files = ZIP.namelist();
    for FileName in Files:
        if not FileName[-3:] == ".py": continue;    # compile onyl python
        if FileName+"c" in Files: continue;         # do not recomplile
        src_data = ZIP.read(FileName);
        src_info = ZIP.getinfo(FileName);
        timestamp = int(time.time());
        if src_data[-1] != "\n": src_data += "/";
        src_data.replace("\r\n","\n");  #windows->unix
        src_data.replace("\r","\n");    #mac->unix
        
        bin_obj  = compile(src_data,"<string>","exec");
        # assamble .pyc file
        bin_str = imp.get_magic();
        bin_str += chr(timestamp      &0xff);
        bin_str += chr((timestamp>>8) &0xff);
        bin_str += chr((timestamp>>16)&0xff);
        bin_str += chr((timestamp>>24)&0xff);
        bin_str += marshal.dumps(bin_obj);
        
        ZIP.writestr(FileName+"c",bin_str);
        print "Compile: %s(%i)\t\t -> (%i)"%(FileName, len(src_data), len(bin_str));
    ZIP.close();
    

if __name__=="__main__":
    Compile("/usr/PPLT/Export/JVisu.zip");
