from math import ceil
from math import log
from time import sleep
import random

def aleatorio(lista):
    indice = random.randint(0, len(lista)-1)
    result = lista[indice]
    lista.pop(indice)
    return result

def mostrar_toda_pt(page_table):
    res = ""
    keys = page_table.keys()
    keys.sort()
    for k in page_table:
        res += (f"PTE {k} | PFN:{page_table[k]}\n")
    return res

def mostrar_todo_mapeamento(page_table, virt_adresses, page_size):
    res = "VA = Virtual Adress | PTE = PageTableEntry | PFN = PageFrameNumber | PA = Physical Adress\n"
    for i in virt_adresses:
        pte = (i[0] // page_size)         
        res += (f"VAN: {i[0]} | PTE: {pte} | PFN: {page_table[pte]} | PA: {i[1]}")
    return res    

# Maquina com X bits
qtd_virt_adress = 2 ** (int(input("Qual o tamanho em bits da sua máquina? ")))
virt_adresses = [[x, []] for x in range(qtd_virt_adress)]

# tamanho em bytes 
tamanho_pagina = (int(input("Qual o tamanho em Bytes de UMA página? ")))

# calculo da quantidade total de bytes
qtd_paginas = qtd_virt_adress // tamanho_pagina

minimo_bits = log(ceil(qtd_paginas / 8), 2)
print("Quantos bits é necessário para representar sua PTE? ")
if (int(input()) < minimo_bits):
    print(f"Errado... Precisamos de pelo menos {minimo_bits} bits!\n")
else:
    print("Correto!\n")

print("Vamos considerar que nossa PTE é de 4 bytes, qual seu tamanho? ")
tamanho_pt = qtd_paginas * 4
if (int(input()) != tamanho_pt):
    print(f"Errado... nossa PageTable tem tamanho total de {tamanho_pt} Bytes\n")
else:
    print("Correto!")

pfn_number = [x for x in range(qtd_paginas)]

print("Iremos abstrair os metadados utilizados, ou seja:\n",
      "Nossa PageTable irá ter o bit mais signicativo p/\n",
      "representar se está na memória (1) ou se esta em \n",
      "disco (0), e os bits menos significativos irão re-\n",
      "-presentar o endereço do PageFrame\n")
print("OBS: Não é assim que as máquinas representam, porém\n",
      "para fins didáticos, vamos representar nesse esquema:")
print("PTE X: [Dirty Bit], [PFN]")     
      
# gerando uma PT onde armazena PTE de 4 bytes
pte_table = {}
for i in range(qtd_paginas):
    temp_bytes = []
    if (random.randint(0,1) == 1):
        temp_bytes.append(1)
        temp_bytes.append(aleatorio(pfn_number))
    else:
        temp_bytes.append(0)
        temp_bytes.append("DISCO")
    pte_table[i] = temp_bytes
print(pte_table)


def recupera_disco(pte_table, virt_adresses, v_addr, pte):
        pte_table[pte][0] = 1
        offset = v_addr % tamanho_pagina
        # adiciono 6 bits no final
        pfn_base = pte_table[pte][1]
        endereco_fisico = (pfn_base * tamanho_pagina) + offset
        virt_adresses[v_addr][1] = endereco_fisico

# "MMU"
for i in range(qtd_virt_adress):
    v_addr = virt_adresses[i][0]
    pte = v_addr // tamanho_pagina
    if (pte_table[pte][0] == 1):
        recupera_disco(pte_table, virt_adresses, v_addr, pte)
    else:
        virt_adresses[i][1] = "DISK"

print("Vamos começar o exercício:\n")
print(  (f"Máquina de {qtd_virt_adress} endereços\n"),
        (f"Cada página tem {tamanho_pagina} endereços\n"), 
        "\n1- Você irá digitar quantas endereços virtuais deseja traduzir\n",
        "2- Após isso irá ser sorteado um número entre 0 e (2^16)-1 para traduzir\n",
        "3- Após isso, acesse a PT quantas vezes quiser para ver qual endereço de uma certa PTE\n",
        "   3A - Se o endereço estiver no DISCO aparecerá DISK, e você pode digitar RECUPERAR para recuperar ele da memória secundária",
        "   3B - ou digitar qualquer coisa para ver outra PTE",
        "OBS: Finja que é a MMU, se acessar a PTE errada, sua tradução vai ficar errada\n",
        "4- Quando terminar a tradução digite 'next', isso irá te mostrar o mapeamento correto\n",
        "5- Após, traduzir todos endereços desejados, você terá as opções:\n",
        "   5A - Mostrar a PT,\n",
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
                        recupera_disco(pte_table, virt_adresses, (i + (int(pte)*64)), int(pte))
                        
                    print("só pra mostrar que é lento:")
                    for i in range(3):
                        print("Recuperando...")
                        sleep(1)
                    print("RECUPERADO!!")
                    print(f"PTE {pte} mapeia para -> {pte_table[int(pte)][1]}")
                    
            pte = input("Qual a próxima PTE gostaria de olhar? (ou 'next' para finalizar)\n")
    print("O mapeamento correto é: ")
    print(f"endereco virtual: {endereco_vitual} -> endereço fisico: {virt_adresses[endereco_vitual][1]}")
    calculo -= 1    