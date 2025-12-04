
import streamlit as st
import subprocess
import os
import base64
from pathlib import Path

# -------------------------------------------------------
# ----------- BASIC OVERLEAF-STYLE PAGE CONFIG ----------
# -------------------------------------------------------
st.set_page_config(
    page_title="LaTeX Builder",
    layout="wide",
    page_icon="📝"
)

st.markdown("""
<style>
    .code-editor textarea {
        font-family: 'Fira Code', monospace !important;
        font-size: 15px !important;
    }
    .pdf-viewer {
        border: 1px solid #ddd;
        border-radius: 8px;
        height: 90vh;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# ------------------- LATEX TEMPLATES --------------------
# -------------------------------------------------------
resume_template = r"""
\documentclass{article}
\begin{document}

\begin{center}
    {\Huge \textbf{<<NAME>>}} \\[4pt]
    <<EMAIL>> | <<PHONE>> \\[2pt]
    <<LINKEDIN>>
\end{center}

\section*{Education}
<<EDUCATION>>

\section*{Experience}
<<EXPERIENCE>>

\section*{Skills}
<<SKILLS>>

\end{document}
"""

research_template = r"""
\documentclass{article}
\usepackage{abstract}
\title{<<TITLE>>}
\author{<<AUTHOR>>}
\date{}

\begin{document}
\maketitle

\begin{abstract}
<<ABSTRACT>>
\end{abstract}

\section{Introduction}
<<INTRO>>

\section{Methods}
<<METHODS>>

\section{Results}
<<RESULTS>>

\section{Conclusion}
<<CONCLUSION>>

\end{document}
"""

thesis_template = r"""
\documentclass{report}
\begin{document}

\title{<<TITLE>>}
\author{<<AUTHOR>>}
\date{}
\maketitle

\chapter{Introduction}
<<INTRO>>

\chapter{Review of Literature}
<<ROL>>

\chapter{Methodology}
<<METHODOLOGY>>

\chapter{Results}
<<RESULTS>>

\chapter{Conclusion}
<<CONCLUSION>>

\end{document}
"""

# -------------------------------------------------------
# ------------------ TEMPLATE DICTIONARY -----------------
# -------------------------------------------------------
templates = {
    "Academic Resume": resume_template,
    "Research Paper": research_template,
    "Mini Thesis": thesis_template
}

# -------------------------------------------------------
# ---------------------- SIDEBAR UI ----------------------
# -------------------------------------------------------
st.sidebar.title("📌 LaTeX Builder")

template_choice = st.sidebar.selectbox(
    "Select Template",
    list(templates.keys())
)

st.sidebar.markdown("### Auto-fill Fields")

name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone")
linkedin = st.sidebar.text_input("LinkedIn URL")

title = st.sidebar.text_input("Title (Research/Thesis)")
abstract = st.sidebar.text_area("Abstract / Summary")
skills = st.sidebar.text_area("Skills")
education = st.sidebar.text_area("Education")
experience = st.sidebar.text_area("Experience")
intro = st.sidebar.text_area("Introduction")
methods = st.sidebar.text_area("Methods / Methodology")
results = st.sidebar.text_area("Results")
conclusion = st.sidebar.text_area("Conclusion")
rol = st.sidebar.text_area("Review of Literature")

# -------------------------------------------------------
# ---------------- GENERATE LATEX FILLED DATA -----------
# -------------------------------------------------------
def fill_template(template):
    filled = template.replace("<<NAME>>", name)\
        .replace("<<EMAIL>>", email)\
        .replace("<<PHONE>>", phone)\
        .replace("<<LINKEDIN>>", linkedin)\
        .replace("<<EDUCATION>>", education)\
        .replace("<<EXPERIENCE>>", experience)\
        .replace("<<SKILLS>>", skills)\
        .replace("<<TITLE>>", title)\
        .replace("<<AUTHOR>>", name)\
        .replace("<<ABSTRACT>>", abstract)\
        .replace("<<INTRO>>", intro)\
        .replace("<<METHODS>>", methods)\
        .replace("<<RESULTS>>", results)\
        .replace("<<CONCLUSION>>", conclusion)\
        .replace("<<ROL>>", rol)
    return filled

# -------------------------------------------------------
# ---------------------- MAIN LAYOUT ---------------------
# -------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 LaTeX Editor")

    default_tex = fill_template(templates[template_choice])

    latex_code = st.text_area(
        "Edit LaTeX Code",
        default_tex,
        height=700,
        key="latex_editor"
    )

with col2:
    st.subheader("📄 PDF Preview")

    # Compile LaTeX to PDF
    if st.button("Compile PDF", type="primary"):
        with open("document.tex", "w") as f:
            f.write(latex_code)

        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "document.tex"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if Path("document.pdf").exists():
            with open("document.pdf", "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                pdf_base64 = base64.b64encode(pdf_bytes).decode()

                pdf_display = f'<iframe class="pdf-viewer" src="data:application/pdf;base64,{pdf_base64}" width="100%" height="100%"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            st.download_button("⬇ Download PDF", pdf_bytes, file_name="output.pdf")

        st.download_button("⬇ Download LaTeX", latex_code, file_name="document.tex")

# -------------------------------------------------------
# ---------------- CLEANUP AUX FILES ---------------------
# -------------------------------------------------------
for f in ["document.aux", "document.log"]:
    if os.path.exists(f):
        os.remove(f)
