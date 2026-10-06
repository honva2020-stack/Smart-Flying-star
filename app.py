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
# ២. ប្រព័ន្ធទិន្នន័យ Cures & SVG Graphics HD
# ==========================================
def get_cure_visual(m, w):
    combo = f"{m}-{w}"
    
    # គំនូរ SVG បង្កប់កូដ (មិនបាត់រូបភាព ១០០%)
    svg_wulou = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='35' r='20' fill='#F5B041'/><circle cx='50' cy='70' r='28' fill='#F5B041'/><path d='M 45 15 C 45 5, 55 5, 55 15' stroke='#E67E22' stroke-width='4' fill='none'/></svg>"
    svg_water = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M50 10 C 20 40, 20 70, 50 90 C 80 70, 80 40, 50 10' fill='#3498DB'/><path d='M50 30 C 35 50, 35 70, 50 85 C 65 70, 65 50, 50 30' fill='#85C1E9'/></svg>"
    svg_mountain = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><polygon points='10,90 50,20 90,90' fill='#7F8C8D'/><polygon points='40,90 70,40 100,90' fill='#BDC3C7'/></svg>"
    svg_bamboo = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><rect x='35' y='10' width='12' height='80' rx='3' fill='#2ECC71'/><rect x='55' y='20' width='12' height='70' rx='3' fill='#27AE60'/><line x1='32' y1='35' x2='49' y2='35' stroke='#229954' stroke-width='3'/><line x1='32' y1='65' x2='49' y2='65' stroke='#229954' stroke-width='3'/><line x1='52' y1='50' x2='69' y2='50' stroke='#1E8449' stroke-width='3'/></svg>"
    svg_pottery = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M 30 30 C 0 60, 20 90, 50 90 C 80 90, 100 60, 70 30 Z' fill='#D35400'/><rect x='40' y='10' width='20' height='20' fill='#E67E22'/><ellipse cx='50' cy='10' rx='10' ry='5' fill='#BA4A00'/></svg>"
    svg_yinyang = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='50' r='45' fill='#FFF' stroke='#2C3E50' stroke-width='3'/><path d='M 50 5 A 45 45 0 0 0 50 95 A 22.5 22.5 0 0 0 50 50 A 22.5 22.5 0 0 1 50 5' fill='#2C3E50'/><circle cx='50' cy='27.5' r='6' fill='#FFF'/><circle cx='50' cy='72.5' r='6' fill='#2C3E50'/></svg>"

    # តក្កវិជ្ជាទូទៅសម្រាប់តារាង
    if m == 5 or w == 5 or m == 2 or w == 2:
        return svg_wulou, "ឃ្លោកស្ពាន់/លោហៈ", "#c0392b"
    elif combo in ["9-7", "7-9"]:
        return svg_pottery, "វត្ថុដីឥដ្ឋ/គ្រីស្តាល់", "#d35400"
    elif combo in ["1-6", "6-1"]:
        return svg_bamboo, "លោហៈ ឬ រុក្ខជាតិ", "#2980b9"
    elif w == 9 and m == 9:
        return svg_water, "ទឹកផុស (ទាញលាភយុគ៩)", "#e74c3c"
    elif w == 9: 
        return svg_water, "ចលនាទឹក (Water)", "#e74c3c"
    elif m == 9: 
        return svg_mountain, "វត្ថុថ្ម/ភ្នំ (Mountain)", "#e74c3c"
    elif w == 1:
        return svg_water, "ចលនាទឹក (Water)", "#27ae60"
    elif m == 1:
        return svg_mountain, "វត្ថុថ្ម/ភ្នំ (Mountain)", "#27ae60"
    elif m == 8 and w == 8:
        return svg_mountain, "រក្សាភាពស្ងៀមស្ងាត់", "#7f8c8d" 
    else:
        return svg_yinyang, "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d"

