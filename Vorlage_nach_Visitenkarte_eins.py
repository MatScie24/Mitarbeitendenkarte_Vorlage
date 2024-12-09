import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile

# Add this as the first Streamlit command
st.set_page_config(page_title="Template for personal card", page_icon="📇")

#---------------------------------------------------------
# Title and Header
st.title('Template for personal card')

# Create a container for responsive layout
with st.container():
    # Create two columns for layout with added space
    col1, col2 = st.columns([2, 1], gap="large")  # Use gap="large" for more space

    # Display the card template image in the second column
    with col2:
        st.image("Bild2.png", caption="Example of the Personal Card Template", use_column_width=True)  # Adjust width as needed

    # Display the selection lines in the first column
    with col1:
        #---------------------------------------------------------
        # Options for the selectbox
        options = ["select...", "Prof.", "Dr.", "Dr.-Ing","Dr.rer.nat.","M.Sc.","B.Sc.","Other"]

        # Selectbox for expertise with 'Other' option
        title = st.selectbox("Enter Title", options)

        # If 'Other' is selected, show a text input for custom title
        if title == "Other":
            custom_title = st.text_input("Please specify your title")
            title = custom_title  # Use the custom input instead of "Other"

        # Collect inputs from the user
        First_name = st.text_input("Enter First Name")
        Surname = st.text_input("Enter Surname")

        #---------------------------------------------------------
        # Options for the selectbox
        options = ["select...", "Institutsleitung", "Bereichsleitung", "Abteilungsleitung","Gruppenleitung","Wissenschaftlicher Mitarbeiter","Wissenschaftliche Mitarbeiterin","Mitarbeiter","Mitarbeiterin","Werksleitung","Komm. Gruppenleitung","Technischer Mitarbeiter","Technische Mitarbeiterin","Ingenieur","Ingenieurin","Chemielaborant","Chemielaborantin","Techniker","Technikerin", "Other"]

        # Selectbox for expertise with 'Other' option
        position = st.selectbox("Enter Position", options)

        # If 'Other' is selected, show a text input for custom position
        if position == "Other":
            custom_position = st.text_input("Please specify your position")
            position = custom_position  # Use the custom input instead of "Other"

        #---------------------------------------------------------
        picture = st.file_uploader("Upload your picture", type=["png", "jpeg", "jpg"])
        expertise_1 = st.text_input("Expertise/Workfield 1")
        expertise_2 = st.text_input("Expertise/Workfield 2")
        expertise_3 = st.text_input("Expertise/Workfield 3")

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

# Helper function to check text length
def check_text_length(pdf, text, max_width, font_size, initial_x, initial_y):
    pdf.set_font("Arial", size=font_size)
    while pdf.get_string_width(text) > max_width:
        font_size -= 1
        pdf.set_font("Arial", size=font_size)
        if font_size < 6:  # Minimum readable font size
            return 6
    return font_size

# When the user clicks 'Generate PDF'
if st.button("Generate PDF"):
    # Create PDF instance
    pdf = PDF()
    pdf.add_page()

    # Check text lengths and show warnings
    position_lines = len(position.split('\n'))
    name_length = len(f"{title} {First_name} {Surname}")
    
    # Calculate approximate lines for each expertise entry
    expertise_lines = []
    pdf.set_font("Arial", size=10)
    for exp in [expertise_1, expertise_2, expertise_3]:
        if exp:
            lines = len(exp) * pdf.get_string_width("a") / 45
            expertise_lines.append(lines)

    warning_messages = []
    
    if position_lines > 1:
        warning_messages.append("Position text is too long and may be displayed in smaller font.")
    
    if name_length > 30:
        warning_messages.append("Name is too long and may be displayed in smaller font.")
    
    if any(lines > 2 for lines in expertise_lines):
        warning_messages.append("Some expertise entries exceed two lines and will be displayed in smaller font.")

    if warning_messages:
        st.warning("\n".join(warning_messages))

    # Set the background image for the name and position
    pdf.image("Bild1.png", x=55, y=10, w=55, h=60)  # Adjust the position and size as needed

    # Add position text in white with dynamic font size
    pdf.set_text_color(255, 255, 255)
    position_font_size = check_text_length(pdf, position, 51, 10, 57, 17)
    pdf.set_font("Arial", size=position_font_size)
    pdf.set_y(17)
    pdf.set_x(57)
    pdf.multi_cell(51, 6, txt=position, align='L')

    # Add name with dynamic font size
    name_text = f"{title} {First_name}"
    name_font_size = check_text_length(pdf, name_text, 51, 15, 57, 25)
    pdf.set_font("Arial", size=name_font_size)
    pdf.set_y(25)
    pdf.set_x(57)
    pdf.cell(51, 6, txt=name_text, ln=True, align='L')
    
    surname_font_size = check_text_length(pdf, Surname, 51, name_font_size, 57, pdf.get_y())
    pdf.set_font("Arial", size=surname_font_size)
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
    
    # Add expertise entries with dynamic font size
    current_y = 40  # Start 5 mm higher than the previous value of 45
    base_expertise_font_size = 10
    
    for expertise in [expertise_1, expertise_2, expertise_3]:
        if expertise:
            pdf.set_font("Arial", size=base_expertise_font_size)
            
            # Calculate approximate number of lines needed
            lines_needed = len(expertise) * pdf.get_string_width("a") / 45
            
            # Only reduce font size if more than 2 lines are needed
            if lines_needed > 2:
                pdf.set_font("Arial", size=8)  # Reduce to 8pt if text exceeds 2 lines
            
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
