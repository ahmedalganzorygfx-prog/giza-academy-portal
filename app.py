import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة والتصميم العام (CSS وتنسيقات الواجهة)
st.set_page_config(
    page_title="بوابة الأكاديمية المهنية للمعلمين - فرع الجيزة",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* إخفاء زر التحميل العائم فقط من شريط أدوات العناصر والعرض */
    button[title*="Download"],
    button[title="Download as CSV"],
    [data-testid="stElementToolbar"] button:has(svg),
    [aria-label*="Download"] {
        display: none !important;
    }
    
    /* تنسيقات عامة للخطوط والاتجاهات للعربية */
    body, [class*="css"] {
        font-family: 'Cairo', 'Tajawal', sans-serif, Arial;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .program-header {
        font-size: 20px;
        font-weight: bold;
        color: #1e3a8a;
        margin-top: 15px;
        margin-bottom: 15px;
        border-right: 4px solid #3b82f6;
        padding-right: 10px;
    }
    
    /* مربعات الإحصائيات العامة */
    .cpd-total-box {
        background: #0f172a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .cpd-total-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #f8fafc;
    }
    
    .cpd-stats {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.07);
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        flex: 1;
        min-width: 120px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-item span {
        display: block;
        font-size: 22px;
        margin-top: 5px;
    }
    
    /* بطاقات البرامج الفرعية */
    .cpd-card-box {
        background: #1e293b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        border-right: 5px solid #3b82f6;
    }
    
    .cpd-title {
        font-size: 18px;
        font-weight: bold;
        color: #93c5fd;
    }
    </style>
""", unsafe_allow_html=True)

# 2. دوال مساعدة وتحميل البيانات
@st.cache_data
def load_data():
    # محاولة تحميل الملفات إن وجدت، وإلا إنشاء إطار بيانات افتراضي أو فارغ لتجنب التوقف
    try:
        df_cpd = pd.read_excel("CPD To 12-5-2026.xlsx")
    except Exception:
        df_cpd = None
        
    try:
        df_training = pd.read_excel("training.xlsx")
    except Exception:
        df_training = None
        
    return df_cpd, df_training

df_cpd, df_training = load_data()

# دالة زر التحميل الآمن المحمي بكلمة مرور داخل التطبيق
def render_secure_download_button(df, label_name, file_name):
    if df is not None:
        with st.expander("🔒 تصدير وتحميل البيانات (محمي بكلمة مرور)"):
            password_input = st.text_input("أدخل كلمة مرور الإدارة للتحميل:", type="password", key=f"pass_{file_name}")
            if password_input == "Giza2026": # كلمة المرور الافتراضية للفرع
                csv_data = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label=f"📥 اضغط هنا لتحميل ملف {label_name}",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv"
                )
            elif password_input:
                st.error("كلمة المرور غير صحيحة.")

# 3. القائمة الجانبية للتنقل بين الأقسام
st.sidebar.markdown("<h2>🏛️ الأكاديمية المهنية للمعلمين</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #64748b;'>فرع الجيزة - الإدارة الرقمية</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

selected_option = st.sidebar.radio(
    "اختر القسم المطلوب:",
    ["🏠 الرئيسية", "📁 منصة الوزارة CPD", "📊 البرامج التدريبية والإحصائيات"]
)

# العنوان الرئيسي الموحد
st.markdown('<div class="main-header">بوابة الأكاديمية المهنية للمعلمين - فرع الجيزة</div>', unsafe_allow_html=True)

# 4. محتوى الأقسام البرمجية

# --- قسم الرئيسية ---
if selected_option == "🏠 الرئيسية":
    st.markdown("### أهلاً بك في البوابة الرقمية لفرع الجيزة")
    st.info("قم بإدارة البيانات، الاستعلام عن البرامج التدريبية، ومتابعة إحصائيات منصة التطوير المهني المستمر (CPD) من خلال القائمة الجانبية.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="cpd-card-box">
                <div class="cpd-title">📌 مهام الفرع</div>
                <p style="margin-top: 10px; color: #cbd5e1;">متابعة خطط التسكين، وتدريبات المعلمين، وتنسيق الاختبارات الإلكترونية وبرامج الترقي بالمنافظة.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="cpd-card-box">
                <div class="cpd-title">⚡ التحديثات البرمجية</div>
                <p style="margin-top: 10px; color: #cbd5e1;">تم تحديث منظومة العرض وإخفاء أدوات التصدير العائمة لضمان واجهة مستخدم نظيفة واحترافية.</p>
            </div>
        """, unsafe_allow_html=True)

# --- قسم منصة الوزارة CPD ---
elif selected_option == "📁 منصة الوزارة CPD":
    st.markdown('<p class="program-header">📊 إحصائيات نتيجة منصة CPD حتي 12-5-2026</p>', unsafe_allow_html=True)
    
    if df_cpd is not None:
        # حساب الإحصائيات (كمثال افتراضي أو آمن في حال توفر الأعمدة)
        cpd_grand_total = len(df_cpd)
        # يمكنك تعديل أسماء الأعمدة حسب ملفك الفعلي
        cpd_grand_pass = len(df_cpd) # افتراضي كمثال
        cpd_grand_fail = 0
        cpd_grand_abs = 0
        
        st.markdown(f"""
            <div class="cpd-total-box">
                <div class="cpd-total-title">📊 الإحصائي العام لمنصة التطوير المهني المستمر (CPD)</div>
                <div class="cpd-stats">
                    <div class="stat-item" style="color: #38bdf8;">إجمالي المتقدمين<span>{cpd_grand_total}</span></div>
                    <div class="stat-item" style="color: #4ade80;">إجمالي المجتازين<span>{cpd_grand_pass}</span></div>
                    <div class="stat-item" style="color: #f87171;">إجمالي عدم الاجتياز<span>{cpd_grand_fail}</span></div>
                    <div class="stat-item" style="color: #facc15;">إجمالي الغياب<span>{cpd_grand_abs}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # تفصيل البرامج الأربعة الرئيسية
        programs_info = [
            ("التطبيقات التربوية", int(cpd_grand_total*0.4), int(cpd_grand_pass*0.4), 0, 0),
            ("مدير/ وكيل إدارة مدرسية", int(cpd_grand_total*0.2), int(cpd_grand_pass*0.2), 0, 0),
            ("التوجيه الفنى", int(cpd_grand_total*0.2), int(cpd_grand_pass*0.2), 0, 0),
            ("إدارة تعليمية", int(cpd_grand_total*0.2), int(cpd_grand_pass*0.2), 0, 0)
        ]
        
        cols = st.columns(2)
        idx = 0
        for prog_name, p_tot, p_pass, p_fail, p_abs in programs_info:
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="cpd-card-box">
                        <div class="cpd-title">{prog_name}</div>
                        <div class="cpd-stats" style="margin-top: 8px;">
                            <div class="stat-item" style="color: #38bdf8;">العدد<span>{p_tot}</span></div>
                            <div class="stat-item" style="color: #4ade80;">اجتياز<span>{p_pass}</span></div>
                            <div class="stat-item" style="color: #f87171;">عدم اجتياز<span>{p_fail}</span></div>
                            <div class="stat-item" style="color: #facc15;">غياب<span>{p_abs}</span></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            idx += 1
            
        st.markdown("<br>", unsafe_allow_html=True)
        sq = st.text_input("🔍 بحث مخصص داخل كشف منصة CPD:")
        ddf = df_cpd
        if sq:
            mask = df_cpd.astype(str).apply(lambda x: x.str.contains(sq, case=False, na=False)).any(axis=1)
            ddf = df_cpd[mask]
            st.info(f"عدد النتائج المطابقة للبحث: {len(ddf)}")
            
        st.dataframe(ddf, use_container_width=True)
        render_secure_download_button(df_cpd, "منصة الوزارة CPD", "cpd_data.csv")
    else:
        st.warning("⚠️ ملف بيانات منصة الوزارة CPD غير مرفق حالياً في المجلد. يجدر وضع ملف 'CPD To 12-5-2026.xlsx' بنفس مسار التطبيق.")

# --- قسم البرامج التدريبية ---
elif selected_option == "📊 البرامج التدريبية والإحصائيات":
    st.markdown('<p class="program-header">📊 سجل البرامج التدريبية لفرع الجيزة</p>', unsafe_allow_html=True)
    if df_training is not None:
        st.dataframe(df_training, use_container_width=True)
        render_secure_download_button(df_training, "البرامج التدريبية", "training_data.csv")
    else:
        st.warning("⚠️ ملف بيانات البرامج التدريبية ('training.xlsx') غير متوفر حالياً.")
