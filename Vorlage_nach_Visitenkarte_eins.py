import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile

# Add this as the first Streamlit command
st.set_page_config(page_title="Template for personal card", page_icon="📇", layout="wide")

# Add custom CSS for layout adjustment
st.markdown("""
    <style>
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    .stTitle {
        padding-left: 0;
        margin-left: 0;
    }
    /* Base styling for all input containers */
    .stSelectbox, .stTextInput, .stFileUploader {
        width: calc(100% - 2cm) !important;
        margin-left: 1cm !important;    
        margin-right: 1cm !important;
        padding: 0 !important;
    }
    /* Style for selectbox container */
    .stSelectbox > div {
        width: calc(100% - 2cm) !important;
        margin-left: 1cm !important;
        margin-right: 1cm !important;
        padding: 0 !important;
    }
    /* Style for the actual select element */
    div[data-baseweb="select"] {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    h1 {
        text-align: center;
        font-size: 3em;
    }
    [data-testid="column"] {
        padding: 0;
    }
    /* Ensure file uploader has same alignment */
    .stFileUploader > div {
        width: calc(100% - 2cm) !important;
        margin-left: 1cm !important;
        margin-right: 1cm !important;
        padding: 0 !important;
    }
    /* Align selectbox titles to the left and at the same height as the x-position starting point */
    .stSelectbox label {
        text-align: left !important;
        margin-top: 0 !important;
        margin-left: 0cm !important;
    }
    /* Make the image container responsive with aligned margins */
    [data-testid="column"] > div:has(img) {
        margin-top: 0.8cm;
        margin-left: 0.3cm;
        margin-right: 1cm;  /* Same as selectbox margin */
        width: calc(100% - 1.3cm);
        height: auto;
    }
    
    /* Make the image itself responsive */
    .stImage {
        width: 100%;
        max-width: 300px;
        min-width: 150px;
        margin: 0 auto;
        display: block;
    }
    
    .stImage > img {
        width: 100%;
        height: auto;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        -ms-interpolation-mode: nearest-neighbor;
        transform: translateZ(0);
        backface-visibility: hidden;
    }
    /* Center align the Generate PDF button */
    [data-testid="stButton"] {
        text-align: center;
        margin-left: auto;
        margin-right: auto;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

#---------------------------------------------------------
# Title and Header with center alignment
st.markdown("<h1>Template for personal card</h1>", unsafe_allow_html=True)

# Create a container for responsive layout
with st.container():
    # Create a two-column layout with 3:1 ratio
    col1, col2 = st.columns([3, 1])  # 3/4 for inputs, 1/4 for image

    with col1:
        # Display the selection lines with custom label
        options = ["select...", "Prof.", "Dr.", "Dr.-Ing","Other"]
        title = st.selectbox("Enter Title", options)  # Empty label here since we're using custom label above

        if title == "Other":
            custom_title = st.text_input("Please specify your title")
            title = custom_title

        First_name = st.text_input("Enter First Name")
        Surname = st.text_input("Enter Surname")



    with col2:
        # Display the card template image with responsive sizing
        st.image("Bild2.png", 
                caption="Example of the Personal Card Template",
                use_column_width=True)  # Enable column width scaling
        

    options = ["select...", "Institutsleitung", "Bereichsleitung", "Abteilungsleitung","Gruppenleitung","Wissenschaftlicher Mitarbeiter","Wissenschaftliche Mitarbeiterin","Mitarbeiter","Mitarbeiterin","Werksleitung","Komm. Gruppenleitung","Technischer Mitarbeiter","Technische Mitarbeiterin","Ingenieur","Ingenieurin","Chemielaborant","Chemielaborantin","Techniker","Technikerin", "Other"]
    position = st.selectbox("Enter Position", options)

    if position == "Other":
        custom_position = st.text_input("Please specify your position")
        position = custom_position

    expertise_1 = st.text_input("Expertise/Workfield 1")
    expertise_2 = st.text_input("Expertise/Workfield 2")
    expertise_3 = st.text_input("Expertise/Workfield 3")

    # Picture upload (full width)
    picture = st.file_uploader("Upload your picture", type=["png", "jpeg", "jpg"])

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

    # Picture placeholder
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
