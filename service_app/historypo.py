from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np 
import pymysql as connection
import include.db as db
import include.export_tools as exp


# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data(startDate,finishDate,department,po_no):
    sql = "select t0.po_number,t0.department_name,t0.po_desc,t0.create_time "
    sql += " from po_documents.tbl_po_data t0 "
    sql += " where t0.read_state >= 0 "
    if department != 'ทั้งหมด':
        sql += f" and t0.department_name='{department}' "
    if po_no:
        sql += f" and t0.po_number='{po_no}' "
    sql += f" and (date_format(t0.create_time,'%Y-%m-%d') between date'{startDate}' and '{finishDate}' ) "
    sql += " order by t0.create_time desc; "
    #st.write(sql)
    rows = db.run_query(sql)
    return pd.DataFrame(rows,columns=["PO Number","Department","Description","Create Date"])
    
def showhistirypo():
    with st.container():
        st.header("ประวัติเอกสาร")

        col1, col2,col3,col4,col5 = st.columns([1,1,1,1,1])

        st_d = col1.date_input("วันที่เริ่ม")
        fn_d = col2.date_input("วันสุดท้าย")
        department = col3.selectbox("หน่วยงาน",db.load_department("N"))
        po_no = col4.text_input("เลขที่ PO")

        if col5.button("ค้นหา"):
            #st.write(st_d," ",fn_d)
            df = load_data(st_d,fn_d,department,po_no)
            st.dataframe(df, use_container_width=True)
            st.download_button(label="download as Excel-file",
                data=exp.convert_to_excel(df),
                file_name="export_history.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="excel_download",
            )

        else:
            st.write('Not Select')




    

    
