try:
    import usocket as socket    # socket module allow us to send response over network.
except:
    import socket
from utime import sleep_ms, sleep
import network 
from machine import Pin
import gc 

try:
    from bps_cre import *     
except:
    pass

gc.collect()

# led=Pin("LED",Pin.OUT) # for Raspberry Pi Pico
led = Pin(2, Pin.OUT)   # for esp boards
ssid = bps_ssid     # your network/hotspot/ssid name.
passw = bps_passw    # your network/hotspot/ssid password.

# Connect to the network
sta = network.WLAN(network.STA_IF) # station interface.
sta.active(True)
sta.connect(ssid, passw)  # connecting to network

while not sta.isconnected():
    pass

if sta.isconnected():
    print("Connection status:", sta.isconnected())
    
sta.ifconfig(('192.168.1.23', '255.255.255.0', '192.168.1.1', '218.248.112.65'))
print(sta.ifconfig())
print("http://192.168.1.23")

def web_page():
    html = """<!DOCTYPE html>
            <html>
            <head>
                <title>LED Control</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { background-color: darkslategray; }
                    h1 { color: rgb(137, 185, 226); }
                    button { 
                        display: inline-block;
                        padding: 10px 2px;
                        font-size: 20px;
                        margin: 10px;
                        cursor: pointer;
                        background-color: lightgrey;
                        width: 90px;
                        height: 80px;
                    }
                </style>
                <script>
                    function sendRequest(command) {
                        var xhr = new XMLHttpRequest();
                        xhr.open("GET", "/?led=" + command, true);
                        xhr.send();
                    }
                </script>
            </head>
            <body>
                <h1>LED Control</h1>
                <button 
                    onmousedown="sendRequest('on')" 
                    onmouseup="sendRequest('off')" 
                    ontouchstart="sendRequest('on')" 
                    ontouchend="sendRequest('off')">
                    <b>led_2</b>
                </button> 
            </body>
            </html>
            """
    return html

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind(("", 80))
so.listen(5)

while True:
    try:
        conn, addr = so.accept()
        conn.settimeout(3.0)
        print("Connection made %s" % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print("Content = %s" % request)
        led_on = request.find("/?led=on")
        led_off = request.find("/?led=off")
        print("\nled_on =", led_on)
        print("\nled_off =", led_off)
        if led_on == 6:
            print("\nLED ON\n")
            led.on()
        if led_off == 6:
            print("\nLED OFF\n")
            led.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
