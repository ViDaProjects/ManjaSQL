import json

with open('tables.json', 'r') as arquivo_json:
    dados_do_arquivo = json.load(arquivo_json)

print('Dados lidos do arquivo JSON:')
print(dados_do_arquivo)