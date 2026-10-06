import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Smart Flying Star Pro", page_icon="🧭", layout="centered")

# ==========================================
# ១. ក្បួនតក្កវិជ្ជាគណនាហុងស៊ុយ (២៤ ភ្នំ)
# ==========================================
SECTORS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
SECTOR_NAMES = ['ជើង (N)', 'ជើងកើត (NE)', 'កើត (E)', 'ត្បូងកើត (SE)', 'ត្បូង (S)', 'ត្បូងលិច (SW)', 'លិច (W)', 'ជើងលិច (NW)']
GUAS = [1, 8, 3, 4, 9, 2, 7, 6]
PATH = ['C', 'NW', 'W', 'NE', 'S', 'N', 'SW', 'E', 'SE']
NAMES_DICT = {'SE': 'ត្បូងកើត (SE)', 'S': 'ត្បូង (S)', 'SW': 'ត្បូងលិច (SW)', 'E': 'កើត (E)', 'C': 'កណ្តាល (C)', 'W': 'លិច (W)', 'NE': 'ជើងកើត (NE)', 'N': 'ជើង (N)', 'NW': 'ជើងលិច (NW)'}

POLARITY = {
    1: [1, -1, -1],  2: [-1, 1, 1],
    3: [1, -1, -1],  4: [-1, 1, 1],
    6: [-1, 1, 1],   7: [1, -1, -1],
    8: [-1, 1, 1],   9: [1, -1, -1]
}

def fly_stars(star, direction):
    chart = {}
    curr = star
    for pos in PATH:
        chart[pos] = curr
        curr += direction
        if curr > 9: curr = 1
        if curr < 1: curr = 9
    return chart

