import re

def encontrar_proximo_campo(consulta, conjunto_palavras):
    # Usando uma expressão regular para encontrar o conjunto de palavras e o próximo campo
    padrao = re.compile(f"{conjunto_palavras}\s*\([^)]*\)\s+(\w+)")
    correspondencia = re.search(padrao, consulta)
    
    if correspondencia:
        return correspondencia.group(1)
    else:
        return None

# Exemplo de uso
consulta_sql = "CREATE TABLE employees ( emp_no INT NOT NULL, first_name VARCHAR(14) NOT NULL, last_name VARCHAR(16) NOT NULL, PRIMARY KEY (emp_no) );"

conjunto_palavras = "employees"
proximo_campo = encontrar_proximo_campo(consulta_sql, conjunto_palavras)

print(f"O próximo campo após '{conjunto_palavras}' é: {proximo_campo}")
