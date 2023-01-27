import streamlit as st
import pymysql as connection
import pandas as pd

def init_connection():
    return connection.connect(**st.secrets["mysql"])

#conn = init_connection()

#Select data from database
def run_query(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    finally:
        conn.close()

#Save data to database
def run_saveData(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            #st.info("Save data")
    finally:
        conn.close()

def check_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.check_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()

def update_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.update_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    finally:
        conn.close()

#load machine type data list for selectBox
def load_department(no_all):
    #no_all = Y Show,N = Unshow
    sql = "select distinct t0.department_name from po_documents.tbl_department t0 "
    if no_all == "Y":
        sql += " where t0.department_id > 1 "
    sql += " order by t0.department_id "
    rows = run_query(sql)
    return pd.DataFrame(rows)

#load service group data list for selectbox
def loadServiceGroup(service_No):
    sql = "select distinct t0.service_group from sms_db.tbl_service_group t0, sms_db.tbl_service_list t1 "
    sql += f" where t1.service_no='{service_No}' and t0.machine_type=t1.machine_type order by t0.service_group_id "
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["service_group"])

#load po file data list for table grid
def load_po_file():
    sql = "select distinct t0.po_number,t0.file_location,t0.file_name from po_documents.tbl_po_file t0 "
    sql += " order by t0.file_id "
    rows = run_query(sql)
    return pd.DataFrame(rows)

#load po file data list for sent mail
def get_po_file_name(po_number):
    sql = "select distinct t0.file_id, t0.po_number, t0.file_location from po_documents.tbl_po_file t0 "
    sql += f" where t0.po_number = '{po_number}' "
    sql += " order by t0.file_id "
    rows = run_query(sql)
    #st.write(rows)
    return rows

#load email data for sent mail tag FROM
def get_email_from(user_id):
    sql = "select distinct t0.email, t0.email_password from po_documents.tbl_po_email t0 "
    sql += f" where t0.email_type = 'FROM' and t0.active = 'Y' and t0.user_id = '{user_id}' "
    rows = run_query(sql)
    #st.write(rows)
    return rows

#load email data for sent mail tag TO
def get_email_to():
    sql = "select distinct group_concat(t0.email) email from po_documents.tbl_po_email t0 "
    sql += f" where t0.email_type = 'TO' and t0.active = 'Y'  "
    sql += " order by t0.email_id "
    rows = run_query(sql)
    #st.write(rows)
    return rows

