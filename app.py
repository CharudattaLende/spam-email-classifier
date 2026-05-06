import streamlit as st
from model import predict_email

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📧 Spam Email Classifier")
st.markdown("Paste any email or message below to instantly find out if it's spam.")
st.divider()

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
user_input = st.text_area(
    label="✉️ Enter your message",
    placeholder="e.g. Congratulations! You've won a free iPhone. Click here to claim your prize...",
    height=160,
)

# ---------------------------------------------------------------------------
# Predict button
# ---------------------------------------------------------------------------
if st.button("🔍 Predict", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter a message before predicting.")
    else:
        with st.spinner("Analysing message..."):
            result = predict_email(user_input)

        if result == "Spam":
            st.error(f"🚨 Result: **{result}**  \nThis message looks like spam.")
        else:
            st.success(f"✅ Result: **{result}**  \nThis message looks legitimate.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #888888; font-size: 0.8rem; padding: 8px 0;">
        🛡️ Built by &nbsp;<strong>CL Systems</strong>&nbsp; © 2026
    </div>
    """,
    unsafe_allow_html=True,
)
