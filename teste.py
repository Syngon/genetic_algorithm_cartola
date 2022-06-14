sentencas = {
    'program': '  \"begin\" declaration-list \"end\" ',
    'declaration-list': '  declaration [ \";\" declaration ] ',
    'declaration': ' variable-declaration | function-declaration  ',
    'variable-declaration': '  type-specifier [\"[\"\"]\"]  ',
    'var-decl-list': '  [ var-decl-id \",\"] var-decl-id ',
    'var-decl-id': '  \"Identifier\" [\"[\" \"Integer-Number\" \"]\"] ',
    'type-specifier': '  \"float\" | \"int\" | \"string\" | \"bool\" | \"char\" ',
    'function-declaration': '  type-specifier \"Function\" \"(\" params \")\" statement ',
    'params': '  [ param-list ] ',
    'param-list': '  param-type-list [\";\" param-type-list ] ',
    'param-type-list': '  type-specifier param-id-list ',
    'param-id-list': '  param-id [\";\" param-id ] ',
    'param-id': '  \"Identifier\" [\"[\" \"Integer-Number\" \"]\"] ',
    'compound-stmt': '  \"{\" local-declarations statement-list \"}\" ',
    'local-declarations': '  [ variable-declaration ] ',
    'statement-list': '  [ statement ] ',
    'statement': '  expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | break-stmt ',
    'expression-stmt': '  [ expression ] \";\" ',
    'selection-stmt': '  \"if\" \"(\" expression \")\" statement [ \"else\" statement ] ',
    'iteration-stmt': '  \"while\" \"(\" expression \")\" statement ',
    'return-stmt': '  \"return\" [ expression ] \";\" ',
    'break-stmt': '  \"break\" \";\" ',
    'expression': '  [ var \"=\" ] simple-expression  ',
    'var': '  \"Identifier\" [\"[\" \"Integer-Number\" \"]\"] ',
    'simple-expression': '  [ or-expression \"|\" ] or-expression ',
    'or-expression': '   unary-rel-expression [ & unary-rel-expression ] ',
    'unary-rel-expression': '  [\"!\"] rel-expression ',
    'rel-expression': '  add-expression [ relop add-expression ] ',
    'relop': '  \"=\" | \">\" | \">=\" | \"<\" | \"<=\" | \"==\" | \"!=\" | \"#\" ',
    'add-expression': '  term [ addop term ] ',
    'addop': '  \"+\" | \"-\" ',
    'term': '  unary-expression [ mulop unary-expression ] ',
    'mulop': '  \"*\" | \"/\" ',
    'unary-expression': '  [\"-\"] factor ',
    'factor': '  \"(\" expression \")\" | var | detour | constant  ',
    'constant': '  number | string | \"false\" | \"true\" ',
    'number': '  \"Integer-number\" | \"Float-number\"  ',
    'string': '  \"Constant-String\" | \"Character\" ',
    'detour': '  \"Function\" \"(\" args \")\" ',
    'args': '  [ arg-list ]  ',
    'arg-list': ' expression '
}

count = 0

def teste(sentencas):
    global count
    for key in reversed(sentencas):
        apaga = False
        for key2 in reversed(sentencas):
            if key == key2:
                continue

            if ' {} '.format(key) in sentencas[key2] and sentencas[key] != "":
                print("O QUE VAI ADD: {} -> {}\nO QUE VAI SOFRER MUDANCA: {} -> {}\nO QUE VIROU: {}\n\n\n".format(key, sentencas[key], key2, sentencas[key2], sentencas[key2].replace(key, sentencas[key])))
                sentencas[key2] = sentencas[key2].replace(key, "( {} )".format(sentencas[key])).replace("    ", " ").replace("   ", " ").replace("  ", " ")
                count += 1
                apaga = True

        if apaga:
            sentencas[key] = ""
            apaga = False


def get_by_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")

def teste2(sentencas):
    for key in reversed(sentencas):
        apaga = False
        done = False
        count = len(sentencas) - 1
        count_ciclos = 0

        while done is False:
            if count <= 0:
                count = len(sentencas) - 1

            if ' {} '.format(key) in sentencas[get_by_key(sentencas, count)] and sentencas[key] != "":
                print("O QUE VAI ADD: {} -> {}\nO QUE VAI SOFRER MUDANCA: {} -> {}\nO QUE VIROU: {}\n\n\n".format(key, sentencas[key], key2, sentencas[get_by_key(sentencas, count)], sentencas[get_by_key(sentencas, count)].replace(key, sentencas[key])))
                sentencas[key2] = sentencas[get_by_key(sentencas, count)].replace(key, sentencas[key]).replace("    ", " ").replace("   ", " ").replace("  ", " ")
                apaga = True

            count -= 1
            count_ciclos += 1

            for key2 in sentencas:
                if ' {} '.format(key2) in sentencas[key] and sentencas[key2] != "":
                    count_ciclos = 0

            if count_ciclos > 100:
                done = True

        if apaga:
            sentencas[key] = ""
            apaga = False





teste(sentencas)

for line in sentencas:
    if sentencas[line] != '':
        print('KEY: {} \nChave: {} \n\n\n'.format(line, sentencas[line]))

# teste(sentencas)
#
# for line in sentencas:
#     if sentencas[line] != '':
#         print('KEY: {} \nChave: {} \n\n\n'.format(line, sentencas[line]))

print(count)