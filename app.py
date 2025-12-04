import streamlit as st
from pylatexenc.latex2text import LatexNodes2Text
from fpdf import FPDF
import base64

st.set_page_config(
    page_title="Overleaf-like LaTeX Editor",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# Templates
# ---------------------------
TEMPLATES = {
    "Blank Document": r"""
\section{Hello}
This is a sample.
""",
    "Academic Resume": r"""
\section{Name}
Mohan Duratkar

\section{Education}
MSc Biochemistry (2021)

\section{Skills}
Python, R, CADD, Docking, AI-ML
""",
    "Research Paper": r"""
\section{Title}
My Research Paper

\section{Abstract}
Write abstract here.

\section{Introduction}
Write introduction here.
"""
}

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("📄 LaTeX Builder")
template = st.sidebar.selectbox("Select Template", list(TEMPLATES.keys()))
file_name = st.sidebar.text_input("PDF File Name", "document.pdf")
compile_button = st.sidebar.button("Compile PDF")

# ---------------------------
# Editor Area
# ---------------------------
left, right = st.columns([1, 1])

with left:
    st.subheader("📝 LaTeX Editor")
    latex_code = st.text_area("Write LaTeX code here", value=TEMPLATES[template], height=600)

# ---------------------------
# Function: LaTeX → PDF (Text Only)
# ---------------------------
def latex_to_pdf(latex_text):
    # Step 1: Convert LaTeX → Plain text
    plain_text = LatexNodes2Text().latex_to_text(latex_text)

    # Step 2: Create PDF using FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in plain_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin1")

# ---------------------------
# PDF Generation
# ---------------------------
pdf_data = None
if compile_button:
    try:
        pdf_data = latex_to_pdf(latex_code)
    except Exception as e:
        st.error(f"PDF Generation Error: {e}")

# ---------------------------
# PDF Preview
# ---------------------------
with right:
    st.subheader("📘 PDF Preview")

    if pdf_data:
        # Convert PDF to Base64 for preview
        b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        pdf_display = f'<embed src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download PDF",
            data=pdf_data,
            file_name=file_name,
            mime="application/pdf"
        )
    else:
        st.info("Compile your document to see PDF preview.")
