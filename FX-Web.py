from flask import Flask, render_template, request

import serial, serial.tools.list_ports
import sys
import time
import socket

app = Flask(__name__)

arduino = None

currLevel = 0.4
currColor = ""
currAnim = ""
currPal = ""


@app.route("/")
def home():
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/brightness/", methods=['POST'])
def brightness():
    btn_name = get_btn_name(request)
    print ("Python: " + "Brightness:", btn_name )
    arduino_send_cmd("b "+str(btn_name)+"\n")
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/duration/", methods=['POST'])
def duration():
    duration = request.form['duration']
    print ("Python: " + "Duration:", duration)
    arduino_send_cmd("s "+str(duration)+"\n")
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/color/", methods=['POST'])
def color():
    btn_name = get_btn_name(request)
    print ("Python: " + "Color:", btn_name )
    #arduino_send_cmd("m 0\n")
    arduino_send_cmd("c "+str(btn_name)+"\n")
    templateData = {}
    return render_template('main.html', **templateData);
	
@app.route("/duration2/", methods=['POST'])
def duration2():
    btn_name = get_btn_name(request)
    print ("Python: " + "Duration2:", btn_name )
    arduino_send_cmd("s "+str(btn_name)+"\n")
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/palette/", methods=['POST'])
def palette():
    global currLevel
    global currColor
    global currAnim
    global currPal

    btn_name = get_btn_name(request)
    print ("Python: " + "Palette:", btn_name)
    arduino_send_cmd("P="+str(btn_name)+"\n")
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/anim/", methods=['POST'])
def anim():
    btn_name = get_btn_name(request)
    print ("Python: " + "Animation code:", btn_name)
    arduino_send_cmd("m "+str(btn_name)+"\n")
    templateData = {}
    return render_template('main.html', **templateData);


@app.route("/pal/", methods=['POST'])
def pal():
    global currLevel
    global currColor
    global currAnim
    global currPal

    if 'btnRgb' in request.form:
        arduino_send_cmd("a");
        currPal = "RGB";
    elif 'btnRainbow' in request.form:
        arduino_send_cmd("b");
        currPal = "Rainbow";
    elif 'btnParty' in request.form:
        arduino_send_cmd("d");
        currPal = "Party";
    elif 'btnFire' in request.form:
        arduino_send_cmd("f");
        currPal = "Fire";
    
    templateData = {
      'currAnim': currAnim,
      'currPal': currPal,
      'currLevel': currLevel,
      'currColor': currColor
    };

    return render_template('main.html', **templateData);


def get_btn_name(request):
    btn_name=""
    for key in request.form.keys():
        #print ("Python: " + "Button pressed:", key)
        btn_name = key
    return btn_name


def arduino_get_resp(s):
    time.sleep(.1);
    while (s.in_waiting > 0):
        print(s.readline().decode(), end="");

def arduino_send_cmd(s):
    arduino.flush();
    #s = s+'\n'
    arduino.write(s.encode());
    arduino_get_resp(arduino);
    time.sleep(.1);
    arduino.flush()

# try to detect the USB port where Arduino is connected
def arduino_get_port():
    #print("Listing ports")
    port = None
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p)
        if "Arduino" in p[1]:
            port = p[0]
            print("Arduino detected on port", port)

    #return port
    return "/dev/ttyACM0"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip



if __name__ == "__main__":

    port = None
    
    # use the USB port name if passed
    if len(sys.argv)>1:
        port = sys.argv[1]
        #print("Arduino port: " + port)

    # otherwise tries to detect the port
    # this seems to work only on Windows if Arduino USB driver is installed
    while(port==None):
        port = arduino_get_port()
        if port==None:
            print("Arduino not found. Retrying...")
            time.sleep(5);
    
    # open the serial interface
    arduino = serial.Serial(port, 9600, timeout=1)
    time.sleep(.5);
    
    #print("Port", arduino)
    #print("Current IP is", get_ip())
    #print("Point your browser to http://", get_ip(), sep="")
    print()
    print()
    print()
    print()
    
    print('                ---------------------------------------------------------------------------------------')
    print('                | ,gggggggggggggg ,ggg,          ,gg,ggg,      gg      ,gg ,ggggggg,  ,ggggggggggg,   |')
    print('                | dP""""""88""""""dP"""Y8,      ,dP,dP""Y8a     88     ,8P,dP""""""Y8bdP"""88""""""Y8,|')
    print('                | Yb,_    88      Yb,_  "8b,   d8"  Yb, `88     88     d8,d8,    a  Y8Yb,  88      `8b|')
    print('                |  `""    88       `""    Y8,,8P,    `"  88     88     88 88     "Y8P, `"  88      ,8P|')
    print('                |      ggg88gggg           Y88"          88     88     88 `8baaaa          88aaaad8P" |')
    print('                |         88   8          ,888b          88     88     88,d8P""""          88""""Y8ba |')
    print('                |         88             d8" "8b,        88     88     88d8"               88      `8b|')
    print('                |   gg,   88           ,8P,    Y8,       Y8    ,88,    8PY8,               88      ,8P|')
    print('                |    "Yb,,8P          d8"       "Yb,      Yb,,d8""8b,,dP `Yba,,_____,      88_____,d8,|')
    print('                |      "Y8P,        ,8P,          "Y8      "88"    "88"    `"Y8888888     88888888P"  |')
    print('                ---------------------------------------------------------------------------------------')
    print()
    print()
    print()
    print()
	
    #app.run(host='0.0.0.0', port=800, debug=True)
    #app.run(host='0.0.0.0', port=800)
    #app.run(host='192.168.0.10', port=800, debug=False)
    app.run(host='192.168.0.12', port=800, debug=False)
