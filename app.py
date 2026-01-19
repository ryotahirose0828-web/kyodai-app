import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 0. セッション状態の初期化
# ==========================================
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ==========================================
# 1. データ定義 (2026年度 令和8年度入試対応・完全版)
# ==========================================
UNIVERSITY_DATA = {
    # ---------------------------------------------------------
    # 京都大学 (文系)
    # ---------------------------------------------------------
    "京都大学 (文系)": {
        "法学部": {
            "center_max": 285, "secondary_max": 600,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.3, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 560,
            "eng_rule": "kyodai_special"
        },
        "経済学部 (文系)": {
            "center_max": 300, "secondary_max": 550,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.5},
            "pass_score_mean": 580,
            "eng_rule": "kyodai_special"
        },
        "文学部": {
            "center_max": 265, "secondary_max": 500,
            "secondary_subjects": {"国語": 150, "数学": 100, "英語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.15},
            "pass_score_mean": 485,
            "eng_rule": "kyodai_special"
        },
        "教育学部 (文系)": {
            "center_max": 265, "secondary_max": 650,
            "secondary_subjects": {"国語": 150, "数学": 200, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.15},
            "pass_score_mean": 570,
            "eng_rule": "kyodai_special"
        },
        "総合人間学部 (文系)": {
            "center_max": 175, "secondary_max": 650,
            "secondary_subjects": {"国語": 150, "数学": 200, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.0, "math": 0.0, "eng": 0.0, "soc": 0.25, "sci": 1.0, "info": 0.25},
            "pass_score_mean": 520,
            "eng_rule": "kyodai_special"
        }
    },
    
    # ---------------------------------------------------------
    # 京都大学 (理系)
    # ---------------------------------------------------------
    "京都大学 (理系)": {
        "理学部": {
            # 共テ250点: 地歴も25点(0.25倍)に修正
            # 国数英理(0.25倍=各50点), 社情(0.25倍=各25点)
            "center_max": 250, "secondary_max": 975,
            "secondary_subjects": {"数学": 300, "理科①": 150, "理科②": 150, "英語": 225, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 750,
            "eng_rule": "kyodai_special"
        },
        "経済学部 (理系)": {
            "center_max": 300, "secondary_max": 550,
            "secondary_subjects": {"数学": 150, "英語": 150, "国語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.5},
            "pass_score_mean": 580,
            "eng_rule": "kyodai_special"
        },
        "総合人間学部 (理系)": {
            "center_max": 125, "secondary_max": 700,
            "secondary_subjects": {"数学": 200, "理科①": 100, "理科②": 100, "英語": 150, "国語": 150},
            "weights": {"jap": 0.0, "math": 0.0, "eng": 0.0, "soc": 1.0, "sci": 0.0, "info": 0.25},
            "pass_score_mean": 520,
            "eng_rule": "kyodai_special"
        },
        "工学部": {
            "center_max": 225, "secondary_max": 800,
            "secondary_subjects": {"数学": 250, "理科①": 125, "理科②": 125, "英語": 200, "国語": 100},
            "weights": {"jap": 0.125, "math": 0.125, "eng": 0.25, "soc": 0.5, "sci": 0.125, "info": 0.5},
            "pass_score_mean": 630, 
            "eng_rule": "kyodai_special"
        },
        "医学部 (医学科)": {
            "center_max": 275, "secondary_max": 1000,
            "secondary_subjects": {"数学": 250, "理科①": 150, "理科②": 150, "英語": 300, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 950,
            "eng_rule": "kyodai_special"
        },
        "薬学部": {
            "center_max": 275, "secondary_max": 700,
            "secondary_subjects": {"数学": 200, "理科①": 100, "理科②": 100, "英語": 200, "国語": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 650,
            "eng_rule": "kyodai_special"
        },
        "農学部": {
            "center_max": 300, "secondary_max": 700,
            "secondary_subjects": {"数学": 200, "理科①": 100, "理科②": 100, "英語": 200, "国語": 100},
            "weights": {"jap": 0.35, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.3},
            "pass_score_mean": 660,
            "eng_rule": "kyodai_special"
        }
    },

    # ---------------------------------------------------------
    # 北海道大学 (文系)
    # ---------------------------------------------------------
    "北海道大学 (文系)": {
        "総合入試 (文系)": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 517, 
            "eng_rule": "normal_sum"
        },
        "文学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 522,
            "eng_rule": "normal_sum"
        },
        "法学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15}, 
            "pass_score_mean": 520,
            "eng_rule": "normal_sum"
        },
        "経済学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 520,
            "eng_rule": "normal_sum"
        },
        "教育学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 502,
            "eng_rule": "normal_sum"
        }
    },
    
    # ---------------------------------------------------------
    # 北海道大学 (理系)
    # ---------------------------------------------------------
    "北海道大学 (理系)": {
        "総合入試 (理系)": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.6, "sci": 0.75, "info": 0.15},
            "pass_score_mean": 530,
            "eng_rule": "normal_sum"
        },
        "医学部 (医学科)": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150, "面接": 75},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.6, "sci": 0.75, "info": 0.15},
            "pass_score_mean": 670,
            "eng_rule": "normal_sum"
        },
        "歯学部": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150, "面接/小論": 75},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.6, "sci": 0.75, "info": 0.15},
            "pass_score_mean": 560,
            "eng_rule": "normal_sum"
        },
        "獣医学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.6, "sci": 0.75, "info": 0.15},
            "pass_score_mean": 610,
            "eng_rule": "normal_sum"
        },
        "水産学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.6, "sci": 0.75, "info": 0.15},
            "pass_score_mean": 490,
            "eng_rule": "normal_sum"
        }
    },

    # ---------------------------------------------------------
    # 一橋大学
    # ---------------------------------------------------------
    "一橋大学": {
        "商学部": {
            "center_max": 300, "secondary_max": 700,
            "secondary_subjects": {"英語": 235, "数学": 230, "国語": 110, "社会": 125},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.5},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "経済学部": {
            "center_max": 210, "secondary_max": 790,
            "secondary_subjects": {"英語": 260, "数学": 260, "国語": 110, "社会": 160},
            "weights": {"jap": 0.175, "math": 0.175, "eng": 0.175, "soc": 0.175, "sci": 0.35, "info": 0.35},
            "pass_score_mean": 580,
            "eng_rule": "normal_sum"
        },
        "法学部": {
            "center_max": 250, "secondary_max": 750,
            "secondary_subjects": {"英語": 280, "数学": 180, "国語": 130, "社会": 160},
            "weights": {"jap": 0.2, "math": 0.25, "eng": 0.2, "soc": 0.25, "sci": 0.4, "info": 0.3},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "社会学部": {
            "center_max": 180, "secondary_max": 820,
            "secondary_subjects": {"英語": 230, "数学": 130, "国語": 180, "社会": 280},
            "weights": {"jap": 0.1, "math": 0.1, "eng": 0.1, "soc": 0.1, "sci": 0.9, "info": 0.1},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "SDS学部": {
            "center_max": 250, "secondary_max": 750,
            "secondary_subjects": {"英語": 230, "数学": 330, "国語": 100, "総合": 90},
            "weights": {"jap": 0.2, "math": 0.2, "eng": 0.2, "soc": 0.2, "sci": 0.4, "info": 0.5},
            "pass_score_mean": 630,
            "eng_rule": "normal_sum"
        }
    }
}

# ==========================================
# 2. UI & 入力フォーム
# ==========================================
st.set_page_config(page_title="合格判定シミュレーター", layout="centered")

st.title("大学入試 合格判定シミュレーター")
st.caption("2026年度(令和8年度)新課程入試対応。入力履歴機能付き。")

# 1. 大学・学部選択
st.subheader("1. 志望校選択")
c_uni, c_fac = st.columns(2)
with c_uni:
    selected_univ = st.selectbox("大学", list(UNIVERSITY_DATA.keys()))
with c_fac:
    faculty_list = list(UNIVERSITY_DATA[selected_univ].keys())
    selected_faculty = st.selectbox("学部・方式", faculty_list)

target_data = UNIVERSITY_DATA[selected_univ][selected_faculty]

# 文系・理系の自動判定
is_science_univ = "理系" in selected_univ

# 目標点の設定
st.markdown("---")
target_score = st.number_input(
    "合格目標点 (総合点)", 
    value=float(target_data['pass_score_mean']), 
    step=1.0,
    help="デフォルト値は過去の合格最低点などをベースにした目安です。"
)
st.info(f"目標設定: {target_score} 点 (満点: {target_data['center_max'] + target_data['secondary_max']} 点)")

st.divider()

# 2. 共通テスト入力
st.subheader("2. 共通テスト自己採点")
st.caption("素点（新課程 1000点満点）を入力してください。")

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 国数英")
    val_jap = st.number_input("国語 (200)", 0, 200, 160)
    val_m1 = st.number_input("数学IA (100)", 0, 100, 70)
    val_m2 = st.number_input("数学IIBC (100)", 0, 100, 70)
    st.markdown("---")
    st.markdown("##### 英語 (R/L)")
    val_eng_r = st.number_input("リーディング (100)", 0, 100, 85)
    val_eng_l = st.number_input("リスニング (100)", 0, 100, 75)

with col2:
    if is_science_univ:
        # --- 理系用フォーム ---
        st.markdown("##### 地歴公民・理科 (理系)")
        st.info("理系：地歴1科目、理科2科目")
        
        val_soc_s = st.number_input("地歴公民 (100)", 0, 100, 80, key="soc_s")
        val_sci1 = st.number_input("理科 第1解答科目 (100)", 0, 100, 75, key="sci1")
        val_sci2 = st.number_input("理科 第2解答科目 (100)", 0, 100, 75, key="sci2")
        
        val_soc_total = val_soc_s
        val_sci_total = val_sci1 + val_sci2 
        
    else:
        # --- 文系用フォーム ---
        st.markdown("##### 地歴公民・理科 (文系)")
        st.success("文系：地歴2科目、理科基礎(または専門1)")
        
        val_soc1 = st.number_input("地歴公民 ① (100)", 0, 100, 85, key="soc1")
        val_soc2 = st.number_input("地歴公民 ② (100)", 0, 100, 80, key="soc2")
        val_sci_base = st.number_input("理科 (基礎2 or 専門1) (100)", 0, 100, 80, key="sci_base")
        
        val_soc_total = val_soc1 + val_soc2 
        val_sci_total = val_sci_base 
    
    st.markdown("---")
    st.markdown("##### 情報")
    val_info = st.number_input("情報I (100)", 0, 100, 80)


# ==========================================
# 3. 計算ロジック
# ==========================================
w = target_data["weights"]

# 英語の計算
if target_data["eng_rule"] == "kyodai_special":
    eng_base_score = (val_eng_r * 1.5) + (val_eng_l * 0.5)
else:
    eng_base_score = val_eng_r + val_eng_l

# 科目別スコア計算
score_jap = val_jap * w["jap"]
score_math = (val_m1 + val_m2) * w["math"]
score_eng = eng_base_score * w["eng"]
score_info = val_info * w["info"]

# 理社はここで係数をかけるだけでOK
score_soc = val_soc_total * w["soc"]
score_sci = val_sci_total * w["sci"]

total_center_score = score_jap + score_math + score_eng + score_soc + score_sci + score_info

# ==========================================
# 4. 結果表示
# ==========================================
st.divider()
st.subheader("判定結果")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("共テ換算得点", f"{total_center_score:.2f} / {target_data['center_max']}")
with c2:
    if w["info"] >= 0.5:
        st.metric("情報の換算点", f"{score_info:.1f} (高配点!)")
    else:
        st.metric("情報の換算点", f"{score_info:.1f}")
with c3:
    required_secondary = target_score - total_center_score
    st.metric("二次試験必要点", f"{max(0, required_secondary):.1f}")

# 二次試験シミュレーション
if required_secondary <= 0:
    st.success(f"共通テストのみで目標点を超えています (+{abs(required_secondary):.1f})")
elif required_secondary > target_data["secondary_max"]:
    st.error(f"二次試験で満点を取っても届きません (残り {required_secondary:.1f
