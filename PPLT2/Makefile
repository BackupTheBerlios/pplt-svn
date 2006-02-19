corelib = PPLTCore.cs InnerModule.cs Exceptions.cs Message.cs MessageQueue.cs

all: PPLTCore
	mcs -reference:PPLTCore.dll test.cs
PPLTCore:
	mcs -out:PPLTCore.dll -target:library $(corelib)
