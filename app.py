import streamlit as st
from streamlit_option_menu import option_menu
#from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64
import include.db as db
import service_app.newpo as npo
import service_app.showpo as spo
import service_app.historypo as hpo
import time
import pathlib
import os.path 
import base64

def show_pdf(file_path):
    with open(file_path,"rb") as f:
          base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(layout="wide")

if "login" not in st.session_state:
    st.session_state["login"] = False
    st.session_state.userName = ""
    st.session_state.fullName = ""

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

if not st.session_state["login"]:
    
    with st.form("login_form"):
        imgCol1,imgCol2,imgCol3 = st.columns([1.5,1,2])
        my_logo = add_logo(logo_path="./img/logo.jpg", width=206, height=122)
        imgCol2.image(my_logo,use_column_width=False)
        st.header("PO Documents LogIn")

        userName = st.text_input("User Name").upper()
        passWord = st.text_input("Password ","",20,None,"password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if "login" in st.session_state:
                #แปลงค่ารหัสผ่านให้เป็น base64
                enPassword = passWord.encode('ascii')
                b64_bytes = base64.b64encode(enPassword)
                #แปลงจาก Byte to string
                #st.write(b64_bytes.decode("ascii"))
                #st.write(b64_bytes)
                #ตรวจสอบข้อมูลเจ้าหน้าที่
                sql = 'select  t0.emp_code,concat(t1.emp_fname," ",t1.emp_lname) user_name,t0.password_remark '
                sql += ' from tsc_datacenter.user_data t0,hr_system.employee t1 '
                sql += f' where t0.user_name="{userName}" and t0.password_remark="{b64_bytes.decode("ascii")}" '
                sql += ' and t0.active="Y" and t0.emp_code=t1.emp_code2 '
                #st.write(sql)
                rows = db.run_query(sql)
                if  rows:
                    st.session_state["login"] = True
                    st.session_state.userName = userName
                    for row in rows:
                        #st.write(f"{row[0]} has a :{row[1]}:")
                        st.session_state.fullName = row[1]
                    st.experimental_rerun()
                else:
                    st.info("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                    #enPassword = 'bWFoYWxv'  #passWord.encode('ascii')
                    #b64_bytes =    base64.b64decode('bWFoYWxv')
                    #st.write(b64_bytes)
                    #st.write(b64_bytes.decode("ascii"))

def side_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title = None,
            options = ["เอกสารรออนุมัติ","เอกสารใหม่","ประวัติเอกสาร", "Config", "Logout"],
            icons = ["list-task","file","book","gear","key"],
            menu_icon = "cast",
            default_index = 0,
            #orientation = "horizontal",
            #styles={
            #        "container": {"padding": "0!important", "background-color": "#0a0afa"},
            #        "icon": {"color": "orange", "font-size": "16px"}, 
            #        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            #        "nav-link-selected": {"background-color": "green"},
            #    }
        )
        if "login" in st.session_state:
            st.write('รหัสพนักงาน : ',st.session_state["userName"] )
            st.write('ชื่อพนักงาน  : ',st.session_state["fullName"] )

    if selected == "เอกสารใหม่":
        npo.newpo()
    if selected == "เอกสารรออนุมัติ":
        #show_pdf("data/PO6510-035/Test_1.pdf")
        spo.showpo()
    if selected == "ประวัติเอกสาร":
        hpo.showhistirypo()
    if selected == "Config":
        with st.form("Test"):
            #show_pdf("data/PO6510-035/Test_1.pdf")
            #st.write(os.listdir('//192.168.1.16/po-documents'))
            #os.mkdir("//192.168.1.16/po-documents/data/PO123")
            in_dir = st.text_input("Directory :",value="/app/poDocuments/data/PO123")
            #show_pdf("data/PO6510-035/Test_1.pdf")
            #os.mkdir("//192.168.1.16/po-documents/data/PO123")
            btn_dir = st.form_submit_button("OK",)                               
            if btn_dir:
                st.write(os.path.join(in_dir))
                os.mkdir(in_dir)
                #os.makedirs(in_dir)
                st.info("Create Done.")
        
    if selected == "Logout":
        with st.form("logout_form"):
            st.header("Logout")
            st.write("Confirme Logout")

            submitted = st.form_submit_button("Logout")
            if submitted:
                if "login" in st.session_state:
                    st.session_state["login"] = False
                    st.experimental_rerun()


if st.session_state["login"]:
    side_menu()

st.write(st.session_state["login"])

