import streamlit as st
import pandas as pd

# --- 1. 京大文系学部の配点・合格データ定義 ---
# ご提示いただいた数値を「合格最低点(pass_score_mean)」として設定しています。
# weights: 共通テスト素点を京大配点に換算するための係数

KYODAI_BUNKEI_DATA = {
    "法学部": {
        # 2025年度配点: 共テ270 + 二次615 = 885点満点
        "center_max": 270,
        "secondary_max": 615,
        "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 165},
        # 法学部換算: 900点→270点 (一律0.3倍)
        "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.3, "sci": 0.3},
        "pass_score_mean": 557.55  # user指定値
    },
    "経済学部 (文系)": {
        # 2025年度配点: 共テ250 + 二次600 = 850点満点
        "center_max": 250,
        "secondary_max": 600,
        "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 150}, # 論文等が含まれる場合あり
        # 経済換算: 理科重視 (理科100→50点(0.5倍), 他は0.25倍)
        "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5},
        "pass_score_mean": 546.55  # user指定値
    },
    "文学部": {
        # 配点: 共テ250 + 二次500 = 750点満点
        "center_max": 250,
        "secondary_max": 500,
        "secondary_subjects": {"国語": 150, "数学": 100, "英語": 150, "地歴": 100},
        # 文・教育は理科重視 (理科0.5倍, 他0.25倍)
        "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5},
        "pass_score_mean": 483.75  # user指定値
    },
    "教育学部 (文系)": {
        # 2025年度配点: 共テ240 + 二次675 = 915点満点
        "center_max": 240,
        "secondary_max": 675,
        "secondary_subjects": {"国語": 200, "数学": 150, "英語": 175, "地歴": 150},
        # 教育換算目安: (厳密には科目毎に異なるが近似値として設定)
        # 900→240への圧縮。理科基礎重視。
        "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5}, # 近似設定
        "pass_score_mean": 566.385 # user指定値
    },
    "総合人間学部 (文系)": {
        # 2025年度配点: 共テ225 + 二次600 = 825点満点
        "center_max": 225,
        "secondary_max": 600,
        "secondary_subjects": {"国語": 150, "数学": 100, "英語": 200, "地歴": 150},
        # 総人換算: 5教科均等配点 (理科100→50=0.5? いや総人は400/900などの年もあるが、2025は共テ225)
        # ここでは5教科バランス型として設定 (理科100→50, 他200→~44)
        # 簡易的に一律0.25倍(225点)として計算
        "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5},
        "pass_score_mean": 510.675 # user指定値
    }
}

# --- 2. アプリケーション設定 ---
st.set_page_config(page_title="京大文系 合格判定シミュレーター", layout="centered")

st.title("京大文系 合格判定シミュレーター")
st.markdown("設定された合格最低点（目標値）に基づいて、二次試験での必要点数を算出します。")

# 学部選択エリア
selected_faculty = st.selectbox("志望学部を選んでください", list(KYODAI_BUNKEI_DATA.keys()))
faculty_data = KYODAI_BUNKEI_DATA[selected_faculty]

st.info(f"現在の設定目標点（最低点）: **{faculty_data['pass_score_mean']} 点** / {faculty_data['center_max'] + faculty_data['secondary_max']} 点満点")

st.divider()

# --- 3. 共通テスト入力フォーム (文系特化) ---
st.subheader("1. 共通テスト自己採点 (素点)")
st.caption("手元の自己採点結果（100点満点など）をそのまま入力してください。")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#####  国数英")
    val_jap = st.number_input("国語 (200点満点)", 0, 200, 160)
    val_m1 = st.number_input("数学IA (100点満点)", 0, 100, 70)
    val_m2 = st.number_input("数学IIBC (100点満点)", 0, 100, 70)
    st.markdown("---")
    st.markdown("##### 英語 (京大はR:L=3:1)")
    val_eng_r = st.number_input("リーディング (100点満点)", 0, 100, 85)
    val_eng_l = st.number_input("リスニング (100点満点)", 0, 100, 75)

with col2:
    st.markdown("#####  地歴公民 (2科目)")
    val_soc1 = st.number_input("地歴公民 第1解答科目", 0, 100, 85)
    val_soc2 = st.number_input("地歴公民 第2解答科目", 0, 100, 80)
    st.markdown("---")
    st.markdown("#####  　理科 (基礎2 or 発展1)")
    st.caption("基礎2科目の場合は合計点(100点満点)を入力")
    val_sci = st.number_input("理科 合計", 0, 100, 80)

# --- 4. 計算ロジック ---
# 1. 素点を整理
raw_jap = val_jap
raw_math = val_m1 + val_m2
raw_soc = val_soc1 + val_soc2
raw_sci = val_sci
# 英語: R150 + L50 に換算
raw_eng_kyodai = (val_eng_r * 1.5) + (val_eng_l * 0.5)

# 2. 学部ごとの重み付け計算 (共通テスト圧縮)
w = faculty_data["weights"]
score_jap = raw_jap * w["jap"]
score_math = raw_math * w["math"]
score_soc = raw_soc * w["soc"]
score_sci = raw_sci * w["sci"]
score_eng = raw_eng_kyodai * w["eng"]

total_center_score = score_jap + score_math + score_soc + score_sci + score_eng

# --- 5. 結果表示エリア ---
st.divider()
st.subheader(" 判定結果")

# 共通テスト結果
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("共テ換算得点", f"{total_center_score:.2f} / {faculty_data['center_max']}")
with c2:
    st.metric("英語(京大配点)", f"{raw_eng_kyodai:.0f} / 200")
with c3:
    if w["sci"] >= 0.5:
        st.metric("理科の換算点", f"{score_sci:.1f} (高配点!)")
    else:
        st.metric("理科の換算点", f"{score_sci:.1f}")

# 二次試験シミュレーション
target_score = faculty_data["pass_score_mean"]
required_secondary = target_score - total_center_score

if required_secondary <= 0:
    st.success("共通テストのみで目標点を超えています！")
elif required_secondary > faculty_data["secondary_max"]:
    st.error(f"二次試験で満点を取っても目標に届きません... (残り {required_secondary:.2f}点)")
else:
    st.info(f"合格最低点({target_score}点)まで、二次試験であと **{required_secondary:.2f}** 点必要です。")
    
    # プログレスバー
    progress_val = min(max(required_secondary / faculty_data["secondary_max"], 0.0), 1.0)
    st.progress(progress_val)

    # シミュレーター
    with st.expander(" 二次試験の目標配分を決める", expanded=True):
        st.write("各科目の目標点を設定してください")
        
        sim_total = 0
        # カラム数を科目に合わせる
        sim_cols = st.columns(len(faculty_data["secondary_subjects"]))
        
        for idx, (subj_name, max_pt) in enumerate(faculty_data["secondary_subjects"].items()):
            with sim_cols[idx]:
                # デフォルト値を50%程度に設定
                val = st.slider(f"{subj_name} ({max_pt})", 0, max_pt, int(max_pt*0.5), key=subj_name)
                sim_total += val
        
        # 最終判定
        gap = sim_total - required_secondary
        st.markdown("---")
        st.markdown(f"### シミュレーション合計: {sim_total}点")
        
        if gap >= 0:
            st.success(f" 合格ライン到達！ 余裕: +{gap:.2f}点")
        else:
            st.warning(f" あと {abs(gap):.2f}点 上積みが必要です")