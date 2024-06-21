import tkinter as tk
import requests


class FullScreenApp:
    def __init__(self, master):
        self.master = master
        master.attributes('-fullscreen', True)
        master.configure(background='black')

        self.label = tk.Label(master, text="Weather Updates", font=(
            'Helvetica', 24), fg='white', bg='black')
        self.label.pack(expand=True)

        self.weather_label = tk.Label(master, text="", font=(
            'Helvetica', 18), fg='white', bg='black')
        self.weather_label.pack()

        self.update_weather()

    def update_weather(self):
        api_key = '8788141e3db031b536fe02ab2e720291'
        zipcode = 94089
        url = f'https://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={api_key}'

        try:
            response = requests.get(url)
            data = response.json()
            weather_description = data['weather'][0]['description'].capitalize(
            )
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_str = f"Description: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
            self.weather_label.config(text=weather_str)
        except Exception as e:
            print("Error fetching weather data:", e)

        # Update weather every 10 minutes (600000 milliseconds)
        self.master.after(600000, self.update_weather)


root = tk.Tk()
app = FullScreenApp(root)
root.mainloop()
