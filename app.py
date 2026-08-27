import streamlit as st
import pandas as pd
import altair as alt
import os
import base64

# إعدادات الصفحة وعرض الواجهة بالشكل العريض
st.set_page_config(
    page_title="بوابة الأكاديمية المهنية للمعلمين - فرع الجيزة", 
    page_icon="🏫", 
    layout="wide"
)

# تخصيص واجهة المستخدم والتنسيقات المتناسقة
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
    [data-testid="collapsedControl"] {
        display: none !important;
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

# --- تم إلغاء لوحة التحكم وكلمة المرور نهائياً وأزرار التنزيل متاحة للجميع ---

# --- البحث عن ملف اللوجو بصيغ مختلفة ---
found_logo_path = None
possible_names = ["logo.png", "Logo.png", "LOGO.PNG", "logo.jpg", "Logo.jpg", "LOGO.JPG", "logo.jpeg", "Logo.jpeg"]

for name in possible_names:
    if os.path.exists(name):
        found_logo_path = name
        break

if found_logo_path:
    with open(found_logo_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    img_ext = found_logo_path.split('.')[-1].lower()
    mime_type = "image/jpeg" if img_ext in ["jpg", "jpeg"] else "image/png"
    logo_display_html = f'<img src="data:{mime_type};base64,{encoded_string}" class="app-logo-img">'
else:
    logo_display_html = '<div style="color: #f87171; font-size: 12px; margin-bottom: 10px;">⚠️ لم يتم العثور على الشعار</div>'

st.markdown(f"""
    <div class="app-header-box">
        {logo_display_html}
        <div class="app-main-title">الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
        <div class="app-sub-title">بوابة الخدمات الرقمية وإدارة بيانات المعلمين المتكاملة</div>
    </div>
""", unsafe_allow_html=True)

# دالة لتحميل الملفات
def load_excel_file(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_excel(filename)
            df.index = range(1, len(df) + 1)
            df.index.name = "م"
            return df
        except Exception:
            return None
    return None

# تحميل الملفات
df_training = load_excel_file("training.xlsx")
df_job = load_excel_file("job.xlsx")
df_cader = load_excel_file("cader.xlsx")
df_reassign = load_excel_file("160.xlsx")
df_batch1 = load_excel_file("batch1.xlsx")
df_batch2 = load_excel_file("batch2.xlsx")
df_cpd = load_excel_file("CPD To 12-5-2026.xlsx")

# حساب أعداد السجلات الأساسية
c_training = len(df_training) if df_training is not None else 0
c_job = len(df_job) if df_job is not None else 0
c_cader = len(df_cader) if df_cader is not None else 0
c_reassign = len(df_reassign) if df_reassign is not None else 0
c_batch1 = len(df_batch1) if df_batch1 is not None else 0
c_batch2 = len(df_batch2) if df_batch2 is not None else 0

# دالة مطابقة واستخراج الإحصائيات بدقة تامة من عمود البرنامج وعمود النتيجة
def get_cpd_exact_stats(df, program_keyword):
    if df is not None:
        prog_col = None
        result_col = None
        
        for col in df.columns:
            col_str = str(col).strip()
            if "البرنامج" in col_str:
                prog_col = col
            elif "النتيجة" in col_str or "الحالة" in col_str:
                result_col = col
                
        if prog_col is None:
            prog_col = df.columns[4] if len(df.columns) > 4 else df.columns[-2]
        if result_col is None:
            result_col = df.columns[-1]
            
        sub_df = df[df[prog_col].astype(str).str.contains(program_keyword, case=False, na=False)]
        total = len(sub_df)
        
        if total == 0:
            return 0, 0, 0, 0
            
        res_series = sub_df[result_col].astype(str).str.strip()
        
        passed = len(sub_df[res_series.str.fullmatch("اجتياز", case=False, na=False) | res_series.str.contains("^اجتياز$", regex=True, na=False)])
        failed = len(sub_df[res_series.str.contains("عدم الاجتياز|عدم اجتياز", case=False, na=False)])
        absent = len(sub_df[res_series.str.contains("عدم الحضور|عدم حضور", case=False, na=False)])
        
        return total, passed, failed, absent
    return 0, 0, 0, 0

# حساب الإحصائيات الأربع الدقيقة لكل برنامج من منصة الوزارة
cpd_p1_total, cpd_p1_pass, cpd_p1_fail, cpd_p1_abs = get_cpd_exact_stats(df_cpd, "التطبيقات التربوية")
cpd_p2_total, cpd_p2_pass, cpd_p2_fail, cpd_p2_abs = get_cpd_exact_stats(df_cpd, "مدير/ وكيل إدارة مدرسية")
cpd_p3_total, cpd_p3_pass, cpd_p3_fail, cpd_p3_abs = get_cpd_exact_stats(df_cpd, "التوجيه الفنى")
cpd_p4_total, cpd_p4_pass, cpd_p4_fail, cpd_p4_abs = get_cpd_exact_stats(df_cpd, "إدارة تعليمية")

# حساب الإجمالي العام لجميع برامج منصة الوزارة
cpd_grand_total = cpd_p1_total + cpd_p2_total + cpd_p3_total + cpd_p4_total
cpd_grand_pass = cpd_p1_pass + cpd_p2_pass + cpd_p3_pass + cpd_p4_pass
cpd_grand_fail = cpd_p1_fail + cpd_p2_fail + cpd_p3_fail + cpd_p4_fail
cpd_grand_abs = cpd_p1_abs + cpd_p2_abs + cpd_p3_abs + cpd_p4_abs

# --- الأزرار الأفقية (Tabs) للتنقل المباشر ---
selected_section = st.tabs([
    "🏠 الرئيسية والبحث الشامل",
    "📁 معد البرامج",
    "📁 المسمى الوظيفي",
    "📁 التسكين علي الكادر",
    "📁 قرار 160",
    "📁 ملفات معلم مساعد الدفعة 1",
    "📁 ملفات معلم مساعد الدفعة 2",
    "📁 منصة الوزارة CPD"
])

# 1. شاشة الرئيسية والمؤشرات العامة والبحث الشامل
with selected_section[0]:
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
        check_and_display(df_cpd, "برامج منصة الوزارة CPD")
        st.markdown("---")

    # البطاقات الإحصائية الملونة للبرامج الأساسية
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

    # تقسيم وتحليل بطاقات منصة الوزارة CPD بالتفصيل مع إضافة بطاقة الإجمالي العام في الأعلى
    st.markdown("### 📊 نتيجة منصة CPD حتي 12-5-2026 ")
    
    # بطاقة الإجمالي العام المجمعة
    st.markdown(f"""
        <div class="cpd-total-box">
            <div class="cpd-total-title">🌟 الإجمالي العام لجميع برامج منصة الوزارة CPD</div>
            <div class="cpd-stats">
                <div class="stat-item" style="color: #38bdf8;">إجمالي المتدربين<span>{cpd_grand_total}</span></div>
                <div class="stat-item" style="color: #4ade80;">إجمالي الاجتياز<span>{cpd_grand_pass}</span></div>
                <div class="stat-item" style="color: #f87171;">إجمالي عدم الاجتياز<span>{cpd_grand_fail}</span></div>
                <div class="stat-item" style="color: #fbbf24;">إجمالي عدم الحضور<span>{cpd_grand_abs}</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    cpd_col1, cpd_col2 = st.columns(2)
    with cpd_col1:
        st.markdown(f"""
            <div class="cpd-card-box">
                <div class="cpd-title">📚 التطبيقات التربوية للمعلم المساعد 2026/2025</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p1_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p1_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p1_fail}</span></div>
                    <div class="stat-item" style="color: #fbbf24;">عدم حضور<span>{cpd_p1_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="cpd-card-box">
                <div class="cpd-title">👔 تدريب القيادات / التوجيه الفنى 2026/2025</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p3_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p3_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p3_fail}</span></div>
                    <div class="stat-item" style="color: #fbbf24;">عدم حضور<span>{cpd_p3_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with cpd_col2:
        st.markdown(f"""
            <div class="cpd-card-box">
                <div class="cpd-title">🏫 تدريب القيادات مدير/ وكيل إدارة مدرسية 2026/2025</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p2_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p2_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p2_fail}</span></div>
                    <div class="stat-item" style="color: #fbbf24;">عدم حضور<span>{cpd_p2_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="cpd-card-box">
                <div class="cpd-title">🏢 تدريب القيادات مدير/ وكيل إدارة تعليمية 2026/2025</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p4_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p4_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p4_fail}</span></div>
                    <div class="stat-item" style="color: #fbbf24;">عدم حضور<span>{cpd_p4_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # الرسوم البيانية الشاملة
    st.markdown("### 📈 التحليل البصري ومقارنة أعداد السجلات للبرامج")
    chart_data = pd.DataFrame({
        "البرنامج": ["معد البرامج", "المسمى الوظيفي", "التسكين", "قرار 160", "معلم مساعد 1", "معلم مساعد 2", "منصة الوزارة CPD"],
        "عدد السجلات": [c_training, c_job, c_cader, c_reassign, c_batch1, c_batch2, (len(df_cpd) if df_cpd is not None else 0)]
    })

    chart = alt.Chart(chart_data).mark_bar(color="#3b82f6", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("البرنامج:N", sort=None, title="", axis=alt.Axis(labelAngle=0, labelFontSize=11)),
        y=alt.Y("عدد السجلات:Q", title="إجمالي السجلات"),
        tooltip=["البرنامج", "عدد السجلات"]
    ).properties(height=320)

    st.altair_chart(chart, use_container_width=True)

# دالة عرض الأقسام التفصيلية داخل التبويبات بدون أي قيود على التنزيل
def render_section(title, df, tab_index):
    with selected_section[tab_index]:
        st.markdown(f'<p class="program-header">📁 {title}</p>', unsafe_allow_html=True)
        if df is not None:
            st.metric(label=f"إجمالي السجلات في هذا الكشف", value=len(df))
            search_query = st.text_input(f"🔍 بحث مخصص داخل كشف {title}:", key=f"search_{title}")
            display_df = df
            if search_query:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
                display_df = df[mask]
                st.info(f"عدد النتائج المطابقة للبحث: {len(display_df)}")
            
            # عرض الجدول مع أزرار التنزيل الافتراضية المتاحة للجميع
            st.dataframe(display_df, use_container_width=True)
        else:
            st.error(f"تعذر العثور على ملف الإكسل الخاص بـ '{title}'. تأكد من رفع الملف في المستودع.")

# عرض محتوى كل تبويب تفصيلي
render_section("معد البرامج التدريبية", df_training, 1)
render_section("المسمى الوظيفي", df_job, 2)
render_section("التسكين علي الكادر", df_cader, 3)
render_section("إعادة التعيين (قرار 160)", df_reassign, 4)
render_section("معلم مساعد الدفعة الأولى", df_batch1, 5)
render_section("معلم مساعد الدفعة الثانية", df_batch2, 6)
render_section("نتيجة برامج منصة الوزارة CPD", df_cpd, 7)

# --- تذييل الصفحة (Footer) ---
st.markdown("""
    <style>
    .footer {
        text-align: center;
        padding: 15px;
        margin-top: 30px;
        border-top: 1px solid #e2e8f0;
        color: #475569;
        font-size: 14px;
        font-weight: bold;
        background-color: #f8fafc;
        border-radius: 8px;
    }
    </style>
    <div class="footer">
        تصميم وتنفيذ: <span style="color: #2563eb;">أحمد الجنزوري</span> 🌟
    </div>
""", unsafe_allow_html=True)
