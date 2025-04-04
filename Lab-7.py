import requests
import json
API_KEY = "У  меня работало, но нужно ввести проверяющему свой))"  
MKS = "http://api.open-notify.org/"

def MKS_position():
    try:
        url = MKS + "iss-now.json"
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        if data["message"] == "success":
            timestamp = data["timestamp"]
            latitude = data["iss_position"]["latitude"]
            longitude = data["iss_position"]["longitude"]
            print(" ")
            print("Текущая позиция МКС:",f"  Широта: {latitude}",f"  Долгота: {longitude}",f"  Время получения данных в Unix Timestamp: {timestamp}")
        else:
            print("Не удалось получить позицию МКС.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка при разборе JSON: {e}")

def get_number_of_people_in_space():
    try:
        url = MKS + "astros.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        number = data["number"]
        people = data["people"]
        print(" ")
        print(f"Количество людей, которые сейчас находятся в космосе: {number}")
        for person in people:
            print(f"Космонафт: {person['name']} находится на корабле: {person['craft']}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка при разборе JSON: {e}")
def get_iss_pass_times(latitude, longitude):
    try:
        url = MKS + "iss-pass.json"
        params = {"lat": latitude, "lon": longitude} 
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["message"] == "success":
            print(f"\nВремя пролета МКС над широтой {latitude}, долготой {longitude}:")
            passes = data["response"]
            if passes:
                for i, p in enumerate(passes):
                    duration = p["duration"]
                    risetime = p["risetime"]
                    print(f"  Пролет {i+1}:")
                    print(f"    Время начала (unix timestamp): {risetime}")
                    print(f"    Продолжительность (секунды): {duration}")
            else:
                 print("Над заданной точкой пролеты МКС не обнаружены в ближайшем будущем")
        else:
            print("Не удалось получить время пролета МКС.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка при разборе JSON: {e}")

city_name = "Moscow"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"#units=metric для градусов Цельсия
try:
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    description = data["weather"][0]["description"] 
    print(f"Погода в городе {city_name}:")
    print(f"Описание: {description}")
    print(f"Температура: {temperature}°C")
    print(f"Влажность: {humidity}%")
    print(f"Давление: {pressure} гПа")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к API: {e}")
except KeyError as e:
    print(f"Ошибка при разборе данных JSON: Отсутствует ключ {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

MKS_position()
get_number_of_people_in_space()
get_iss_pass_times(55.75, 37.62)  # Пример: Москва (широта, долгота)
get_iss_pass_times(40.71, -74.01) # Пример: Нью-Йорк