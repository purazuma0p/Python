#!usr/bin/env python3
import smtplib
import os

#メール送信スクリプト
os.system('clear')
art = """
       
 #####   ##   ##  ######## ######             #####   #######  ###  ##  ######
##   ##  #######  ## ## ##  ##  ##           ##   ##   ##  ##   ### ##   ## ###
##       ## # ##     ##     ##  ##           ##        ##       ######   ##  ##
 #####   ##   ##     ##     #####    ######   #####    ####     ## ###   ##  ##
     ##  ##   ##     ##     ##                    ##   ##       ##  ##   ##  ##
##   ##  ##   ##     ##     ##               ##   ##   ##  ##   ##  ##   ## ###
 #####   ##   ##    ####   ####               #####   #######  ###  ##  ######


      
"""
print(art)


server = smtplib.SMTP('smtp.gmail.com', 587) # SMTPサーバーのアドレスとポート番号
server.starttls() # TLS暗号化を開始
server.login("your_email@gmail.com", "your_password") # ログイン情報


in_mail = input("[+]user.from>")
out_mail = input("[+]user.to_user>")
mail = input("[+]user>")
server.sendmail(in_mail,out_mail, mail)

server.quit()

