import re
import json

# A única função que importa aqui é load_sql_json

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
                if col_constraints == "":
                    col_constraints = "None"
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

def extract_table_keys(sql_statements):

    statements = sql_statements.split('CREATE TABLE ')[1:]
    parsed_keys = []
    for table in statements:
        table_name, *table_content = table.split('\n')
        keys = []
        real_table_name = table.split('(')

        for line in table_content:
            matches_primary = re.search(r'PRIMARY KEY \((.*?)\)', line)
            matches_foreign = re.findall(r'FOREIGN KEY \((.*?)\) REFERENCES (\w+) \((.*?)\) ON DELETE CASCADE', line)
            matches_unique = re.findall(r'UNIQUE KEY \((.*?)\)', line)

            if matches_primary:
                keys.append(f'{real_table_name[0]}: PRIMARY KEY ({matches_primary.group(1)})')

            for match in matches_foreign:
                keys.append(f'{real_table_name[0]}: FOREIGN KEY ({match[0]}) REFERENCES {match[1]} ({match[2]}) ON DELETE CASCADE')

            for match in matches_unique:
                keys.append(f'{real_table_name[0]}: UNIQUE KEY ({match})')

        if keys:
            parsed_keys.extend(keys)
    
    return parsed_keys

def create_json_from_keys(keys_list):
    data = {}
    
    for key_info_str in keys_list:
        table_name, key_info = key_info_str.split(' : ')
        key_type, key_details = key_info.split(' (', 1)
        key_details = key_details.rstrip(')')  # Remove the ending parenthesis if it exists
        
        name = key_details.split(')') 
        #print(name)
        
        delete_instructions = None
        references = None
        field_name = None
        
        if 'REFERENCES' in key_details:
            references_info, delete_info = key_details.split(') REFERENCES ')
            field_name = references_info.split('KEY (')[1].strip()[:-1] if 'KEY (' in references_info else None
            
            references_parts = references_info.split(' ')
            references = delete_info.split()[0]
            #references = delete_parts[0] if 'REFERENCES' in references_parts else None
            
            delete_parts = delete_info.split(' ')
            delete_instructions = delete_parts[3] if 'DELETE' in delete_parts else None
            
        #else:
            #field_name = key_details.split('(')[1].strip()[:-1] if '(' in key_details else None
        
        key_data = {
            "field_name": name[0],
            "key_type": key_type,
            "references": references,
            "delete_instructions": delete_instructions
        }
        
        data.setdefault(table_name, []).append(key_data)

    return json.dumps(data, indent=2)

def merge_data(table_text = "", key_text = ""): # Check if key_text is not empty so it doesn't break
    key_json = json.loads(key_text)
    
    for table_json in table_text:
        for key_name, key_value in key_json.items():
        
            if key_name == table_json["table_name"]:
                table_json['key_data'] = key_value
    return table_text

    #first_key = next(iter(key_json.keys()))
    #print(key_json[first_key])

def load_sql_json(file_path: str, tables: list = []) -> list:
    with open(file_path, "r") as file:
        sql_content = file.read()

    sql_content = re.sub(r'[ \t]+', ' ', sql_content)
    #print(sql_content)

    # Precisa transformar vários ' ' em um só

    table_data = parse_sql_file(sql_content)
    
    # Find what are the keys for each table, what type they are and what they reference
    #print(extract_keys(sql_content))
    key_info = extract_table_keys(sql_content)
    
    table_data = remove_key(table_data)
    
    # Add key information into the json file
    keys_json = create_json_from_keys(key_info) # References: is broken
    
    table_data =  merge_data(table_data, keys_json)

    print(table_data)

    #for table in table_data:
    #    tables.append(table)
    #return tables

def main():
    load_sql_json("tabela.sql")

if __name__ == "__main__":
    main()