# ==========================================
# ៣. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #d35400;'>🧭 Smart Flying Star Pro</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>គណនា ២៤ ភ្នំ និងវិភាគកត្តាទាំង៣ (The 3 Factors) សម្រាប់យុគទី៩</p>", unsafe_allow_html=True)
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
    
    # CSS Grid ១០០% គ្មានចន្លោះប្រហោង (Single Line)
    grid_html = "<div style='display: grid; grid-template-columns: repeat(3, 1fr); max-width: 650px; margin: 0 auto; border: 3px solid #2c3e50; background-color: #bdc3c7; gap: 1px;'>"
    
    for pos in order:
        data = final_chart[pos]
        icon, text, color = get_cure_visual(data['m'], data['w'])
        grid_html += f"<div style='position: relative; height: 130px; background-color: #fcfcfc; padding: 5px;'><div style='position: absolute; top: 5px; left: 8px; color: #7f8c8d; font-weight: bold; font-size: 11px;'>{NAMES_DICT[pos]}</div><div style='position: absolute; top: 25px; left: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['m']}</div><div style='position: absolute; top: 25px; right: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['w']}</div><div style='position: absolute; bottom: 35px; left: 50%; transform: translateX(-50%); color: #e74c3c; font-weight: bold; font-size: 26px;'>{data['b']}</div><div style='position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; border-top: 1px dashed #ecf0f1; padding-top: 4px;'>{icon} <span style='font-size: 11px; font-weight: bold; color: {color}; margin-left: 5px;'>{text}</span></div></div>"
        
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # ==========================================
    # ៤. ការវិភាគ The 3 Factors កម្រិត Master
    # ==========================================
    st.markdown("---")
    st.markdown("### 📋 ការវិភាគកត្តាសំខាន់ទាំង៣ (The 3 Factors Analysis)")
    
    tab1, tab2, tab3 = st.tabs(["🚪 ទ្វារធំ (Main Door)", "🛏️ បន្ទប់ដេក (Bedroom)", "🍳 ផ្ទះបាយ (Kitchen)"])
    
    # --- 1. ការវិភាគទ្វារធំ (ផ្តោតលើផ្កាយទឹក Facing Star) ---
    with tab1:
        door_w = final_chart[main_door_sector]['w']
        st.write(f"ទ្វារធំស្ថិតនៅទិស **{NAMES_DICT[main_door_sector]}** ដែលមានផ្កាយមុខផ្ទះ (Facing Star) លេខ **{door_w}**។ (ទ្វារជាតំបន់យ៉ាង ត្រូវមើលផ្កាយទឹក)")
        
        if door_w == 9:
            st.success("🌟 **អបអរសាទរ!** នេះជាផ្កាយលាភ (Wang Qi) ប្រចាំយុគទី៩។ វាជាមាត់ច្រកស្រូបទាញលុយកាក់ដ៏អស្ចារ្យបំផុត។ \n* **វិធីរៀបចំ:** គួរមានទម្រង់យ៉ាងនៅខាងក្រៅ និងដាក់ទឹកផុសខាងក្នុងដើម្បីដាស់ថាមពល។")
        elif door_w == 1:
            st.info("🌱 **ល្អប្រសើរ!** នេះជាផ្កាយអនាគត (Sheng Qi) ល្អសម្រាប់ការកសាងកេរ្តិ៍ឈ្មោះ និងចំណូលរយៈពេលវែង។")
        elif door_w == 8:
            st.warning("⚠️ **ចំណាំ:** ផ្កាយ ៨ ធ្លាប់ជាផ្កាយលាភក្នុងយុគមុន តែបច្ចុប្បន្នបានថយអំណាចហើយ។ គួរប្រើថ្មរក្សាលំនឹង។")
        elif door_w in [2, 5]:
            st.error(f"❌ **គ្រោះថ្នាក់!** ទ្វារបើកចំផ្កាយ {door_w} ដែលជាផ្កាយមហាឧបទ្រព និងជំងឺ។ \n* **វិធីបន្សាប:** ត្រូវព្យួរកណ្តឹងខ្យល់លោហៈ ៦បំពង់ ឬឃ្លោកស្ពាន់ ដាច់ខាត។")
        elif door_w == 7:
            st.error("❌ **ប្រយ័ត្ន!** ផ្កាយ ៧ បង្កហានិភ័យចោរកម្ម និងរឿងអាស្រូវ។ ប្រើទឹកស្ងៀមដើម្បីបន្សាប។")
        else:
            st.write(f"💡 ផ្កាយលេខ {door_w} ជាផ្កាយធ្លាក់យុគ។ គួរប្រើពន្លឺបំភ្លឺឲ្យបានល្អ និងរក្សាភាពស្អាត។")

    # --- 2. ការវិភាគបន្ទប់ដេក (ផ្តោតលើផ្កាយភ្នំ Sitting Star & បម្រាម) ---
    with tab2:
        bed_m = final_chart[bedroom_sector]['m']
        st.write(f"បន្ទប់ដេកស្ថិតនៅទិស **{NAMES_DICT[bedroom_sector]}** ដែលមានផ្កាយភ្នំ (Sitting Star) លេខ **{bed_m}**។ (បន្ទប់ដេកជាតំបន់យិន ត្រូវមើលផ្កាយភ្នំ)")
        
        if bed_m in [2, 3, 5]:
            st.error(f"❌ **បម្រាមដាច់ខាត!** ផ្កាយលេខ {bed_m} គឺជាផ្កាយអវិជ្ជមានដែលហាមប្រាមបំផុតសម្រាប់បន្ទប់ដេក។ វាអាចបង្កជំងឺធ្ងន់ធ្ងរ ឬជម្លោះក្នុងគ្រួសារយ៉ាងខ្លាំង។ \n* **វិធីដោះស្រាយ:** គួរតែប្តូរបន្ទប់ដេកទៅទិសផ្សេង ប្រសិនបើអាច។")
        elif bed_m == 9:
            st.success("🌟 **ល្អឥតខ្ចោះ!** ផ្កាយ ៩ (Wang Qi) ផ្តល់សុខភាព និងភាពសុខដុមរមនាយ៉ាងខ្លាំង។ \n* **ការគាំទ្រ:** គួរតែមានទម្រង់យិន (ដីខ្ពស់/ភ្នំ) នៅខាងក្រៅផ្ទះដើម្បីជួយគាំទ្រ។")
        elif bed_m == 1:
            st.info("🌱 **ល្អប្រសើរ!** ផ្កាយអនាគត (Sheng Qi) ផ្តល់ភាពស្ងប់ស្ងាត់ និងសុខភាពល្អ។")
        elif bed_m == 8:
            st.info("✅ **អាចទទួលយកបាន:** ផ្កាយ ៨ ទោះបីថយយុគ តែក៏ជាទីតាំងល្អសម្រាប់ការសម្រាក និងរក្សាលំនឹងសុខភាព។")
        else:
            st.warning(f"⚠️ ផ្កាយលេខ {bed_m} មិនមែនជាផ្កាយអំណោយផលសម្រាប់បន្ទប់ដេកទេ។ ត្រូវរក្សាភាពស្ងប់ស្ងាត់។")

    # --- 3. ការវិភាគផ្ទះបាយ (ក្បួនបញ្ចធាតុ និងបម្រាមតឹងរ៉ឹង) ---
    with tab3:
        kit_w = final_chart[kitchen_sector]['w']
        kit_m = final_chart[kitchen_sector]['m']
        st.write(f"ផ្ទះបាយស្ថិតនៅទិស **{NAMES_DICT[kitchen_sector]}** មានផ្កាយមុខផ្ទះ **{kit_w}** និងផ្កាយភ្នំ **{kit_m}**។ (ផ្ទះបាយជាធាតុភ្លើង)")
        
        # ឆែកមើលគ្រោះថ្នាក់លាក់មុខ (Safety First ទាំង M និង W)
        if 2 in [kit_w, kit_m] or 5 in [kit_w, kit_m]:
            st.error("❌ **បម្រាមដាច់ខាត!** ផ្ទះបាយស្ថិតនៅទីតាំងដែលមានផ្កាយជំងឺ (២) ឬ មហាឧបទ្រព (៥)។ ថាមពលភ្លើងនៃចង្ក្រាននឹងទៅដុតបញ្ឆេះផ្កាយកាចសាហាវទាំងនេះឲ្យកាន់តែមានឥទ្ធិពល បង្កគ្រោះថ្នាក់ដល់អ្នកផ្ទះ។")
        elif 7 in [kit_w, kit_m]:
            st.error("❌ **គ្រោះថ្នាក់អគ្គិភ័យ!** ផ្កាយ ៧ តំណាងឲ្យការឆេះ និងចោរកម្ម។ មិនគួរមានផ្ទះបាយនៅទីនេះទេ។")
        elif kit_w == 6:
            st.error("⚠️ **ភ្លើងរលាយដែក!** ផ្កាយមុខផ្ទះលេខ ៦ ជាធាតុលោហៈ (Metal) ដែលត្រូវឆេះរលាយដោយធាតុភ្លើងរបស់ផ្ទះបាយ។ នេះមិនមែនជាទីតាំងល្អទេ។")
        elif kit_w in [3, 4] or kit_m in [3, 4]:
            st.success(f"🔥 **ល្អ/ស័ក្តិសម!** ទីតាំងនេះមានផ្កាយឈើ (លេខ ៣ ឬ ៤)។ តាមក្បួនបញ្ចធាតុ 'ឈើបង្កើតភ្លើង' ដែលជួយគាំទ្រដល់ចង្ក្រានបាយបានយ៉ាងល្អ។")
        elif kit_w == 9:
            st.success("🌟 **ល្អឥតខ្ចោះ!** ផ្កាយមុខផ្ទះលេខ ៩ ជាធាតុភ្លើង ត្រូវនឹងធាតុផ្ទះបាយ ដែលជំរុញថាមពលយុគទី៩ ឲ្យកាន់តែខ្លាំងក្លា។")
        else:
            st.info("✅ ទីតាំងនេះមានផ្កាយអព្យាក្រឹត អាចទទួលយកបានសម្រាប់ធ្វើផ្ទះបាយឲ្យតែរក្សាបានភាពស្អាតបាត។")
