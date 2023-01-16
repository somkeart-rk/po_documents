import time
import numpy as np
import pandas as pd
import streamlit as st
import service_app.newpo as npo
import include.db as db
import include.export_tools as exp
import pathlib
import os.path 
import base64

@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def color_priority(val):
    color = 'red' if val == '3-HIGH' else 'black'
    return 'color:{}'.format(color)   

def showpo():
    st.header("เอกสารรออนุมัติ")
    loginName= st.session_state["userName"]
    # # Show user table 
    st.markdown(
        """ <style> 
            .font {font-size:16px;} 
            .standart-text {font-size:14px; }
            </style> 
        """, unsafe_allow_html=True)

    colms = st.columns((0.5, 1, 1, 2),gap="small")
    fields = [f"**№**", f'**PO Number**', f'**Department**', f'**Description**']
    for col, field_name in zip(colms, fields):    # header
        col.write(field_name)

    sql = "select t0.po_id,t0.po_number,t0.department_name department,trim(t0.po_desc) description,t1.file_name,t1.file_location url,t0.read_state status "
    sql += f" from po_documents.tbl_po_data t0, po_documents.tbl_po_file t1 where t0.read_state='OPEN' and t0.po_number = t1.po_number "
    sql += " order by t0.priority desc,t0.create_time asc ;"
    rows = db.run_query(sql)
    df=pd.DataFrame(rows,columns=["№","po_number","department","description","file_name","url","status"])

    def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"><a target="_blank"> </a>'
        pdf_display = f'<iframe  src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.session_state["old_po_number"] = ""
    cnt_row = 1
    for x, po_no in enumerate(df['po_number']):
        col1, col2, col3, col4 = st.columns((0.5, 1, 1, 2),gap="small")
        if st.session_state["old_po_number"] != df['po_number'][x]:
            #st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
            col1.markdown(f"**{cnt_row}** ")  
            col2.markdown(f"**{df['po_number'][x]}**")  
            col3.write(f"**{df['department'][x]}**")  
            col4.write(f"**{df['description'][x]}**")  
            st.session_state["old_po_number"] = df['po_number'][x]
            cnt_row += 1
        with st.expander(df['file_name'][x]):
            show_pdf(df['url'][x])
        #pdf_view = col6.button("View", key=df['url'][x],on_click=show_pdf,args=[df['url'][x]])
    
