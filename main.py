import sql_info_loader as sql_loader

with open("tabela.sql", "r") as file:
    sql_content = file.read()

    all_tables_info = sql_loader.load_sql_json("tabela.sql")

    #print(all_tables_info)
    