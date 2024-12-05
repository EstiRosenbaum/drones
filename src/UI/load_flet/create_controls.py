import re

import flet as ft

from modules.setup_env import get_env_instance
from server.s3_api.s3_actions import get_url
from UI.controls.buttons import Button, IconButton
from UI.controls.container import Container
from UI.controls.inputs import Input, InputNumber, InputTextArea
from UI.controls.list_tile import ListTile
from UI.controls.tab import Tab, Tabs
from UI.form_logic.execute_command import start_execution_thread
from UI.form_logic.helpers import update_status
from UI.form_logic.validation import validate_control_point_input, validate_input
from UI.load_flet.create_control_points import ControlPoints, ControlPointsPopUp
from UI.utils.const import DEFAULT_VALUE

bucket_name = get_env_instance().BUCKET_NAME


def create_all_controls():
    def _change_buttons(button_to_enable: Button, button_to_disable: Button) -> None:
        button_to_enable.disabled = False
        button_to_disable.disabled = True

    def on_tab_click(e: ft.ControlEvent) -> None:
        button_execute = buttons.controls[0]
        generate_button = button_execute.controls[0].controls[0]
        validate_button = button_execute.controls[1]
        if e.data == "0":
            _change_buttons(validate_button, generate_button)
            button_execute.controls[0].controls[1].visible = False
        else:
            _change_buttons(generate_button, validate_button)
        e.page.update()

    def validate(e: ft.ControlEvent) -> None:
        value = start_execution_thread(
            dict_default_value_controls,
            dict_controls_validate,
            e.page,
        )
        if value:
            update_status(status, e.page, value)

    def generate(e: ft.ControlEvent) -> None:
        generate_route_name.data = generate_route_name.value
        value = start_execution_thread(
            dict_default_value_controls,
            dict_controls_generate,
            e.page,
        )
        if value:
            update_status(status, e.page, value)

    def handle_close(
        e: ft.ControlEvent,
        popup: ControlPointsPopUp,
        control_points: ControlPoints,
    ) -> None:
        if e.control.text == "confirm":
            if (
                validate_input(popup.name_input)
                and validate_control_point_input(popup.points_input)
                and popup.not_exist_in_redis()
            ):
                popup.update_control_points(e, control_points)
                popup.clear(e.page)
        else:
            popup.clear(e.page)
        e.page.update()

    def download_generate_file(page: ft.Page) -> None:
        url = get_url(bucket_name, f"{generate_route_name.data}-table.csv")
        if url is not None:
            url = re.sub(r"http://.*?(?=/)", "http://localhost:9000", url)
            page.launch_url(url)

    status = ft.Text("")

    list_tile = ListTile("Apollo", ft.FontWeight.BOLD, ft.TextAlign.CENTER, 60)

    location_error_radius = InputNumber("Location Error Radius", DEFAULT_VALUE.RADIUS)

    distance_below_platform = InputNumber(
        "LOS Safety Distance Below Platform", DEFAULT_VALUE.LOS_BELOW_PLATFORM
    )

    distance_above_peak = InputNumber(
        "LOS Safety Distance Above Peak", DEFAULT_VALUE.LOS_ABOVE_PEAK
    )

    los_safety_angle = InputNumber("LOS Safety Angle", DEFAULT_VALUE.LOS_ANGLE)

    surface = InputNumber("Surface", DEFAULT_VALUE.SURFACE)

    resolution = Input("Resolution")

    generate_route_name = Input("Route Name")

    generate_route_NZ = InputTextArea(
        "Route N.Z.", helper_text="format: Lat,Lng or UTM_e,UTM_n"
    )

    validate_route_name = Input("Route Name")

    validate_route_NZ = InputTextArea(
        "Route N.Z.", helper_text="format: Lat,Lng,Height or UTM_e,UTM_n,Height"
    )

    validate_form = Container(
        ft.Column(controls=[validate_route_name, validate_route_NZ]),
        padding=ft.padding.only(top=10),
    )

    generate_form = Container(
        ft.Column(controls=[generate_route_name, generate_route_NZ]),
        padding=ft.padding.only(top=10),
    )

    validate_tab = Tab(
        validate_form, ft.icons.YOUTUBE_SEARCHED_FOR_OUTLINED, "Validate"
    )

    generate_tab = Tab(generate_form, ft.icons.MAP_SHARP, "Generate")

    tabs = Tabs(tabs=[validate_tab, generate_tab], on_click=on_tab_click, height=430)

    download = IconButton(
        ft.icons.DOWNLOAD,
        on_click=lambda e: download_generate_file(e.page),
        visible=False,
    )

    buttons = ft.Row(
        [
            ft.Column(
                [
                    ft.Row(
                        [
                            Button(
                                text="Generate 3D",
                                on_click=generate,
                                disabled=True,
                            ),
                            download,
                        ]
                    ),
                    Button(
                        "Validate Route",
                        on_click=validate,
                    ),
                ]
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    control_points = ControlPoints(lambda e: e.page.open(popup))

    popup = ControlPointsPopUp(lambda e: handle_close(e, popup, control_points))

    dict_controls = {
        "control_point": control_points.dropdown,
        "radius": location_error_radius,
        "los_platform": distance_below_platform,
        "los_peak": distance_above_peak,
        "los_angle": los_safety_angle,
        "surface": surface,
        "resolution": resolution,
        "status": status,
    }

    dict_controls_generate = {
        **dict_controls,
        "route_path": generate_route_NZ,
        "route_name": generate_route_name,
        "download": download,
        "type": "generate",
    }

    dict_controls_validate = {
        **dict_controls,
        "route_path": validate_route_NZ,
        "route_name": validate_route_name,
        "type": "validate",
    }

    dict_default_value_controls = {
        "route_path": "",
        "control_point": "",
        "radius": DEFAULT_VALUE.RADIUS,
        "los_platform": DEFAULT_VALUE.LOS_BELOW_PLATFORM,
        "los_peak": DEFAULT_VALUE.LOS_ABOVE_PEAK,
        "los_angle": DEFAULT_VALUE.LOS_ANGLE,
        "surface": DEFAULT_VALUE.SURFACE,
        "download": download,
        "resolution": "",
        "status": "",
        "route_name": "",
    }

    return (
        buttons,
        control_points,
        distance_above_peak,
        distance_below_platform,
        location_error_radius,
        los_safety_angle,
        resolution,
        status,
        surface,
        tabs,
        list_tile,
    )
