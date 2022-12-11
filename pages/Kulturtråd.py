import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
from PIL import Image

def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Ladda ner Excel-fil</a>'
    return st.markdown(href, unsafe_allow_html=True)

st.set_page_config(
    page_title = "Kulturtråden",
    page_icon="🧵",
    layout = 'wide',
)

st.title('Kulturtråden Statistik 📈')
st.markdown('---')
c1, c2 = st.columns((1,1))

with c1:
    st.subheader("Excel-fil utseende")
    st.write(
    'Web-App för att sammanställa statistik åt Kulturtråden. ' \
    'Första Excel-filen som ska matas in ska vara lik följande bild, ' \
    'extra viktigt är att kolumn-namnen är samma som i bilden.')
with c2:
    lista_exempel_bild = Image.open(r'Lista_exempel.png')
    st.image(lista_exempel_bild, caption = 'Hur Excel-filen med skol- och programlista ska vara strukturerad.')


lista_file = st.file_uploader('Välj först Excel-filen med skol- och programlista:', type='xlsx', accept_multiple_files=False)

if lista_file:
    st.markdown('---')

    excel_lista = pd.read_excel(lista_file, engine='openpyxl')

    skolor = excel_lista['Skola'].tolist()
    antal_klasser = excel_lista['Antal Klasser'].tolist()
    program = excel_lista['Program'].dropna().tolist()
    antal_tillg = excel_lista['Antal tillgängligt'].dropna().tolist()

    bokning_file = st.file_uploader('Välj nu Excel-filen med alla bokningar från StudyAlong:', type='xlsx', accept_multiple_files=False)

    if bokning_file:
        st.markdown('---')
        excel_bokningar = pd.read_excel(bokning_file, engine='openpyxl')

        ## Obs jag gör dropna här, om något går fel kolla här
        skol_bokningar = [x.lower().replace(' ', '') for x in excel_bokningar['Skola'].dropna().tolist()]
        program_bokningar = [x.lower().replace(' ', '') for x in excel_bokningar['ProgramNamn'].dropna().tolist()]

        skol_dict = {skolor[i]: (x := int(skol_bokningar.count(skolor[i].lower().replace(' ', ''))), y := int(antal_klasser[i]), x/y) for i in range(len(skolor))}
        program_dict = {program[i]: (x := int(program_bokningar.count(program[i].lower().replace(' ', ''))), y := int(antal_tillg[i]), x/y) for i in range(len(program))}

        skol_sorted = sorted(skol_dict, key = lambda k : skol_dict[k][2])
        skol_procent = [skol_dict.get(x)[2] for x in skol_sorted]
        program_sorted = sorted(program_dict, key = lambda k : program_dict[k][2])
        program_procent = [program_dict.get(x)[2] for x in program_sorted]

        df_skolor = pd.DataFrame(skol_dict).T.rename_axis('Skola').reset_index()
        df_skolor.columns = ['Skola', 'Antal bokningar', 'Antal klasser', 'Andel bokningar']
        df_skolor_for_plot = df_skolor.sort_values('Andel bokningar') # sorterar för att göra figuren lättare att läsa

        df_program = pd.DataFrame(program_dict).T.rename_axis('Program').reset_index()
        df_program.columns = ['Program','Antal bokningar', 'Antal tillgängliga bokningar', 'Andel bokningar']

        st.subheader('Ändra graferna till fullskärm innan ni sparar bilderna för att få med hela figuren. (Tryck på fullskärms-symbolen som är upp till höger om figuren)')

        c3, c4 = st.columns((1,1))
        with c3:
            st.dataframe(df_skolor)
            generate_excel_download_link(df_skolor)
        with c4:
            st.dataframe(df_program)
            generate_excel_download_link(df_program)
            
        df_skolor = df_skolor.sort_values('Andel bokningar') # sorterar för att göra figuren lättare att läsa
        st.markdown('---')
        
        fig_skolor = px.bar(df_skolor_for_plot, x = 'Skola', y= 'Andel bokningar', template = 'plotly_white', title = '<b> Andel bokningar (%) för varje skola </b>')
        fig_program = px.bar(df_program, x = 'Program', y = 'Andel bokningar', template = 'plotly_white', title = '<b> Andel bokningar (%) för varje program </b>')

        with c3:
            st.plotly_chart(fig_skolor, use_container_width=True)
        with c4:
            st.plotly_chart(fig_program, use_container_width=True)


