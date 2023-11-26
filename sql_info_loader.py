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

    return {"table_name": table_name, "columns": columns[1:], "primary_key": primary_key}

def extract_all_tables(sql_content):
    # Split SQL content into individual CREATE TABLE statements
    create_table_statements = re.split(r'\bCREATE TABLE\b', sql_content)
    
    # Remove empty strings resulting from the split
    create_table_statements = [statement.strip() for statement in create_table_statements if statement.strip()]

    # Extract information for each table
    all_table_info = []
    for table_sql in create_table_statements:
        table_info = extract_table_info("CREATE TABLE " + table_sql)  # Add "CREATE TABLE" back for parsing
        all_table_info.append(table_info)

    return all_table_info

with open("tabela.sql", "r") as file:
    sql_content = file.read()

all_tables_info = extract_all_tables(sql_content)
print(all_tables_info)
for table_info in all_tables_info:
    print("\nNome da Tabela:", table_info["table_name"])
    print("Campos:")
    for column in table_info["columns"]:
        print(f"- {column['name']}: {column['type']} {column['constraints']}")
    print("Chave Primária:", table_info["primary_key"])