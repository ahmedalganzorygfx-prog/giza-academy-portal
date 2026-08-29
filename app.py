import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="بوابة فرع الجيزة - الأكاديمية المهنية للمعلمين",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Arabic / RTL styling and professional look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #2a5298;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="main-header">
        <h1>🎓 بوابة فرع الجيزة - الأكاديمية المهنية للمعلمين</h1>
        <p>إدارة البرامج التدريبية، التنمية المهنية، وملفات المعلمين المستهدفين للترقي</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">إشراف: أ/ أحمد الجنزوري (مدير الفرع)</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("قائمة التصفح الرئيسية")
app_mode = st.sidebar.selectbox("اختر القسم:", [
    "الرئيسية والإحصائيات",
    "إدارة الدورات وبرامج التنمية المهنية",
    "متابعة المعلمين والمرشحين للترقي",
    "تقارير الإنجاز وتصدير البيانات",
    "الإعدادات والدعم الفني"
])

# Sample Data Generation for demonstration
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    data = {
        "رقم المعلم": [f"EG-{i:04d}" for i in range(1, 101)],
        "اسم المعلم": [f"معلم تجربى {i}" for i in range(1, 101)],
        "الإدارة التعليمية": np.random.choice(["العجوزة", "الدقي", "الشيخ زايد", "6 أكتوبر", "الجيزة", "البدرشين"], 100),
        "التخصص": np.random.choice(["حاسب آلي", "لغة عربية", "رياضيات", "لغة إنجليزية", "دراسات اجتماعية", "علوم"], 100),
        "حالة البرنامج التدريبي": np.random.choice(["مجتاز", "قيد التدريب", "متخلف عن الحضور"], 100, p=[0.75, 0.20, 0.05]),
        "درجة الاختبار": np.random.randint(60, 100, 100),
        "تاريخ التسجيل": pd.date_range(start="2026-01-01", periods=100, freq="D").strftime("%Y-%m-%d")
    }
    return pd.DataFrame(data)

df = load_sample_data()

if app_mode == "الرئيسية والإحصائيات":
    st.subheader("📊 لوحة المؤشرات والإحصائيات العامة لفرع الجيزة")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي المعلمين المسجلين", len(df))
    with col2:
        st.metric("عدد المجتازين للتدريب", len(df[df["حالة البرنامج التدريبي"] == "مجتاز"]))
    with col3:
        st.metric("نسبة النجاح العامة", f"{(len(df[df['حالة البرنامج التدريبي'] == 'مجتاز']) / len(df)) * 100:.1f}%")
    with col4:
        st.metric("عدد الإدارات التابعة", df["الإدارة التعليمية"].nunique())
        
    st.markdown("---")
    st.markdown("### 📈 توزيع حالات التدريب حسب التخصص")
    chart_data = pd.crosstab(df["التخصص"], df["حالة البرنامج التدريبي"])
    st.bar_chart(chart_data)

elif app_mode == "إدارة الدورات وبرامج التنمية المهنية":
    st.subheader("📚 برامج التنمية المهنية وحقائب التدريب")
    st.info("هنا يتم متابعة الجداول الزمنية للحقائب التدريبية الخاصة بالمعلمين والمرشحين للترقي.")
    
    # Example table
    courses_df = pd.DataFrame({
        "اسم البرنامج التدريبي": ["استخدام التكنولوجيا في التعليم الحديث", "مهارات القيادة التربوية والإشراف", "استراتيجيات التفكير الناقد", "تطبيقات الذكاء الاصطناعي في التعليم"],
        "الفئة المستهدفة": ["معلمو الحاسب الآلي", "الوظائف الإشرافية والمدارس", "معلمو المرحلة الاعدادية", "جميع التخصصات"],
        "تاريخ البداية": ["2026-03-01", "2026-03-10", "2026-03-15", "2026-04-01"],
        "الحالة": ["جارٍ الآن", "مجدول", "مجدول", "قيد التحضير"]
    })
    st.dataframe(courses_df, use_container_width=True)

elif app_mode == "متابعة المعلمين والمرشحين للترقي":
    st.subheader("👥 استعلام ومتابعة بيانات المعلمين")
    
    search_term = st.text_input("🔍 ابحث برقم المعلم، الاسم، أو الإدارة التعليمية:")
    
    filtered_df = df.copy()
    if search_term:
        filtered_df = df[
            df["رقم المعلم"].str.contains(search_term, case=False) |
            df["اسم المعلم"].str.contains(search_term, case=False) |
            df["الإدارة التعليمية"].str.contains(search_term, case=False) |
            df["التخصص"].str.contains(search_term, case=False)
        ]
        
    st.dataframe(filtered_df, use_container_width=True)
    st.write(f"عدد النتائج المعروضة: {len(filtered_df)}")

elif app_mode == "تقارير الإنجاز وتصدير البيانات":
    st.subheader("📥 تقارير الأداء وتصدير البيانات")
    st.markdown("يمكنك تصفية البيانات وتصدير النتائج النهائية بصيغة CSV أو Excel لتقديمها للجهات المختصة.")
    
    selected_admin = st.selectbox("تصفية حسب الإدارة التعليمية:", ["الكل"] + list(df["الإدارة التعليمية"].unique()))
    
    export_df = df.copy()
    if selected_admin != "الكل":
        export_df = df[df["الإدارة التعليمية"] == selected_admin]
        
    st.dataframe(export_df, use_container_width=True)
    
    # Corrected download button syntax (fixed the stray colon bug)
    csv_data = export_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="💾 تصدير النتائج الحالية لملف CSV",
        data=csv_data,
        file_name="cpd_export.csv",
        mime="text/csv"
    )

elif app_mode == "الإعدادات والدعم الفني":
    st.subheader("⚙️ الإعدادات العامة للبوابة")
    st.write("إصدار النظام: v2.4.0 (محدث لعام 2026)")
    st.write("جهة الإشراف: فرع الجيزة - الأكاديمية المهنية للمعلمين")
    st.success("جميع الاتصالات وقواعد البيانات مؤمنة وتعمل بكفاءة عالية.")
