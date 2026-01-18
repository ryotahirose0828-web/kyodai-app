import streamlit as st
import pandas as pd

# ==========================================
# 1. データ定義 (大学 > 学部 > 配点データ)
# ==========================================
# 2025年度新課程対応: 共通テストは「情報(100点)」を含めた1000点満点ベース
# weights: 各科目の素点(100or200)に掛ける係数

UNIVERSITY_DATA = {
    "京都大学 (文系)": {
        "法学部": {
            # 1000点を270点に圧縮 (一律0.27倍)
            "center_max": 270, "secondary_max": 615,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 165},
            "weights": {"jap": 0.27, "math": 0.27, "eng": 0.27, "soc": 0.27, "sci": 0.27, "info": 0.27},
            "pass_score_mean": 557.55,
            "eng_rule": "kyodai_special" # 京大式: R150/L50
        },
        "経済学部 (文系)": {
            # 1000点を250点に圧縮 (一律0.25倍)
            "center_max": 250, "secondary_max": 600,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 546.55,
            "eng_rule": "kyodai_special"
        },
        "文学部": {
            # 1000点を250点に圧縮 (一律0.25倍)
            "center_max": 250, "secondary_max": 500,
            "secondary_subjects": {"国語": 150, "数学": 100, "英語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 483.75,
            "eng_rule": "kyodai_special"
        },
        "教育学部 (文系)": {
            # 1000点を240点に圧縮 (一律0.24倍近似)
            "center_max": 240, "secondary_max": 675,
            "secondary_subjects": {"国語": 200, "数学": 150, "英語": 175, "地歴": 150},
            "weights": {"jap": 0.24, "math": 0.24, "eng": 0.24, "soc": 0.24, "sci": 0.24, "info": 0.24},
            "pass_score_mean": 566.385,
            "eng_rule": "kyodai_special"
        },
        "総合人間学部 (文系)": {
            # 1000点を225点に圧縮 (一律0.225倍近似)
            "center_max": 225, "secondary_max": 600,
            "secondary_subjects": {"国語": 150, "数学": 100, "英語": 200, "地歴": 150},
            "weights": {"jap": 0.225, "math": 0.225, "eng": 0.225, "soc": 0.225, "sci": 0.225, "info": 0.225},
            "pass_score_mean": 510.675,
            "eng_rule": "kyodai_special"
        }
    },
    "北海道大学 (文系)": {
        # 北大共通ルール:
        # 国数英(各200) → x0.3 (各60点)
        # 地歴(200)・理科(100) → x0.4 (80点/40点)
        # 情報(100) → x0.15 (15点)
        # 合計満点: 315点
        "総合入試 (文系)": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 550, # 満点増に伴い微調整
            "eng_rule": "normal_sum" # 北大式: 単純合計
        },
        "文学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 555,
            "eng_rule": "normal_sum"
        },
        "法学部": {
            # 法学部独自: 270点満点換算 (全体を約0.857倍するイメージだが、ここでは係数を調整)
            # 簡易的に 総合入試の配点比率 × (270/315) とする
            "center_max": 270, "secondary_max": 480,
            "secondary_subjects": {"国語": 160, "数学": 160, "英語": 160},
            "weights": {"jap": 0.257, "math": 0.257, "eng": 0.257, "soc": 0.34, "sci": 0.34, "info": 0.13}, 
            "pass_score_mean": 560,
            "eng_rule": "normal_sum"
        },
        "経済学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 553,
            "eng_rule": "normal_sum"
        },
        "教育学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 545,
            "eng_rule": "normal_sum"
        }
    }
}

# ==========================================
# 2. UI & 入力フォーム
# ==========================================
st.set_page_config(page_title="合格判定シミュレーター", layout="centered")

st.title("大学入試 合格判定シミュレーター")
st.caption("新課程入試（情報Iを含む1000点満点）に対応しています。")

# 1. 大学・学部選択
st.subheader("STEP 1: 志望校選択")
c_uni, c_fac = st.columns(2)
with c_uni:
    selected_univ = st.selectbox("大学", list(UNIVERSITY_DATA.keys()))
with c_fac:
    faculty_list = list(UNIVERSITY_DATA[selected_univ].keys())
    selected_faculty = st.selectbox("学部・方式", faculty_list)

