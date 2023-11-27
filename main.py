import sql_info_loader as sql_loader

with open("tabela.sql", "r") as file:
    sql_content = file.read()

    all_tables_info = sql_loader.extract_all_tables(sql_content)

    sql_loader.print_tables(all_tables_info)
    