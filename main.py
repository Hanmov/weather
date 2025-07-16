import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Погода"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label='Введите город', width=400)
    wether_data = ft.Text('')

    def get_info(e):
        if len(user_data.value) < 2:
            return

        API = 'a3debb042aabb74bcfccef1ea03618ba'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={API}&units=metric'
        res = requests.get(URL).json()
        temp = res['main']['temp']
        wether_data.value = 'Погода: ' + str(temp)
        page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.SUNNY, on_click=change_theme),
                ft.Text('Погодная программа')
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([wether_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton('Получить', on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main)    