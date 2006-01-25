import pyDCPU;

core = pyDCPU.Core();

rand = core.MasterTreeAdd(None, "Master.Debug.Random", None, None);

core.SymbolTreeCreateSymbol("/bool", rand, "Bool");
core.SymbolTreeCreateSymbol("/int", rand, "Integer");
core.SymbolTreeCreateSymbol("/float", rand, "Float");
core.SymbolTreeCreateSymbol("/str", rand, "String");
core.SymbolTreeCreateSymbol("/a_bool", rand, "ArrayBool");
core.SymbolTreeCreateSymbol("/a_int", rand, "ArrayInteger");
core.SymbolTreeCreateSymbol("/a_float", rand, "ArrayFloat");
core.SymbolTreeCreateSymbol("/a_str", rand, "ArrayString");
core.SymbolTreeCreateSymbol("/stream", rand, "Stream");
core.SymbolTreeCreateSymbol("/sequence", rand, "Sequence");

print  core.SymbolTreeGetValue("/bool");
print  core.SymbolTreeGetValue("/int");
print  core.SymbolTreeGetValue("/float");
print  core.SymbolTreeGetValue("/str");
print  core.SymbolTreeGetValue("/a_bool");
print  core.SymbolTreeGetValue("/a_int");
print  core.SymbolTreeGetValue("/a_float");
print  core.SymbolTreeGetValue("/a_str");
print  core.SymbolTreeRead("/stream",79);   # read max. 79 bytes
print  core.SymbolTreeRead("/sequence");    # read sequence
