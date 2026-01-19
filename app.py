import streamlit as st
import pandas as pd

# ==========================================
# 1. データ定義 (2026年度 令和8年度入試対応)
# ==========================================
# データ出典: Benesse マナビジョン (2026年度入試情報)
# pass_score_mean: 過去の合格最低点データをベースにした目標点(参考値)
# weights: 共通テスト素点(100/200点)にかける係数

UNIVERSITY_DATA = {
    # ---------------------------------------------------------
    # 京都大学 (2026年度 最新配点)
    # ---------------------------------------------------------
    "京都大学 (文系)": {
        "法学部": {
            # 共テ285点: 950点を285点に圧縮 (全科目x0.3)
            # 情報は素点50点扱いx0.3=15点 (つまり100点素点に対しては係数0.15)
            "center_max": 285, "secondary_max": 600,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.3, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 560,
            "eng_rule": "kyodai_special"
        },
        "経済学部 (文系)": {
            # 共テ300点: 全科目50点均等 (理科・情報も0.5倍で50点)
            "center_max": 300, "secondary_max": 550,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.5},
            "pass_score_mean": 580,
            "eng_rule": "kyodai_special"
        },
        "文学部": {
            # 共テ265点: 国数英社理50(0.25/0.5) + 情報15(0.15)
            "center_max": 265, "secondary_max": 500,
            "secondary_subjects": {"国語": 150, "数学": 100, "英語": 150, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.15},
            "pass_score_mean": 485,
            "eng_rule": "kyodai_special"
        },
        "教育学部 (文系)": {
            # 共テ265点: 国数英社理50 + 情報15
            "center_max": 265, "secondary_max": 650,
            "secondary_subjects": {"国語": 150, "数学": 200, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.15},
            "pass_score_mean": 570,
            "eng_rule": "kyodai_special"
        },
        "総合人間学部 (文系)": {
            # 共テ175点: 国数英社30, 理30, 情25
            "center_max": 175, "secondary_max": 650,
            "secondary_subjects": {"国語": 150, "数学": 200, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.15, "sci": 0.3, "info": 0.25},
            "pass_score_mean": 515,
            "eng_rule": "kyodai_special"
        }
    },

    # ---------------------------------------------------------
    # 北海道大学 (2026年度 配点)
    # ---------------------------------------------------------
    "北海道大学 (文系)": {
        # 全学部共通テスト315点満点 (情報15点)
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
    # 一橋大学 (2026年度 配点)
    # ---------------------------------------------------------
    "一橋大学": {
        "商学部": {
            # 共テ300点: 全科目50点均等
            "center_max": 300, "secondary_max": 700,
            "secondary_subjects": {"英語": 235, "数学": 230, "国語": 110, "社会": 125},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.5, "info": 0.5},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "経済学部": {
            # 共テ210点: 全科目35点均等
            "center_max": 210, "secondary_max": 790,
            "secondary_subjects": {"英語": 260, "数学": 260, "国語": 110, "社会": 160},
            "weights": {"jap": 0.175, "math": 0.175, "eng": 0.175, "soc": 0.175, "sci": 0.35, "info": 0.35},
            "pass_score_mean": 580,
            "eng_rule": "normal_sum"
        },
        "法学部": {
            # 共テ250点: 国英40, 数社50, 理40, 情30
            "center_max": 250, "secondary_max": 750,
            "secondary_subjects": {"英語": 280, "数学": 180, "国語": 130, "社会": 160},
            "weights": {"jap": 0.2, "math": 0.25, "eng": 0.2, "soc": 0.25, "sci": 0.4, "info": 0.3},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "社会学部": {
            # 共テ180点: 理科90点, 他は20点(情10点)
            "center_max": 180, "secondary_max": 820,
            "secondary_subjects": {"英語": 230, "数学": 130, "国語": 180, "社会": 280},
            "weights": {"jap": 0.1, "math": 0.1, "eng": 0.1, "soc": 0.1, "sci": 0.9, "info": 0.1},
            "pass_score_mean": 600,
            "eng_rule": "normal_sum"
        },
        "SDS学部": {
            # 共テ250点: 情50点, 他40点
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

st.title("大学入試 合格判定シミュレーター (2026対応)")
st.caption("2026年度(令和8年度)の最新配点に対応。共通テスト(1000点満点)と志望校の配点から目標点を算出します。")

# 1. 大学・学部選択
st.subheader("1. 志望校選択")
c_uni, c_fac = st.columns(2)
with c_uni:
    selected_univ = st.selectbox("大学", list(UNIVERSITY_DATA.keys()))
with c_fac:
    faculty_list = list(UNIVERSITY_DATA[selected_univ].keys())
    selected_faculty = st.selectbox("学部・方式", faculty_list)

target_data = UNIVERSITY_DATA[selected_univ][selected_faculty]

# 目標点の設定
st.markdown("---")
target_score = st.number_input(
    "合格目標点 (総合点)", 
    value=float(target_data['pass_score_mean']), 
    step=1.0,
    help="デフォルト値は過去のデータに基づく目安です。配点変更により変動する可能性があります。"
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
    st.markdown("##### 地歴公民・理科")
    st.caption("※一橋大は地歴公民2科目、理科1科目(基礎2or専門1)の素点を入力")
    val_soc1 = st.number_input("地歴公民 ① (100)", 0, 100, 85)
    val_soc2 = st.number_input("地歴公民 ② (100)", 0, 100, 80)
    val_sci = st.number_input("理科 (基礎2 or 専門1) (100)", 0, 100, 75)
    st.markdown("---")
    st.markdown("##### 情報")
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
    # 通常: 単純合計 (200点満点)
    eng_base_score = val_eng_r + val_eng_l

# 共通テスト換算得点の計算
score_jap = val_jap * w["jap"]
score_math = (val_m1 + val_m2) * w["math"]
score_eng = eng_base_score * w["eng"]
score_soc = (val_soc1 + val_soc2) * w["soc"]
score_sci = val_sci * w["sci"]
score_info = val_info * w["info"]

total_center_score = score_jap + score_math + score_eng + score_soc + score_sci + score_info

# ==========================================
# 4. 結果表示
# ==========================================
st.divider()
st.subheader("判定結果")

# 数値表示
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("共テ換算得点", f"{total_center_score:.2f} / {target_data['center_max']}")
with c2:
    # 情報配点の強調表示
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
    st.error(f"二次試験で満点を取っても届きません (残り {required_secondary:.1f}点)")
else:
    st.info(f"目標達成まで、二次試験であと {required_secondary:.1f} 点 / {target_data['secondary_max']}点")
    
    prog = min(required_secondary / target_data["secondary_max"], 1.0)
    st.progress(prog)

    with st.expander("二次試験の配分シミュレーション", expanded=True):
        st.write("各科目の目標点数を入力してください。")
        
        sim_total = 0
        cols = st.columns(len(target_data["secondary_subjects"]))
        
        for idx, (subj, max_pt) in enumerate(target_data["secondary_subjects"].items()):
            with cols[idx]:
                # 数値入力に変更
                val = st.number_input(
                    f"{subj} (/{max_pt})", 
                    min_value=0, 
                    max_value=max_pt, 
                    value=int(max_pt * 0.6), # デフォルト6割
                    step=1,
                    key=f"sim_{subj}"
                )
                sim_total += val
        
        gap = sim_total - required_secondary
        st.markdown(f"**シミュレーション合計: {sim_total}点**")
        
        if gap >= 0:
            st.success(f"目標クリア (余裕: +{gap:.1f}点)")
        else:
            st.warning(f"あと {abs(gap):.1f}点 足りません")