target_data = UNIVERSITY_DATA[selected_univ][selected_faculty]
st.info(f" 目標設定: **{target_data['pass_score_mean']} 点** / 合計 {target_data['center_max'] + target_data['secondary_max']} 点")

st.divider()

# 2. 共通テスト入力
st.subheader("STEP 2: 共通テスト自己採点")
st.caption("素点を入力してください。「情報」が追加されています。")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#####  主要科目")
    val_jap = st.number_input("国語 (200)", 0, 200, 160)
    val_m1 = st.number_input("数学IA (100)", 0, 100, 70)
    val_m2 = st.number_input("数学IIBC (100)", 0, 100, 70)
    st.markdown("---")
    st.markdown("#####  英語 (R/L)")
    val_eng_r = st.number_input("リーディング (100)", 0, 100, 85)
    val_eng_l = st.number_input("リスニング (100)", 0, 100, 75)

with col2:
    st.markdown("#####  地歴公民・理科")
    val_soc1 = st.number_input("地歴公民 ① (100)", 0, 100, 85)
    val_soc2 = st.number_input("地歴公民 ② (100)", 0, 100, 80)
    val_sci = st.number_input("理科基礎 合計 (100)", 0, 100, 75)
    st.markdown("---")
    st.markdown("#####  情報")
    val_info = st.number_input("情報I (100)", 0, 100, 80)


# ==========================================
# 3. 計算ロジック
# ==========================================
w = target_data["weights"]

# 英語の計算 (大学分岐)
if target_data["eng_rule"] == "kyodai_special":
    # 京大式: R150 + L50 (素点200点満点に換算)
    eng_base_score = (val_eng_r * 1.5) + (val_eng_l * 0.5)
else:
    # 北大式: 単純合計
    eng_base_score = val_eng_r + val_eng_l

# 共通テスト換算得点の計算
score_jap = val_jap * w["jap"]
score_math = (val_m1 + val_m2) * w["math"]
score_eng = eng_base_score * w["eng"]
score_soc = (val_soc1 + val_soc2) * w["soc"]
score_sci = val_sci * w["sci"]
score_info = val_info * w["info"] # 情報の加算

total_center_score = score_jap + score_math + score_eng + score_soc + score_sci + score_info

# ==========================================
# 4. 結果表示
# ==========================================
st.divider()
st.subheader(" 判定結果")

# 数値表示
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("共テ換算得点", f"{total_center_score:.2f} / {target_data['center_max']}")
with c2:
    if selected_univ == "北海道大学 (文系)":
         st.metric("情報の換算点", f"{score_info:.1f} (0.15倍)")
    else:
         st.metric("情報の換算点", f"{score_info:.1f}")
with c3:
    required_secondary = target_data["pass_score_mean"] - total_center_score
    st.metric("二次試験必要点", f"{max(0, required_secondary):.1f}")

# 二次試験シミュレーション
if required_secondary <= 0:
    st.success(f" 共通テストのみで目標点を超えています！ (+{abs(required_secondary):.1f})")
elif required_secondary > target_data["secondary_max"]:
    st.error(f" 二次試験で満点を取っても届きません... (残り {required_secondary:.1f}点)")
else:
    st.info(f"目標達成まで、あと **{required_secondary:.1f}** 点 / {target_data['secondary_max']}点")
    
    prog = min(required_secondary / target_data["secondary_max"], 1.0)
    st.progress(prog)

    with st.expander(" 二次試験の配分シミュレーション", expanded=True):
        st.write("科目のスライダーを動かして調整してください。")
        
        sim_total = 0
        cols = st.columns(len(target_data["secondary_subjects"]))
        
        for idx, (subj, max_pt) in enumerate(target_data["secondary_subjects"].items()):
            with cols[idx]:
                val = st.slider(f"{subj}", 0, max_pt, int(max_pt * 0.6), key=f"sim_{subj}")
                sim_total += val
        
        gap = sim_total - required_secondary
        st.markdown(f"### シミュレーション合計: {sim_total}点")
        
        if gap >= 0:
            st.success(f" 目標クリア！ 余裕: +{gap:.1f}点")
        else:
            st.warning(f" あと {abs(gap):.1f}点 足りません")
