import re 

def extract_table_info(sql):
    # Encontrar o nome da tabela
    table_match = re.search(r"CREATE TABLE (\w+)", sql)
    table_name = table_match.group(1) if table_match else None

    # Encontrar os campos e suas características
    columns_match = re.findall(r"(\w+)\s+(\w+(?:\(\d+\))?)\s*([^,]*)(?:,|\))", sql)
    columns = [{"name": col[0], "type": col[1], "constraints": col[2].strip()} for col in columns_match]

    # Encontrar a chave primária
    primary_key_match = re.search(r"PRIMARY KEY (([^)]+))", sql)
    primary_key = primary_key_match.group(1).split(",") if primary_key_match else []

    return {"table_name": table_name, "columns": columns, "primary_key": primary_key}


with open("tabela.sql", "r") as file:
    sql_content = file.read()


table_info = extract_table_info(sql_content)

print(table_info)


print("Nome da Tabela:", table_info["table_name"])
print("Campos:")
for column in table_info["columns"]:
    print(f"- {column['name']}: {column['type']} {column['constraints']}")
print("Chave Primária:", table_info["primary_key"])