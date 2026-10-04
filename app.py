import streamlit as st

# ១. កំណត់ទម្រង់ទំព័រ (Mobile Friendly UI)
st.set_page_config(page_title="Smart Flying Star", page_icon="🧭", layout="centered")

# ២. ក្បួនតក្កវិជ្ជាហុងស៊ុយ (Feng Shui Logic)
class SmartFlyingStar:
    def __init__(self, period, degree):
        self.period = period
        self.degree = degree
        self.flight_path = ['C', 'NW', 'W', 'NE', 'S', 'N', 'SW', 'E', 'SE']
        self.base_chart = {}
        
    def calculate_base_chart(self):
        current_star = self.period
        for sector in self.flight_path:
            self.base_chart[sector] = current_star
            current_star = current_star + 1 if current_star < 9 else 1
            
    def determine_facing(self):
        if 337.5 <= self.degree or self.degree < 22.5: return 'ជើង (N)'
        elif 22.5 <= self.degree < 67.5: return 'ជើងកើត (NE)'
        elif 67.5 <= self.degree < 112.5: return 'កើត (E)'
        elif 112.5 <= self.degree < 157.5: return 'ត្បូងកើត (SE)'
        elif 157.5 <= self.degree < 202.5: return 'ត្បូង (S)'
        elif 202.5 <= self.degree < 247.5: return 'ត្បូងលិច (SW)'
        elif 247.5 <= self.degree < 292.5: return 'លិច (W)'
        elif 292.5 <= self.degree < 337.5: return 'ជើងលិច (NW)'

def analyze_sector(sector_name, mountain, water, base):
    combo = f"{mountain}-{water}"
    interpretations = {
        "8-8": "🌟 **Double 8 (រាជាលាភ):** ទីតាំងល្អឥតខ្ចោះសម្រាប់ការទាញយកទ្រព្យ។ ចលនាទឹក (ឡាបូ/ទ្វារ) នឹងដាស់លាភសំណាងបានយ៉ាងលឿន។",
        "1-6": "🧠 **បញ្ញា និង ជោគជ័យ (ទឹក-ដែក):** កំពូលថាមពលសម្រាប់ការសិក្សា កាត់ត និងការងារច្នៃប្រឌិត។ ស័ក្តិសមបំផុតសម្រាប់តុធ្វើការ។",
        "5-2": "⚠️ **ផ្កាយជំងឺ និង ឧបទ្រព (ដី-ដី):** ទាមទារការបន្សាបជាដាច់ខាត។ ត្រូវប្រើធាតុដែក ដូចជាពណ៌ស ឬប្រផេះ ដើម្បីទប់ទល់។",
        "7-9": "🔥 **ភ្លើង និង ដែក (ប្រទាញប្រទង់):** ផ្កាយ ៩ ជាផ្កាយលាភយុគថ្មី តែត្រូវប្រយ័ត្នបញ្ហាពាក្យសម្តីដោយសារឥទ្ធិពលផ្កាយ ៧។",
        "9-7": "🔥 **ភ្លើង និង ដែក (ប្រទាញប្រទង់):** ផ្កាយ ៩ ជាផ្កាយលាភយុគថ្មី តែត្រូវប្រយ័ត្នបញ្ហាពាក្យសម្តីដោយសារឥទ្ធិពលផ្កាយ ៧។"
    }
    
    # ស្វែងរកអត្ថន័យបន្សំផ្កាយ
    meaning = interpretations.get(combo) or interpretations.get(f"{water}-{mountain}") or "🔮 ថាមពលចម្រុះ ទាមទារការពិនិត្យទម្រង់បរិស្ថាន (Form) បន្ថែម។"
    
    # បង្កើតជាប្រអប់ទម្លាក់ចុះ (Expander) ស្អាតៗ
    with st.expander(f"📍 ទិស{sector_name} [ ភ្នំ: {mountain} | ទឹក: {water} | គោល: {base} ]", expanded=True):
        st.markdown(meaning)

# ៣. ការរចនាផ្ទាំងបង្ហាញ (UI Setup)
st.markdown("<h2 style='text-align: center; color: #E67E22;'>🧭 Smart Flying Star</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>កម្មវិធីវិភាគហុងស៊ុយផ្កាយហោះផ្ទាល់ខ្លួនរបស់អ្នក</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1:
    period_input = st.number_input("🌟 បញ្ចូលលេខយុគ", min_value=1, max_value=9, value=8)
with col2:
    degree_input = st.number_input("🧭 ដឺក្រេមុខផ្ទះ", min_value=0.0, max_value=360.0, value=0.0, step=1.0)

# ប៊ូតុងគណនា
if st.button("🔮 ចាប់ផ្តើមគណនា", use_container_width=True, type="primary"):
    app = SmartFlyingStar(period=period_input, degree=degree_input)
    app.calculate_base_chart()
    facing = app.determine_facing()
    
    st.success(f"🏠 **ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing} ({degree_input} ជាក់ស្តែង)**")
    
    st.markdown("### 📊 លទ្ធផលវិភាគទីតាំងសំខាន់ៗ")
    
    # ទិន្នន័យ Mockup សម្រាប់ប្លង់ N2/S2 (បងអាចសរសេរក្បួនគណនាស្វ័យប្រវត្តិបន្ថែមនៅថ្ងៃក្រោយ)
    mock_mountain = {'W': 1, 'S': 3, 'N': 7}
    mock_water = {'W': 6, 'S': 8, 'N': 9}
    
    sectors = [
        ('លិច (W) - តុធ្វើការ', 'W'), 
        ('ត្បូង (S) - ឡាបូលាងចាន', 'S'), 
        ('ជើង (N) - ទ្វារមុខ', 'N')
    ]
    
    for name, code in sectors:
        analyze_sector(name, mock_mountain.get(code), mock_water.get(code), app.base_chart.get(code))
        
    st.info("💡 **គន្លឹះ:** សូមចុចប៊ូតុង Share នៅខាងក្រោម Safari រួចជ្រើសរើស **'Add to Home Screen'** ដើម្បីដំឡើងជា App!")
