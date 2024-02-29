import streamlit as st
import pandas as pd  # For handling dates
from fpdf import FPDF  # For generating PDF files

from fpdf import FPDF  # Ensure you have fpdf2 installed

from fpdf import FPDF

from datetime import date

class PDF(FPDF):
    def header(self):
        # Make sure to add the font before setting it
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 12)
        self.cell(0, 10, 'Bezwaarbrief', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        # Reuse the added font for consistency
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(name, adres, kenteken, boetebedrag, datum_boete, omschrijving, extra_argumenten, boetenummer):
    pdf = PDF()
    pdf.add_page()
    
    # Since we've already added the font in the header, we don't need to add it again for the body
    pdf.set_font("DejaVu", size=9)
    today = date.today()

    bezwaar_text = f"""
    {name}
    {adres}
    {kenteken}
    {datum_boete}

    Aan het hoofd van de afdeling Bezwaar en Beroep
    CJIB
    Postbus 1794
    8901 CB Leeuwarden

    Asterdam, {today}

    Betreft: Bezwaarschrift boetebeschikking [kenmerk/boetenummer]

    Geachte heer/mevrouw,

    Hierbij maak ik, {name}, bezwaar tegen de boetebeschikking met kenmerk {boetenummer}, gedateerd op [datum van de boete], voor het overtreden van de maximumsnelheid op {adres}.

    Mijn bezwaren tegen deze boetebeschikking zijn als volgt:

    1. Volgens mijn informatie mag op de locatie: {adres} waar de overtreding zou hebben plaatsgevonden niet geflitst worden. Ik verzoek u vriendelijk om dit na te gaan en te bevestigen.

    2. {boetebedrag} Ik ben van mening dat de boete disproportioneel hoog is in verhouding tot de vermeende overtreding. Ik verzoek om heroverweging van de boetebedrag.

    3. Ik heb reeds een boete ontvangen voor een vergelijkbaar vergrijp in dezelfde periode. Het lijkt hier om een dubbele bestraffing te gaan voor hetzelfde vergrijp, wat naar mijn mening onrechtvaardig is.

    4. Ik ben ervan overtuigd dat ik mij aan de snelheidslimiet heb gehouden. De meting van de snelheidscamera, waarop de beschikking gebaseerd is, kan onnauwkeurig zijn geweest door een niet geijkte camera. Ik verzoek om bewijs van de recente ijking van de betreffende camera.

    Gezien bovenstaande punten verzoek ik u de boetebeschikking te heroverwegen en deze in te trekken. Bijgevoegd vindt u kopieën van documenten die mijn bezwaren ondersteunen.

    Ik verzoek vriendelijk om een schriftelijke bevestiging van de ontvangst van dit bezwaarschrift, en zie graag uw reactie tegemoet binnen de wettelijke termijn.

    Met vriendelijke groet,

    {name}

    """
    pdf.multi_cell(0, 5, bezwaar_text)
    
    pdf.output(f"{name}_bezwaar_{datum_boete}.pdf")

def main():
    st.markdown('<h1 style="color: black; text-align: center;">Gratis-Bezwaar.nl</h1>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Kies je boete", help="Upload hier je boete")

    if uploaded_file is not None:
        st.success('Bedankt voor het uploaden van je boete.')

        with st.form("info_form"):
            name = st.text_input("Naam", value="Michael Schoustra")
            adres = st.text_input("Adres", value="Koninginneweg 1, 1234AB Amsterdam")
            kenteken = st.text_input("Kenteken", value="12-AB-34")
            boetenummer = st.text_input("Boetenummer", value="123456789")
            boetebedrag = st.text_input("Boetebedrag", value="€ 95,00")
            datum_boete = st.date_input("Datum boete", value=pd.to_datetime("2021-01-01"))
            omschrijving = st.text_area("Omschrijving", value="Te hard gereden")
            extra_argumenten = st.text_input("Extra argumenten", value="")

            submitted = st.form_submit_button("Bevestig gegevens")
        
        if submitted:
            create_pdf(name, adres, kenteken, boetebedrag, datum_boete, omschrijving, extra_argumenten, boetenummer)
            
            # Provide the PDF for download
            with open(f"{name}_bezwaar_{datum_boete}.pdf", "rb") as pdf_file:
                st.download_button(label="Download bezwaarbrief",
                                   data=pdf_file,
                                   file_name=f"{name}_bezwaar_{datum_boete}.pdf",
                                   mime="application/pdf")

if __name__ == '__main__':
    main()