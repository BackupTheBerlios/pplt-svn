# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for master-slave      #
# based communication.                                                        #
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #

# lockMessage:
#   + wenn diese Nachricht ein Modul erreicht, hat allein der sendene Thread 
#     das Recht mit seinen Kinder/Eltern (je nach Richtung) zu kommunizieren!
#   + diese Sperre kann nur durch eine unlogMessage vom selben thread, oder
#     vom system entfernt werden.
#   + Das bedeutet vor allem für Interface-Module, dass sie keine PushMessages
#     aussenden dürfen, sondern lediglich die emfangenen Daten einer PopMessage
#     des threads zur Verfügung stellen müssen.

class lockMessage:
    def __init__(self, threadID):
        self._ThreadID = threadID;

    def getThreadID(self): return self._ThreadID;
    

    
class unlockMessage:
    def __init__(self, threadID):
        self._ThreadID = threadID;
    
    def getThreadID(self): return self._ThreadID;


class popMessage:
    pass;


class pushMessage:
    pass;

