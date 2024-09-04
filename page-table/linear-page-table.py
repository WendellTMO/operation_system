from math import ceil
from math import log
from time import sleep
import random

def informacoes():
    print(chr(27) + "[2J")
    print(" Iremos abstrair os metadados utilizados, ou seja:\n",
          "Nossa PageTable irá ter o bit mais signicativo p/\n",
          "representar se está na memória (1) ou se esta em \n",
          "disco (0), e os bits menos significativos irão re-\n",
          "-presentar o endereço do PageFrame\n")
    print("OBS: Não é assim que as máquinas representam, porém\n",
          "para fins didáticos, vamos representar nesse esquema:")
    print("PTE X: [Dirty Bit], [PFN]")
    ok = input("\nDigite 'ok' para continuar, ou digite qualquer coisa para sair\n")
    if (ok != "ok"): exit()
    print(chr(27) + "[2J")

    
def aleatorio(lista):
    indice = random.randint(0, len(lista)-1)
    result = lista[indice]
    lista.pop(indice)
    return result

def mostrar_toda_pt(page_table):
    res = ""    
    for k in page_table:
        res += (f"PTE {k} | PFN:{page_table[k]}\n")
    return res

def mostrar_todo_mapeamento(page_table, virt_adresses, page_size):
    res = "VA = Virtual Adress | PTE = PageTableEntry | PFN = PageFrameNumber | PA = Physical Adress\n"
    for i in virt_adresses.keys():
        pte = (virt_adresses[i] // page_size)         
        res += (f"VAN: {i} | PTE: {pte} | PFN: {page_table[pte]} | PA: {virt_adresses[i]}\n")
    return res    

def fim(page_table, virt_adresses, page_size):
    print("\nTodos endereços foram traduzidos!\n",
          "Digite a opção desejada:\n",
          "[1] Mostrar PT\n",
          "[2] Mostar todo mapeamento\n",
          "[X] Sair\n")
    escolha = int(input())
    if (escolha == 1):
        print(mostrar_toda_pt(page_table))
        fim(page_table, virt_adresses, page_size)
    elif (escolha == 2):
        print(mostrar_todo_mapeamento(page_table, virt_adresses, page_size))
        fim(page_table, virt_adresses, page_size)
    elif (escolha == 0):
        exit()
    else:
        fim(page_table, virt_adresses, page_size)
        

def recupera_disco(pte_table, virt_adresses, v_addr, pte):
        pte_table[pte][0] = 1
        offset = v_addr % tamanho_pagina
        # adiciono 6 bits no final
        pfn_base = pte_table[pte][1]
        endereco_fisico = (int(pfn_base) * tamanho_pagina) + offset
        virt_adresses[v_addr] = endereco_fisico

# Maquina com X bits
print("# Exemplo: 16KB = 2^14, então é uma máquina de 14 bits")
print("# obs: muitos bits = maior a espera")
qtd_virt_adress = 2 ** (int(input("Qual o tamanho em BITS da sua máquina?\n")))
# virt_adresses = [[x, []] for x in range(qtd_virt_adress)]
virt_adresses = {}

# tamanho em bytes 
tamanho_pagina = (int(input("Qual o tamanho em BYTES de UMA página nessa máquina?\n")))

# calculo da quantidade total de bytes
qtd_paginas = qtd_virt_adress // tamanho_pagina

minimo_bits = log(ceil(qtd_paginas / 8), 2)
print("# Pergunta 1")
print("Quantos bits é necessário para representar sua PTE? ")
if (int(input()) != minimo_bits):
    print(f"Errado... Precisamos de no MÍNIMO {minimo_bits} bits!")
else:
    print("Correto!")

print("\n# Pergunta 2")
print("Para fins didáticos, estamos considerando que cada PTE tem tamanho de 4 Bytes")
print("Assim, qual o tamanho da PageTable?")
tamanho_pt = qtd_paginas * 4
if (int(input()) != tamanho_pt):
    print(f"Errado... nossa PageTable tem tamanho total de {tamanho_pt} Bytes")
else:
    print("Correto!")
sleep(2)
informacoes()

print("Isso pode demorar um pouco...")
pfn_number = [x for x in range(qtd_paginas)]
print(chr(27) + "[2J")

# gerando uma PT onde armazena PTE de 4 bytes
pte_table = {}
print("Isso pode demorar um pouco...")
for i in range(qtd_paginas):
    temp_bytes = []
    if (random.randint(0,1) == 1):
        temp_bytes.append(1)
        temp_bytes.append(aleatorio(pfn_number))
    else:
        temp_bytes.append(0)
        temp_bytes.append("DISCO")
    pte_table[i] = temp_bytes
print(chr(27) + "[2J")

print("Vamos começar o exercício:\n")
print((f"Dado uma Máquina de {qtd_virt_adress} endereços\n"),
        (f"onde cada página tem {tamanho_pagina} endereços\n"), 
        "1- Você irá digitar quantas endereços virtuais deseja traduzir\n",
        (f"2- Após isso irá ser sorteado um número entre 0 e {qtd_virt_adress}-1 para traduzir\n"),
        "3- Após isso, acesse a PT quantas vezes quiser para ver qual endereço de uma certa PTE\n",
        "   3A - Se o endereço estiver no DISCO aparecerá DISK, e você pode digitar RECUPERAR para recuperar ele da memória secundária\n",
        "   3B - ou digitar qualquer coisa para ver outra PTE\n",
        "OBS: Finja que VOCÊ é a MMU, se acessar a PTE errada, sua tradução vai ficar errada\n",
        "4- Quando terminar a tradução digite 'next', isso irá te mostrar o mapeamento correto\n",
        "5- Após, traduzir todos endereços desejados, você terá as opções:\n",
        "   5A - Mostrar toda a PT,\n",
        "   5B - Mostrar todos endereços virtuais mapeados,\n",
        "   5C - Sair\n")

calculo = int(input("Quantas endereços deseja traduzir?\n"))
while (calculo > 0):
    endereco_vitual = random.randint(0, (qtd_virt_adress - 1))
    print(f"Traduza o endereço virtual {endereco_vitual}")
    pte = input("Qual PTE gostaria de olhar?\n")
    while (pte != "next"):
            print(f"pte {pte} mapeia para -> {pte_table[int(pte)][1]}")
            if (pte_table[int(pte)][0] == 0):
                if ((input("Para recuperar digite 'RECUPERAR' ") == "RECUPERAR")):
                    pte_table[int(pte)][1] = aleatorio(pfn_number)
                    for i in range(0, tamanho_pagina - 1):
                        recupera_disco(pte_table, virt_adresses, (i + (int(pte)*tamanho_pagina)), int(pte))
                        
                    print("só pra mostrar que é lento:")
                    for i in range(3):
                        print("Recuperando...")
                        sleep(1)
                    print("RECUPERADO!!")
                    print(f"PTE {pte} mapeia para -> {pte_table[int(pte)][1]}")
                    
            pte = input("Qual a próxima PTE gostaria de olhar? (ou 'next' para finalizar)\n")
    print("O mapeamento correto é: ")
    pte_table[int(endereco_vitual//tamanho_pagina)][1] = aleatorio(pfn_number)
    for i in range(0, tamanho_pagina):
        recupera_disco(pte_table, virt_adresses, (i + (int(endereco_vitual//tamanho_pagina)*tamanho_pagina)), int(endereco_vitual//tamanho_pagina))
    
    print(f"endereco virtual: {endereco_vitual} -> endereço fisico: {virt_adresses[endereco_vitual]}")
    calculo -= 1

fim(pte_table, virt_adresses, tamanho_pagina)