class Field:

    def __init__(self, id: str, name: str, type: str)-> None:
        self.field_id = id
        self.field_name = name
        self.type = type
        self.constraints = ""
        self.value = ""
        self.is_foreign_key = 0
        self.origin_field_name = ""
        self.origin_table_name = ""
        self.foreign_key_constraints = ""

#preciso fazer método para pegar o nome?