import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 吉拉米代部落深度旅遊導覽",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (保留您優化的深色模式/白底黑字修復專區)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為粉色，字體為深色 (配合部落稻浪可微調為暖色系，此處保留原廠粉色設定) */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    
    /* 2. 強制所有一般文字元素為深色 */
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #333333 !important;
    }

    /* === 3. 核心修復：強制輸入框與選單在深色模式下維持「白底黑字」 === */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important; 
        border: 1px solid #cccccc !important;
        color: #333333 !important; 
    }
    
    input { color: #333333 !important; }
    div[data-baseweb="select"] span { color: #333333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #333333 !important; }
    svg { fill: #333333 !important; color: #333333 !important; }

    /* === 4. 特別加強：日期選單高亮 === */
    div[data-testid="stDateInput"] > label {
        color: #2E8B57 !important; /* 改為森林綠系以符合部落生態 */
        font-size: 24px !important;
        font-weight: 900 !important;
        text-shadow: 0px 0px 5px rgba(46, 139, 87, 0.4);
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 3px solid #3CB371 !important; 
        background-color: #F0FFF0 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(60, 179, 113, 0.3); 
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (改為部落風格的暖橘綠漸層) */
    .header-box {
        background: linear-gradient(135deg, #4CAF50 0%, #FF9800 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    
    /* 輸入卡片 */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #E8F5E9;
        margin-bottom: 20px;
    }
    
    /* 按鈕 */
    .stButton>button {
        width: 100%;
        background-color: #FF8C00;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
    }
    
    /* 資訊看板 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 時間軸 */
    .timeline-item {
        border-left: 3px solid #4CAF50;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '🌾';
        position: absolute;
        left: -13px;
        top: 0;
        background: #FFF0F5;
        border-radius: 50%;
    }
    .day-header {
        background: #E8F5E9;
        color: #2E8B57 !important;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #2E8B57 !important; font-size: 18px; }
    .spot-tag { 
        font-size: 12px; background: #FFF3E0; color: #E65100 !important; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 住宿卡片 */
    .hotel-card {
        background: #F8F8FF;
        border-left: 5px solid #20B2AA;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .hotel-tag {
        font-size: 11px;
        background: #20B2AA;
        color: white !important;
        padding: 2px 6px;
        border-radius: 8px;
        margin-right: 5px;
    }
    
    /* 景點名錄小卡 */
    .mini-card {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #eee;
        font-size: 14px;
        margin-bottom: 8px;
        border-left: 3px solid #FF9800;
    }
    .flower-badge {
        background: #4CAF50; color: white !important; padding: 1px 5px; border-radius: 4px; font-size: 11px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (吉拉米代部落與周邊資源)
# ==========================================
all_spots_db = [
    # --- 【核心】吉拉米代部落 (Cilamitay) ---
    {"name": "吉拉米代天空梯田", "region": "部落核心", "type": "網美景觀", "highlight": "世界百大綠色旅遊", "fee": "免門票", "desc": "海岸山脈下的百年有機梯田，不同季節有綠浪或黃金稻穗的絕美景觀。"},
    {"name": "百年水圳步道", "region": "部落核心", "type": "生態健行", "highlight": "文化遺產", "fee": "導覽需預約", "desc": "阿美族先民沿著懸崖峭壁手工開鑿的水圳，體驗部落先人的智慧與水資源巡禮。"},
    {"name": "富里小天祥 (鱉溪峽谷)", "region": "部落核心", "type": "自然秘境", "highlight": "峽谷奇岩", "fee": "免門票", "desc": "石門橋下由鱉溪切穿都巒山層形成的峽谷，岩壁陡峭，媲美太魯閣天祥。"},
    {"name": "部落廚房風味餐", "region": "部落核心", "type": "在地美食", "highlight": "阿美族料理", "fee": "需預約/付費", "desc": "使用在地有機米與野菜，品嚐最道地的阿美族傳統石頭火鍋與柴燒料理。"},
    {"name": "麻荖漏山 (新港山)", "region": "部落核心", "type": "重裝登山", "highlight": "海岸山脈最高峰", "fee": "免門票", "desc": "海拔1682公尺，適合有登山經驗的熱血山友，挑戰豐富林相與陡峭地形。"},

    # --- 【周邊】富里鄉與羅山 ---
    {"name": "羅山有機村", "region": "富里周邊", "type": "農村體驗", "highlight": "全台第一有機村", "fee": "免門票", "desc": "體驗泥火山豆腐DIY，漫步於無毒無農藥的純淨農村環境。"},
    {"name": "羅山泥火山與大瀑布", "region": "富里周邊", "type": "奇觀", "highlight": "地質生態", "fee": "免門票", "desc": "罕見的泥火山地貌，以及遠眺壯觀的羅山瀑布。"},
    {"name": "富里農會 (羅山展售中心)", "region": "富里周邊", "type": "採買伴手禮", "highlight": "富麗米", "fee": "免門票", "desc": "購買知名的富里有機米，品嚐富麗米便當與米蛋捲，一旁還有稻草藝術造景。"},
    {"name": "東里鐵馬驛站", "region": "富里周邊", "type": "單車漫遊", "highlight": "最美舊車站", "fee": "免門票", "desc": "玉富自行車道的起點，舊火車站改建，擁抱無邊際的田野與山脈風光。"},
    {"name": "六十石山", "region": "富里周邊", "type": "賞花景觀", "highlight": "金針花海/星空", "fee": "免門票", "desc": "8-9月金針花季，非花季時則是俯瞰花東縱谷與夜觀星空的頂級秘境。"},
    {"name": "明里菸樓", "region": "富里周邊", "type": "人文歷史", "highlight": "客家聚落", "fee": "免門票", "desc": "保存完整的日治時期大阪式菸樓，見證花東縱谷曾經的菸葉繁華。"},
    
    # --- 【體驗】原民手作與活動 ---
    {"name": "阿美族捕魚/狩獵體驗", "region": "部落體驗", "type": "深度文化", "highlight": "傳統技藝", "fee": "套裝行程付費", "desc": "跟著部落獵人學習陷阱製作，或在溪流體驗傳統八卦網撒網。"},
    {"name": "編織與手作體驗", "region": "部落體驗", "type": "手作", "highlight": "文創", "fee": "付費體驗", "desc": "使用月桃葉或打包帶，學習阿美族傳統編織技法，製作實用小籃子。"}
]

# 住宿資料庫
hotels_db = [
    {"name": "吉拉米代部落接待家庭", "region": "部落核心", "tag": "深度體驗", "price": 1200, "desc": "住進部落人家，體驗最真實的阿美族日常與熱情。"},
    {"name": "月荷塘民宿", "region": "富里周邊", "tag": "生態有機", "price": 2800, "desc": "位於羅山有機村，結合生態導覽與手作體驗的溫馨民宿。"},
    {"name": "磚窯居", "region": "富里周邊", "tag": "歷史特色", "price": 2500, "desc": "由老磚窯廠改建，具備濃厚懷舊風情與廣大庭院。"},
    {"name": "邊界花東", "region": "富里周邊", "tag": "縱谷景觀", "price": 3200, "desc": "優質設計風格，窗外就是綠油油的稻田與海岸山脈。"},
    {"name": "低調民宿", "region": "富里周邊", "tag": "隱私放鬆", "price": 3000, "desc": "遠離塵囂，適合想要徹底放空、看書看星空的旅人。"}
]

# ==========================================
# 4. 邏輯核心：動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(travel_date, days_str, group):
    # 根據季節給出不同主題
    m = travel_date.month
    if m in [8, 9]:
        status_title = "🌻 縱谷金針花與部落豐收季"
    elif m in [5, 6, 10, 11]:
        status_title = "🌾 天空梯田黃金稻浪大賞"
    else:
        status_title = "🌿 峽谷水圳與生態秘境探索"

    tribe_spots = [s for s in all_spots_db if s['region'] in ["部落核心", "部落體驗"]]
    surround_spots = [s for s in all_spots_db if s['region'] == "富里周邊"]
    
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # --- Day 1: 吉拉米代核心探索 ---
    d1_spot1 = next((s for s in tribe_spots if s['name'] == "百年水圳步道"), tribe_spots[0])
    d1_spot2 = next((s for s in tribe_spots if s['name'] == "吉拉米代天空梯田"), tribe_spots[1])
    
    # 午餐穿插部落風味餐
    food_spot = next((s for s in tribe_spots if s['name'] == "部落廚房風味餐"), None)
    if food_spot:
         itinerary[1] = [d1_spot1, food_spot, d1_spot2]
    else:
         itinerary[1] = [d1_spot1, d1_spot2]
    
    # --- Day 2: 縱谷生態與文化 ---
    if day_count >= 2:
        d2_spot1 = next((s for s in surround_spots if s['name'] == "羅山有機村"), surround_spots[0])
        d2_spot2 = next((s for s in tribe_spots if s['name'] == "富里小天祥 (鱉溪峽谷)"), tribe_spots[2])
        itinerary[2] = [d2_spot1, d2_spot2]

    # --- Day 3: 打卡與滿載而歸 ---
    if day_count == 3:
        # 花季去六十石山，非花季去鐵馬驛站
        if m in [8, 9, 10]:
            d3_spot1 = next((s for s in surround_spots if s['name'] == "六十石山"), surround_spots[2])
        else:
            d3_spot1 = next((s for s in surround_spots if s['name'] == "東里鐵馬驛站"), surround_spots[2])
            
        d3_spot2 = next((s for s in surround_spots if s['name'] == "富里農會 (羅山展售中心)"), surround_spots[3])
        itinerary[3] = [d3_spot1, d3_spot2]

    return status_title, itinerary

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌾 2026 吉拉米代部落深度導覽</div>
        <div class="header-subtitle">吉拉米代部落推廣協會 邀請您踏入山林 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # 日期選單
        travel_date = st.date_input("📅 預計到訪日期", value=date(2026, 5, 20))
    with col2:
        days_str = st.selectbox("🕒 停留天數", ["一日遊 (精華快閃)", "二日遊 (部落過夜)", "三日遊 (縱谷深度)"])
        group = st.selectbox("👥 出遊夥伴", ["情侶/夫妻", "親子生態團", "長輩漫遊", "熱血背包客"])
    
    if st.button("🚀 生成部落專屬行程"):
        st.session_state['generated'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generated'):
    status_title, itinerary = generate_dynamic_itinerary(travel_date, days_str, group)
    
    st.markdown(f"""
    <div class="info-box">
        <h4>{status_title}</h4>
        <p>為您規劃 <b>{travel_date.strftime('%Y/%m/%d')}</b> 出發的 <b>{group}</b> 專屬行程！(小提醒：部落導覽請提早預約)</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 顯示行程 ---
    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">Day {day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            # 簡單的時間標籤
            if i == 0: time_label = "☀️ 上午"
            elif i == 1 and len(spots) == 3: time_label = "🍲 中午"
            else: time_label = "🌤️ 下午"
            
            # 標籤生成
            tags_html = f'<span class="spot-tag">{spot["type"]}</span>'
            tags_html += f'<span class="spot-tag" style="background:#2E8B57;color:white!important;">{spot["highlight"]}</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{time_label}：{spot['name']}</div>
                <div style="margin: 5px 0;">{tags_html}</div>
                <div style="font-size: 14px; color: #555;">
                    💰 {spot['fee']} <br>
                    📝 {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 住宿推薦 (僅多日遊顯示) ---
    if "一日" not in days_str:
        st.markdown("### 🏨 縱谷與部落優質住宿推薦")
        
        rec_hotels = hotels_db
        # 隨機秀 3 間
        for h in random.sample(rec_hotels, min(3, len(rec_hotels))):
            st.markdown(f"""
            <div class="hotel-card">
                <div style="font-weight:bold; color:#006400;">{h['name']} <span class="hotel-tag">{h['tag']}</span></div>
                <div style="font-size:13px; color:#666; margin-top:3px;">
                    💲 預估單晚 {h['price']}起 | {h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 頁尾景點總覽 ---
with st.expander("📖 查看 吉拉米代與周邊 觀光資源名錄"):
    st.markdown("#### 花蓮富里南區觀光總覽")
    # 依區域分類顯示
    for region in ["部落核心", "富里周邊", "部落體驗"]:
        st.markdown(f"**【{region}】**")
        region_spots = [s for s in all_spots_db if s['region'] == region]
        cols = st.columns(2)
        for i, s in enumerate(region_spots):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="mini-card">
                    <b>{s['name']}</b> <span class="flower-badge">{s['highlight']}</span><br>
                    <span style="color:#888; font-size:12px;">{s['desc']}</span>
                </div>
                """, unsafe_allow_html=True)
