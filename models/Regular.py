from dataclasses import dataclass

@dataclass
class Regular:
    regular_id: int
    regular_expression: str
    expression_status: int
