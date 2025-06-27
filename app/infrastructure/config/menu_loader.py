import json
from typing import Dict
from app.domain.entities.menu.menu_item import MenuItem, MenuOption


class MenuLoader:
    """Carga la configuración de menús desde JSON"""

    @staticmethod
    def load_from_file(config_path: str = 'menus_config.json') -> Dict[str, MenuItem]:
        """Carga menús desde archivo JSON"""
        with open(config_path, encoding='utf-8') as f:
            config = json.load(f)

        menus = {}
        for menu_id, menu_data in config.items():
            # Crear opciones
            options = []
            for opt_data in menu_data.get('options', []):
                option = MenuOption(
                    key=opt_data['key'],
                    label=opt_data['label'],
                    target_menu_id=opt_data.get('target_menu_id'),
                    action=opt_data.get('action')
                )
                options.append(option)

            # Crear menú
            menu = MenuItem(
                id=menu_data['id'],
                title=menu_data['title'],
                message=menu_data['message'],
                options=options,
                action=menu_data.get('action'),
                is_dynamic=menu_data.get('is_dynamic', False),
                dynamic_data_key=menu_data.get('dynamic_data_key')
            )

            menus[menu_id] = menu

        return menus
