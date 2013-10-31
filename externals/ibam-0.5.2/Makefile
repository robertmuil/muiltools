# IBAM, the Intelligent Battery Monitor
# Copyright (C) 2001-2003, Sebastian Ritterbusch (IBAM@Ritterbusch.de)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
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
IBAM_VERSION=0.5.2

CC=g++
CFLAGS=-O3 -DIBAM_VERSION=\"$(IBAM_VERSION)\" -Wall

PREFIX=/usr

INSTALL=install -m 755
RM=rm -f
RMDIR=rm -rf
INSTDIR=install -d

all:    ibam

ibam:	ibam.cpp ibam.inl ibam.hpp
	$(CC) $(CFLAGS) ibam.cpp -o ibam

krell:	ibam-krell.so

ibam-krell.so: ibam-krell.o
	$(CC) $(CFLAGS) -fPIC -shared -Wl -o ibam-krell.so ibam-krell.o

ibam-krell.o: ibam-krell.cpp ibam.hpp ibam.inl
	$(CC) $(CFLAGS) -fPIC `pkg-config gtk+-2.0 --cflags` `gdk-pixbuf-config --cflags` -c ibam-krell.cpp

krell1:	ibam-krell1.so

ibam-krell1.so: ibam-krell1.o
	$(CC) $(CFLAGS) -shared -Wl -o ibam-krell1.so ibam-krell1.o

ibam-krell1.o: ibam-krell1.cpp ibam.hpp ibam.inl
	$(CC) $(CFLAGS) -fPIC `gtk-config --cflags` `imlib-config --cflags-gdk` -c ibam-krell1.cpp

install: ibam
	$(INSTALL) ./ibam $(PREFIX)/local/bin/
	-$(INSTALL) ./ibam-krell.so $(PREFIX)/local/lib/gkrellm/plugins/
	-$(INSTALL) ./ibam-krell1.so $(PREFIX)/local/lib/gkrellm/plugins/

source-archive:	clean
	$(RMDIR) ibam-$(IBAM_VERSION)
	mkdir ibam-$(IBAM_VERSION)
	-cp -f * ibam-$(IBAM_VERSION)
	-$(RM) ibam-$(IBAM_VERSION).tar.gz
	tar cvfz ibam-$(IBAM_VERSION).tar.gz ibam-$(IBAM_VERSION)
	$(RMDIR) ibam-$(IBAM_VERSION)

deb:	source-archive
	@echo
	@echo "***************************************"
	@echo "THIS IS UNTESTED - HELP IS APPRECIATED!"
	@echo "***************************************"
	@echo "/me does not know debian... :)"
	dpkg-buildpackage -rfakeroot -us -uc ibam-$(IBAM_VERSION).tar.gz
	-$(RM)	ibam-$(IBAM_VERSION).tar.gz

rpm:	source-archive
	rpm -ta --clean ibam-$(IBAM_VERSION).tar.gz
	-$(RM)	ibam-$(IBAM_VERSION).tar.gz

uninstall:
	$(RM)	$(PREFIX)/local/bin/ibam
	$(RM)	$(PREFIX)/local/lib/gkrellm/plugins/ibam-krell.so

clean:
	$(RMDIR) core ibam ibam-krell.so ibam-krell1.so *.o *~ ibam-*.tar.gz ibam-*.rpm
