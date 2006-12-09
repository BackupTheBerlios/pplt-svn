# ########################################################################## #
# SequenceConnection.py
#
# 2006-11-23
# Copyright 2006 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #

from SequenceConnection import CSequenceConnection
from Exceptions import ItemBusy
import threading
import logging


class CAsyncSequenceConnection (CSequenceConnection):
    _d_condition = None
    _d_timeout   = None
    _d_logger    = None


    def __init__(self, parent, child = None, timeout=1.0):
        CSequenceConnection.__init__(self, parent, child)
        
        self._d_timeout   = timeout
        self._d_condition = threading.Condition(self._d_buffer_lock)
        self._d_logger    = logging.getLogger("PPLT.core")

        
    def recv(self):
        self._d_logger.debug("Try to get a chunk on anything")
        self._d_condition.acquire()

        if self.autolock():
            self._reserve()

        if len(self._d_buffer) > 0:
            data = self._d_buffer.pop(0)
            
            if self.autolock():
                self._release()
            
            self._d_condition.release()

            return data

        self._d_condition.wait(self._d_timeout)
        if len(self._d_buffer) == 0:
            raise ItemBusy("Timeout while recv() ")

        data = self._d_buffer.pop(0)

        if self.autolock():
            self._release()
        
        self._d_condition.release()
        
        return data


    def push(self, data):
        self._d_logger.debug("push some data...")
        
        self._d_condition.acquire()

        self._d_buffer.append(data)
        
        self._d_logger.debug("Event status in asycSeqCon: %s"%self._d_events_enabled)

        if self._d_events_enabled:
            self._d_condition.release()
            self._d_child_module.notify_data()
            return

        self._d_condition.notify()
        self._d_condition.release()



