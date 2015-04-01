from flask import Flask, render_template, redirect, request
import pywapi
import time
import sendgrid
import serial

app = Flask(__name__)

@app.route('/')
def index():
	ser = serial.Serial("COM3", 9600, timeout=0)
	while 1:
		val = ser.readline()
		if '1' in str(val):
			return redirect('/weather')
		elif '2' in str(val):
			return redirect('/sms')
		elif '3' in str(val):
			return redirect('/email')
		time.sleep(1)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
	if request.method == 'POST':
		phone_number = request.form['phone-text']
		recipient = str(phone_number) + "@vtext.com"
		content = "Emergency: Patient is in trouble."
		send_email(recipient, content)

	return render_template('sms.html')

@app.route('/email', methods=['GET', 'POST'])
def email():
	if request.method == 'POST':
		recipient = request.form['email-text']
		content = "Emergency: Patient needs medical attention and has activated emergency notification switch."
		send_email(recipient, content)

	return render_template('email.html')

@app.route('/weather', methods=['GET'])
def weather():
	city = pywapi.get_weather_from_weather_com('USNJ0190')

	curr_temp = c_to_f(int(city['current_conditions']['temperature']))
	curr_real_feel = c_to_f(int(city['current_conditions']['feels_like']))
	curr_wind_speed = int(city['current_conditions']['wind']['speed'])
	curr_wind_dir = city['current_conditions']['wind']['text']
	text = city['current_conditions']['text']
	curr_humidity = city['current_conditions']['humidity']

	tonight_temp = c_to_f(int(city['forecasts'][0]['low']))
	tonight_wind_speed = int(city['forecasts'][0]['night']['wind']['speed'])
	tonight_text = city['forecasts'][0]['night']['text']
	tonight_wind_dir = city['forecasts'][0]['night']['wind']['text']

	tomorrow_temp = c_to_f(int(city['forecasts'][1]['high']))
	tomorrow_wind_speed = int(city['forecasts'][1]['day']['wind']['speed'])
	tomorrow_text = city['forecasts'][1]['day']['text']
	tomorrow_wind_dir = city['forecasts'][1]['day']['wind']['text']

	ser = serial.Serial('COM3', 9600)
	message = ser.readline()
	ser.write(message)

	return render_template('weather.html', temp=curr_temp, actual_temp=curr_real_feel, wind_speed=curr_wind_speed, status=text, 
		humidity=curr_humidity, wind_direction = curr_wind_dir, night_temp=tonight_temp, night_wind_speed=tonight_wind_speed, 
		night_wind_dir=tonight_wind_dir, night_status=tonight_text, tom_temp=tomorrow_temp, tom_wind_speed=tomorrow_wind_speed,
		tom_status=tomorrow_text, tom_wind_dir=tomorrow_wind_dir)

def c_to_f(original):
	return int((1.8 * original) + 32)

def send_email(recipient, content):
	sg = sendgrid.SendGridClient('username', 'password')
	message = sendgrid.Mail()
	message.add_to('<' + recipient)
	message.set_subject('Emergency: Patient is in trouble')
	message.set_from('<test@shaantam.com>')
	message.set_text(content)
	status, msg = sg.send(message)

if __name__ == "__main__":
    app.run(debug=True)
