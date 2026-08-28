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

# تخصيص واجهة المستخدم وتصغير العناوين والبطاقات وحل مشكلة القائمة الجانبية تماماً
st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    h3, .stMarkdown h3 {
        direction: rtl !important;
        text-align: right !important;
        font-size: 16px !important;
    }
    
    /* حل جذري لمشكلة القائمة الجانبية: إخفاء النصوص تماماً عند تصغيرها لتجنب الحروف العمودية */
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 0px !important;
        min-width: 0px !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"] span, 
    [data-testid="stSidebar"][aria-expanded="false"] p,
    [data-testid="stSidebar"][aria-expanded="false"] label,
    [data-testid="stSidebar"][aria-expanded="false"] div {
        display: none !important;
    }

    /* تصميم الهيدر المركزي المتكامل بتشغيل مساحة أصغر */
    .app-header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px 15px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        border: 1px solid #334155;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .app-logo-img {
        width: 130px !important;
        min-width: 130px !important;
        max-width: 130px !important;
        height: auto !important;
        border-radius: 10px;
        object-fit: contain;
        background: rgba(255, 255, 255, 0.05);
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 12px;
    }
    .app-main-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        margin: 0 0 6px 0 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        line-height: 1.2;
        text-align: center;
    }
    .app-sub-title {
        font-size: 14px !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
        margin: 0 !important;
        text-align: center;
    }

    /* تصغير البطاقات الإحصائية لتوفير مساحة أوسع */
    .metric-card-1 { background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-2 { background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-3 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); padding: 10px; border-radius: 10px; color: #333; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-4 { background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-5 { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-6 { background: linear-gradient(135deg, #cb356b 0%, #bd3f32 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-7 { background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-8 { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    .metric-card-9 { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 10px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 3px 5px rgba(0,0,0,0.1); margin-bottom: 8px; }
    
    .cpd-card-box { background: #1e293b; border: 1px solid #334155; padding: 10px; border-radius: 10px; color: white; margin-bottom: 10px; box-shadow: 0 3px 5px rgba(0,0,0,0.15); }
    .cpd-total-box { background: linear-gradient(135deg, #0f172a 100%, #1e3a8a 0%); border: 1.5px solid #3b82f6; padding: 12px; border-radius: 10px; color: white; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .cpd-title { font-size: 13px; font-weight: bold; color: #38bdf8; margin-bottom: 6px; border-bottom: 1px solid #475569; padding-bottom: 4px; }
    .cpd-total-title { font-size: 14px; font-weight: bold; color: #facc15; margin-bottom: 8px; border-bottom: 1px solid #3b82f6; padding-bottom: 4px; text-align: center; }
    .cpd-stats { display: flex; justify-content: space-around; text-align: center; font-size: 12px; }
    .stat-item span { display: block; font-size: 14px; font-weight: bold; margin-top: 2px; }

    .card-title { font-size: 12px !important; font-weight: bold; margin-bottom: 3px; }
    .card-number { font-size: 18px; font-weight: bold; }
    .program-header { font-size: 16px !important; font-weight: bold; color: #1e293b; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin-top: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

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
    logo_display_html = '<div style="color: #f87171; font-size: 11px; margin-bottom: 8px;">⚠️ لم يتم العثور على الشعار</div>'

# عرض الهيدر الرئيسي المصغر والمدمج
st.markdown(f"""
    <div class="app-header-box">
        {logo_display_html}
        <div class="app-main-title">الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
        <div class="app-sub-title">بوابة الخدمات الرقمية وإدارة بيانات المعلمين المتكاملة</div>
    </div>
""", unsafe_allow_html=True)

# --- زر تحكم جانبي لرفع الملفات عند الحاجة ---
with st.sidebar:
    st.markdown("### ⚙️ إدارة وتحديث الملفات")
    st.info("إذا لم يتوفر الملف على السيرفر، يمكنك رفعه مباشرة هنا:")
    
    uploaded_file_override = st.file_uploader("رفع ملف إكسل عام أو بديل", type=["xlsx", "xls"])
    if uploaded_file_override is not None:
        st.success(f"تم تحميل الملف: {uploaded_file_override.name}")

# --- القائمة الرئيسية الأفقية تحت العنوان الرئيسي مباشرة ---
menu_options = [
    "🏠 الرئيسية والبحث الشامل",
    "📁 معد البرامج",
    "📁 اعتماد TOT",
    "📁 المسمى الوظيفي",
    "📁 التسكين علي الكادر",
    "📁 قرار 160",
    "📁 ملفات معلم مساعد الدفعة 1",
    "📁 ملفات معلم مساعد الدفعة 2",
    "📁 منصة الوزارة CPD"
]

selected_option = st.pills("🗂️ الانتقال السريع بين الأقسام:", menu_options, default=menu_options[0])
st.markdown("---")

# دالة لتحميل الملفات
def load_excel_file(filename):
    if uploaded_file_override is not None and uploaded_file_override.name == filename:
        try:
            df = pd.read_excel(uploaded_file_override)
            df.index = range(1, len(df) + 1)
            df.index.name = "م"
            return df
        except Exception:
            pass
            
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
df_tot = load_excel_file("Accrediation.xlsx")
df_job = load_excel_file("job.xlsx")
df_cader = load_excel_file("cader.xlsx")
df_reassign = load_excel_file("160.xlsx")
df_batch1 = load_excel_file("batch1.xlsx")
df_batch2 = load_excel_file("batch2.xlsx")
df_cpd = load_excel_file("CPD To 12-5-2026.xlsx")

# حساب أعداد السجلات الأساسية
c_training = len(df_training) if df_training is not None else 0
c_tot = len(df_tot) if df_tot is not None else 0
c_job = len(df_job) if df_job is not None else 0
c_cader = len(df_cader) if df_cader is not None else 0
c_reassign = len(df_reassign) if df_reassign is not None else 0
c_batch1 = len(df_batch1) if df_batch1 is not None else 0
c_batch2 = len(df_batch2) if df_batch2 is not None else 0
c_cpd = len(df_cpd) if df_cpd is not None else 0

# دالة عرض الجدول والبيانات مع زر التصدير (Export)
def display_batch_stats_and_table(df, batch_title, has_specs=True, spec_keyword="التخصص علي الكادر"):
    if df is not None:
        total_records = len(df)
        spec_col = None
        admin_col = None
        
        for col in df.columns:
            col_s = str(col).strip()
            if has_specs and ("التخصص علي الكادر" in col_s or "التخصص على الكادر" in col_s or (col_s == spec_keyword)):
                spec_col = col
                break
        
        if has_specs and spec_col is None:
            for col in df.columns:
                col_s = str(col).strip()
                if "تخصص" in col_s and "مؤهل" not in col_s and "المؤهل" not in col_s:
                    spec_col = col
                    break

        for col in df.columns:
            col_s = str(col).strip()
            if "الادارة" in col_s or "الإدارة" in col_s:
                admin_col = col
                break

        spec_counts = df[spec_col].astype(str).str.strip().value_counts() if (has_specs and spec_col is not None) else pd.Series(dtype=int)
        admin_counts = df[admin_col].astype(str).str.strip().value_counts() if admin_col is not None else pd.Series(dtype=int)

        stats_html = f'<div class="stat-item" style="color: #38bdf8; font-size: 14px;">الإجمالي العام<span>{total_records}</span></div>'
        if has_specs:
            stats_html += f'<div class="stat-item" style="color: #4ade80; font-size: 14px;">عدد التخصصات<span>{len(spec_counts)}</span></div>'
        stats_html += f'<div class="stat-item" style="color: #facc15; font-size: 14px;">عدد الإدارات<span>{len(admin_counts)}</span></div>'

        st.markdown(f"""
            <div class="cpd-total-box">
                <div class="cpd-total-title">📊 إحصائيات {batch_title}</div>
                <div class="cpd-stats">
                    {stats_html}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if has_specs and not spec_counts.empty:
            st.markdown(f"### 📋 تفصيل أعداد المعلمين بكل تخصص:")
            spec_cols = st.columns(3)
            idx = 0
            for spec_name, spec_count in spec_counts.items():
                with spec_cols[idx % 3]:
                    st.markdown(f"""
                        <div class="cpd-card-box">
                            <div class="cpd-title">{spec_name}</div>
                            <div style="text-align: center; font-size: 16px; font-weight: bold; color: #4ade80; margin-top: 3px;">{spec_count}</div>
                        </div>
                    """, unsafe_allow_html=True)
                idx += 1
            st.markdown("<br>", unsafe_allow_html=True)

        if not admin_counts.empty:
            st.markdown("### 🏫 تفصيل أعداد المعلمين بكل إدارة تعليمية:")
            admin_cols = st.columns(3)
            idx = 0
            for admin_name, admin_count in admin_counts.items():
                with admin_cols[idx % 3]:
                    st.markdown(f"""
                        <div class="cpd-card-box">
                            <div class="cpd-title" style="color: #facc15;">إدارة {admin_name}</div>
                            <div style="text-align: center; font-size: 16px; font-weight: bold; color: #38bdf8; margin-top: 3px;">{admin_count}</div>
                        </div>
                    """, unsafe_allow_html=True)
                idx += 1
            st.markdown("<br>", unsafe_allow_html=True)
        
        sq = st.text_input(f"🔍 بحث مخصص داخل كشف {batch_title}:", key=f"search_{batch_title}")
        ddf = df
        if sq:
            mask = df.astype(str).apply(lambda x: x.str.contains(sq, case=False, na=False)).any(axis=1)
            ddf = df[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(ddf)}")
        
        csv_data = ddf.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=f"📥 تصدير النتائج الحالية لملف CSV ({len(ddf)} سجل)",
            data=csv_data,
            file_name=f"{batch_title}_export.csv",
            mime="text/csv",
        )
        
        st.dataframe(ddf, use_container_width=True)
    else:
        st.error(f"ملف بيانات {batch_title} غير متوفر. يمكنك رفعه من القائمة الجانبية.")

# دالة استخراج إحصائيات منصة الوزارة CPD
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

cpd_p1_total, cpd_p1_pass, cpd_p1_fail, cpd_p1_abs = get_cpd_exact_stats(df_cpd, "التطبيقات التربوية")
cpd_p2_total, cpd_p2_pass, cpd_p2_fail, cpd_p2_abs = get_cpd_exact_stats(df_cpd, "مدير/ وكيل إدارة مدرسية")
cpd_p3_total, cpd_p3_pass, cpd_p3_fail, cpd_p3_abs = get_cpd_exact_stats(df_cpd, "التوجيه الفنى")
cpd_p4_total, cpd_p4_pass, cpd_p4_fail, cpd_p4_abs = get_cpd_exact_stats(df_cpd, "إدارة تعليمية")

cpd_grand_total = cpd_p1_total + cpd_p2_total + cpd_p3_total + cpd_p4_total
cpd_grand_pass = cpd_p1_pass + cpd_p2_pass + cpd_p3_pass + cpd_p4_pass
cpd_grand_fail = cpd_p1_fail + cpd_p2_fail + cpd_p3_fail + cpd_p4_fail
cpd_grand_abs = cpd_p1_abs + cpd_p2_abs + cpd_p3_abs + cpd_p4_abs

# 1. شاشة الرئيسية والبحث الشامل
if selected_option == "🏠 الرئيسية والبحث الشامل":
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
        check_and_display(df_tot, "اعتماد TOT")
        check_and_display(df_job, "المسمى الوظيفي")
        check_and_display(df_cader, "التسكين علي الكادر")
        check_and_display(df_reassign, "إعادة التعيين (قرار 160)")
        check_and_display(df_batch1, "معلم مساعد الدفعة الأولى")
        check_and_display(df_batch2, "معلم مساعد الدفعة الثانية")
        check_and_display(df_cpd, "برامج منصة الوزارة CPD")
        st.markdown("---")

    # البطاقات الإحصائية المصغرة والمدمجة
    st.markdown("### 📌 مؤشرات الإحصاء العامة لبرامج الفرع")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="metric-card-1"><div class="card-title">معد البرامج التدريبية</div><div class="card-number">{c_training}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-7"><div class="card-title">اعتماد TOT</div><div class="card-number">{c_tot}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-8"><div class="card-title">منصة الوزارة CPD</div><div class="card-number">{c_cpd}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card-2"><div class="card-title">المسمى الوظيفي</div><div class="card-number">{c_job}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-5"><div class="card-title">معلم مساعد (الدفعة الأولى)</div><div class="card-number">{c_batch1}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-9"><div class="card-title">إعادة التعيين (قرار 160)</div><div class="card-number">{c_reassign}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card-3"><div class="card-title">التسكين علي الكادر</div><div class="card-number">{c_cader}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card-6"><div class="card-title">معلم مساعد (الدفعة الثانية)</div><div class="card-number">{c_batch2}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # تحضير بيانات الرسوم البيانية للأعمدة فقط
    chart_data = pd.DataFrame({
        "البرنامج": ["معد البرامج", "اعتماد TOT", "المسمى الوظيفي", "التسكين", "قرار 160", "معلم مساعد 1", "معلم مساعد 2", "منصة الوزارة CPD"],
        "عدد السجلات": [c_training, c_tot, c_job, c_cader, c_reassign, c_batch1, c_batch2, c_cpd]
    })

    st.markdown("### 📊 مقارنة أعداد السجلات (الأعمدة البيانية)")
    bar_chart = alt.Chart(chart_data).mark_bar(color="#3b82f6", cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X("البرنامج:N", sort=None, title="", axis=alt.Axis(labelAngle=0, labelFontSize=11)),
        y=alt.Y("عدد السجلات:Q", title="إجمالي السجلات"),
        tooltip=["البرنامج", "عدد السجلات"]
    ).properties(height=300)
    
    st.altair_chart(bar_chart, use_container_width=True)

# 2. عرض قسم "معد البرامج التدريبية"
elif selected_option == "📁 معد البرامج":
    st.markdown('<p class="program-header">📁 معد البرامج التدريبية</p>', unsafe_allow_html=True)
    if df_training is not None:
        tr_total = len(df_training)
        tr_passed = 0
        tr_failed = 0
        
        accre_col = None
        for col in df_training.columns:
            if "حالة الاعتماد" in str(col).strip():
                accre_col = col
                break
        
        if accre_col is not None:
            accre_series = df_training[accre_col].astype(str).str.strip()
            tr_passed = len(df_training[accre_series.str.contains("اجتاز|بنجاح", case=False, na=False)])
            tr_failed = len(df_training[accre_series.str.contains("لم يجتاز|لم يعتمد|راسب|عدم", case=False, na=False)])
        
        st.markdown(f"""
            <div class="cpd-total-box">
                <div class="cpd-total-title">📊 إحصائيات اعتماد معد البرامج التدريبية</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{tr_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتاز الاعتماد بنجاح<span>{tr_passed}</span></div>
                    <div class="stat-item" style="color: #f87171;">لم يجتاز<span>{tr_failed}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        search_query = st.text_input("🔍 بحث مخصص داخل كشف معد البرامج التدريبية:")
        display_df = df_training
        if search_query:
            mask = df_training.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            display_df = df_training[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(display_df)}")
        
        csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير النتائج الحالية لملف CSV", data=csv_data, file_name="training_export.csv", mime="text/csv")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.error("تعذر العثور على ملف الإكسل الخاص بـ 'معد البرامج التدريبية' (training.xlsx).")

# 3. عرض قسم "اعتماد TOT"
elif selected_option == "📁 اعتماد TOT":
    st.markdown('<p class="program-header">📁 اعتماد TOT</p>', unsafe_allow_html=True)
    if df_tot is not None:
        tot_total = len(df_tot)
        
        spec_col = None
        for col in df_tot.columns:
            if "تخصص الاعتماد" in str(col).strip():
                spec_col = col
                break
        
        if spec_col is not None:
            spec_counts = df_tot[spec_col].astype(str).str.strip().value_counts()
            
            st.markdown(f"""
                <div class="cpd-total-box">
                    <div class="cpd-total-title">🌟 إحصائيات برنامج اعتماد TOT</div>
                    <div class="cpd-stats">
                        <div class="stat-item" style="color: #38bdf8; font-size: 14px;">إجمالي المتقدمين<span>{tot_total}</span></div>
                        <div class="stat-item" style="color: #4ade80; font-size: 14px;">عدد التخصصات<span>{len(spec_counts)}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📋 تفصيل أعداد المعلمين بكل تخصص:")
            spec_cols = st.columns(3)
            idx = 0
            for spec_name, spec_count in spec_counts.items():
                with spec_cols[idx % 3]:
                    st.markdown(f"""
                        <div class="cpd-card-box">
                            <div class="cpd-title">{spec_name}</div>
                            <div style="text-align: center; font-size: 16px; font-weight: bold; color: #4ade80; margin-top: 3px;">{spec_count}</div>
                        </div>
                    """, unsafe_allow_html=True)
                idx += 1
        else:
            st.warning("⚠️ لم يتم العثور على عمود 'تخصص الاعتماد' في ملف Accrediation.xlsx.")
            st.metric(label="إجمالي المتقدمين", value=tot_total)
        
        st.markdown("<br>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 بحث مخصص داخل كشف اعتماد TOT:")
        display_df = df_tot
        if search_query:
            mask = df_tot.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            display_df = df_tot[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(display_df)}")
        
        csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير النتائج الحالية لملف CSV", data=csv_data, file_name="tot_export.csv", mime="text/csv")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.error("تعذر العثور على ملف الإكسل الخاص بـ 'اعتماد TOT' (Accrediation.xlsx).")

# 4. عرض قسم "المسمى الوظيفي"
elif selected_option == "📁 المسمى الوظيفي":
    st.markdown('<p class="program-header">📁 المسمى الوظيفي</p>', unsafe_allow_html=True)
    if df_job is not None:
        job_total = len(df_job)
        giza_count = 0
        ext_count = 0
        
        branch_col = None
        admin_col = None
        
        for col in df_job.columns:
            col_s = str(col).strip()
            if "الفرع" in col_s:
                branch_col = col
            elif "الادارة" in col_s or "الإدارة" in col_s:
                admin_col = col
                
        if branch_col is not None:
            branch_series = df_job[branch_col].astype(str).str.strip()
            giza_count = len(df_job[branch_series.str.contains("الجيزة", case=False, na=False)])
            ext_count = job_total - giza_count
        elif admin_col is not None:
            admin_series = df_job[admin_col].astype(str).str.strip()
            giza_count = len(df_job[admin_series.str.contains("الجيزة", case=False, na=False)])
            ext_count = job_total - giza_count
        else:
            giza_count = job_total
            ext_count = 0

        st.markdown(f"""
            <div class="cpd-total-box">
                <div class="cpd-total-title">📊 إحصائيات برنامج المسمى الوظيفي</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{job_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">محافظة الجيزة<span>{giza_count}</span></div>
                    <div class="stat-item" style="color: #f87171;">خارج الجيزة<span>{ext_count}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        sq = st.text_input("🔍 بحث مخصص داخل كشف المسمى الوظيفي:")
        ddf = df_job
        if sq:
            mask = df_job.astype(str).apply(lambda x: x.str.contains(sq, case=False, na=False)).any(axis=1)
            ddf = df_job[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(ddf)}")
        
        csv_data = ddf.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير النتائج الحالية لملف CSV", data=csv_data, file_name="job_export.csv", mime="text/csv")
        st.dataframe(ddf, use_container_width=True)
    else:
        st.error("ملف المسمى الوظيفي (job.xlsx) غير متوفر.")

# بقية الأقسام الأخرى
elif selected_option == "📁 التسكين علي الكادر":
    st.markdown('<p class="program-header">📁 التسكين علي الكادر</p>', unsafe_allow_html=True)
    display_batch_stats_and_table(df_cader, "التسكين علي الكادر", has_specs=True, spec_keyword="التخصص علي الكادر")

elif selected_option == "📁 قرار 160":
    st.markdown('<p class="program-header">📁 إعادة التعيين (قرار 160)</p>', unsafe_allow_html=True)
    display_batch_stats_and_table(df_reassign, "إعادة التعيين (قرار 160)", has_specs=True, spec_keyword="التخصص علي الكادر")

elif selected_option == "📁 ملفات معلم مساعد الدفعة 1":
    st.markdown('<p class="program-header">📁 ملفات معلم مساعد الدفعة الأولى</p>', unsafe_allow_html=True)
    display_batch_stats_and_table(df_batch1, "معلم مساعد الدفعة الأولى", has_specs=True, spec_keyword="التخصص علي الكادر")

elif selected_option == "📁 ملفات معلم مساعد الدفعة 2":
    st.markdown('<p class="program-header">📁 ملفات معلم مساعد الدفعة الثانية</p>', unsafe_allow_html=True)
    display_batch_stats_and_table(df_batch2, "معلم مساعد الدفعة الثانية", has_specs=True, spec_keyword="التخصص علي الكادر")

elif selected_option == "📁 منصة الوزارة CPD":
    st.markdown('<p class="program-header">📊 إحصائيات نتيجة منصة CPD حتي 12-5-2026</p>', unsafe_allow_html=True)
    if df_cpd is not None:
        st.markdown(f"""
            <div class="cpd-total-box">
                <div class="cpd-total-title">🌟 الإجمالي العام لجميع برامج منصة الوزارة CPD</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_grand_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_grand_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_grand_fail}</span></div>
                    <div class="stat-item" style="color: #fbbf24;">غياب<span>{cpd_grand_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cpd_col1, cpd_col2 = st.columns(2)
        with cpd_col1:
            st.markdown(f"""
                <div class="cpd-card-box">
                    <div class="cpd-title">📚 التطبيقات التربوية للمعلم المساعد</div>
                    <div class="cpd-stats">
                        <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p1_total}</span></div>
                        <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p1_pass}</span></div>
                        <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p1_fail}</span></div>
                        <div class="stat-item" style="color: #fbbf24;">غياب<span>{cpd_p1_abs}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="cpd-card-box">
                    <div class="cpd-title">👔 القيادات / التوجيه الفنى</div>
                    <div class="cpd-stats">
                        <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p3_total}</span></div>
                        <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p3_pass}</span></div>
                        <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p3_fail}</span></div>
                        <div class="stat-item" style="color: #fbbf24;">غياب<span>{cpd_p3_abs}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with cpd_col2:
            st.markdown(f"""
                <div class="cpd-card-box">
                    <div class="cpd-title">🏫 مدير/ وكيل إدارة مدرسية</div>
                    <div class="cpd-stats">
                        <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p2_total}</span></div>
                        <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p2_pass}</span></div>
                        <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p2_fail}</span></div>
                        <div class="stat-item" style="color: #fbbf24;">غياب<span>{cpd_p2_abs}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="cpd-card-box">
                    <div class="cpd-title">🏢 مدير/ وكيل إدارة تعليمية</div>
                    <div class="cpd-stats">
                        <div class="stat-item" style="color: #38bdf8;">الإجمالي<span>{cpd_p4_total}</span></div>
                        <div class="stat-item" style="color: #4ade80;">اجتياز<span>{cpd_p4_pass}</span></div>
                        <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{cpd_p4_fail}</span>C</div>
                        <div class="stat-item" style="color: #fbbf24;">غياب<span>{cpd_p4_abs}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sq = st.text_input("🔍 بحث مخصص داخل كشف منصة الوزارة CPD:")
        ddf = df_cpd
        if sq:
            mask = df_cpd.astype(str).apply(lambda x: x.str.contains(sq, case=False, na=False)).any(axis=1)
            ddf = df_cpd[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(ddf)}")
        
        csv_data = ddf.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير النتائج الحالية لملف CSV", data=csv_data, file_name="cpd_export.csv", mime="text/csv")
        st.dataframe(ddf, use_container_width=True)
    else:
        st.error("ملف منصة الوزارة CPD غير متوفر.")

# --- تذييل الصفحة (Footer) ---
st.markdown("""
    <style>
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 20px;
        border-top: 1px solid #e2e8f0;
        color: #475569;
        font-size: 13px;
        font-weight: bold;
        background-color: #f8fafc;
        border-radius: 6px;
    }
    </style>
    <div class="footer">
        تصميم وتنفيذ: <span style="color: #2563eb;">أحمد الجنزوري مدير الفرع</span> 🌟
    </div>
""", unsafe_allow_html=True)
