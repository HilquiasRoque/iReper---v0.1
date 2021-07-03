import PySimpleGUI as sg
import json
import iReperFunc as ir

# Carregamentos iniciais

repertorio = dict()
nome_rep = 'repertorio.json'
ir.load_create_Arquivo_dic(nome_rep, repertorio)

menu_layout = [['Músicas', ['Adicionar', 'Deletar', 'Sortear', 'Salvar e Sair']],
               ['Listas', ['Listar']],
               ['Editar', ['Alterar Dados', 'Sorteio']],
               ['Help', ['Sobre', 'Ajuda']]]

srt = [[sg.Menu(menu_layout, )],
       [sg.Text('Sorteie suas músicas!')],
       [sg.Text('Digite abaixo os temas das músicas que deseja sortear.')],
       [sg.Text('(digite "todas" para usar todos os temas)')],
       [sg.Input(size=(43, 1), key='-Stemas-', default_text=''), sg.Button('Sortear!', bind_return_key=True)],
       [sg.Output(size=(50, 3), key='-OUT-')],
       [sg.Button('Confirmar!', bind_return_key=True)]]

add = [[sg.Menu(menu_layout, )],
       [sg.Text('Adicione uma música nova ao seu repertório:')],
       [sg.Text('Título  '), sg.Input(size=(50, 1), key='-Musica-', do_not_clear=False, focus=True)],
       [sg.Text('Autor  '), sg.Input(size=(50, 1), key='-Autor-', do_not_clear=False)],
       [sg.Text('Temas'), sg.Input(size=(50, 1), key='-Tema-', do_not_clear=False)],
       [sg.Button('Registrar', bind_return_key=True)]]

dlt = [[sg.Menu(menu_layout, )],
       [sg.Text('Apague uma música do seu repertório:')],
       [sg.Text('Nome da música:'), sg.Input(size=(40, 1), key='-Nmu-')],
       [sg.Text('Nome do autor:   '), sg.Input(size=(40, 1), key='-Nau-')],
       [sg.Button('Apagar!', bind_return_key=True)]]

lst = [[sg.Menu(menu_layout, )],
       [sg.Text('Visualise informações do seu repertório:')],
       [sg.Combo(values=['Por Autores', 'Por Títulos', 'Não Usadas', 'Usadas'], enable_events=True,
                 key='Select')],
       [sg.Output(size=(50, 5), key='-OUT2-')]]

# ----------- Layouts em Colunas

layout = [[sg.Column(add, key='-add-'),
           sg.Column(dlt, visible=False, key='-dlt-'),
           sg.Column(srt, visible=False, key='-srt-'),
           sg.Column(lst, visible=False, key='-lst-')]]

window = sg.Window('iReper v1.0', layout, use_default_focus=True, grab_anywhere=True)
autoReset = 3
quantas = 2
ir.rstUsos(repertorio, autoReset)

s2 = dict()
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Salvar e Sair'):
        open(nome_rep, 'w').write(json.dumps(repertorio))
        break
    if event == 'Deletar':
        window['-add-'].update(visible=False)
        window['-dlt-'].update(visible=True)
        window['-srt-'].update(visible=False)
        window['-lst-'].update(visible=False)
        window['-bsc-'].update(visible=False)
    if event == 'Adicionar':
        window['-add-'].update(visible=True)
        window['-dlt-'].update(visible=False)
        window['-srt-'].update(visible=False)
        window['-lst-'].update(visible=False)
        window['-bsc-'].update(visible=False)
    if event == 'Sortear':
        window['-OUT-'].update('')
        window['-add-'].update(visible=False)
        window['-dlt-'].update(visible=False)
        window['-srt-'].update(visible=True)
        window['-lst-'].update(visible=False)
        window['-bsc-'].update(visible=False)
    if event == 'Listar':
        window['-OUT2-'].update('')
        window['-add-'].update(visible=False)
        window['-dlt-'].update(visible=False)
        window['-srt-'].update(visible=False)
        window['-lst-'].update(visible=True)
        window['-bsc-'].update(visible=False)
    if window['-add-']:
        if event == 'Registrar':
            mnome = values['-Musica-']
            anome = values['-Autor-']
            tnome = values['-Tema-']
            if mnome == '' or anome == '' or tnome == '':
                sg.popup('Preencha todos os campos!')
            else:
                if ir.checkDisponivel(mnome, anome, repertorio):
                    ir.copyData_toDict(mnome, anome, tnome, repertorio)
                    sg.popup('Música adicionada com sucesso!')
                else:
                    sg.popup('Esta música já consta no cadastro!')
    if window['-dlt-']:
        if event == 'Apagar!':
            nmus = values['-Nmu-']
            naut = values['-Nau-']
            if naut == '' or nmus == '':
                sg.popup('Preencha todos os campos!')
            else:
                if not ir.checkDisponivel(nmus, naut, repertorio):
                    ir.dltMusica(nmus, naut, repertorio)
                    window['-Nmu-'].update('')
                    window['-Nau-'].update('')
                    sg.popup('Música apagada com sucesso!')
                else:
                    sg.popup('''Música não encontrada!
    O nome da música e o nome do autor não batem...''')
    if window['-srt-']:
        if event == 'Sortear!':
            s1 = dict()
            s2 = dict()
            if values['-Stemas-'] == '':
                window['-OUT-'].update('')
                sg.popup('Você precisa especificar o(s) tema(s) a ser(em) sorteado(s)!')
            else:
                window['-OUT-'].update('')
                temas = str(values['-Stemas-']).split(', ')
                s1 = ir.srtMusicas1(temas, repertorio)
                s2 = ir.srtMusicas2(s1, quantas)
                for k, v in s2.items():
                    print(f'{str(v[0]).title()} - ({str(v[1]).title()})')
        if event == 'Confirmar!':
            window['-OUT-'].update('')
            for k, v in repertorio.items():
                if k in s2.keys():
                    v[2] += 1
                    sg.popup('O uso das músicas foi registrado!')
            open(nome_rep, 'w').write(json.dumps(repertorio))
    if window['-lst-']:
        if values['Select'] == 'Por Autores':
            window['-OUT2-'].update('')
            ir.listAutores(repertorio)
        if values['Select'] == 'Por Títulos':
            window['-OUT2-'].update('')
            ir.listMusicas(repertorio)
        if values['Select'] == 'Não Usadas':
            window['-OUT2-'].update('')
            ir.listNaousadas(repertorio)
        if values['Select'] == 'Usadas':
            window['-OUT2-'].update('')
            ir.listUsadas(repertorio)
window.close()
