from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MenuOption:
    """Representa una opción dentro de un menú"""
    key: str
    label: str
    target_menu_id: Optional[str] = None
    action: Optional[str] = None


@dataclass
class MenuItem:
    """Representa un ítem de menú completo"""
    id: str
    title: str
    message: str
    options: List[MenuOption]
    action: Optional[str] = None
    is_dynamic: bool = False
    dynamic_data_key: Optional[str] = None
