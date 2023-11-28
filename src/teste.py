sql_script = """
CREATE TABLE employees (
    emp_no      INT             NOT NULL,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      ENUM ('M','F')  NOT NULL,    
    hire_date   DATE            NOT NULL,
    PRIMARY KEY (emp_no)
);
"""

def encontra_e_mostra_proxima_palavra(script, termo):
    palavras = script.split()
    for i, palavra in enumerate(palavras):
        if termo.upper() == palavra:
            proxima_palavra = palavras[i + 1] if i + 1 < len(palavras) else None
            print(f"Encontrou '{termo}' na palavra '{palavra}'. Próxima palavra: {proxima_palavra}")
            return True
    return False

# Chamando a função para procurar "NOT NULL" e mostrar a próxima palavra
encontrado = encontra_e_mostra_proxima_palavra(sql_script, "(")

if not encontrado:
    print("Termo não encontrado no script.")
