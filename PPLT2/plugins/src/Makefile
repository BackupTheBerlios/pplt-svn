OBJ = NULLModule.o HexDumpModule.o LoopbackModule.o RandomModule.o TimeModule.o

all: $(OBJ)
	$(CC) -shared -o PPLTCoreStdPackage.so.2.0.0 $(OBJ)

clean:
	rm -f *.so.*
	rm -f *.o
