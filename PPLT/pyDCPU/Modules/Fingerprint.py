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

import md5;

def Fingerprint(Name, Parent = None, Address = None, TypeName = None, 
                Parameter = None, DefaultUser = None, CacheTime = None, 
                Root = None):
    """ Calc a fingerprint from parameters, name, etc... """
    fingerprint = md5.new(Name);
    if Parent:
        fingerprint.update(Parent);
    if Address:
        fingerprint.update(Address);
    if TypeName:
        fingerprint.update(TypeName);
    if DefaultUser:
        fingerprint.update(DefaultUser);
    if CacheTime != None:
        fingerprint.update(str(CacheTime));
    if Root:
        fingerprint.update(Root);
    if Parameter:
        ParaLst = Parameter.keys();
        ParaLst.sort();
        for Para in ParaLst:
            fingerprint.update(str(Para)+str(Parameter[Para]));
    return(fingerprint.hexdigest());
