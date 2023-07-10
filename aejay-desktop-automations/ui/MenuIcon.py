from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from typing import Callable, List, cast
from screen_management import FunkyState

def _empty_callback():
    pass

class MenuIcon:
    def __init__(
            self, 
            change_callback: Callable[[FunkyState], None] = lambda _: None,
            exit_callback: Callable[[], None] = _empty_callback,
        ) -> None:
        self.funky_state: FunkyState = FunkyState.NORMAL
        self.change_callback = change_callback
        self.exit_callback = exit_callback

        image = self._create_image()
        menu_items: List[MenuItem] = []
        for state in FunkyState:
            menu_item = MenuItem(state.value, self._on_option_selected, radio=True, checked=lambda item: item.text == self.funky_state.value)
            menu_items.append(menu_item)
        menu_items.append(MenuItem("Exit", self._on_exit_clicked))

        self.icon = Icon("aejay", image, "Aejay Automations", menu=Menu(
            *menu_items
        ))

    def set_funkiness(self, state: FunkyState) -> None:
        for item in cast(List[MenuItem], self.icon.menu):
            if item.text == state.value:
                self._on_option_selected(self.icon, item)
                return
    
    def _create_image(self):
        # Generate an image for the icon
        image = Image.new('RGB', (64, 64), "cyan")
        ImageDraw.Draw(image)
        return image

    def _on_option_selected(self, icon: Icon, item: MenuItem) -> None:
        self.funky_state = FunkyState.from_value(item.text)
        self.change_callback(self.funky_state)
        icon.update_menu()

    def _on_exit_clicked(self, icon: Icon) -> None:
        self.exit_callback()
        icon.stop()
