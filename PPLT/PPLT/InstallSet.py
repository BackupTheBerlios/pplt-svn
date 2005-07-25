class InstallSet:
	def __init__(self):
		self.__Servers = {};
		self.__Devices = {};
		self.__CoreMods = {};

	def JoinServers(self, Source):
		ServerLst = Source.GetServerList();

		for Server in ServerLst:
			name = Server.GetName();
			if self.__Servers.has_key(name):
				if self.__Servers[name].Version() >= Server.Version():
					continue;
			if isinstance(Source,DataBase):
				
			newServer = Item(Server,Source,);


