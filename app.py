from distutils.log import debug
from flask import Flask, redirect, render_template, request
from predict_module import prediksi

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def predict():
  if request.method == "GET":
    print("GET NIH")
    return render_template('predict.html')
  elif request.method == "POST":
    img = request.files['file']
    img.save("static/upload.jpg")
    prediksi("static/upload.jpg")

    return render_template('predict.html', tampilhasil=True)



if __name__ == "__main__":
  app.run(debug=True)