import streamlit as st
import pandas as pd
from datetime import datetime
import io

# إعداد الصفحة لتكون بعرض عريض
st.set_page_config(page_title="لوحة البيانات المحمية بكلمة مرور", layout="wide")

# ==================== 1. تنسيقات الـ CSS (إخفاء زر التحميل الافتراضي فقط) ====================
st.markdown("""
    <style>
    /* إخفاء شريط الأدوات وزر التحميل الافتراضي العائم فوق الجداول والرسومات البيانية */
    [data-testid="stElementToolbar"],
    [data-testid="baseButton-header"],
    button[title*="Download"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 2. محتوى التطبيق والجداول الخاصة بك ====================
st.title("🛡️ لوحة البيانات المحمية بكلمة مرور للتحميل")
st.write("تم إخفاء أزرار التنزيل الافتراضية، وإلغاء العلامة المائية. ولتحميل البيانات، يرجى استخدام زر التحميل الآمن أدناه وإدخال كلمة المرور.")

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
# عرض الجدول (بدون زر التنزيل الافتراضي)
st.dataframe(df, use_container_width=True)

# ==================== 3. نظام التحميل الآمن بكلمة مرور ====================
st.markdown("---")
st.subheader("📥 منطقة التنزيل الآمن للبيانات")

# استخدام Session State لحفظ حالة نافذة إدخال كلمة المرور لكل جلسة
if "show_password_input" not in st.session_state:
    st.session_state.show_password_input = False

# زر يضغط عليه المستخدم لبدء عملية التنزيل
if st.button("تنزيل ملف البيانات (Excel)"):
    st.session_state.show_password_input = True

# إذا قام المستخدم بالضغط على زر التنزيل، تظهر خانة إدخال كلمة المرور
if st.session_state.show_password_input:
    entered_password = st.text_input("الرجاء إدخال كلمة مرور المدير/المسؤول للسماح بالتحميل:", type="password")
    
    if entered_password:
        # كلمة المرور المحددة (يمكنك تغييرها حسب رغبتك)
        CORRECT_PASSWORD = "Admin123SecurePassword"
        
        if entered_password == CORRECT_PASSWORD:
            st.success("كلمة المرور صحيحة! جاري تجهيز الملف للتحميل...")
            
            # تحويل جدول البيانات إلى ملف Excel في الذاكرة
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            
            # زر التحميل الفعلي يظهر فقط عند صحة كلمة المرور
            st.download_button(
                label="اضغط هنا لتأكيد تحميل الملف الآن",
                data=processed_data,
                file_name=f"Secure_Data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.")
