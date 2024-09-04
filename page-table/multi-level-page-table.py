import random
import math

bits_maquina = int(input("Quantos bits tem essa sua máquina? "))

page_bytes = int(input("Quantos Bytes tem cada page da sua máquina? "))
bits_page_size = math.ceil(math.log(page_bytes, 2))


# pegando cada entry como 4 bytes
quantidade_pages = (2 ** bits_maquina) // page_bytes
tamanho_pt = math.ceil(quantidade_pages * (2 ** 2))
print(f"quantidade de pages (v_adrress): {quantidade_pages}")
print(f"tamanho da page_table: {tamanho_pt}")


bits_page_table = math.ceil(math.log(page_bytes, 2))
print(f"bits utilizados para representar a pt: {bits_page_table}")

# quantos page frame estou utilizando pra minha PT?
# o tamanho dos page da memoria virtual = tamanho dos page frame
pfn_utilizados = tamanho_pt // page_bytes
print(f"pfn_utilizados: {pfn_utilizados}")

# bits para representar o meu page_directory
bits_page_directory = math.ceil(math.log(pfn_utilizados,2))
print(f"bits para representar meu page_directory: {bits_page_directory}")

page_directory = {}
page_table = {}

solve_qtd = int(input("Quantos endereços gostaria de traduzir? "))
while (solve_qtd > 0):
    virtual_address = random.randint(0, (2**bits_maquina) - 1)
    print(f"traduza o endereço virtual {virtual_address}")
    page = virtual_address // page_bytes
    pd_id = page // (2 ** (bits_maquina - bits_page_table - bits_page_directory))

    posi_memoria = random.randint(pfn_utilizados, (tamanho_pt + pfn_utilizados) - 1)
    v1 = page_directory.get(pd_id, "X")
    if (v1 == "X"):
        page_directory[pd_id] = random.randint(0, 2**(bits_page_directory))
    
    page_offset = page % (2 ** bits_page_directory)
    page_table[page_directory[pd_id] + page_offset] = random.randint(0, 2**(bits_maquina - bits_page_size))

    physical_adress = page_table[page_directory[pd_id] + page_offset] + (virtual_address % page_bytes)

    # solve 
    resposta = input("Olhe sua PD ou digite FIM para sair: ")
    while(resposta != "FIM"):
        if resposta == "A":
            print(f"O seu PD_ID é {pd_id}")
        if resposta == "B":
            print(f"O PD mapeia para a PT {page_directory[pd_id]}")
        if resposta == "C":
            print(f"Sua PT + PageOffset guarda {page_table[page_directory[pd_id] + page_offset]}")
        
        resposta = input("Digite 'A' pra ver o PageDirect, 'B' para ver a PageTableMapeada,\n'C' pra ver o que a PTE guarda ou 'FIM' para ver a resposta\n")
        continue

    print(f"Endereço virtual: {virtual_address} está mapeado para o endereço físico {physical_adress}")
    
    solve_qtd -= 1
