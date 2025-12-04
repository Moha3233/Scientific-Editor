import streamlit as st
import subprocess
import tempfile
import base64
import os

st.set_page_config(page_title="Overleaf-like Editor", layout="wide")

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.title("📄 LaTeX Templates")

templates = {
    "Blank Document": r"""
\documentclass{article}
\begin{document}
Hello World!
\end{document}
""",

    "Academic Research Paper": r"""
\documentclass{article}
\usepackage{times}
\usepackage{graphicx}
\title{Your Research Title}
\author{Your Name}
\date{}
\begin{document}
\maketitle

\begin{abstract}
Write abstract here.
\end{abstract}

\section{Introduction}
Write introduction here.

\end{document}
""",

    "Resume / CV": r"""
\documentclass[a4paper,12pt]{article}
\usepackage{geometry}
\geometry{margin=1in}
\begin{document}

\begin{center}
{\LARGE Your Name}\\
\vspace{2mm}
your.email@example.com | +91-XXXXXXXXXX
\end{center}

\section*{Education}
Degree | Year | Institute

\section*{Experience}
Job Role | Company

\section*{Projects}
Project details here.

\end{document}
"""
}

selected_template = st.sidebar.selectbox("Choose Template", list(templates.keys()))
download_filename = st.sidebar.text_input("Filename", "document.pdf")

# ------------------------------
# Editor + Preview Layout
# ------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✍️ LaTeX Editor")
    latex_code = st.text_area("Write LaTeX code here", templates[selected_template], height=500)

compile_btn = st.sidebar.button("Compile PDF")

# ------------------------------
# Compile LaTeX
# ------------------------------
pdf_bytes = None
error_text = ""

if compile_btn:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, "main.tex")

        with open(tex_file, "w") as f:
            f.write(latex_code)

        # Try compiling using Tectonic (clean, modern LaTeX engine)
        try:
            compile_cmd = ["tectonic", tex_file, "--outdir", tmpdir]
            result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                pdf_path = os.path.join(tmpdir, "main.pdf")
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
            else:
                error_text = result.stderr

        except Exception as e:
            error_text = str(e)

# ------------------------------
# Display PDF or Errors
# ------------------------------
with col2:
    st.subheader("📘 PDF Preview")

    if pdf_bytes:
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button("Download PDF", pdf_bytes, file_name=download_filename)

    elif error_text:
        st.error("⚠️ LaTeX Compilation Failed")
        st.code(error_text)
    else:
        st.info("PDF will appear here after compiling.")
