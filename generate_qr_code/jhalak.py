import qrcode

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

if __name__ == "__main__":
    name = "JHALAK"
    phone_number = "7868445321"
    data = f"{name} - {phone_number}"  # Concatenate name and phone number
    filename = "JHALAK_QRCode.png"
    generate_qr_code(data, filename)
    print(f"QR code with name '{name}' and phone number '{phone_number}' generated successfully and saved as '{filename}'")
