import streamlit as st
import io

from ast_analyzer import parse_code_structure
from bug_detector import detect_issues
from complexity import analyze_complexity, plot_complexity_graph
from quality_analyzer import analyze_quality
from ai_module2 import generate_ai_report, generate_documentation

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------- SESSION STATE ----------
if "results" not in st.session_state:
    st.session_state["results"] = None

if "documentation" not in st.session_state:
    st.session_state["documentation"] = None

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Code Analyzer", layout="wide")

# ---------- HEADER ----------
st.title("AI-Assisted Code Analysis and Documentation Tool")
st.markdown("""
An intelligent platform that combines static analysis with AI-driven insights to evaluate code quality, detect issues, and generate professional documentation—helping developers write cleaner, more maintainable software.
""")
# st.markdown("Analyze code. Detect issues. Generate documentation. All in one place.")
st.markdown("---")

# ---------- INPUT SECTION (IMAGE + INPUT SIDE BY SIDE) ----------
col1, col2 = st.columns(2)

code = ""

with col1:
    st.image("Cover_Image.png", width="stretch")

with col2:
    uploaded_file = st.file_uploader("Upload Python file (.py / .txt)", type=["py", "txt"])
    code_input = st.text_area("Or paste your Python code here:", height=300)

    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")
    elif code_input.strip() != "":
        code = code_input

    if st.button("🔍 Analyze Code"):
        if not code.strip():
            st.warning("Please provide code.")
        else:
            with st.spinner("Analyzing..."):
                structure = parse_code_structure(code)
                issues = detect_issues(code)
                complexity = analyze_complexity(code)
                quality = analyze_quality(code)
                ai_report = generate_ai_report(code, issues)

                st.session_state["results"] = {
                    "structure": structure,
                    "issues": issues,
                    "complexity": complexity,
                    "quality": quality,
                    "ai_report": ai_report
                }
                st.session_state["documentation"] = None  # Reset documentation when new code is analyzed   

st.markdown("---")

# ---------- RESULTS DASHBOARD ----------
if st.session_state["results"]:

    results = st.session_state["results"]
    comp = results["complexity"]
    quality = results["quality"]

    # ---------- TOP METRICS ----------
    st.subheader("📈 Overview")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

    col1.metric("Lines of Code (LOC)", quality.get("loc", 0))
    col2.metric("Cyclomatic Complexity", quality.get("cyclomatic_complexity", 0))
    col3.metric("Halstead Volume", quality.get("halstead_volume", 0))
    col4.metric("Maintainability Index", quality.get("maintainability_index", 0))
    col5.metric("Rating", quality.get("rating", "N/A"))

    st.markdown("---")

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🤖 AI Report", "📄 Documentation"])

    # ---------- TAB 1: ANALYSIS ----------
    with tab1:
        st.subheader("Code Structure")
        st.json(results["structure"])

        st.subheader("Issues")
        if results["issues"]:
            for issue in results["issues"]:
                st.write(f"- {issue}")
        else:
            st.write("No issues found.")

        st.subheader("Complexity")

        col1, col2, col3 = st.columns(3)
        col1.metric("Time", comp.get("time_complexity"))
        col2.metric("Space", comp.get("space_complexity"))
        # col3.metric("Rating", quality.get("rating"))

        st.caption(comp.get("explanation", ""))

        if comp.get("valid"):
            fig = plot_complexity_graph(
                comp.get("time_complexity"),
                comp.get("space_complexity")
            )
            st.pyplot(fig, width="content")
        else:
            st.warning("Graph not available due to invalid code.")

        st.subheader("Code Quality")

        if quality.get("code_smells"):
            for q in quality["code_smells"]:
                st.write(f"- {q}")
        else:
            st.write("No major issues detected.")

    # ---------- TAB 2: AI REPORT ----------
    with tab2:
        st.subheader("AI Analysis")
        st.text_area("Report", results["ai_report"], height=700)

    # ---------- TAB 3: DOCUMENTATION ----------
    with tab3:
        st.subheader("Documentation")

        if not code.strip():
            st.warning("Provide code first.")
        else:
            # ✅ Generate only once (avoid repeated API calls)
            if not st.session_state.get("documentation"):
                with st.spinner("Generating documentation..."):
                    st.session_state["documentation"] = generate_documentation(code)

            # ---------- DISPLAY ----------
            st.text_area(
                "Generated Documentation",
                st.session_state["documentation"],
                height=700
            )

            # ---------- PDF FUNCTION ----------
            def create_documentation_pdf(documentation_text):
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer)
                styles = getSampleStyleSheet()

                elements = []
                elements.append(Paragraph("Software Documentation", styles["Title"]))

                lines = documentation_text.split("\n")

                for line in lines:
                    line = line.strip()

                    if line.startswith("###"):
                        elements.append(Paragraph(line.replace("###", ""), styles["Heading2"]))
                        elements.append(Spacer(1, 8))
                    elif line == "":
                        elements.append(Spacer(1, 6))
                    else:
                        elements.append(Paragraph(line, styles["Normal"]))
                        elements.append(Spacer(1, 6))

                doc.build(elements)
                buffer.seek(0)
                return buffer

            doc_pdf = create_documentation_pdf(st.session_state["documentation"])

            st.download_button(
                label="⬇️ Download Documentation as PDF",
                data=doc_pdf,
                file_name="Documentation.pdf",
                mime="application/pdf"
            )
