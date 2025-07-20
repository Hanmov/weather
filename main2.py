import flet as ft
import sqlite3
import requests

def main(page: ft.Page):
    page.title = "Погода"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 530
    page.window_resizable = False

    user_login = ft.TextField(label='Логин', width=200)
    user_pass = ft.TextField(label='Пароль', password=True, width=200)
    btn_reg = ft.OutlinedButton(text='Зарегистрироваться', width=200, disabled=True)
    btn_auth = ft.OutlinedButton(text='Войти', width=200, disabled=True)

    city_input = ft.TextField(label='Введите город', width=300)
    weather_info = ft.Text('')

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()

    def register(e):
        db = sqlite3.connect('Hanmov.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT             
        )""")     
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')")
        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        page.snack_bar = ft.SnackBar(ft.Text('Успешная регистрация!'))
        page.snack_bar.open = True
        page.update()

    def auth_user(e):
        db = sqlite3.connect('Hanmov.db')
        cur = db.cursor() 
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'")
        if cur.fetchone() is not None:
            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(
                    ft.NavigationDestination(
                        icon=ft.icons.WB_SUNNY,
                        label='Погода',
                        selected_icon=ft.icons.WB_SUNNY_OUTLINED
                    )
                )
            
            user_login.value = ''
            user_pass.value = ''
            page.snack_bar = ft.SnackBar(ft.Text('Успешная авторизация!'))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Неверно введены данные'))
            page.snack_bar.open = True
            page.update()
        db.close()

    def get_weather(e):
        if len(city_input.value) < 2:
            return

        API = 'a3debb042aabb74bcfccef1ea03618ba'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_input.value}&appid={API}&units=metric&lang=ru'
        try:
            res = requests.get(URL).json()
            temp = res['main']['temp']
            description = res['weather'][0]['description']
            weather_info.value = (f'Погода в городе {city_input.value}:\n'
                                f'Температура: {temp}°C\n')
        except:
            weather_info.value = 'Ошибка получения данных'
        page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    panel_register = ft.Column(
        [
            ft.Row([ft.IconButton(ft.icons.SUNNY, on_click=change_theme)], 
                alignment=ft.MainAxisAlignment.END),
            ft.Text('Регистрация', size=20, text_align=ft.TextAlign.CENTER),
            user_login,
            user_pass,
            btn_reg
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    panel_auth = ft.Column(
        [
            ft.Row([ft.IconButton(ft.icons.SUNNY, on_click=change_theme)], 
                alignment=ft.MainAxisAlignment.END),
            ft.Text('Авторизация', size=20, text_align=ft.TextAlign.CENTER),
            user_login,
            user_pass,
            btn_auth
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    panel_weather = ft.Column(
        [
            ft.Row([ft.IconButton(ft.icons.SUNNY, on_click=change_theme)], 
                alignment=ft.MainAxisAlignment.END),
            ft.Text('Погодная программа', size=15, text_align=ft.TextAlign.CENTER),
            city_input,
            ft.ElevatedButton('Получить погоду', on_click=get_weather),
            weather_info
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()
        
        if index == 0:
            page.add(panel_register)
        elif index == 1:
            page.add(panel_auth)
        elif index == 2:
            page.add(panel_weather)

    user_login.on_change = validate
    user_pass.on_change = validate
    btn_reg.on_click = register
    btn_auth.on_click = auth_user

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Регистрация'),
            ft.NavigationDestination(icon=ft.icons.LOGIN, label='Авторизация'),
        ],
        on_change=navigate
    )

    page.add(panel_register)

ft.app(target=main)