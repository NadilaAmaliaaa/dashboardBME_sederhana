import asyncio

from microdot import Microdot, Response, send_file

import urequests as requests #urequest hanya digunakan jika pada micropython, jika pada desktop gunakan request biasa
import network
from machine import Pin, I2C
from bme_module import BME280Module
import gc


app = Microdot()
Response.default_content_type = 'application/json'

SSID = "BOE-"
PASSWORD = ""

sda = Pin(5)
scl = Pin(4)

bme_module = BME280Module(0, scl, sda)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    print("Connected:", wlan.isconnected())  # Harus True
    print("Config:", wlan.ifconfig())
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print("Menghubungkan ke Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Masih mencoba...")
    
    print("Wi-Fi Terhubung!")
    print("Alamat IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Hubungkan ke Wi-Fi
ip_address = connect_wifi(SSID, PASSWORD)

@app.route('/')
def index(request):
    return send_file('templates/ppt.html')

@app.route('/static/<path:path>')
def static_files(request, path):
    return send_file('static/' + path)

#API Flask
FLASK_API_URL = "http://192.168.57.64:5050"

@app.route('/api/tanaman')
def get_tanaman(request):
    try:
        response = requests.get(f"{FLASK_API_URL}/api/tanaman")  # Ambil dari Flask
        data = response.json()  # Ubah ke JSON
        response.close()  # Tutup request
        print(gc.mem_free())  # Lihat sisa memori bebas
        gc.collect()
        return data  # Kirim ke frontend

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/bme')
def get_bme(request):
    temp, pressure,humdt, altitude = bme_module.get_sensor_readings()
    # Data simulasi
    suhu = temp
    tekanan = pressure
    alt = round(altitude)
        
    data = {
        "temperature": suhu,
        "pressure": tekanan,
        "altitude": alt 
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{FLASK_API_URL}/api/predict", json=data, headers=headers, timeout=30)
    result = response.json()
    response.close()

    zone = result.get("zone", "Tidak diketahui")
    conf = result.get("conf", "Tidak diketahui")

    data['zone'] = zone
    data['conf'] = conf
    return data

if __name__ == '__main__':
    app.run(host=ip_address, port=5007, debug=True)


