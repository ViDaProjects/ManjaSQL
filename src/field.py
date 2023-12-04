class Field:

    def __init__(self, id: str, name: str, type: str, constraints: str)-> None:
        self.field_id = id
        self.field_name = name
        self.type = type
        self.constraints = constraints
        self.key_type = ""
        self.origin_table_name = ""
        self.foreign_key_constraints = ""
