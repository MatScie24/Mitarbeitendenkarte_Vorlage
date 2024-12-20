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

# Add this near your other buttons
if st.button("Show Preview"):
    # Sample data
    sample_title = "Dr."
    sample_name = "John-hermann"
    sample_surname = "Doeasdd dsafsadf"
    sample_position = "Wissenschaftliche Mitarbeiterin"
    sample_expertise1 = "Artificial Intelligence and Machine Learning "
    sample_expertise2 = "Artificial Intelligence and Machine Learning "
    sample_expertise3 = "Artificial Intelligence and Machine Learning "

    # Create PDF with sample data
    pdf = PDF()
    pdf.add_page()

    # Colors for gradient
    start_color = (0, 119, 154)
    end_color = (1, 74, 107)

    # Gradient box for name and position
    pdf.gradient_fill(55, 10, 55, 60, start_color, end_color)

    # Add position text in white
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=10)
    pdf.set_y(17)
    pdf.set_x(57)
    pdf.multi_cell(51, 6, txt=sample_position, align='L')

    # Add name
    pdf.set_font("Arial", size=15)
    pdf.set_y(25)
    pdf.set_x(57)
    pdf.cell(51, 6, txt=f"{sample_title} {sample_name}", ln=True, align='L')
    pdf.set_x(57)
    pdf.cell(51, 6, txt=sample_surname, ln=False, align='L')

    # Picture placeholder
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(10, 10, 45, 60)
    
    # Add expertise entries
    current_y = 43
    pdf.set_font("Arial", size=10)
    
    for expertise in [sample_expertise1, sample_expertise2, sample_expertise3]:
        pdf.set_y(current_y)
        pdf.set_x(57)
        pdf.cell(5, 4, txt="-", ln=0)
        pdf.set_x(60)
        text_height = pdf.multi_cell(51, 4, txt=expertise, align='L')
        current_y = pdf.get_y() + 0.5

    # Save preview PDF
    preview_pdf = "preview.pdf"
    pdf.output(preview_pdf)

    # Show download button for preview
    with open(preview_pdf, "rb") as pdf_file:
        st.download_button(
            label="Download Preview PDF",
            data=pdf_file,
            file_name="preview.pdf",
            mime="application/pdf"
        )
        
    st.success("Preview PDF generated! Click the download button above to view it.")

# When the user clicks 'Generate PDF'
if st.button("Generate PDF"):
    # Create PDF instance
    pdf = PDF()
    pdf.add_page()

    # Colors for gradient
    start_color = (0, 119, 154)
    end_color = (1, 74, 107)

    # Gradient box for name and position (increased height to 60mm)
    pdf.gradient_fill(55, 10, 55, 60, start_color, end_color)

    # Add position text in white
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=10)
    pdf.set_y(17)
    pdf.set_x(57)
    # The line break is controlled by the width (45) and height (6) parameters in multi_cell
    # If the text is longer than 45mm, it will automatically break to the next line
    # The height of 6mm determines the vertical spacing between lines
    pdf.multi_cell(51, 6, txt=position, align='L')

    # Add name
    pdf.set_font("Arial", size=15)
    pdf.set_y(25)
    pdf.set_x(57)
    pdf.cell(51, 6, txt=f"{title} {First_name}", ln=True, align='L')
    pdf.set_x(57)
    pdf.cell(51, 6, txt=Surname, ln=False, align='L')

    # Picture placeholder/handling
    pdf.set_draw_color(0, 0, 0)
    if picture is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
            tmpfile.write(picture.getvalue())
            tmpfile_path = tmpfile.name
        pdf.image(tmpfile_path, x=10, y=10, w=45, h=60)
    else:
        pdf.rect(10, 10, 45, 60)
    
    # Add expertise entries directly under name in gradient box
    current_y = 43
    pdf.set_font("Arial", size=10)
    # Removed black border box
    
    for expertise in [expertise_1, expertise_2, expertise_3]:
        if expertise:  # Keep the check for non-empty expertise
            pdf.set_y(current_y)
            pdf.set_x(57)
            pdf.cell(5, 4, txt="-", ln=0)
            pdf.set_x(60)
            text_height = pdf.multi_cell(51, 4, txt=expertise, align='L')
            current_y = pdf.get_y() + 0.5

    # Save and display the PDF
    pdf_output = f"{First_name}_{Surname}_guideline.pdf"
    pdf.output(pdf_output)

    # Provide the download link
    with open(pdf_output, "rb") as pdf_file:
        st.download_button(label="Download your PDF", data=pdf_file, file_name=pdf_output, mime="application/pdf")
