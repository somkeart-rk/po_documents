# Import modules
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
### Add new subclass for adding attachments
from email.mime.application import MIMEApplication
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd
import include.db as db
import streamlit as st

def sendEmail(mailType ):
    # Define the HTML document
    html = '''
        <html>
            <body>
                <h1>Daily S&P 500 prices report</h1>
                <p>Hello, welcome to your report!</p>
                <a href="https://www.google.com">Login to read attachment file</a>

            </body>
        </html>
        '''

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'somkeart@gmail.com'
    password = 'lpwuvtybjfshgzck'
    email_to = 'somkeart@thaisock.com'

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Purchase request email - {date_str}'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)



def sentEmailWithAtth(po_number,department,mail_details):
    # Define the HTML document
    # Add an image element
    ##############################################################
    html = f'''
        <html>
            <body>
                <p>เรียน คุณอลิศรา </p>
                <p>    {department} มีการขอซื้อสินค้าและฝ่ายจัดซื้อได้มีการขอราคาจากผู้ขาย จึงได้ส่งเอกสารให้พิจารณาเพื่ออนุมัติและดำเนินการต่อ <p>
                <p>หมายเหตุ {mail_details} </p>
                <img src='cid:myimageid' width="700">
            </body>
        </html>
        '''
    ##############################################################

    # Define a function to attach files as MIMEApplication to the email
        ## Add another input extra_headers default to None
    ##############################################################
    def attach_file_to_email(email_message, filename, extra_headers=None):
        # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())
        # Add header/name to the attachments    
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Set up the input extra_headers for img
        ## Default is None: since for regular file attachments, it's not needed
        ## When given a value: the following code will run
            ### Used to set the cid for image
        if extra_headers is not None:
            for name, value in extra_headers.items():
                file_attachment.add_header(name, value)
        # Attach the file to the message
        email_message.attach(file_attachment)
    ##############################################################    

    # Set up the email addresses and password. Please replace below with your email address and password
    #gmail
    #email_from = 'somkeart@gmail.com'
    #password = 'lpwuvtybjfshgzck'
    #zoho mail
    email_from = 'somkeart@thaisock.com'
    password = 'gk5Wb3PjTFh4'
    if st.session_state["userName"] == 'OST14011':
        email_from = 'somkeart@thaisock.com'
        password = 'gk5Wb3PjTFh4'

    if st.session_state["userName"] == 'OST21005':
        email_from = 'somkeart@thaisock.com'
        password = 'gk5Wb3PjTFh4'

    email_to = ['somkeart@thaisock.com','purchase_manager@thaisock.com']

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = f" {','.join(email_to)} "  # email_to
    email_message['Subject'] = f'เอกสารเสนออนุมัติหมายเลข {po_number} แผนก {department} วันที่ {date_str}'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

    # Attach more (documents)
    ## Apply function with extra_header on chart.png. This will render chart.png in the html content
    ##############################################################
    #attach_file_to_email(email_message, 'chart.png', {'Content-ID': '<myimageid>'})
    ##############################################################
    #attach_file_to_email(email_message, 'excel_report.xlsx')
    #attach_file_to_email(email_message, 'fpdf_pdf_report.pdf')

    #load data from database by po number
    #st.write(po_number)
    rows = db.get_po_file_name(po_number)
    df=pd.DataFrame(rows,columns=['file_id','po_number','file_location'])
    #st.write(df)
    for x, file_name in enumerate(df['po_number']):
        #st.write(df['file_location'][x])
        attach_file_to_email(email_message, df['file_location'][x])

    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    #with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    with smtplib.SMTP_SSL("smtppro.zoho.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string) 








