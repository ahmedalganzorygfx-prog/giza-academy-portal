import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة لتكون بعرض عريض لتناسب الجداول
st.set_page_config(page_title="لوحة البيانات المحمية", layout="wide")

# ==================== 1. تنسيقات الـ CSS (إخفاء زر التحميل + العلامة المائية) ====================
st.markdown("""
    <style>
    /* إخفاء شريط الأدوات وزر التحميل العائم فوق الجداول والرسومات البيانية */
    [data-testid="stElementToolbar"],
    [data-testid="baseButton-header"],
    button[title*="Download"] {
        display: none !important;
    }

    /* تصميم العلامة المائية الخلفية */
    .watermark-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        align-content: space-around;
        z-index: 999999;
        pointer-events: none; /* يسمح بالتفاعل مع الصفحة والنقر بشكل طبيعي تماماً */
        overflow: hidden;
    }

    .watermark-text {
        color: rgba(150, 150, 150, 0.15); /* لون رمادي خفيف جداً لا يعيق القراءة */
        font-size: 22px;
        font-weight: bold;
        transform: rotate(-30deg); /* ميلان النص لتعشيق الشاشة */
        user-select: none;
        white-space: nowrap;
        padding: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 2. إعداد بيانات العلامة المائية الديناميكية ====================
# (يمكن ربطها لاحقاً بنظام تسجيل الدخول أو الـ Session State الخاص بك)
user_name = "أحمد الجنزوري"
user_code = "PAT-GIZ-01"
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
watermark_content = f"{user_name} - {user_code} - {current_time}"

# حقن العلامة المائية في الصفحة عبر كود HTML متكرر لتغطية الشاشة بالكامل
watermark_html = f"""
<div class="watermark-container">
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
    <div class="watermark-text">{watermark_content}</div>
</div>
"""
st.markdown(watermark_html, unsafe_allow_html=True)

# ==================== 3. محتوى التطبيق والجداول الخاصة بك ====================
st.title("🛡️ لوحة البيانات الحساسة والمحمية")
st.write("هذه الصفحة مؤمنة بحيث تم إخفاء أزرار التحميل والتنزيل العائمة، مع وجود علامة مائية سرية باسم المستخدم ووقت الزيارة.")

# مثال على جدول بيانات حساس
data = {
    "م": [1, 2, 3, 4],
    "اسم الموظف": ["محمد علي", "سارة أحمد", "محمود حسن", "فاطمة إبراهيم"],
    "المنصب": ["معلم أول", "معلم خبير", "مدرب إلكتروني", "رئيس قسم"],
    "التقييم السنوي": ["امتياز", "جيد جداً", "امتياز", "امتياز"],
    "الرقم القومي": ["2900101********", "2951205********", "2880314********", "2920722********"]
}

df = pd.DataFrame(data)

st.subheader("بيانات الموظفين السرية")
# عرض الجدول (بدون زر التنزيل الذي تم إخفاؤه بالـ CSS)
st.dataframe(df, use_container_width=True)
