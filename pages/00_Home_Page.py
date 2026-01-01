import streamlit as st

# Set page config
st.set_page_config(
    page_title="Smart Traffic Violation Detector",
    page_icon="assets/logo.png",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Marquee styling */
    .marquee-container {
        width: 100%;
        background-color: var(--secondary-background-color);
        padding: 10px 0;
        border-bottom: 2px solid var(--secondary-background-color);
        margin-bottom: 20px;
    }
    .marquee-text {
        font-size: 18px;
        font-weight: 600;
        color: #e74c3c;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: var(--text-color);
        font-size: 60px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Subtitle styling */
    .sub-title {
        text-align: center;
        font-size: 24px;
        color: var(--text-color);
        font-weight: 400;
    }
    
    /* List item styling */
    .feature-list {
        font-size: 16px;
        line-height: 1.8;
        color: var(--text-color);
    }
    .feature-list li {
        margin-bottom: 8px;
    }
    .list-item-heading {
        font-weight: 600;
        font-size: 19px;
    }
</style>
""", unsafe_allow_html=True)



# Hero Section
st.markdown(
    """
    <h1 class="main-title">
        🚦 Smart Traffic Violation Pattern Detector
    </h1>

    <p class="sub-title">
        An intelligent, data-driven dashboard designed to uncover trends, hotspots,<br>
        and behavior patterns in traffic violations for smarter and safer cities.
    </p>
    """,
    unsafe_allow_html=True
)

st.write("---")

st.markdown("""
    <h3>🔍 What This System Does</h3>
    """,
    unsafe_allow_html=True
)
# Image + Text Layout
col1, col2 = st.columns([1, 1.2], gap='small', border=True)

with col1:
    st.image("assets/vector-image-traffic.png")

with col2:
    st.markdown(
        """
        <div class="feature-list">
        
        <ul>
            <li>
                📊 <b class="list-item-heading">Know Your Data</b>
                <br>Automated dataset profiling & quality checks
            </li>
            <li>
                🚦 <b class="list-item-heading">AI-Based Risk Prediction</b>
                 <br>Uses machine learning to predict traffic violation risk levels 
                 (Low / Medium / High) based on historical patterns and contextual factors 
                 such as time and vehicle type.
            </li>
            <li>
                 🌦️ <b class="list-item-heading">Weather Violation Recommendation</b>
                  <br>An AI-powered decision support system that recommends the most likely 
                   traffic violations under specific weather conditions to help authorities 
                 focus enforcement effectively.
             </li>
            <li>
                ⬆️ <b class="list-item-heading">Manual Data Upload</b>
                <br>Upload your own datasets for custom analysis
            </li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
   
st.write("---")
# Marquee Section
st.markdown("""
<div class="marquee-container">
    <marquee class="marquee-text" behavior="scroll" direction="left">
        🚦 Real-time Traffic Insights  |  📊 Analyzing Violation Trends  |  🗺️ Identifying High-Risk Zones  |  🚗 Driver Behavior Analytics  |  ⛈️ Weather Impact Assessment  |  🛡️ Promoting Safer Roads
    </marquee>
</div>
""", unsafe_allow_html=True)