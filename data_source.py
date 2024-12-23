import random
import aiohttp
from datetime import datetime
import asyncio
import serial


# URL вашего сервера
url = 'https://4c1f-34-125-82-134.ngrok-free.app'

# Параметры подключения к Arduino
SERIAL_PORT = 'COM3'  # Замените на порт, к которому подключено ваше Arduino
BAUD_RATE = 9600

# Функция для тестирования
# async def send_temperature():
#     async with aiohttp.ClientSession() as session:
#         while True:
#             temperature = round(random.uniform(20.0, 30.0), 2)
#             timestamp = datetime.now().isoformat()
#             payload = {"timestamp": timestamp, "temperature": temperature}
#             try:
#                 async with session.post(f"{url}/temperature", json=payload) as response:
#                     print(f"Sent: {payload}, Response: {response.status}")
#             except Exception as e:
#                 print(f"Error sending temperature: {e}")
#             await asyncio.sleep(1)


async def send_temperature():
    # Подключение к Arduino через последовательный порт
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print(f"Connected to Arduino on {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        return

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Чтение данных с Arduino
                if arduino.in_waiting > 0:
                    line = arduino.readline().decode('utf-8').strip()
                    try:
                        temperature = float(line)  # Преобразуем строку в число
                        timestamp = datetime.now().isoformat()
                        payload = {"timestamp": timestamp, "temperature": temperature}

                        # Отправка данных на сервер
                        async with session.post(f"{url}/temperature", json=payload) as response:
                            print(f"Sent: {payload}, Response: {response.status}")
                    except ValueError:
                        print(f"Invalid data from Arduino: {line}")
            except Exception as e:
                print(f"Error reading from Arduino or sending data: {e}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(send_temperature())
