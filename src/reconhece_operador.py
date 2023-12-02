def mapear_operador(string_operador):
    operadores = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '=': lambda x, y: x == y
    }

    return operadores.get(string_operador, None)

# Exemplo de uso
operador_string = ">"

# Mapear a string do operador para uma função
operador = mapear_operador(operador_string)

if operador:
    resultado = operador("CREATE TABLEEE", "CREATE TABLE")  # Substitua 5 e 3 pelos valores que deseja comparar
    print(f"O resultado da comparação é: {resultado}")
else:
    print("Operador não reconhecido.")
