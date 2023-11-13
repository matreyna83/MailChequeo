import email
import imaplib
import pprint
import datetime
import mailbox
import re
import datetime
import mysql.connector

###PARTE 1###
###CONNECTION DB###

cnx = mysql.connector.connect(user='sql10661695',
                              password='A9r1EKyhxY',
                              host='sql10.freemysqlhosting.net',
                              database='sql10661695')
cursor = cnx.cursor()
if cnx and cnx.is_connected():
    with cnx.cursor() as cursor:
        result_sql = cursor.execute("SELECT * FROM mails")
        rows = cursor.fetchall()
        print("Total mails in table: ", cursor.rowcount)
        print("\nMails En DB")
        for rows in rows:
            print("MailId = ", rows[0], )
            print("Fecha = ", rows[1])
            print("From = ", rows[2])
            print("Subject  = ", rows[3], "\n")
else:
    print("Could not connect")



###PARTE 2###
###CHECK MAILS###

print ("\n")
print('Connect with IMAP')
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')

print('Login details')
username = "melichallenge2@gmail.com"
print ("Username: " + username)
password = "zird hzyq dyeh uvom"

print('Login to mail')
imap_server.login(username, password)
print ("Server Response:")
print(imap_server.welcome)

# Selecting the inbox of the logged in account
imap_server.select('Inbox')

# search
result, data = imap_server.uid('Search', None, "TEXT Incident")
i = len(data[0].split())


print ("\n")
print ("Cantidad de Mails: " + str(i))

for x in range(i):
    latest_email_uid = data[0].split()[x]

    result = re.search('b\'(.*)\'', str(latest_email_uid))
    # print(result.group(1))
    uid_number = result.group(1)
    print ("Message UID: " + str(uid_number))
    result, email_data = imap_server.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen')
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    print ("Fecha de recepcion: " + str(local_date))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    print ("From: " + email_from)
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
    print ("Subject: " + subject)

    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            result_sql = cursor.execute("SELECT * FROM mails WHERE mailUID = %s", (uid_number,))
             # gets the number of rows affected by the command executed
            rows = cursor.fetchall()
            ##print ("number of affected rows: {}".format(row_count))
            if len(rows) == 0:
                print("No existe mail en DB")
                result_sql = cursor.execute("INSERT INTO mails (mailUID, fecha_recepcion, mailFrom, subject) VALUES (%s, %s, %s, %s)", (uid_number,str(local_date), email_from, subject,))
                cnx.commit()
                print(cursor.rowcount, "record inserted.")
            else:
                print("Existe mail en DB")


###PARTE 3###
###RESULT DB###
print ("DB despues de ejecucion")
if cnx and cnx.is_connected():
    with cnx.cursor() as cursor:
        result = cursor.execute("SELECT * FROM mails")
        rows = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        print("\nMails En DB")
        for rows in rows:
            print("MailId = ", rows[0], )
            print("Fecha = ", rows[1])
            print("From = ", rows[2])
            print("Subject  = ", rows[3], "\n")
else:
    print("Could not connect")

cnx.close()