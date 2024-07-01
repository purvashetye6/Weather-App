import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import requests

def get_weather(city):
    API_KEY = "66df86d20c93fef45c8647c29d2fa1f2"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        icon_id = data['weather'][0]['icon']
        weather = data['weather'][0]['description']
        temperature = round(data['main']['temp'] - 273.15, 2)
        city = data['name']
        country = data['sys']['country']

        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

        return (icon_url, temperature, weather, city, country)
    else:
        return None

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        messagebox.showerror("Error", "City not found. Please enter a valid city name.")
        return
    icon_url, temperature, weather, city, country = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    weather_label.configure(text=f"Weather: {weather}")

def clear_entry(event):
    city_entry.delete(0, tk.END)
    city_entry.unbind('<FocusIn>')

root = ttk.Window(themename='morph')
root.title("Weather APP")
root.geometry("400x500")

city_entry = ttk.Entry(root, font=("Helvetica", 18))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter a City: ")
city_entry.bind('<FocusIn>', clear_entry)

search_button = ttk.Button(root, text="Search", command=search, bootstyle="Warning")
search_button.pack(pady=10)

location_frame = ttk.Frame(root)
location_frame.pack(pady=20)

location_label = tk.Label(location_frame, font=("Helvetica", 25))
location_label.pack()

icon_label = tk.Label(root)
icon_label.pack(pady=10)

temperature_label = tk.Label(root, font=("Helvetica", 20))
temperature_label.pack()

weather_label = tk.Label(root, font=("Helvetica", 20))
weather_label.pack()

root.mainloop()
