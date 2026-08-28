import streamlit as st
import pandas as pd
import altair as alt
import os
import base64

# إعدادات الصفحة
st.set_page_config(
    page_title="بوابة الأكاديمية المهنية للمعلمين - فرع الجيزة", 
    page_icon="🏫", 
    layout="wide",
    initial_sidebar_state="expanded"  # ضمان أن تبدأ القائمة مفتوحة وثابتة دائماً
)

# تخصيص الاتجاهات والخطوط فقط بدون أي تأثير على القائمة الجانبية
st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    h3, .stMarkdown h3 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* تصميم الهيدر المركزي المتكامل */
    .app-header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 40px 20px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 30px;
        border: 1px solid #334155;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .app-logo-img {
        width: 180px !important;
        min-width: 180px !important;
        max-width: 180px !important;
        height: auto !important;
        border-radius: 12px;
        object-fit: contain;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 20px;
    }
    .app-main-title {
        font-size: 34px !important;
        font-weight: 800 !important;
        margin: 0 0 10px 0 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        line-height: 1.2;
        text-align: center;
    }
    .app-sub-title {
        font-size: 18px !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
        margin: 0 !important;
        text-align: center;
    }

    .metric-card-1 { background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-2 { background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-3 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); padding: 15px; border-radius: 12px; color: #333; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-4 { background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-5 { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-6 { background: linear-gradient(135deg, #cb356b 0%, #bd3f32 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    
    .cpd-card-box { background: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 12px; color: white; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
    .cpd-total-box { background: linear-gradient(135deg, #0f172a 100%, #1e3a8a 0%); border: 2px solid #3b82f6; padding: 18px; border-radius: 14px; color: white; margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); }
    .cpd-title { font-size: 15px; font-weight: bold; color: #38bdf8; margin-bottom: 10px; border-bottom: 1px solid #475569; padding-bottom: 5px; }
    .cpd-total-title { font-size: 17px; font-weight: bold; color: #facc15; margin-bottom: 12px; border-bottom: 1px solid #3b82f6; padding-bottom: 6px; text-align: center; }
    .cpd-stats { display: flex; justify-content: space-around; text-align: center; font-size: 13px; }
    .stat-item span { display: block; font-size: 16px; font-weight: bold; margin-top: 4px; }

    .card-title { font-size: 14px !important; font-weight: bold; margin-bottom: 5px; }
    .card-number { font-size: 22px; font-weight: bold; }
    .program-header { font-size: 20px !important; font-weight: bold; color: #1e293b; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-top: 20px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)
