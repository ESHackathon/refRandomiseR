

import streamlit as st
import pandas as pd
import rispy
import zipfile
import io
import tempfile
import os
# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )
#
# # Using "with" notation
if "splitby" not in st.session_state:
    st.session_state["splitby"] =""
if "nsplits" not in st.session_state:
    st.session_state["nsplits"] = 0
if "n_records" not in st.session_state:
    st.session_state["n_records"] = 0
if "splitvalues" not in st.session_state:
    st.session_state["splitvalues"] = []
if "reset" not in st.session_state:
    st.session_state["reset"] = False
if "outdfs" not in st.session_state:
    st.session_state.outdfs=[]
if "my_text" not in st.session_state:
    st.session_state["my_text"]="0"
if "outtext" not in st.session_state:
    st.session_state.outtext = []
if "mystate" not in st.session_state:
    st.session_state["mystate"] = 48


def clear_text():

    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""

def randomise_me(mytype='csv'):

    st.session_state["n_records"] = st.session_state.df.shape[0]



    st.markdown("## ✔️ Uploaded file with **:red[{}]** records".format(st.session_state["n_records"]))


    st.markdown('''##  Define Record Batches''')
    st.write("Please enter a number below, corresponding to the percentage of records you want in a batch. After hitting the 'Enter' key you can add a number for the next batch, until 100% of the data are allocated.")
    st.text_input(
        "Percentage of records in each batch", placeholder="Type a number and press Enter to submit", key='widget', on_change=clear_text
    )


    number = st.session_state['my_text']

    if not number.isdigit():
        number=number.replace("%", "").strip()
    try:
        number = int(number)
    except:
        st.write("_:red[Please enter a single digit]_")

    if type(number)== int and number > 0 and not number + sum(st.session_state.splitvalues) > 100:

        st.session_state.splitvalues.append(number)
        st.session_state.outtext.append("   Added a batch of **:red[{}%]**, approximately **:red[{}]** records".format(number, int((number / 100) * st.session_state["n_records"])))




    #st.write(st.session_state.splitvalues)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Click **:red[here]** to reset inputs", type='tertiary'):
            st.session_state.splitvalues = []
            st.session_state.outdfs = []
            st.session_state.outtext = []
            st.session_state.number_input = 0.0

    for o in st.session_state.outtext:
        st.markdown(o)
    if sum(st.session_state.splitvalues)<100:
        st.markdown("## **:red[{}%]** of dataset allocated so far; **:green[{}%]** left".format(sum(st.session_state.splitvalues), 100-sum(st.session_state.splitvalues)))
    else:
        st.markdown("## **:green[100% allocated!]** Please click 'Submit' above to create batches.")




    if sum(st.session_state.splitvalues) == 100:
        with col2:
            if st.button("✔️ Submit", type='primary'):
                #print("submitted")

                for i, va in enumerate(st.session_state.splitvalues):

                    if (i + 1) < len(st.session_state.splitvalues):

                        thisn = int((va / 100) * st.session_state["n_records"])

                        mypart = st.session_state.df.sample(n=thisn, random_state=st.session_state.mystate)

                        st.session_state.outdfs.append(mypart)
                        st.session_state.df.drop(mypart.index, inplace=True)
                        # st.write(st.session_state.df.shape[0])
                    else:
                        st.session_state.outdfs.append(st.session_state.df)
                        # st.write(st.session_state.df.shape[0])
                # [st.write(d.shape) for d in st.session_state.outdfs]

                buf = io.BytesIO()

                with zipfile.ZipFile(buf, "x") as csv_zip:
                    for i, tempdf in enumerate(st.session_state.outdfs):
                        if mytype=='csv':
                            csv_zip.writestr("batch_{}_{}.csv".format(i, tempdf.shape[0]), pd.DataFrame(tempdf).to_csv())
                        else:
                            csv_zip.writestr("batch_{}_{}.ris".format(i, tempdf.shape[0]), rispy.dumps(list(tempdf["refs"])))
                            csv_zip.writestr("batch_{}_{}.csv".format(i, tempdf.shape[0]), pd.DataFrame(list(tempdf["refs"])).to_csv())

                with col3:
                    st.download_button(
                        label="Download zip",
                        data=buf.getvalue(),
                        file_name="RefRandomiser.zip",
                        mime="application/zip",
                        icon=":material/download:",
                        type='primary'
                    )


# with st.sidebar:
# #     # if st.session_state["splitby"] =="":
# #     #
# #     #     st.radio(
# #     #
# #     #         "How do you want to split records?",
# #     #
# #     #         ("Percentage", "Absolute numbers"), key="splitby")
# #
#     st.session_state["mystate"]=st.number_input("Enter random seed", value=48, max_value=1000, min_value=1, step=1)

st.markdown(
    '''# 🎲 :rainbow[RefRandomiser]: A tool to split and randomise search results''')


st.markdown("""
An explanation of why randomisation and independent dataset splits are important can be found [here](Rationale) and our tool information sheet to cite [here](About) if you find this tool helpful. 
""", unsafe_allow_html=True)


st.write("A tutorial video that shows how to use this app can be found on the bottom of this page.")

st.markdown('''##  File Upload''')
uploaded_file = st.file_uploader("Upload RIS or CSV file")



if uploaded_file is not None:
    #try:
        if "csv" in uploaded_file.name.lower():
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.df = st.session_state.df.sample(frac=1.0, random_state=st.session_state.mystate)
            randomise_me(mytype='csv')


        elif "ris" in uploaded_file.name.lower():





            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)

            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            with open(path, 'r', encoding='utf-8') as bibliography_file:
                entries = rispy.load(bibliography_file)
            #print(entries)

            st.session_state.df = pd.DataFrame()
            st.session_state.df["refs"] = entries
            st.session_state.df = st.session_state.df.sample(frac=1.0, random_state=st.session_state.mystate)

            randomise_me(mytype='ris')


        else:
            st.write("Please upload a RIS or CSV file. Encoding errors may appear on files that are not utf-8 encoded")

    # except:
    #     pass
        #st.write("An unknown error occurred. This may be due to file encoding, please try to supply an utf-8 encoded CSV or RIS file.")