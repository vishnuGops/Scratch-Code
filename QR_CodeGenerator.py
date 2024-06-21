import qrcode

qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=2,
)

qr.add_data('www.vishnugops.com')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("Output/QRCodes/websiteQRCode1.png")
