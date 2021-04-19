# coding = utf-8

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, jsonify, request
import sys

app = Flask(__name__)

@app.route('/Check_Schedule', methods=['POST'])
def schedule():

    dataSend =  {
            "version": "2.0",
            "template": {
                "outputs": [
                    
                    {
                        "simpleText": {
                            "text" : "내일 일정입니다!"
                            }
                           
                        }
                    ,
                    {
                        "simpleImage": {
                            "imageUrl": "http://104.198.0.192:9900/static/output.png",
                            "altText": "에러"
                        }
                    }
                ]
            }
        }
    
    return jsonify(dataSend)

@app.route('/')
def home():
    return render_template('img.html')
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9900,debug=True)