def calculate_flying_stars(period, degree):
    norm_deg = (degree + 22.5) % 360
    facing_idx = int(norm_deg // 45)
    sub_m_idx = int((norm_deg % 45) // 15)
    sitting_idx = (facing_idx + 4) % 8
    
    base_chart = fly_stars(period, 1)
    
    m_star = base_chart[SECTORS[sitting_idx]]
    m_gua = GUAS[sitting_idx] if m_star == 5 else m_star
    m_dir = POLARITY[m_gua][sub_m_idx]
    m_chart = fly_stars(m_star, m_dir)
    
    w_star = base_chart[SECTORS[facing_idx]]
    w_gua = GUAS[facing_idx] if w_star == 5 else w_star
    w_dir = POLARITY[w_gua][sub_m_idx]
    w_chart = fly_stars(w_star, w_dir)
    
    final_chart = {}
    for pos in PATH:
        final_chart[pos] = {'m': m_chart[pos], 'w': w_chart[pos], 'b': base_chart[pos]}
    return final_chart, SECTOR_NAMES[facing_idx]

# ==========================================
# ២. ប្រព័ន្ធទិន្នន័យ Cures & ការដោះស្រាយបញ្ហា (Trouble-shooting)
# ==========================================
def get_cure_visual(m, w):
    combo = f"{m}-{w}"
    
    svg_wulou = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='35' r='20' fill='#F5B041'/><circle cx='50' cy='70' r='28' fill='#F5B041'/><path d='M 45 15 C 45 5, 55 5, 55 15' stroke='#E67E22' stroke-width='4' fill='none'/></svg>"
    svg_water = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M50 10 C 20 40, 20 70, 50 90 C 80 70, 80 40, 50 10' fill='#3498DB'/><path d='M50 30 C 35 50, 35 70, 50 85 C 65 70, 65 50, 50 30' fill='#85C1E9'/></svg>"
    svg_mountain = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><polygon points='10,90 50,20 90,90' fill='#7F8C8D'/><polygon points='40,90 70,40 100,90' fill='#BDC3C7'/></svg>"
    svg_bamboo = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><rect x='35' y='10' width='12' height='80' rx='3' fill='#2ECC71'/><rect x='55' y='20' width='12' height='70' rx='3' fill='#27AE60'/><line x1='32' y1='35' x2='49' y2='35' stroke='#229954' stroke-width='3'/><line x1='32' y1='65' x2='49' y2='65' stroke='#229954' stroke-width='3'/><line x1='52' y1='50' x2='69' y2='50' stroke='#1E8449' stroke-width='3'/></svg>"
    svg_pottery = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M 30 30 C 0 60, 20 90, 50 90 C 80 90, 100 60, 70 30 Z' fill='#D35400'/><rect x='40' y='10' width='20' height='20' fill='#E67E22'/><ellipse cx='50' cy='10' rx='10' ry='5' fill='#BA4A00'/></svg>"
    svg_yinyang = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='50' r='45' fill='#FFF' stroke='#2C3E50' stroke-width='3'/><path d='M 50 5 A 45 45 0 0 0 50 95 A 22.5 22.5 0 0 0 50 50 A 22.5 22.5 0 0 1 50 5' fill='#2C3E50'/><circle cx='50' cy='27.5' r='6' fill='#FFF'/><circle cx='50' cy='72.5' r='6' fill='#2C3E50'/></svg>"

    if m == 5 or w == 5 or m == 2 or w == 2: return svg_wulou, "ឃ្លោកបន្សាប", "#c0392b"
    elif combo in ["9-7", "7-9"]: return svg_pottery, "ដីឥដ្ឋ/គ្រីស្តាល់", "#d35400"
    elif combo in ["1-6", "6-1"]: return svg_bamboo, "លោហៈ/រុក្ខជាតិ", "#2980b9"
    elif w == 9 and m == 9: return svg_water, "ទឹកផុស (ទាញលាភ)", "#e74c3c"
    elif w == 9: return svg_water, "ចលនាទឹក", "#e74c3c"
    elif m == 9: return svg_mountain, "វត្ថុថ្ម/ភ្នំ", "#e74c3c"
    elif w == 1: return svg_water, "ចលនាទឹក", "#27ae60"
    elif m == 1: return svg_mountain, "វត្ថុថ្ម/ភ្នំ", "#27ae60"
    elif m == 8 and w == 8: return svg_mountain, "រក្សាភាពស្ងៀមស្ងាត់", "#7f8c8d" 
    else: return svg_yinyang, "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d"

interpretations_p9 = {
    "9-9": "🌟 **មហាសំណាងទ្វេដងប្រចាំយុគ (Double 9):** ជាទីតាំងល្អឥតខ្ចោះបំផុតប្រចាំយុគទី៩។\n*   ✅ **ដំណោះស្រាយប្រើប្រាស់បន្ទប់:** បើចង់រករឿងលុយកាក់ គួរប្រើបន្ទប់នេះជាកន្លែងធ្វើការ កន្លែងប្រជុំ ឬទទួលភ្ញៀវ (ឲ្យមានចលនាចុះឡើង)។ បើចង់បានសុខភាពល្អ គួររៀបចំបន្ទប់នេះជាកន្លែងសម្រាក ឬអានសៀវភៅស្ងាត់ៗ។",
    "8-8": "⚠️ **ផ្កាយថយយុគ (Double 8):** អំណាចលុយកាក់បានថយចុះ។\n*   🛡️ **ដំណោះស្រាយប្រើប្រាស់បន្ទប់:** គួររក្សាលំនឹងដោយប្រើថ្ម។ បើជាបន្ទប់ដេកនៅប្រើបាន ព្រោះវាត្រូវការភាពស្ងប់ស្ងាត់ (Yin)។ តែបើជាកន្លែងរកស៊ី មិនសូវមានថាមពលអូសទាញខ្លាំងទៀតទេ។",
    "5-2": "⚠️ **មហាឧបទ្រព និងជំងឺ (៥ លឿង + ២ ខ្មៅ):** ជាទីតាំងគ្រោះថ្នាក់បំផុត។\n*   🛡 **ដំណោះស្រាយប្រើប្រាស់បន្ទប់ (Trouble-shooting):** បើមិនអាចជៀសវាងបាន ដាច់ខាតត្រូវបិទទ្វារទុកចោល កុំប្រើម៉ាស៊ីនត្រជាក់រំខាន ឬកុំធ្វើសកម្មភាពអ៊ូអរនៅទីនេះ។ រក្សាភាពស្ងាត់ជ្រងំបំផុត (Yin State) និងត្រូវព្យួរឃ្លោកស្ពាន់បន្សាប។",
    "2-5": "⚠️ **មហាឧបទ្រព និងជំងឺ (២ ខ្មៅ + ៥ លឿង):** ដូចគ្នានឹង 5-2 ដែរ។",
    "1-6": "🧠 **កំពូលបញ្ញា (១ ស + ៦ ស):** ថាមពលដ៏ប្រសើរបំផុតសម្រាប់ការសិក្សា។\n*   ✅ **ដំណោះស្រាយប្រើប្រាស់បន្ទប់:** រៀបចំជាបន្ទប់ធ្វើការ ឬបន្ទប់កូនចៅរៀនសូត្រ។ ប្រើសំឡេងតន្ត្រីស្រាលៗ ឬកណ្តឹងខ្យល់ដើម្បីដាស់ថាមពលបញ្ញា។",
    "6-1": "🧠 **កំពូលបញ្ញា (៦ ស + ១ ស):** ដូចគ្នានឹង 1-6 ដែរ។ ផ្តល់ផលល្អប្រសើរខ្លាំងដល់មុខតំណែង។",
    "9-7": "🔥 **ភ្លើងរលាយដែក (៩ ស្វាយ + ៧ ក្រហម):** ងាយរងបញ្ហាពាក្យសម្តី ឬចោរកម្ម។\n*   🛡️ **ដំណោះស្រាយ:** បើនៅទីនេះមានចលនាខ្លាំង ជម្លោះនឹងរឹតតែខ្លាំង។ ត្រូវប្រើ 'ធាតុដី' (កុលាលភាជន៍ ថ្មពណ៌លឿង) ធ្វើជាស្ពានផ្សះផ្សារ (ភ្លើងបង្កើតដី ដីបង្កើតមាស)។",
    "7-9": "🔥 **ភ្លើងរលាយដែក (៧ ក្រហម + ៩ ស្វាយ):** ដូចគ្នានឹង 9-7 ដែរ។"
}

def get_interpretation(m, w):
    combo = f"{m}-{w}"
    if combo in interpretations_p9: return interpretations_p9[combo]
    return "💡 **ថាមពលចម្រុះ:** ផ្កាយទឹក(ស្តាំ) តំណាងឲ្យលាភ ផ្កាយភ្នំ(ឆ្វេង) តំណាងឲ្យសុខភាព។\n*   👉 **ក្បួន Master:** បើចង់ទាញលាភ ត្រូវធ្វើសកម្មភាពមានចលនា (យ៉ាង)។ បើចង់បានសុខភាព ត្រូវរក្សាភាពស្ងប់ស្ងាត់ (យិន)។"

# ==========================================
# ៣. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #d35400;'>🧭 Smart Flying Star Pro</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>គណនា ២៤ ភ្នំ និងផ្តល់ដំណោះស្រាយកម្រិត Master (The 3 Factors & Trouble-shooting)</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1: period_input = st.number_input("🌟 យុគសាងសង់ផ្ទះ", min_value=1, max_value=9, value=8)
with col2: degree_input = st.number_input("🧭 អង្សាទិសមុខផ្ទះ", min_value=0.0, max_value=360.0, value=355.0, step=1.0)

st.markdown("### 📍 ការជ្រើសរើសទីតាំង (The 3 Factors)")
col3, col4, col5 = st.columns(3)
with col3: main_door_sector = st.selectbox("🚪 ទ្វារធំ", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=0)
with col4: bedroom_sector = st.selectbox("🛏️ បន្ទប់ដេក", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=1)
with col5: kitchen_sector = st.selectbox("🍳 ផ្ទះបាយ", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=2)


if st.button("🔮 គណនាទិសហុងស៊ុយ", use_container_width=True, type="primary"):
    final_chart, facing_name = calculate_flying_stars(period_input, degree_input)
    st.success(f"🏠 **ប្លង់ដើម: ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing_name} ({degree_input} ដឺក្រេ)**")
    
    st.markdown("### 🗺️ តារាងផ្កាយហោះ (Flying Star Chart)")
    
    order = ['SE', 'S', 'SW', 'E', 'C', 'W', 'NE', 'N', 'NW']
    grid_html = "<div style='display: grid; grid-template-columns: repeat(3, 1fr); max-width: 650px; margin: 0 auto; border: 3px solid #2c3e50; background-color: #bdc3c7; gap: 1px;'>"
    
    for pos in order:
        data = final_chart[pos]
        icon, text, color = get_cure_visual(data['m'], data['w'])
        grid_html += f"<div style='position: relative; height: 130px; background-color: #fcfcfc; padding: 5px;'><div style='position: absolute; top: 5px; left: 8px; color: #7f8c8d; font-weight: bold; font-size: 11px;'>{NAMES_DICT[pos]}</div><div style='position: absolute; top: 25px; left: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['m']}</div><div style='position: absolute; top: 25px; right: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['w']}</div><div style='position: absolute; bottom: 35px; left: 50%; transform: translateX(-50%); color: #e74c3c; font-weight: bold; font-size: 26px;'>{data['b']}</div><div style='position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; border-top: 1px dashed #ecf0f1; padding-top: 4px;'>{icon} <span style='font-size: 11px; font-weight: bold; color: {color}; margin-left: 5px;'>{text}</span></div></div>"
        
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # ==========================================
    # ៤. ការវិភាគ The 3 Factors & ការផ្តល់ដំណោះស្រាយ (Trouble-shooting)
    # ==========================================
    st.markdown("---")
    st.markdown("### 📋 ការវិភាគកត្តាសំខាន់ទាំង៣ និងដំណោះស្រាយ (The 3 Factors & Trouble-shooting)")
    
    tab1, tab2, tab3 = st.tabs(["🚪 ទ្វារធំ (Main Door)", "🛏️ បន្ទប់ដេក (Bedroom)", "🍳 ផ្ទះបាយ (Kitchen)"])
    
    # --- 1. ការវិភាគទ្វារធំ ---
    with tab1:
        door_w = final_chart[main_door_sector]['w']
        st.write(f"ទ្វារធំស្ថិតនៅទិស **{NAMES_DICT[main_door_sector]}** មានផ្កាយមុខផ្ទះលេខ **{door_w}**។ (ទ្វារជារបស់យ៉ាង ត្រូវកេះដាស់ដោយចលនា)")
        
        if door_w == 9:
            st.success("🌟 **អស្ចារ្យណាស់!** នេះជាផ្កាយលាភ (Wang Qi) យុគទី៩។ \n* **💡 ដំណោះស្រាយទាញលាភ:** ត្រូវបើកទ្វារនេះឲ្យបានញឹកញាប់ និងប្រើបន្ទប់តំបន់នេះជាកន្លែងទទួលភ្ញៀវ ឬធ្វើការ (សកម្មភាពយ៉ាង) ដើម្បីស្រូបយកលុយកាក់ពេញលេញ។")
        elif door_w == 1:
            st.info("🌱 **ទ្វារល្អ!** ជាផ្កាយអនាគត (Sheng Qi) ល្អសម្រាប់កេរ្តិ៍ឈ្មោះ។ \n* **💡 ដំណោះស្រាយទាញលាភ:** បើកទ្វារនេះជាប្រចាំ វាប្រៀបដូចជាការសន្សំទ្រព្យទុកសម្រាប់អនាគតអញ្ចឹង។")
        elif door_w == 8:
            st.warning("⚠️ **ថាមពលថយចុះ:** ផ្កាយ ៨ លែងជាស្តេចលាភទៀតហើយ។ \n* **💡 ដំណោះស្រាយ Trouble-shooting:** ទោះបីលែងសូវខ្លាំង តែវាមិនមែនជាផ្កាយគ្រោះថ្នាក់ទេ។ អាចប្រើប្រាស់បានធម្មតា គ្រាន់តែមិនរំពឹងលុយធំចូលតាមច្រកនេះ។")
        elif door_w in [2, 5]:
            st.error(f"❌ **គ្រោះថ្នាក់!** ទ្វារបើកចំផ្កាយជំងឺ និងឧបទ្រព។ \n* **💡 ដំណោះស្រាយ Trouble-shooting:** បើប្តូរទ្វារមិនបាន ដាច់ខាតត្រូវរក្សាទ្វារនេះឲ្យស្ងាត់បំផុតកុំសូវប្រើ (Yin state) និងត្រូវចងកណ្តឹងខ្យល់លោហៈ ៦ បំពង់នៅមាត់ទ្វារដើម្បីបន្សាបរាល់ពេលបើក។")
        elif door_w == 7:
            st.error("❌ **ប្រយ័ត្នចោរកម្ម!** ផ្កាយ ៧ បង្កហានិភ័យបាត់បង់លុយកាក់។ \n* **💡 ដំណោះស្រាយ:** ដាក់ថូទឹក ឬអាងទឹកស្ងៀមៗ (Yin Water) នៅក្បែរទ្វារ ដើម្បីឲ្យទឹកលាងសម្អាតជាតិលោហៈមុតស្រួចចេញ។")
        else:
            st.write(f"💡 ផ្កាយ {door_w} ជាផ្កាយធ្លាក់យុគ។ ត្រូវរក្សាទ្វារឲ្យស្អាត មានពន្លឺ និងសណ្តាប់ធ្នាប់។")

    # --- 2. ការវិភាគបន្ទប់ដេក ---
    with tab2:
        bed_m = final_chart[bedroom_sector]['m']
        st.write(f"បន្ទប់ដេកស្ថិតនៅទិស **{NAMES_DICT[bedroom_sector]}** មានផ្កាយភ្នំលេខ **{bed_m}**។ (ការគេងជារបស់យិន ត្រូវការភាពស្ងប់ស្ងាត់)")
        
        if bed_m in [2, 3, 5]:
            st.error(f"❌ **បម្រាមដាច់ខាត!** ផ្កាយលេខ {bed_m} បង្កជំងឺ និងជម្លោះ។ \n* **💡 ដំណោះស្រាយ Trouble-shooting:** ជម្រើសទី១: ដូរបន្ទប់។ ជម្រើសទី២: បើដូរមិនបាន ដាច់ខាតហាមតម្លើងទូរទស្សន៍ ឬម៉ាស៊ីនបំពងសំឡេងនៅទីនេះ។ ត្រូវធ្វើឲ្យបន្ទប់នេះស្ងាត់ជ្រងំ (Yin) ដើម្បីកុំឲ្យផ្កាយអាក្រក់ភ្ញាក់ឡើង។")
        elif bed_m == 9:
            st.success("🌟 **ល្អឥតខ្ចោះ!** ផ្កាយ ៩ (Wang Qi) ការពារសុខភាព និងគ្រួសារបានល្អណាស់។ \n* **💡 ដំណោះស្រាយ:** គ្រាន់តែគេង និងសម្រាកនៅទីនេះជាប្រចាំ គឺជាការទទួលបានថាមពលប្រកបដោយសិរីសួស្តីហើយ។")
        elif bed_m == 1:
            st.info("🌱 **ល្អប្រសើរ!** ផ្តល់ភាពស្ងប់ស្ងាត់ ស័ក្តិសមបំផុតសម្រាប់បន្ទប់ដេកកុមារ ឬអ្នកសិក្សា។")
        elif bed_m == 8:
            st.info("✅ **អាចទទួលយកបាន:** ទីតាំងនេះនៅតែផ្តល់ភាពស្ងប់ស្ងាត់ល្អសម្រាប់ការសម្រាក (Yin Activity)។")
        else:
            st.warning(f"⚠️ ផ្កាយលេខ {bed_m} មិនមែនជាទីតាំងដ៏ប្រសើរបំផុតទេ។ ត្រូវរក្សាភាពស្ងប់ស្ងាត់ (Yin) ជានិច្ច។")

    # --- 3. ការវិភាគផ្ទះបាយ ---
    with tab3:
        kit_w = final_chart[kitchen_sector]['w']
        kit_m = final_chart[kitchen_sector]['m']
        st.write(f"ផ្ទះបាយស្ថិតនៅទិស **{NAMES_DICT[kitchen_sector]}** មានផ្កាយមុខផ្ទះ **{kit_w}** និងផ្កាយភ្នំ **{kit_m}**។")
        
        if 2 in [kit_w, kit_m] or 5 in [kit_w, kit_m]:
            st.error("❌ **បម្រាមដាច់ខាត!** ភ្លើងចង្ក្រាននឹងដុតបញ្ឆេះផ្កាយជំងឺ និងឧបទ្រព។ \n* **💡 ដំណោះស្រាយ Trouble-shooting:** នេះជាទីតាំងអាក្រក់បំផុត គួរតែរើចង្ក្រានចេញ។ បើមិនអាចរើបាន ត្រូវដាក់វត្ថុលោហៈធ្ងន់ៗ (ដូចជាឆ្នាំងស្ពាន់ធំៗ) នៅក្បែរចង្ក្រានដើម្បីបន្សាប។")
        elif 7 in [kit_w, kit_m]:
            st.error("❌ **គ្រោះថ្នាក់អគ្គិភ័យ!** ផ្កាយ ៧ បូកនឹងភ្លើងចង្ក្រាន ងាយបង្កជាភ្លើងឆេះ ឬជម្លោះហិង្សា។ \n* **💡 ដំណោះស្រាយ:** រក្សាផ្ទះបាយឲ្យមានខ្យល់ចេញចូលល្អបំផុត និងជៀសវាងការតាំងកាំបិតស្រួចៗនៅខាងក្រៅ។")
        elif kit_w == 6:
            st.error("⚠️️ **ភ្លើងរលាយដែក!** លោហៈ (៦) ត្រូវឆេះរលាយដោយភ្លើង។ \n* **💡 ដំណោះស្រាយ:** ដាក់ថ្ម ឬរបស់ធ្វើពីដីឥដ្ឋនៅចន្លោះចង្ក្រាន ដើម្បីធ្វើជាស្ពានផ្សះផ្សារ (ភ្លើងបង្កើតដី ដីការពារលោហៈ)។")
        elif kit_w in [3, 4] or kit_m in [3, 4]:
            st.success(f"🔥 **ល្អ/ស័ក្តិសម!** ទីតាំងមានផ្កាយឈើ (៣ ឬ ៤)។ \n* **💡 ការបកស្រាយបញ្ចធាតុ:** ឈើបង្កើតភ្លើង! វាជួយគាំទ្រដល់ចង្ក្រានបាយបានយ៉ាងល្អ។")
        elif kit_w == 9:
            st.success("🌟 **ល្អឥតខ្ចោះ!** ផ្កាយ ៩ ជាធាតុភ្លើង ត្រូវនឹងធាតុផ្ទះបាយ ដែលជំរុញថាមពលយុគទី៩ ឲ្យកាន់តែខ្លាំងក្លា និងនាំភាពរុងរឿង។")
        else:
            st.info("✅ ទីតាំងនេះមានផ្កាយអព្យាក្រឹត អាចទទួលយកបានសម្រាប់ធ្វើផ្ទះបាយ។")

    # ==========================================
    # ៥. ផ្នែកវិភាគលម្អិតតាមបន្ទប់ (Detailed Room Analysis)
    # ==========================================
    st.markdown("---")
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយលម្អិតតាមទិស (Period 9 Analysis)")
    
    for pos in order:
        data = final_chart[pos]
        meaning = get_interpretation(data['m'], data['w'])
        with st.expander(f"📍 {NAMES_DICT[pos]} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]", expanded=False):
            st.markdown(meaning)
