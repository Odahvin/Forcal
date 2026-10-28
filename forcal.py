import random
import os
from pathlib import Path
import unicodedata
import time
import json

os.system('')
print('\033[2J\033[H', end='')

BASE = Path(__file__).parent

# carrega as duas dificuldades de uma vez
DIFICULDADES = {}
for nome in ('facil', 'dificil'):
    with open(BASE / f'forcal-{nome}.json', 'r', encoding='utf-8') as f:
        DIFICULDADES[nome] = json.load(f)

NOMES = {'facil': 'fácil', 'dificil': 'difícil'}

MENU = ('Escolha a dificuldade das palavras escrevendo:\n'
        'Configurar Fácil\nConfigurar Difícil\n'
        '(Essa configuração pode ser feita a qualquer momento.)\n>> ')

vidas = {
    0: '''
 |‾‾|
 O  |
/|\\ |
/ \\ |
''',

    1: '''
 |‾‾|
 O  |
/|\\ |
/   |
''',

    2: '''
 |‾‾|
 O  |
/|\\ |
    |
''',

    3: '''
 |‾‾|
 O  |
/|  |
    |
''',

    4: '''
 |‾‾|
 O  |
 |  |
    |
''',

    5: '''
 |‾‾|
 O  |
    |
    |
''',

    6: '''
 |‾‾|
    |
    |
    |
''',
}


def normalizar_texto(texto):
    texto_separado = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto_separado if not unicodedata.combining(c))


def limpar():
    print('\033[2J\033[H', end='')


def iniciar(dados):
    dicas = 3
    vida = 6
    letras_dentro = ''
    letras_fora = ''
    letras_dica = ''
    categoria = random.choice(list(dados))
    escolha = random.choice(list(dados[categoria]))
    subcategoria = dados[categoria][escolha]
    palavra_escolhida = escolha
    letras_lista = ''.join(set(l for l in palavra_escolhida if l.isalpha()))
    palavra_escol_norm = normalizar_texto(palavra_escolhida)
    segredo_linhas = [letra if not letra.isalpha() else '_'
                      for letra in palavra_escolhida]
    return dicas, vida, letras_dentro, letras_fora, letras_dica, categoria, subcategoria, palavra_escolhida, letras_lista, palavra_escol_norm, segredo_linhas


def chutar_letra(segredo_linhas, vida=None, chute=None, dica=False, letras_dentro=None, letras_fora=None, letras_dica=None, dicas=None):
    if dica:
        while True:
            letra_da_dica = random.choice(letras_lista)
            if normalizar_texto(letra_da_dica) not in letras_dentro + letras_fora + letras_dica:
                letras_dica += normalizar_texto(letra_da_dica)
                for num, letra in enumerate(palavra_escol_norm):
                    if letra.upper() == normalizar_texto(letra_da_dica):
                        segredo_linhas[num] = palavra_escolhida[num]

                dicas -= 1
                return segredo_linhas, vida, chute, dica, letras_dentro, letras_fora, letras_dica, dicas

    if chute:
        if chute_normalizado not in palavra_escol_norm:
            vida -= 1
            letras_fora += chute_normalizado
            return segredo_linhas, vida, chute, dica, letras_dentro, letras_fora, letras_dica, dicas

        elif chute_normalizado in palavra_escol_norm:
            letras_dentro += chute_normalizado

            for num, letra in enumerate(palavra_escol_norm):
                if letra.upper() == chute_normalizado:
                    segredo_linhas[num] = palavra_escolhida[num]
            return segredo_linhas, vida, chute, dica, letras_dentro, letras_fora, letras_dica, dicas


def sair(mensagem='>> '):
    limpar()
    print(f'Você tem {dicas} dicas')
    print(f'Categoria: {categoria} - {subcategoria}')
    print(vidas[vida])
    print(' '.join(palavra_escolhida))
    print(mensagem)
    ver()


def ver():
    abc = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
    abctemp = abc
    for letra in abc:
        if letra in letras_dentro:
            abctemp = abctemp.replace(letra, f'\033[32m{letra}\033[0m')

        elif letra in letras_fora:
            abctemp = abctemp.replace(letra, f'\033[31m{letra}\033[0m')

        elif letra in letras_dica:
            abctemp = abctemp.replace(letra, f'\033[33m{letra}\033[0m')

    print(f'{abctemp}')


def ler_dificuldade(texto):
    # devolve 'facil', 'dificil' ou None, olhando só a última palavra digitada
    partes = normalizar_texto(texto).lower().split()
    if not partes:
        return None
    if partes[-1] in ('facil', '1'):
        return 'facil'
    if partes[-1] in ('dificil', '2'):
        return 'dificil'
    return None


palavra_escolhida = None

