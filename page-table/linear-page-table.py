import random

def aleatorio(lista):
    indice = random.randint(0, len(lista)-1)
    result = lista[indice]
    lista.pop(indice)
    return result

# 16KB
qtd_virt_adress = 2 ** 14
virt_adresses = [[x, []] for x in range(qtd_virt_adress)]

# tamanho em bytes -> 64B
tamanho_pagina = 2 ** 6

# 2 ** 8
qtd_paginas = qtd_virt_adress // tamanho_pagina

# table_size = 4 bytes
tamanho_pt = qtd_paginas * 4

pfn_number = [x for x in range(qtd_paginas)]

# gerando uma PT onde armazena PTE de 4 bytes
pte_table = {}
for i in range(qtd_paginas):
    temp_bytes = []
    for j in range(4):
        if (j == 3):
            temp_bytes.append(aleatorio(pfn_number))
        else:
            temp_bytes.append([])
    pte_table[i] = temp_bytes
    
# "MMU"
for i in range(qtd_virt_adress):
    v_addr = virt_adresses[i][0]
    pte = v_addr // tamanho_pagina
    offset = v_addr % tamanho_pagina
    
    # adiciono 6 bits no final
    pfn_base = pte_table[pte][3]
    
    endereco_fisico = (pfn_base * (2**6)) + offset
    
    virt_adresses[i][1] = endereco_fisico

print("Máquina de 16KB de endereços")
print("Cada página é de 64B")
print("\n1- Você irá digitar quantas endereços virtuais deseja traduzir")
print("2- Após isso irá ser sorteado um número entre 0 e (2^16)-1 para traduzir")
print("3- Após isso, acesse a PT quantas vezes quiser para ver qual endereço de uma certa PTE")
print("4- Quando desejar sair digite FIM, irá te mostrar qual o mapeamento correto!")
calculo = int(input("Quantas endereços deseja traduzir?\n"))
while (calculo > 0):
    endereco_vitual = random.randint(0, (2**14)-1)
    print(f"Traduza o endereço virtual {endereco_vitual}")
    
    pte = input("Qual PTE gostaria de olhar?\n")
    while (pte != "FIM"):
        print(f"pte {pte} mapeia para -> {pte_table[int(pte)][3]}")
        pte = input()
    print("O mapeamento correto é: ")
    print(f"endereco virtual: {endereco_vitual} -> endereço fisico: {virt_adresses[endereco_vitual][1]}")
    calculo -= 1    