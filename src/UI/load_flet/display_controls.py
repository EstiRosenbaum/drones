import flet as ft

from server.s3_api.create_bucket_s3 import create_bucket_s3
from UI.controls.container import Container
from UI.form_logic.helpers import update_status
from UI.load_flet.create_controls import create_all_controls


def main(page: ft.Page):
    (
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
    ) = create_all_controls()
    status_value = create_bucket_s3()
    if status_value:
        update_status(status, page, status_value)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    content = ft.ResponsiveRow(
        [
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                col={"sm": 3, "md": 3, "lg": 3},
                run_spacing={"xs": 25},
                controls=[
                    tabs,
                    control_points,
                ],
            ),
            ft.Column(
                spacing=15,
                col={"sm": 3, "md": 3, "lg": 3},
                controls=[
                    location_error_radius,
                    distance_below_platform,
                    distance_above_peak,
                    los_safety_angle,
                    surface,
                    resolution,
                ],
            ),
            buttons,
        ],
        col={"sm": 3, "md": 3, "lg": 5},
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add(
        ft.Card(
            content=Container(
                ft.Column(
                    [list_tile, content, status],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=50,
            ),
            width=1200,
        )
    )
