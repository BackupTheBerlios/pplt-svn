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

import xml.dom.minidom;
import os.path;
import zipfile;
import shutil;
import string;
import logging;

""" This module install PPLT-Modules """

def InstallDCPUMod(FileName,Name,InGroup,ModulePath):
	logger = logging.getLogger("PPLT");
	if not os.path.exists(FileName):
		logger.error("Error %s not found"%FileName);
		return(False);

	if not zipfile.is_zipfile(FileName):
		logger.error("Invalid or damaged ZIP");
		return(False);

	grplst = InGroup.split('.');
	pathlst = [ModulePath];
	for item in grplst:
		if item != '':
			pathlst.append(item);

	dirname =  os.path.normpath(string.join(pathlst,'/'));
	logger.info("Install %s to %s"%(FileName,dirname));
	if not os.path.isdir(dirname):
		try:
			os.makedirs(dirname,0755);
		except:
			logger.error("Error while create dir %s"%dirname);
			return(False);
	try:
		shutil.copy(FileName, dirname+'/'+Name+'.zip');
	except:
		logger.error("Error while copy file %s"%FileName);
		return(False);
	return(True);



def InstallPPLTMod(FileName, ModulePath):
	#construct new filepath
	logger = logging.getLogger("PPLT");
	dest = os.path.normpath(os.path.join(ModulePath,'Mods'));
	filename = os.path.normpath(os.path.join(dest, os.path.basename(FileName)));

	logger.info("Install %s"%FileName);

	if not os.path.isdir(dest):
		try:
			os.makedirs(dest,0755);
		except:
			logger.error("Error while create dir %s"%dest);
			return(False);
	try:
		shutil.copy(FileName, filename);
	except:
		logger.error("Error while copy file %s"%FileName);
		return(False);
	return(True);



def InstallSet(FileName, ModulePath):
	logger = logging.getLogger("PPLT");
	doc = xml.dom.minidom.parse(FileName);
	coremodlist = doc.getElementsByTagName('DCPUMod');
	ppltmodlist = doc.getElementsByTagName('PPLTMod');

	zipdir = os.path.dirname(os.path.abspath(FileName));
   
	for mod in coremodlist:
		fname = os.path.join(zipdir,mod.getAttribute('file'));
		name = mod.getAttribute('as');
		group = mod.getAttribute('in');
		if not InstallDCPUMod(fname, name, group, ModulePath):
			logger.error("Error while install %s"%name);
				
	for mod in ppltmodlist:
		fname = os.path.join(zipdir,mod.getAttribute('file'));
		if not InstallPPLTMod(fname, ModulePath):
			logger.error("Error while install %s"%fname);

	return(True);
        
