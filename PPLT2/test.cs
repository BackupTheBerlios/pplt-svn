using System;
using System.Collections;
using PPLTInnerModule;
using PPLTMessages;
using PPLTSymbol;

class testProg{
    static void Main(){
        IfInnerModule mod = new RandomGenerator("test");
        IfInnerModule mod2 = new HexDump("hex");
        Symbol sym = new Symbol("sm", "test");
        mod.Register(mod2,"Bool");
        mod2.Register(sym);
        Console.WriteLine("Module and symbol loaded... get value.");
        Console.WriteLine("Symbol returned: {0}",sym.Value);
        Console.WriteLine("Symbol type: {0}.",sym.Type);
    }
}    