import qrcode

img = qrcode.make("http://127.0.0.1:5000")
img.save("qr.png", "PNG")