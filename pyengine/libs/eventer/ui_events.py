"""Define ui elements basic events"""
#### Python Packages ####

#### My Packages ####


class ButtonEvents:
    """Define buttons events class"""

    current_active_button = None

    @staticmethod
    def button_hover(button: object, hover: bool = True) -> None:
        """
        Change the button state to hover

        Arguments:
            button: hovered button
        """
        if button.active:
            return

        if hover:
            button.active_color = button.hover_color
        else:
            button.active_color = button.base_color

    @staticmethod
    def button_select(button: object) -> None:
        """
        Change the button state to select

        Arguments:
            button: selected button
        """
        if ButtonEvents.current_active_button is not None:
            ButtonEvents.current_active_button.active = False
            ButtonEvents.current_active_button.active_color = (
                ButtonEvents.current_active_button.base_color
            )

        button.active_color = button.select_color
        button.active = True
        ButtonEvents.current_active_button = button
