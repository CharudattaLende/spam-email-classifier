import streamlit as st
from model import predict_email

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Session state for demo examples
# ---------------------------------------------------------------------------
if "demo_type" not in st.session_state:
    st.session_state.demo_type = None

spam_msg = "Congratulations! You've been selected as our lucky winner. Click NOW to claim your FREE iPhone 15 Pro. Limited time offer — expires in 24 hours!"
safe_msg = "Hi team, just a reminder that our weekly sync is tomorrow at 3pm. Please review the agenda doc before joining. See you there!"

# ---------------------------------------------------------------------------
# Custom styling - Matches the beautiful preview design
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: #0b0b14 !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0b0b14 0%, #1a1a2e 100%) !important;
            padding: 0 !important;
        }
        
        .main {
            background: transparent !important;
            padding-top: 0 !important;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding: 2rem 0 !important;
            max-width: 100% !important;
        }
        
        /* Badge styling */
        .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: rgba(99, 70, 220, 0.18);
            border: 1px solid rgba(140, 100, 255, 0.38);
            border-radius: 99px;
            padding: 8px 16px;
            font-size: 0.7rem;
            font-weight: 500;
            color: #c4b0ff;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin: 0 auto 1.2rem;
        }
        
        .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #8b5cf6;
            box-shadow: 0 0 7px #8b5cf6;
        }
        
        /* Title styling */
        .title-main {
            font-family: 'Syne', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.15;
            background: linear-gradient(135deg, #fff 25%, #c4b0ff 65%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 auto 0.8rem;
            text-align: center;
        }
        
        .subtitle-main {
            font-size: 0.95rem;
            color: #8e8aa5;
            max-width: 420px;
            line-height: 1.6;
            font-weight: 300;
            margin: 0 auto 2.2rem;
            text-align: center;
            padding: 0 1.5rem;
        }
        
        /* Card styling */
        .card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 18px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            margin: 0 auto 2rem;
            max-width: 580px;
            width: 100%;
        }
        
        .card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(140, 100, 255, 0.55), transparent);
        }
        
        /* Label styling */
        .lbl {
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #6b6880;
            margin-bottom: 1rem;
            display: block;
        }
        
        /* Demo buttons container */
        .demo-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 1.2rem;
            width: 100%;
        }
        
        /* Toggle buttons */
        [data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            color: #6b6880 !important;
            font-size: 0.8rem !important;
            height: 36px !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="baseButton-secondary"]:hover {
            background: rgba(99, 70, 220, 0.15) !important;
            border-color: rgba(139, 92, 246, 0.4) !important;
            color: #c4b0ff !important;
        }
        
        /* Textarea styling */
        .stTextArea textarea {
            width: 100% !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #e8e6f0 !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.9rem !important;
            padding: 14px 14px !important;
            resize: none !important;
            line-height: 1.5 !important;
        }
        
        .stTextArea textarea::placeholder {
            color: #3f3c52 !important;
        }
        
        .stTextArea textarea:focus {
            border-color: rgba(139, 92, 246, 0.6) !important;
            box-shadow: 0 0 12px rgba(99, 70, 220, 0.15) !important;
        }
        
        /* Button styling */
        [data-testid="baseButton-primary"] {
            width: 100% !important;
            margin-top: 16px !important;
            background: linear-gradient(135deg, #6346dc, #8b5cf6 60%, #a78bfa) !important;
            border: none !important;
            border-radius: 10px !important;
            color: #fff !important;
            font-family: 'Syne', sans-serif !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
            padding: 12px 20px !important;
            box-shadow: 0 4px 22px rgba(99, 70, 220, 0.38) !important;
            transition: all 0.3s ease !important;
            height: 40px !important;
        }
        
        [data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 32px rgba(99, 70, 220, 0.5) !important;
        }
        
        /* Result cards */
        .result-spam {
            background: rgba(220, 53, 80, 0.12);
            border: 1px solid rgba(220, 53, 80, 0.35);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-top: 1.2rem;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        
        .result-safe {
            background: rgba(34, 197, 120, 0.10);
            border: 1px solid rgba(34, 197, 120, 0.3);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-top: 1.2rem;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        
        .r-icon {
            font-size: 1.8rem;
            flex-shrink: 0;
        }
        
        .r-title {
            font-family: 'Syne', sans-serif;
            font-size: 0.98rem;
            font-weight: 700;
            margin: 0;
        }
        
        .r-desc {
            font-size: 0.78rem;
            opacity: 0.75;
            margin-top: 3px;
            margin: 0;
        }
        
        .result-spam .r-title, .result-spam .r-desc {
            color: #ff6b82;
        }
        
        .result-safe .r-title, .result-safe .r-desc {
            color: #34c578;
        }
        
        /* Stats section */
        .stats {
            display: flex;
            justify-content: space-around;
            gap: 1rem;
            margin-top: 1.6rem;
            padding-top: 1.4rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .stat-item {
            text-align: center;
            flex: 1;
        }
        
        .s-num {
            font-family: 'Syne', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #c4b0ff;
            margin-bottom: 4px;
        }
        
        .s-lbl {
            font-size: 0.7rem;
            color: #5a5770;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        
        /* Footer */
        .footer-container {
            background: rgba(255, 255, 255, 0.02);
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding: 2.5rem 1.5rem;
            margin-top: 3rem;
            text-align: center;
        }
        
        .footer-text {
            font-size: 0.8rem;
            color: #5a5770;
            letter-spacing: 0.04em;
            margin: 0;
            line-height: 1.6;
        }
        
        .footer-highlight {
            color: #8b5cf6;
            font-weight: 600;
        }
        
        /* Column alignment */
        [data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header with badge
# ---------------------------------------------------------------------------
st.markdown('<div class="badge"><span class="dot"></span> AI-Powered · Instant Detection</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title-main">Is that email<br>spam or legit?</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-main">Paste any message and our trained classifier tells you instantly — no guesswork.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Main card with input
# ---------------------------------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<label class="lbl">✦ Your message</label>', unsafe_allow_html=True)

# Demo buttons in columns
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button("Try spam example", use_container_width=True, key="spam_demo"):
        st.session_state.demo_msg = spam_msg
        st.session_state.demo_type = "spam"
        st.rerun()

with col2:
    if st.button("Try safe example", use_container_width=True, key="safe_demo"):
        st.session_state.demo_msg = safe_msg
        st.session_state.demo_type = "safe"
        st.rerun()

# Text area with demo content if selected
if "demo_msg" in st.session_state:
    user_input = st.text_area(
        label="Message",
        value=st.session_state.demo_msg,
        placeholder="Paste email content here…",
        height=120,
        label_visibility="collapsed"
    )
else:
    user_input = st.text_area(
        label="Message",
        placeholder="Paste email content here…",
        height=120,
        label_visibility="collapsed"
    )

# Analyze button
if st.button("Analyse Message →", use_container_width=True, key="analyze_btn"):
    if not user_input.strip():
        st.markdown('''
            <div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:1rem 1.2rem;color:#fbbf24;font-size:0.82rem;margin-top:1rem;text-align:center;">
            ⚠️ Please paste a message first.
            </div>
        ''', unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Analyzing..."):
            result = predict_email(user_input)
        
        if result == "Spam":
            st.markdown('''
                <div class="result-spam">
                    <div class="r-icon">🚨</div>
                    <div>
                        <p class="r-title">Spam Detected</p>
                        <p class="r-desc">Strong spam signals found. Do not click any links.</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
                <div class="result-safe">
                    <div class="r-icon">✅</div>
                    <div>
                        <p class="r-title">Looks Legitimate</p>
                        <p class="r-desc">No spam patterns detected. This message appears safe.</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

# Stats section
st.markdown("""
    <div class="stats">
        <div class="stat-item">
            <div class="s-num">5,574</div>
            <div class="s-lbl">Trained on</div>
        </div>
        <div class="stat-item">
            <div class="s-num">~98%</div>
            <div class="s-lbl">Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="s-num">Naive Bayes</div>
            <div class="s-lbl">Model</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="footer-container">
        <p class="footer-text">
            🛡️ Built with <span class="footer-highlight">AI Technology</span> by <span class="footer-highlight">CL Systems</span>
        </p>
        <p class="footer-text" style="margin-top: 8px; font-size: 0.75rem; opacity: 0.6;">
            © 2026 · Spam Detection Classifier · Powered by Naive Bayes
        </p>
    </div>
""", unsafe_allow_html=True)
