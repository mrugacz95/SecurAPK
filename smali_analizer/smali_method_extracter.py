import re

from antlr4 import FileStream, ParseTreeWalker, CommonTokenStream

from smali_analizer.SmaliLexer import SmaliLexer, ParseTreeListener
from smali_analizer.SmaliParser import SmaliParser, ParserRuleContext


def smali_package_to_dot_notataion(package):
    package = package[1:-1]
    return re.sub("/", ".", package)


smali_type_to_normal = {
    'V': 'void',  # can only be used for return types
    'Z': 'boolean',
    'B': 'byte',
    'S': 'short',
    'C': 'char',
    'I': 'int',
    'J': 'long',
    'F': 'float',
    'D': 'double',
}


def resolve_type(type):
    array_count = 0
    while type[0] == '[':
        array_count += 1
        type = type[1:]
    if type in smali_type_to_normal:
        type = smali_type_to_normal[type]
    else:
        type = smali_package_to_dot_notataion(type)
    for i in range(array_count):
        type += "[]"
    return type


class SmaliListener(ParseTreeListener):
    def enterFm5c(self, ctx: ParserRuleContext):
        path = ctx.method.text
        package, method = re.split("->", path)
        package = smali_package_to_dot_notataion(package)
        method, returns = re.findall("([a-zA-Z;<>$0-9]+\([\[a-zA-Z/;$0-9]*\))(.*)", method)[0]
        returns = resolve_type(returns)
        params = []
        method, all_params = re.findall("([a-zA-Z;<>$0-9]+)\((.*)\)", method)[0]
        for param in re.finditer("(\[+[VZBSCIJFD]|(L[a-zA-Z$0-9./]+;))", all_params):
            params.append(resolve_type(param.group(0)))
        print(f"<{package}: {returns} {method}({','.join(params)})>")


def analize(apk_path):
    input = FileStream(apk_path)
    lexer = SmaliLexer(input)
    stream = CommonTokenStream(lexer)
    parser = SmaliParser(stream)
    tree = parser.sFiles()
    printer = SmaliListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
