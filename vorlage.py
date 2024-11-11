import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile

# Add this as the first Streamlit command
st.set_page_config(page_title="Template for personal card", page_icon="📇")

#---------------------------------------------------------
# Title and Header
st.title('Template for personal card')
#---------------------------------------------------------
# Options for the selectbox
options = ["select...", "Prof.", "Dr.", "Dr.-Ing","Dr.rer.nat.","M.Sc.","B.Sc.","Other"]

# Selectbox for expertise with 'Other' option
title = st.selectbox("Enter Title", options)

# If 'Other' is selected, show a text input for custom expertise
if title == "Other":
    custom_expertise = st.text_input("Please specify your title")
else:
    custom_expertise = title
# Collect inputs from the user
#title = st.selectbox("Enter Title",
 #   ("select...", "Prof.", "Dr.", "Dr.-Ing","Dr.rer.nat.","M.Sc.","B.Sc."),
#)
#---------------------------------------------------------
First_name = st.text_input("Enter First Name")
Surname = st.text_input("Enter Surname")
#---------------------------------------------------------
# Options for the selectbox
options = ["select...", "Institutsleitung", "Bereichsleitung", "Abteilungsleitung","Gruppenleitung","Wissenschaftlicher Mitarbeiter","Wissenschaftliche Mitarbeiterin","Mitarbeiter","Mitarbeiterin","Werksleitung","Komm. Gruppenleitung","Technischer Mitarbeiter","Technische Mitarbeiterin","Ingenieur","Ingenieurin","Chemielaborant","Chemielaborantin","Techniker","Technikerin", "Other"]

# Selectbox for expertise with 'Other' option
position = st.selectbox("Enter Position", options)

# If 'Other' is selected, show a text input for custom expertise
if position == "Other":
    custom_expertise = st.text_input("Please specify your position")
else:
    custom_expertise = position
#---------------------------------------------------------
#position = st.selectbox("Enter Position",
#    ("select...", "Institutsleitung", "Bereichsleitung", "Abteilungsleitung","Gruppenleitung","Wissenschaftlicher Mitarbeiter","Wissenschaftliche Mitarbeiterin","Mitarbeiter","Mitarbeiterin","Werksleitung","Komm. Gruppenleitung","Technischer Mitarbeiter","Technische Mitarbeiterin","Ingenieur","Ingenieurin","Chemielaborant","Chemielaborantin","Techniker","Technikerin"),
#)
#---------------------------------------------------------
picture = st.file_uploader("Upload your picture", type=["png", "jpeg", "jpg"])
expertise_1 = st.text_input("Expertise/Workfield 1")
expertise_2 = st.text_input("Expertise/Workfield 2")
expertise_3 = st.text_input("Expertise/Workfield 3")


from fpdf import FPDF

class PDF(FPDF):
    def gradient_fill(self, x, y, w, h, start_color, end_color, steps=100):
        r1, g1, b1 = start_color
        r2, g2, b2 = end_color
        
        for i in range(steps):
            r = r1 + (r2 - r1) * i / steps
            g = g1 + (g2 - g1) * i / steps
            b = b1 + (b2 - b1) * i / steps
            
            self.set_fill_color(int(r), int(g), int(b))
            self.rect(x, y + i * (h / steps), w, h / steps, 'F')

# When the user clicks 'Generate PDF'
if st.button("Generate PDF"):
    # Create PDF instance
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", size=10)

    # Colors for gradient (RGB format)
    start_color = (0, 119, 154)  # Blue
    end_color = (1, 74, 107)  # Light blue

    # Gradient box (2.54x6 cm)
    pdf.gradient_fill(10, 10, 60, 25.4, start_color, end_color)

    # Add text inside the gradient box
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(15)
    pdf.set_x(10)
    pdf.cell(60, 6, txt=f"{title} {First_name}", ln=True, align='L')
    pdf.set_x(10)
    pdf.cell(60, 6, txt=Surname, ln=False, align='L')

    # Handle image upload
    if picture is not None:
        # Save uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
            tmpfile.write(picture.getvalue())
            tmpfile_path = tmpfile.name
        
        # Add the image to the PDF
        pdf.image(tmpfile_path, x=45.35, y=11.35, w=22.7, h=22.7)


    # Another gradient box for the position
    pdf.gradient_fill(10, 36.4, 60, 6.1, start_color, end_color)

    pdf.set_y(36.4)
    pdf.set_x(10)
    pdf.cell(60, 6.1, txt=custom_expertise, ln=True, align='C')

    # White box with black rim for expertise
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(10, 43.5, 60, 30.5)

    # Set initial position
    current_y = 43.5
    pdf.set_text_color(0, 0, 0)

    # Handle each expertise entry
    for expertise in [expertise_1, expertise_2, expertise_3]:
        if expertise:  # Only process if there's content
            pdf.set_y(current_y)
            pdf.set_x(10)
            # Add bullet point (using dash instead of bullet)
            pdf.cell(5, 4, txt="-", ln=0)
            # Add expertise text
            pdf.set_x(15)  # Indent the text
            text_height = pdf.multi_cell(55, 4, txt=expertise, align='L')
            # Update Y position for next entry
            current_y = pdf.get_y()

    # Save and display the PDF
    pdf_output = f"{First_name}_{Surname}_guideline.pdf"
    pdf.output(pdf_output)

    # Provide the download link
    with open(pdf_output, "rb") as pdf_file:
        st.download_button(label="Download your PDF", data=pdf_file, file_name=pdf_output, mime="application/pdf")
