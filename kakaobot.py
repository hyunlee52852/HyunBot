# coding = utf-8
 
from flask import Flask, render_template, jsonify, request
import sys
import CreateImage


app = Flask(__name__)

@app.route('/Reload_Schedule', methods=['POST'])
def reload():
    CreateImage.makeimage()

    dataSend =  {
            "version": "2.0",
            "template": {
                "outputs": [
                    
                    {
                        "simpleText": {
                            "text" : "아래 이미지로 재설정 완료했습니다!"
                            }
                           
                        }
                    ,
                    {
                        "simpleImage": {
                            "imageUrl": "http://34.83.145.171:9900/static/output.png",
                            "altText": "에러"
                        }
                    }
                ]
            }
        }
        
    return jsonify(dataSend)


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
                            "imageUrl": "http://34.83.145.171:9900/static/output.png",
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


