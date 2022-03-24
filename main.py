from flask import Flask, render_template, Response, request,redirect,url_for
from necklace_camera import NecklaceVideoCamera
from tshirt_camera import TshirtVideoCamera
from makeup_camera import MakeupVideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def makeup_gen(camera):
    while True:
        frame = camera.get_frame(110,20,20)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    x = input('Enter video type: ')
    if x == 'tshirt':
        return Response(gen(TshirtVideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    if x == 'necklace':
        return Response(gen(NecklaceVideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    if x == 'makeup':
        return Response(makeup_gen(MakeupVideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080, debug=True)
