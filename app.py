import streamlit as st
import pandas as pd
import altair as alt
import os

# إعدادات الصفحة وعرض الواجهة بالشكل العريض
st.set_page_config(
    page_title="بوابة الأكاديمية المهنية للمعلمين - فرع الجيزة", 
    page_icon="🏫", 
    layout="wide"
)

# تخصيص واجهة المستخدم بالكامل وإلغاء القائمة الجانبية التقليدية
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
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    .metric-card-1 { background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-2 { background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-3 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); padding: 15px; border-radius: 12px; color: #333; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-4 { background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-5 { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-card-6 { background: linear-gradient(135deg, #cb356b 0%, #bd3f32 100%); padding: 15px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .card-title { font-size: 14px !important; font-weight: bold; margin-bottom: 5px; }
    .card-number { font-size: 22px; font-weight: bold; }
    .program-header { font-size: 20px !important; font-weight: bold; color: #1e293b; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-top: 20px; margin-bottom: 15px; }
    .top-header { background-color: #1e293b; color: white; padding: 14px 15px; border-radius: 8px; text-align: center; font-size: 17px; font-weight: bold; margin-bottom: 20px; }
    .nav-container { background-color: #f8fafc; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .footer-container { text-align: center; padding: 15px; margin-top: 30px; border-top: 1px solid #e2e8f0; color: #475569; font-size: 14px; font-weight: bold; background-color: #f8fafc; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# عنوان الصفحة العلوي
st.markdown('<div class="top-header">🏫 الأكاديمية المهنية للمعلمين - فرع الجيزة (بوابة الخدمات الرقمية)</div>', unsafe_allow_html=True)

# دالة ذكية لتحميل ملفات الإكسل برمجياً بالكلمات المفتاحية
def find_and_load_excel(keyword):
    for file in os.listdir('.'):
        if file.endswith('.xlsx') and keyword in file:
            try:
                df = pd.read_excel(file)
                df.index = range(1, len(df) + 1)
                df.index.name = "م"
                return df, file
            except Exception:
                pass
    return None, None

# تحميل الملفات الستة
df_reassign, name_reassign = find_and_load_excel("160")
df_cader, name_cader = find_and_load_excel("التسكين")
df_job, name_job = find_and_load_excel("مسمى")
df_training, name_training = find_and_load_excel("معد")
df_batch1, name_batch1 = find_and_load_excel("الاولى")
df_batch2, name_batch2 = find_and_load_excel("الثانية")

# حساب أعداد السجلات
c_reassign = len(df_reassign) if df_reassign is not None else 0
c_cader = len(df_cader) if df_cader is not None else 0
c_job = len(df_job) if df_job is not None else 0
c_training = len(df_training) if df_training is not None else 0
c_batch1 = len(df_batch1) if df_batch1 is not None else 0
c_batch2 = len(df_batch2) if df_batch2 is not None else 0

# --- القائمة الأفقية العلوية للتنقل ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
st.markdown("#### 🗂️ لوحة التنقل الرئيسية للبرامج والخدمات")
selected_section = st.selectbox("اختر القسم المطلوب عرضه:", [
    "🏠 الرئيسية والمؤشرات العامة والبحث الشامل",
    "📁 معد البرامج التدريبية",
    "📁 المسمى الوظيفي",
    "📁 التسكين علي الكادر",
    "📁 إعادة التعيين (قرار 160)",
    "📁 معلم مساعد الدفعة الأولى",
    "📁 معلم مساعد الدفعة الثانية"
], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 1. شاشة الرئيسية والمؤشرات العامة والبحث الشامل
if selected_section == "🏠 الرئيسية والمؤشرات العامة والبحث الشامل":
    
    st.markdown("### 🔎 البحث الشامل بالكود في كافة الملفات والبرامج")
    global_search_code = st.text_input("أدخل كود المعلم للبحث الفوري عنه في جميع الكشوفات:", placeholder="مثال: 3089097")

    if global_search_code:
        st.markdown("---")
        st.subheader("🎯 نتائج البحث الشامل:")
        
        def check_and_display(df, program_name):
            found = False
            if df is not None:
                mask = df.astype(str).apply(lambda x: x.str.contains(global_search_code, case=False, na=False)).any(axis=1)
                result = df[mask]
                if not result.empty:
                    found = True
                    st.markdown(f"#### تم العثور على نتائج في برنامج: <span style='color: #2563eb;'>{program_name}</span>", unsafe_allow_html=True)
                    st.dataframe(result, use_container_width=True)
            return found

        check_and_display(df_training, "معد البرامج التدريبية")
        check_and_display(df_job, "المسمى الوظيفي")
        check_and_display(df_cader, "التسكين علي الكادر")
        check_and_display(df_reassign, "إعادة التعيين (قرار 160)")
        check_and_display(df_batch1, "معلم مساعد الدفعة الأولى")
        check_and_display(df_batch2, "معلم مساعد الدفعة الثانية")
        st.markdown("---")

    # البطاقات الإحصائية الملونة
    st.markdown("### 📌 مؤشرات الإحصاء العامة لبرامج الفرع")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="metric-card-1"><div class="card-title">معد البرامج التدريبية</div><div class="card-number">{c_training}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-4"><div class="card-title">إعادة التعيين (قرار 160)</div><div class="card-number">{c_reassign}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card-2"><div class="card-title">المسمى الوظيفي</div><div class="card-number">{c_job}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-5"><div class="card-title">معلم مساعد (الدفعة الأولى)</div><div class="card-number">{c_batch1}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card-3"><div class="card-title">التسكين علي الكادر</div><div class="card-number">{c_cader}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-6"><div class="card-title">معلم مساعد (الدفعة الثانية)</div><div class="card-number">{c_batch2}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # الرسوم البيانية
    st.markdown("### 📈 التحليل البصري ومقارنة أعداد السجلات للبرامج")
    chart_data = pd.DataFrame({
        "البرنامج": ["معد البرامج", "المسمى الوظيفي", "التسكين", "قرار 160", "معلم مساعد 1", "معلم مساعد 2"],
        "عدد السجلات": [c_training, c_job, c_cader, c_reassign, c_batch1, c_batch2]
    })

    chart = alt.Chart(chart_data).mark_bar(color="#3b82f6", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("البرنامج:N", sort=None, title="", axis=alt.Axis(labelAngle=0, labelFontSize=11)),
        y=alt.Y("عدد السجلات:Q", title="إجمالي السجلات"),
        tooltip=["البرنامج", "عدد السجلات"]
    ).properties(height=320)

    st.altair_chart(chart, use_container_width=True)

# دالة عرض الأقسام التفصيلية
def render_section(title, df):
    st.markdown(f'<p class="program-header">📁 {title}</p>', unsafe_allow_html=True)
    if df is not None:
        st.metric(label=f"إجمالي السجلات في هذا الكشف", value=len(df))
        search_query = st.text_input(f"🔍 بحث مخصص داخل كشف {title}:", key=f"search_{title}")
        display_df = df
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            display_df = df[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(display_df)}")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.error(f"تعذر العثور على ملف الإكسل الخاص بـ '{title}'.")

# توجيه الشاشات حسب الاختيار
if selected_section == "📁 معد البرامج التدريبية":
    render_section("معد البرامج التدريبية", df_training)
elif selected_section == "📁 المسمى الوظيفي":
    render_section("المسمى الوظيفي", df_job)
elif selected_section == "📁 التسكين علي الكادر":
    render_section("التسكين علي الكادر", df_cader)
elif selected_section == "📁 إعادة التعيين (قرار 160)":
    render_section("إعادة التعيين (قرار 160 لسنة 2024)", df_reassign)
elif selected_section == "📁 معلم مساعد الدفعة الأولى":
    render_section("معلم مساعد الدفعة الأولى", df_batch1)
elif selected_section == "📁 معلم مساعد الدفعة الثانية":
    render_section("معلم مساعد الدفعة الثانية", df_batch2)

# --- تذييل الصفحة (Footer) ---
st.markdown("""
    <div class="footer-container">
        تصميم وتنفيذ: <span style="color: #2563eb;">أحمد الجنزوري</span> 🌟
    </div>
""", unsafe_allow_html=True)
