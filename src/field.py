class Field:

    def __init__(self, id: str, name: str, type: str)-> None:
        self.field_id = id
        self.field_name = name
        self.type = type
        self.constraints = ""
        self.is_foreign_key = False
        self.origin_field_name = ""
        self.origin_table_name = ""
        self.foreign_key_constraints = ""
