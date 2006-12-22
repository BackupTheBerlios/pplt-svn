all: 
	gcc `pkg-config --cflags --libs lintouch-server` -D_GNU_SOURCE -shared ltpyserver.c -o ltpyserver.so

install:
	cp ltpyserver.so /opt/lintouch/lib/lintouch/server-plugins/