try:
    while True:
        dificuldade_atual = ler_dificuldade(input(MENU))
        if dificuldade_atual:
            break
        limpar()
        print('Opção inválida.\n')

    dados = DIFICULDADES[dificuldade_atual]
    limpar()

    while True:
        dicas, vida, letras_dentro, letras_fora, letras_dica, categoria, subcategoria, palavra_escolhida, letras_lista, palavra_escol_norm, segredo_linhas = iniciar(
            dados)
        mostrar_subcategoria = False
        while True:

            print(f'Você tem {dicas} dicas')
            print(
                f"Categoria: {categoria} {f'- {subcategoria}' if mostrar_subcategoria else ''}")
            print(vidas[vida])
            if vida > 0:
                # linha 1, desce pra linha 2
                print(' '.join(segredo_linhas))
            if vida <= 0:
                print(' '.join(c for c in palavra_escolhida))
            print()  # linha 2 placeholder, desce pra linha 3
            ver()  # linha 3, desce pra linha 4

            if vida > 0:
                if '_' in segredo_linhas:
                    # sobe pra linha 2 e escreve ali, desce pra linha 3
                    chute = input('\033[2A>> ').upper().strip()
                    if chute.lower().startswith('configurar'):
                        nova = ler_dificuldade(chute)

                        if nova is None:
                            print('\033[1A\033[2K', end='')
                            print('Use: Configurar Fácil ou Configurar Difícil')
                            time.sleep(1.5)

                        elif nova != dificuldade_atual:
                            dificuldade_atual = nova
                            dados = DIFICULDADES[nova]
                            sair(f'Dificuldade alterada para {NOMES[nova]}!')
                            time.sleep(2)
                            limpar()
                            break

                        # mesma dificuldade (ou não entendida): nada muda
                        limpar()
                        continue

                    chute_normalizado = normalizar_texto(chute)

                    if chute_normalizado == palavra_escol_norm:
                        segredo_linhas = palavra_escolhida
                        print('\033[2A' + ' '.join(segredo_linhas))
                        print(
                            f'\033[2KVocê descobriu a palavra! Nova palavra sorteada!\033[1B')
                        time.sleep(2)
                        limpar()
                        break

                if not '_' in segredo_linhas:
                    print(
                        f'\033[2AVocê descobriu a palavra! Nova palavra sorteada!\033[1B')
                    time.sleep(2)
                    limpar()
                    break

            if vida <= 0:
                print(f'\033[2AVocê ficou sem vidas! Partida encerrada\033[1B')
                time.sleep(2)
                limpar()
                break

            # volta pra linha 2 e apaga, desce pra linha 3
            print('\033[1A\033[2K', end='')

            if not chute or not chute[0].isalpha():
                # escreve na linha 2, desce pra linha 3
                print('Escreva uma letra.')
                time.sleep(1)
                # volta pra 2 e apaga, dps sobe pra 1 e apaga, loop recomeça ali
                print('\033[1A\033[2K\033[1A\033[2K', end='')

            if chute and chute[0].isalpha():
                if chute.lower() == 'sair':
                    raise SystemExit

                elif chute.lower() in ['dica', 'dicas']:
                    if dicas <= 0:
                        print('Você não tem mais dicas disponíveis.')
                        time.sleep(1)

                    elif dicas == 1 or len(set(normalizar_texto(letras_lista)) - set(letras_dentro) - set(letras_dica)) <= 1:
                        if not mostrar_subcategoria:
                            mostrar_subcategoria = True
                            dicas -= 1
                        else:
                            print(
                                'Não é possível pedir mais dicas faltando apenas 1 letra.')
                            time.sleep(1)
                    else:
                        segredo_linhas, vida, chute, dica, letras_dentro, letras_fora, letras_dica, dicas = chutar_letra(
                            segredo_linhas=segredo_linhas, vida=vida, chute=chute, dica=True, letras_dentro=letras_dentro, letras_fora=letras_fora, letras_dica=letras_dica, dicas=dicas)

                else:

                    chute_normalizado = normalizar_texto(chute[0])

                    if chute_normalizado in letras_dentro + letras_fora + letras_dica:
                        print(f'Letra {chute[0]} já usada.')
                        time.sleep(1)
                        print('\033[1A\033[2K\033[1A\033[2K', end='')
                    else:
                        segredo_linhas, vida, chute, dica, letras_dentro, letras_fora, letras_dica, dicas = chutar_letra(
                            segredo_linhas=segredo_linhas, vida=vida, chute=chute, dica=False, letras_dentro=letras_dentro, letras_fora=letras_fora, letras_dica=letras_dica, dicas=dicas)
            limpar()

except (KeyboardInterrupt, EOFError, SystemExit):
    if palavra_escolhida and vida > 0 and '_' in segredo_linhas:
        sair()

print('Jogo encerrado.\nObrigado por jogar!')
try:
    input('Pressione ENTER para sair.')
except (KeyboardInterrupt, EOFError):
    pass
