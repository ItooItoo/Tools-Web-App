import os
import os.path
from flask import Flask, render_template, redirect, request, send_file
import pyqrcode
from pyqrcode import QRCode
import png
import requests

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        url = request.form.get("url")  # Get user's link
        qr = pyqrcode.create(url)
        a = qr.png("qrcode.png", scale=8) # Generate qrcode 
        return redirect("/download") # redirect to download route
    else:
        if os.path.exists("E:\Flask\qrcode.png") == True: 
            os.remove("E:\Flask\qrcode.png")    # if exists delete this file when new will be generate
    return render_template("qrcode.html") 

@app.route("/download",methods=['GET','POST'])
def download():

    
    return (send_file('/Flask/qrcode.png',attachment_filename='qrcode.png'))  # Send file for user

@app.route("/weather",methods=['GET','POST'])
def weather():
    if request.method == 'POST':
        API_KEY = '080f0ae474b49f6788a765043df219a2' # OpenWether API_KEY
        
        user_location = request.form.get("user-location") # Get user's input
        if user_location == None:
            user_location = 'London'
        try:
            weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_location}&APPID={API_KEY}") # Get JSON file from api with user location
            celcius_temp = weather.json()['main']['temp'] - 273.15
            feels_temp = weather.json()['main']['feels_like'] - 273.15
            pressure = weather.json()['main']['pressure']
            wind_speed = weather.json()['wind']['speed']
            humidity = weather.json()['main']['humidity']
            icon = weather.json()['weather'][0]['icon']
            weather_description = weather.json()['weather'][0]['description']
        except KeyError:
            return render_template("weather.html")
        return render_template("weather.html",weather=weather.text,celcius_temp=round(celcius_temp),icon=icon,weather_description=weather_description,pressure=pressure,user_location=user_location,wind_speed=wind_speed,humidity=humidity)
    else:
        icon='01d'
        return render_template("weather.html",icon=icon)
    

@app.route("/conventer",methods=['GET','POST'])
def conventer():
    if request.method == 'POST':
        mile_input = request.form.get("mile")
        inch_input = request.form.get("inch")
        feet_input = request.form.get("feet")
        yard_input = request.form.get("yard")
        kilometers = 0
        centimeters = 0
        f_centimeters = 0
        meters = 0
        
        if mile_input:
            kilometers = float(mile_input) * 1.609344
        if inch_input:
            centimeters = float(inch_input) * 2.54
        if feet_input:
            f_centimeters = float(feet_input) * 30.48
        if yard_input:
            meters = float(yard_input) * 0.9144


        return render_template("conventer.html", kilometers=round(kilometers,6),centimeters=round(centimeters,6),f_centimeters=round(f_centimeters,6),meters=round(meters,6))
    else:
        return render_template("conventer.html")

if __name__ == '__main__':
    app.run(debug=True)
