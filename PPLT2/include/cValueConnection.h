/***************************************************************************
 *            cValueConnection.h
 *
 *  Sun Apr 23 01:17:48 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
 
#ifndef PPLT_VALUECONNECTION_H
#define PPLT_VALUECONNECTION_H

#include "cConnection.h"
#include "Logging.h"
#include <sys/timex.h>

/**\file cValueConnection.h
 * \brief This file contains the cValueConnection class definitions.
 *
 * This class is the base class for connection between a module that
 * provides data in shape of a value like the iIntegerModule.
 * @see cIntegerConnection */
namespace PPLTCore{
    /** This class defines the basic interface for a connection
     * to a module that provieds data in shape of values.
     *
     * \b Note: Please don't use this class directily to instance a
     * value connection to you module. Use the classes
     * cIntergerConnection, ... instead. */
    class cValueConnection: public cConnection{
        private:
            struct timeval  d_last_update;
            struct timeval  d_cache_time;

        protected:
            /**Updates the timestamp of the last cache update to now.*/
            void UpdateTimestamp();
            /**Retuns true if last_update-now < cache_time */
            bool CacheTimeElapsed();

        public:
            /** Constructor. */
            cValueConnection(cModule *parent, cDisposable *child=0);
            /** Destructor. */
            virtual ~cValueConnection();

            /**Returns the current caching time in seconds.*/
            double CacheTime();
            /**Sets the caching time in seconds.*/
            void CacheTime(double time);

            virtual int Integer() = 0;
            virtual void Integer(int) = 0;

            virtual std::string String() = 0;
            virtual void String(std::string) = 0;
    };

}


#endif
