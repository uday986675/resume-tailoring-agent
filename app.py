import re
from reportlab.platypus import Paragraph, Spacer, ListFlowable, ListItem, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from xml.sax.saxutils import escape
import streamlit as st
from graph import workflow
from document_parser import extract_text


def build_resume_pdf(markdown_text: str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles for a resume look
    styles.add(ParagraphStyle(
        name="ResumeName", parent=styles["Title"],
        fontSize=18, leading=22, spaceAfter=4, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="ResumeH1", parent=styles["Heading1"],
        fontSize=13, leading=16, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#1a1a1a"),
    ))
    styles.add(ParagraphStyle(
        name="ResumeH2", parent=styles["Heading2"],
        fontSize=11, leading=14, spaceBefore=8, spaceAfter=3,
        textColor=colors.HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name="ResumeH3", parent=styles["Heading3"],
        fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="ResumeBody", parent=styles["Normal"],
        fontSize=10, leading=13, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="ResumeBullet", parent=styles["Normal"],
        fontSize=10, leading=13, leftIndent=14, bulletIndent=4,
        spaceAfter=2,
    ))

    story = []
    lines = markdown_text.splitlines()
    i = 0

    # Inline markdown → ReportLab markup
    def inline(text: str) -> str:
        # 1. Remove Emojis and weird symbols
        # This regex removes emoji ranges safely
        text = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27BF]', '', text)
        # Remove the weird pipe characters and extra spaces
        text = re.sub(r'\s*[|•]\s*', ' | ', text).strip(" |")
        
        # 2. Escape HTML
        text = escape(text)
        
        # 3. Bold and Italics
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
        
        # 4. Links (Email, LinkedIn, GitHub)
        text = re.sub(
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', 
            r'<a href="mailto:\1" color="blue"><u>\1</u></a>', 
            text
        )

        def add_url_link(match):
            url = match.group(1)
            if not url.startswith("http"):
                url = "https://" + url
            return f'<a href="{url}" color="blue"><u>{match.group(1)}</u></a>'
            
        text = re.sub(
            r'(linkedin\.com\/[a-zA-Z0-9_-]+|github\.com\/[a-zA-Z0-9_-]+)', 
            add_url_link, 
            text
        )
        
        return text

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if not line.strip():
            i += 1
            continue

        # Headings
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["ResumeName"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]).upper(), styles["ResumeH1"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["ResumeH2"]))
        elif line.startswith("#### "):
            story.append(Paragraph(inline(line[5:]), styles["ResumeH3"]))

        # Bullets (possibly grouped)
        elif line.lstrip().startswith(("- ", "* ", "• ")):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith(("- ", "* ", "• ")):
                bullet = lines[i].lstrip()[2:].strip()
                items.append(ListItem(
                    Paragraph(inline(bullet), styles["ResumeBullet"]),
                    leftIndent=14,
                ))
                i += 1
            story.append(ListFlowable(
                items, bulletType="bullet", start="•",
                leftIndent=14, bulletFontSize=8,
            ))
            story.append(Spacer(1, 4))
            continue

        # Horizontal rule
        elif line.strip() in ("---", "***", "___"):
            from reportlab.platypus import HRFlowable
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=colors.HexColor("#cccccc")))
            story.append(Spacer(1, 4))

        # Normal paragraph
        else:
            story.append(Paragraph(inline(line), styles["ResumeBody"]))

        i += 1

    doc.build(story)
    return buffer.getvalue()


st.set_page_config(
    page_title="Resume Intelligence Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Intelligence Agent")
st.write("Upload your resume and job description to generate a tailored resume.")


col1, col2 = st.columns(2)


with col1:
    st.subheader("📄 Resume")

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )


with col2:
    st.subheader("💼 Job Description")

    jd = st.text_area(
        "Paste the job description",
        height=400,
        placeholder="Paste the job description here..."
    )


if st.button("Generate Tailored Resume", type="primary"):

    if resume_file is None:
        st.warning("Please upload your resume.")
        st.stop()

    if not jd.strip():
        st.warning("Please enter the job description.")
        st.stop()

    with st.spinner("Extracting documents..."):

        resume = extract_text(resume_file)

    if not resume.strip():
        st.error("Could not extract text from the resume.")
        st.stop()

    if not jd.strip():
        st.error("Could not extract text from the job description.")
        st.stop()

    initial_state = {
        "resume": resume,
        "jd": jd,
        "revision_count": 0
    }

    with st.spinner("Analyzing and tailoring your resume..."):

        result = workflow.invoke(initial_state)

    if isinstance(result["tailored_resume"], list):
        result["tailored_resume"] = "".join(
            block.get("text", "") for block in result["tailored_resume"] if isinstance(block, dict)
        )

    st.success("Tailored resume generated successfully! 🎉")

    st.subheader("Tailored Resume")
    st.text_area("Result", value=result["tailored_resume"], height=700)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    story = []

    for line in result["tailored_resume"].splitlines():
        line = line.strip()
        if line:
            story.append(Paragraph(escape(line), styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)

    pdf_bytes = build_resume_pdf(result['tailored_resume'])

    st.download_button(
        label="📄 Download Resume as PDF",
        data=pdf_bytes,
        file_name="tailored_resume.pdf",
        mime="application/pdf",
    )