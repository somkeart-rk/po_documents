import streamlit as st
import pandas as pd
import include.db as db
import include.sendmail as sent_mail
import time
import pathlib
import os.path 
import base64
import smtplib, ssl


def newpo():
    with st.form("new_form"):
        st.header("เอกสารใหม่")
        col1,col2,col3 = st.columns(3)
        Department = col1.selectbox("หน่วยงาน",db.load_department("Y"))
        PoNo = col2.text_input("เลขที่ PO")
        priority = col3.selectbox("ความเร่งด่วนของงาน",["1-LOW","2-MEDIUM","3-HIGH"])
        PoDescription = st.text_area("รายละเอียดการสั่งซื้อ",max_chars=1000)
    
        uploaded_files = st.file_uploader("เลือกไฟล์ PDF ที่่ต้องการอัพโหลด",type=["pdf"],accept_multiple_files=True)
        st.info("ตรวจสอบข้อมูลให้ถูกต้องก่อนกดบันทึกเอกสาร")
        submitted = st.form_submit_button("บันทึกเอกสาร")
        if submitted:
            loginName= st.session_state["userName"]
            # check upload file
            file_count = 0
            if uploaded_files is None or len(PoNo) == 0 :
                st.warning('ต้องอัพโหลไฟล์ก่อน หรือเลขที่ PO ไม่ระบุ')
            else:
                PoNo = PoNo.upper().replace("/","-")
                #parent_path = pathlib.Path(__file__).parent.parent.resolve()
                #Upload on server
                parent_path = (r"/opt/poDocuments")
                #Upload on local
                #parent_path = (r"D:\Temp")
                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)
                data_path = os.path.join(parent_path, "data")
                new_folder = os.path.join(data_path,PoNo)  
                #st.write(new_folder)
                os.makedirs(new_folder)         
                #st.write(os.listdir("/opt/poDocuments"))
                save_path = os.path.join(new_folder)
                for uploaded_file in uploaded_files:
                    complete_name = os.path.join(save_path, uploaded_file.name)
                    destination_file = open(complete_name,"wb")
                    destination_file.write(uploaded_file.getbuffer())
                    destination_file.close()
                    file_count += 1
                    file_path = complete_name.replace("\\","\\\\")
                    sql = "INSERT INTO `po_documents`.`tbl_po_file`(`po_number`,`file_location`,`file_name`,`user_create`) "
                    sql += f" VALUES('{PoNo}','{file_path}','{uploaded_file.name}','{loginName}' ); "
                    #st.write(sql)
                    db.run_saveData(sql)

                sql = "INSERT INTO `po_documents`.`tbl_po_data`(`po_number`,`department_name`,`po_desc`,"
                sql += "`priority`,`file_count`,`user_create`) "
                sql += f" VALUES('{PoNo}','{Department}','{PoDescription}','{priority[0]}','{file_count}','{loginName}' ); "
                #st.write(sql)
                db.run_saveData(sql)

                #save data into database
                #st.info(f"Job No# : {jobRunning} has been created.")
                
                sent_mail.sentEmailWithAtth(PoNo,Department ,PoDescription )
                
                st.success("อัพโหลดและส่งเมล์เสร็จเรียบร้อย")

def Closejob(po_No):
    CloseJob_form = st.container() #st.form(key="Close Job")
    if 'pChange' not in st.session_state:
        st.session_state['pChange'] = ''
        st.session_state['sDetail'] = ''

    def make_clickable(val):
        # target _blank to open new window
        return '<a target="_blank" href="{}">🔗</a>'.format(val)
    def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"><a target="_blank"> </a>'
        pdf_display = f'<iframe  src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    CloseJob_form.subheader("เอกสารประกอบการตัดสินใจ")

    sql = "select distinct t0.file_name,t0.file_location url from po_documents.tbl_po_file t0 "
    sql += f" where t0.po_number='{po_No}' order by t0.file_id "
    rows = db.run_query(sql)
    df=pd.DataFrame(rows,columns=["file_name","url"])
    #df = df.style.format({'url': make_clickable})
    col1, col2 = CloseJob_form.columns((1, 1),gap="small")
    for y, file_name in enumerate(df['url']):
        col1.write(df['file_name'][y])
        pdf_view = col2.button("View", key=file_name,on_click=show_pdf,args=[df['url'][y]])
        #if pdf_view:
        #    show_pdf("data/PO6510-035/Test_1.pdf")

    #CloseJob_form.write(df.to_html(escape = False), unsafe_allow_html = True)
    #CloseJob_form.write(df)

    CloseJob_form.button("ตรวจสอบแล้ว",on_click=saveData,args=[po_No,])


def saveData(po_no,):
    partChange = st.session_state.pChange
    serviceDetail = st.session_state.sDetail
    sqlUpdate = f"UPDATE `sms_db`.`tbl_service_list` SET `status`= 'CLOSE' WHERE `service_no`='{po_no}'; "
    #st.write(sqlUpdate)
    #db.run_saveData(sqlUpdate)

    sqlAddDetail = "INSERT INTO `sms_db`.`tbl_service_detail`(`service_no`,`service_group`,`part_detail`,`service_detail`) "
    sqlAddDetail += f" VALUES('{po_no}','{po_no}','{partChange}','{serviceDetail}'); "
    #st.write(sqlAddDetail)
    #db.run_saveData(sqlAddDetail)
    #st.info(f"งานหมายเลข : {po_no} ปิดเรียบร้อย")
    #time.sleep(0.5)
 
