import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# メールアカウント設定
email_address = ""                  # 送信元メールアドレス
email_password = ""                 # パスワード
smtp_server = "smtp.gmail.com"      # SMTPサーバーのアドレス
smtp_port = 587                     # SMTPサーバーのポート番号

# メールの内容設定
recipient_email = ""                # 送信先メールアドレス
subject = "title"                   # メールの件名
body = ""                           # メールの本文

# MIMEメッセージを作成
message = MIMEMultipart()
message["From"] = email_address
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# 画像ファイルを添付
file_path = "image.jpg"
with open(file_path, "rb") as attachment:
    img = MIMEImage(attachment.read(), _subtype="jpg")
    img.add_header("Content-Disposition", "attachment", filename="image.jpg")
    message.attach(img)

# SMTPサーバーに接続してメールを送信
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLSを使用して接続のセキュリティを確保
    server.login(email_address, email_password)
    server.sendmail(email_address, recipient_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()
