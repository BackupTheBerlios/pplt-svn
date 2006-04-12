#include "../include/Logging.h"

using namespace PPLTCore;
using namespace log4cplus;
using namespace log4cplus::helpers;

void PPLTCore::initLogging(){
    SharedObjectPtr<Appender>  app(new ConsoleAppender());
    app->setName("ConLog");
    std::string pattern = "[%t] %-5p %c{2} - %m [%l]%n";
    app->setLayout( std::auto_ptr<Layout>(new PatternLayout(pattern)));
    Logger::getRoot().addAppender(app);
}

void Log(Logger log, int level, const char* file, int line, std::string func_name, std::string pat){
    log.forcedLog((LogLevel)level, pat, file, line);
}
