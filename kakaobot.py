# coding = utf-8
 
from flask import Flask, render_template, jsonify, request
import sys
 
app = Flask(__name__)

@app.route('/Check_Schedule', methods=['POST'])
def schedule():
    
    dataSend = 
                {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleImage": {
                            "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                            "altText": "보물상자입니다"
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


