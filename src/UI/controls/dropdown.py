import flet as ft


class Dropdown(ft.Dropdown):
    def __init__(
        self, on_change, value: str = "", options=[], label: str = "", width=None
    ) -> None:
        super().__init__()
        self.value = value
        self.options = options
        self.label = label
        self.on_change = on_change
        self.width = width

    def add_option(self, value: str) -> None:
        self.options.append(ft.dropdown.Option(value))
        self.value = value

    def remove_option(self, value: str) -> None:
        option = self._find_option(value)
        if option is not None:
            self.options.remove(option)

    def _find_option(self, option_name: str):
        for option in self.options:
            if option_name == option.key:
                return option
        return None
