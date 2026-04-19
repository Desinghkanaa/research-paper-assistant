import streamlit as st

st.set_page_config(
    page_title="Research Paper Assistant",
    layout="wide",
)


st.markdown("""
<style>

/* Main background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* Hero Title */
.hero-title {
    font-size: 48px;
    font-weight: 700;
    color: white;
}

.hero-sub {
    font-size: 20px;
    color: #94a3b8;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: #6366f1;
}

/* Card Title */
.card-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* Card Text */
.card-text {
    font-size: 14px;
    color: #cbd5f5;
}

/* Tag */
.tag {
    display: inline-block;
    padding: 5px 10px;
    margin: 4px;
    background: #1e293b;
    border-radius: 10px;
    font-size: 12px;
}

/* Stats */
.stat {
    font-size: 28px;
    font-weight: bold;
    color: #6366f1;
}
.stat-label {
    font-size: 14px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True

)

# Hero section

st.markdown('<div class="hero-title">AI Research Paper Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Build, Analyze & Improve Research Papers using AI</div>', unsafe_allow_html=True)

st.write("")

st.markdown("""
This platform combines two powerful modules:

- 🧱 **Constructor** → Generate IEEE research papers  
- 🔍 **Deconstructor** → Analyze and interact with papers  

👉 Designed for modern academic workflows.
""")

st.subheader("Use the sidebar to open Constructor or Deconstructor")

st.write("")
st.divider()


# Coloum view

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat">2</div><div class="stat-label">Core Modules</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat">AI</div><div class="stat-label">Powered</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat">PDF</div><div class="stat-label">Analysis</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat">RAG</div><div class="stat-label">Architecture</div>', unsafe_allow_html=True)

st.divider()


# Main Grid

col1, col2 = st.columns(2)

# CONSTRUCTOR
with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🧱 Research Paper Constructor</div>
        <div class="card-text">
        Generate IEEE-style research papers from your GitHub project or idea.
        </div>

        <div class="tag">IEEE Format</div>
        <div class="tag">Auto Writing</div>
        <div class="tag">Structured Output</div>

        <hr>

        • Generate Abstract, Intro, Methodology<br>
        • Use GitHub repository as input<br>
        • Add author & institution<br>
    </div>
    """, unsafe_allow_html=True)

# DECONSTRUCTOR
with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔍 Research Paper Deconstructor</div>
        <div class="card-text">
        Upload research papers and chat with them using AI.
        </div>

        <div class="tag">PDF Analysis</div>
        <div class="tag">Chat UI</div>
        <div class="tag">Gap Detection</div>

        <hr>

        • Upload PDF documents<br>
        • Ask questions (chat)<br>
        • Extract insights & limitations<br>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# st.title("Research Paper Assistant")
# st.subheader("Use the sidebar to open Constructor or Deconstructor")

# st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>© 2026 AI Research Paper Assistant | MCA Final Year Project</div>",
    unsafe_allow_html=True
)