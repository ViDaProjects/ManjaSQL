class TableA:
    def __init__(self, data):
        self.data = data

class TableB:
    def __init__(self, data):
        self.data = data

def inner_join(table_a, table_b, on_column):
    result = []

    for row_a in table_a.data:
        for row_b in table_b.data:
            if row_a[on_column] == row_b[on_column]:
                result.append({**row_a, **row_b})  # Merge os dicionários

    return result

# Exemplo de uso
data_a = [
    {'ID': 1, 'Name': 'Alice', 'Age': 25},
    {'ID': 2, 'Name': 'Bob', 'Age': 30},
    {'ID': 3, 'Name': 'Charlie', 'Age': 22}
]

data_b = [
    {'ID': 2, 'Salary': 50000},
    {'ID': 3, 'Salary': 60000},
    {'ID': 4, 'Salary': 70000}
]

table_a = TableA(data_a)
table_b = TableB(data_b)

result = inner_join(table_a, table_b, 'ID')
print(result)
