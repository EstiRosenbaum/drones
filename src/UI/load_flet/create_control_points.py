from typing import Callable

import flet as ft

from redis_cache.connect_redis import Redis
from UI.controls.buttons import IconButton, PopUpButton
from UI.controls.dropdown import Dropdown
from UI.controls.inputs import Input
from UI.controls.popup import PopUp
from UI.form_logic.validation import mark_input_error, validate_control_point_input
from UI.utils.const import FolderInRedis


class ControlPointsDropdown(Dropdown):
    def __init__(self, on_change, value: str = "", label: str = "") -> None:
        super().__init__(on_change, value, options=[], label=label, width=200)

    def build(self) -> None:
        redis = Redis()
        keys = redis.get_keys(FolderInRedis.CONTROL_POINTS)
        options = [item.split(":")[1] for item in keys]

        for option in options:
            self.add_option(option)
        self.value = ""


class HandlingShownPoints(ft.Column):
    def __init__(
        self, name: str = "", points: str = "", delete_action: Callable = None
    ) -> None:
        super().__init__()
        self.delete_action = delete_action
        self.antenna_name = name
        self.antenna_points = points
        self.display_points = ft.Text(points, width=170)
        self.edit_points = Input(
            "Control Point",
            helper_text="format: Lat,Lng,Height or UTM_e,UTM_n,Height",
            width=230,
        )

        self.display_view = ft.Row(
            [
                self.display_points,
                IconButton(
                    icon=ft.icons.CREATE_OUTLINED, on_click=lambda e: self.edit()
                ),
                IconButton(ft.icons.DELETE_OUTLINE, on_click=lambda e: self.delete()),
            ],
            spacing=0,
            visible=False,
        )

        self.edit_view = ft.Row(
            width=350,
            controls=[
                self.edit_points,
                IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    on_click=lambda e: self.save(),
                ),
            ],
            visible=False,
        )

        self.controls = [self.display_view, self.edit_view]

    def delete(self) -> None:
        self.display_view.visible = False
        self.delete_action()

    def edit(self) -> None:
        self._change_inputs(self.display_view, self.edit_view)
        self.edit_points.value = self.display_points.value
        self.update()

    def save(self) -> None:
        if validate_control_point_input(self.edit_points):
            redis = Redis()
            redis.update_value_to_folder(
                FolderInRedis.CONTROL_POINTS, self.antenna_name, self.edit_points.value
            )
            self.edit_points.error_text = None
            self._change_inputs(self.edit_view, self.display_view)
            self.display_points.value = self.edit_points.value
        self.update()

    def _change_inputs(
        self, row_displayed: ft.Row, row_to_be_displayed: ft.Row
    ) -> None:
        row_displayed.visible = False
        row_to_be_displayed.visible = True


class ControlPoints(ft.Column):
    def __init__(self, add_clicked) -> None:
        super().__init__()
        self.dropdown = ControlPointsDropdown(
            label="list of control point", on_change=self.on_selected
        )
        self.add_clicked = add_clicked

        self.control_points_list = ft.Row(
            controls=[
                self.dropdown,
                IconButton(
                    ft.icons.ADD, tooltip="add new control-points", on_click=add_clicked
                ),
            ],
            spacing=5,
        )

        self.shown_points = HandlingShownPoints(delete_action=self._delete_option)

        self.controls = [ft.Column([self.control_points_list, self.shown_points])]

    def _delete_option(self) -> None:
        redis = Redis()
        redis.remove_value_from_folder(
            FolderInRedis.CONTROL_POINTS, self.dropdown.value
        )
        self.dropdown.remove_option(self.dropdown.value)
        self.update()

    def on_selected(self, e):
        redis = Redis()
        points = redis.get_value(
            f"{FolderInRedis.CONTROL_POINTS}:{self.dropdown.value}"
        )
        self.shown_points.display_view.visible = True
        self.shown_points.edit_view.visible = False
        self.shown_points.display_points.value = points
        self.shown_points.antenna_name = self.dropdown.value
        self.dropdown.error_text = None
        self.update()


class ControlPointsPopUp(PopUp):
    def __init__(self, handle_close) -> None:
        self.name_input = Input(label="name")
        self.points_input = Input(
            label="points", helper_text="format: Lat,Lng,Height or UTM_e,UTM_n,Height"
        )
        super().__init__(
            title="add new control-points",
            content=ft.Column(
                [
                    ft.Text("please enter name and point to create new control points"),
                    self.name_input,
                    self.points_input,
                ],
                height=130,
            ),
            actions=[
                PopUpButton("cancel", handle_close),
                PopUpButton("confirm", handle_close),
            ],
        )

    def clear(self, page: ft.Page) -> None:
        page.close(self)
        self.name_input.value = ""
        self.points_input.value = ""
        self.points_input.error_text = None
        self.name_input.error_text = None

    def update_control_points(
        self, e: ft.ControlEvent, control_points: ControlPoints
    ) -> None:
        redis = Redis()
        redis.update_value_to_folder(
            FolderInRedis.CONTROL_POINTS, self.name_input.value, self.points_input.value
        )
        control_points.dropdown.add_option(self.name_input.value)
        control_points.on_selected(e)
        control_points.shown_points.display_view.visible = True
        control_points.shown_points.display_points.value = self.points_input.value
        control_points.update()

    def not_exist_in_redis(self) -> bool:
        redis = Redis()
        value = redis.get_value(
            f"{FolderInRedis.CONTROL_POINTS}:{self.name_input.value}"
        )
        if value is not None:
            mark_input_error(self.name_input, "is already exist")
            self.update()
            return False
        return True
