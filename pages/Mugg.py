import streamlit as st
from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageFont
import math

st.set_page_config(
    page_title = "Mugg",
    page_icon="☕",
    layout = 'wide',
)

st.title('Cirkulära tryck på cylinder-formade muggar ☕')

mugg_diameter_bild = Image.open(r'mugg-diameter.png')
c1, c2 = st.columns((2,1))

with c1:
    st.write(
        'Hur en logga ska placeras på en cylinder-formad mugg för att undvika vertikal utsträckning. ' \
        'För att beräkna detta behövs diametern på muggen samt den horisontella längden på loggan.')

with c2:
    st.image(mugg_diameter_bild, width = 200)

st.markdown('---')

c3, c4, c5 = st.columns((1,1,1))

mugg_latex = Image.open(r'mugg-latex.png')

with c3:
    D = st.number_input('Fyll i diametern på muggen (mm):', min_value = 0.01)
    L = st.number_input('Fyll i längden i horisontell led på loggan (mm)', min_value = 0.00, max_value = D)
    x = D*math.asin(L/D)
    st.write(f'Längden i horisontell led på den utsträckta loggan bör sättas till {round(x,5)} mm')

    ## hade varit coolt men orkar inte fixa
    #myFont = ImageFont.truetype("arial.ttf", 20)
    #logga_vanlig.text((60,210), f'Diameter innan utsträckning = {L} mm', font = myFont,  fill = (0,0,0))
    #st.image(logga, width = 250)
    
with c4:
    st.subheader('Härledning: ')
    st.latex(r'''
    \text{Med symbolerna:} ''')
    st.latex(r'''
    \begin{equation*} D = \text{Diametern på muggen} \end{equation*} 
    \\
    \begin{equation*}
      L = \text{Längden på originella loggan}
    \end{equation*} 
    \\
    \begin{equation*}
      x = \text{Hur lång den utsträckta loggan ska vara}
    \end{equation*} 
    ''')
    st.latex(r'''
    \text{Geometrin ger oss att:} ''')
    st.latex(r'''
    \begin{equation*}
      \frac{D}{2}\theta = x \iff \theta = \frac{2x}{D}
    \end{equation*} \\ ''')
    st.latex(r'''
    \text{och} ''')
    st.latex(r'''
    \begin{equation*}
    \sin(\frac{\theta}{2}) = \frac{L/2}{D/2} \iff \\
    \sin(\frac{x}{D}) = \frac{L}{D}
    \end{equation*} ''')
    st.latex(r'''
    \text{Längden som den utsträckta loggan ska ha är därför:} ''')
    st.latex(r'''
    \begin{equation*} 
        \boxed{x = D\arcsin(\frac{L}{D})}
    \end{equation*} 
    ''')

with c5:
    st.image(mugg_latex)