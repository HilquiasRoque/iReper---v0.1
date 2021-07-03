# Todas as funções usadas no Main
import random
import json


def checkArquivo(nome_arquivo):
    try:
        a = open(nome_arquivo, 'r')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def load_create_Arquivo_dic(arq_nome, var_nome):
    if checkArquivo(arq_nome):
        with open(arq_nome, 'r') as file_json:
            temp_var = json.loads(file_json.read())
            var_nome.update(temp_var)
    else:
        open(arq_nome, 'w').write(json.dumps(var_nome))


def copyData_toDict(musica, autor, temas, dicio):
    while True:
        idmus = generateID()
        if idmus in dicio.keys():
            continue
        else:
            break
    tmslst = temas.split(', ')
    templist = [musica, autor, 0]
    for i in tmslst:
        templist.append(i)
    dicio[idmus] = templist


def checkDisponivel(musica, autor, dicio):
    c = 0
    for k in dicio:
        if dicio[k][0] == musica and dicio[k][1] == autor:
            c += 1
    if c == 0:
        return True
    else:
        return False


def generateID():
    templist = list()
    for c in range(0, 5):
        templist.append(random.choice('0123456789abcdefghijklmnopqrstuvxywz!@#$%&'))
    idmus = ''.join([str(caracter) for caracter in templist])
    return idmus


def listAutores(dicio):
    tempdicio = dict()
    for k, v in dicio.items():
        if k != '00000':
            if v[1] not in tempdicio.keys():
                tempdicio[v[1]] = 1
            else:
                tempdicio[v[1]] += 1
    for k, v in sorted(tempdicio.items()):
        print(f'{str(k).title()} - (Músicas: {v})')


def listNaousadas(dicio):
    templist = list()
    for k, v in dicio.items():
        if k != '00000':
            if v[2] == 0:
                templist.append(v[0])
    for i in sorted(templist):
        print(f'{str(i).title()}')


def listMusicas(dicio):
    tempdict = dict()
    teste = dict()
    for k, v in dicio.items():
        if k != '00000':
            teste[v[0]] = v[1]
            if teste.items() not in tempdict.items():
                tempdict.update(teste)
    for k, v in sorted(tempdict.items()):
        print(f'{str(k).title()} - ({str(v).title()})')


def showALLdata(tit, aut, dicio):
    for k, v in dicio.items():
        if k != '00000':
            if v[0] == tit and v[1] == aut:
                print(f'- ID "{k}"')
                print(f'- Música: {str(v[0]).title()}.')
                print(f'- Autor: {str(v[1]).title()}')
                print(f'- Usos até o momento: {v[2]}')
                print(f'- Temas: {v[3:]}')


def listUsadas(dicio):
    tempdict = dict()
    for k, v in dicio.items():
        if k != '00000':
            if v[2] > 0:
                tempdict[v[0]] = v[2]
    for k, v in sorted(tempdict.items()):
        print(f'{str(k).title()} - (Usos: {v})')


def dltMusica(musica, autor, dicio):
    for key, value in list(dicio.items()):
        if value[0] == musica and value[1] == autor:
            del dicio[key]


def srtMusicas1(tms, dicio):
    tempdicio = dict()
    if 'todas' not in tms:
        for i in tms:
            for k, v in dicio.items():
                if k != '00000':
                    if i in v:
                        if v[2] == 0:
                            tempdicio[k] = [v[0], v[1]]
    else:
        for k, v in dicio.items():
            if k != '00000':
                if v[2] == 0:
                    tempdicio[k] = [v[0], v[1]]
    return tempdicio


def srtMusicas2(dicio, qttd):
    final = dicio.copy()
    while len(final) > qttd:
        key = random.choice(list(final.keys()))
        del final[key]
    return final


def rstUsos(dicio, limt):
    for k, v in dicio.items():
        if k != '00000':
            if v[2] != 0:
                if v[2] > limt:
                    v[2] = 0
                else:
                    v[2] += 1
