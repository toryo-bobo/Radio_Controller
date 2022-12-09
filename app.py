from flask import Flask, render_template, request
import os
from flask import send_from_directory
import RPi.GPIO as GPIO
import smbus

## i2c
i2c = smbus.SMBus(1)
addr = 0x00 # example

app = Flask(__name__)

class Motor:
    LF = 21
    LB = 22
    RF = 23
    RB = 24
    state = "stop"
    speed = "0"

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        state = "stop"
        speed = "0"
        speed_arr = [0x000, 0x400, 0x800, 0xa00, 0xf00, 0xfff]
        GPIO.setup(self.LF, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RF, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RB, GPIO.OUT, initial=GPIO.LOW)
        self.reset()

    def __del__(self):
        self.reset()
        GPIO.cleanup()

    def reset(self):
        GPIO.output(self.LF, GPIO.LOW)
        GPIO.output(self.LB, GPIO.LOW)
        GPIO.output(self.RF, GPIO.LOW)
        GPIO.output(self.RB, GPIO.LOW)

    def update_control(self, ctrl):
        self.state = ctrl

    def update_speed(self, speed):
        self.speed = speed

    def get_control(self):
        return self.state

    def get_speed(self):
        return self.speed

    def state_ctrl(self):
        self.reset()
        value = self.state
        if value == "go":
            GPIO.output(self.LF, GPIO.HIGH)
            GPIO.output(self.RF, GPIO.HIGH)
        elif value == "back":
            GPIO.output(self.LB, GPIO.HIGH)
            GPIO.output(self.RB, GPIO.HIGH)
        elif value == "stop":
            pass
        elif value == "right":
            GPIO.output(self.LB, GPIO.HIGH)
            GPIO.output(self.RF, GPIO.HIGH)
        elif value == "left":
            GPIO.output(self.LF, GPIO.HIGH)
            GPIO.output(self.RB, GPIO.HIGH)

    # def speed_ctrl(self):
    #     value = int(self.speed)
    #     #command format: i2c communication address, writable address, writing data (list type)
    #     data00 = int(value % 16)
    #     data01 = int(value // 16)
    #     i2c.write_i2c_block_data(addr, 0x01, [data01, data00])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def greeting():
    return "Hello!!"

@app.route("/index")
def index():
    name = request.args.get("name")
    value = request.args.get("value")
    ctrl = motor.get_control()
    speed = motor.get_speed()
    return render_template("index.html", name=name, value=value, ctrl=ctrl, speed=speed)

@app.route("/index", methods=["POST"])
def post():
    ctrl = request.form.get("ctrl", None)
    control(ctrl)
    name = request.args.get("name")
    value = request.args.get("value")
    ctrl = motor.get_control()
    speed = motor.get_speed()
    return render_template("index.html", name=name, value=value, ctrl=ctrl, speed=speed)

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup()

def control(ctrl):
    print("received data is {}".format(ctrl))
    if(ctrl == "stop" or ctrl == "go" or ctrl == "back"):
        motor.update_control(ctrl)
    else:
        motor.update_speed(ctrl)
    motor.state_ctrl()
    # motor.speed_ctrl()

motor = Motor()
    
if __name__ == "__main__":
    try:
        #app.run(debug=False, host="0.0.0.0", port=443)
        #app.run(debug=False, host="0.0.0.0", port=80)
        app.run()
    except Exception as e:
        print(type(e))
        print(e)
        del motor
