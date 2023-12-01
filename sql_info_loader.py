import re
import json

'''Colocar enum como parte do type
Colocar tipo de key no mesmo nível de "importância" que o column'''

def parse_keys(column_lines):
    key_words = {
        "PRIMARY": "PRIMARY KEY",
        "UNIQUE": "UNIQUE KEY",
        "FOREIGN": "FOREIGN KEY"
    }

    keys = []
    for line in column_lines:
        parts = line.strip().split(' ')
        if len(parts) > 2:
            if parts[2] in key_words:
                keys.append({
                    "type": key_words[parts[2]],
                    "constraints": "(" + ' '.join(parts[3:]) + ")"
                })

    return keys

# Multiple tables get put on to only one json file, fix it
def parse_sql_file(sql_content: str) -> list:

    tables = re.findall(r'CREATE TABLE\s+(\w+)\s+\((.*?)\);', sql_content, re.DOTALL)

    all_tables_info = []
    for table in tables:
        table_name = table[0]
        columns = table[1].split('\n')
        columns_info = []

        keys = parse_keys(columns)

        for column in columns:
            column = column.strip().strip(',')
            if column:
                col_parts = column.split()
                col_name = col_parts[0]
                col_type = col_parts[1]
                col_constraints = ' '.join(col_parts[2:])
                columns_info.append({
                    "name": col_name,
                    "type": col_type,
                    "constraints": col_constraints
                })

        all_tables_info.append({
            "table_name": table_name,
            "columns": columns_info + keys
        })

    return all_tables_info

def remove_key(table_data: list) -> list:
    for table in table_data:
        #print(table)
        columns = table["columns"]
        table["columns"] = [col for col in columns if col["type"].upper() != "KEY"]
    return table_data

def load_sql_json(file_path: str, tables: list = []) -> list:
    with open(file_path, "r") as file:
        sql_content = file.read()
    table_data = parse_sql_file(sql_content)
    
    # Find what are the keys for each table, what type they are and what they reference

    table_data = remove_key(table_data)
    
    # Add key information into the json file

    for table in table_data:
        tables.append(table)
    return tables

def main():
    load_sql_json("tabela.sql")

if __name__ == "__main__":
    main()