class Field:

    field_id = int
    field_name = str
    type = str
    constraints = str
    value = str
    is_foreign_key = bool
    origin_field_name = str
    origin_table_name = str
    foreign_key_constraints = str 

    def __init__(self, id: int, name: str, type: str, constraints: str) -> None:
        self.field_id = id
        self.field_name = name
        self.type = type
        self.constraints = constraints
        self.value = ""
        self.is_foreign_key = 0
        self.origin_field_name = ""
        self.origin_table_name = ""
        self.foreign_key_constraints = ""

#preciso fazer método para pegar o nome?