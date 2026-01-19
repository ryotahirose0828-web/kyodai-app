import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 0. セッション状態の初期化 (履歴機能用)
# ==========================================
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ==========================================
# 1. データ定義 (2026年度 令和8年度入試対応)
# ==========================================
UNIVERSITY_DATA = {
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
            "weights": {"jap": 0.15, "math": 0.15, "eng": 0.15, "soc": 0.15, "sci": 0.3, "info": 0.25},
            "pass_score_mean": 515,
            "eng_rule": "kyodai_special"
        }
    },
    "京都大学 (理系)": {
        "工学部": {
            "center_max": 225, "secondary_max": 800,
            "secondary_subjects": {"数学(Ⅲ含む)": 250, "理科(2科目)": 250, "英語": 200, "国語": 100},
            "weights": {"jap": 0.125, "math": 0.125, "eng": 0.25, "soc": 0.5, "sci": 0.125, "info": 0.5},
            "pass_score_mean": 630,
            "eng_rule": "kyodai_special"
        },
        "理学部": {
            "center_max": 275, "secondary_max": 975,
            "secondary_subjects": {"数学(Ⅲ含む)": 300, "理科(2科目)": 300, "英語": 225, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 750,
            "eng_rule": "kyodai_special"
        },
        "医学部 (医学科)": {
            "center_max": 275, "secondary_max": 1000,
            "secondary_subjects": {"数学(Ⅲ含む)": 250, "理科(2科目)": 300, "英語": 300, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 950,
            "eng_rule": "kyodai_special"
        },
        "薬学部": {
            "center_max": 275, "secondary_max": 700,
            "secondary_subjects": {"数学(Ⅲ含む)": 200, "理科(2科目)": 200, "英語": 200, "国語": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 650,
            "eng_rule": "kyodai_special"
        },
        "農学部": {
            "center_max": 300, "secondary_max": 700,
            "secondary_subjects": {"数学(Ⅲ含む)": 200, "理科(2科目)": 200, "英語": 200, "国語": 100},
            "weights": {"jap": 0.35, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.3},
            "pass_score_mean": 660,
            "eng_rule": "kyodai_special"
        }
    },
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
    "北海道大学 (理系)": {
        "総合入試 (理系)": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 530,
            "eng_rule": "normal_sum"
        },
        "医学部 (医学科)": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150, "面接": 75},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 670,
            "eng_rule": "normal_sum"
        },
        "歯学部": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150, "面接/小論": 75},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 560,
            "eng_rule": "normal_sum"
        },
        "獣医学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 610,
            "eng_rule": "normal_sum"
        },
        "水産学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 490,
            "eng_rule": "normal_sum"
        }
    },
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
st.caption("素点（新課程 1000点満点）を入力してください。理系は理科2科目の合計を入力してください。")

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
    st.caption("※理系は理科2科目(200点満点)の合計を入力すると自動で圧縮されます。")
    val_soc1 = st.number_input("地歴公民 ① (100)", 0, 100, 85)
    val_soc2 = st.number_input("地歴公民 ② (100)", 0, 100, 80)
    val_sci = st.number_input("理科 (基礎2 or 専門2) (200)", 0, 200, 150)
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

# 理科の計算（ここを修正：変数名を score_sci に統一）
score_sci = 0
if "理系" in selected_univ:
    # 理系: 素点200点入力
    score_sci = val_sci * w["sci"]
else:
    # 文系: 素点100点入力
    score_sci = val_sci * w["sci"]

score_jap = val_jap * w["jap"]
score_math = (val_m1 + val_m2) * w["math"]
score_eng = eng_base_score * w["eng"]
score_info = val_info * w["info"]

# 社会の科目数補正
if "京都大学 (理系)" in selected_univ or "北海道大学 (理系)" in selected_univ:
    # 理系は地歴1科目のみ(高得点)利用
    score_soc = max(val_soc1, val_soc2) * w["soc"]
else:
    # 文系は2科目利用
    score_soc = (val_soc1 + val_soc2) * w["soc"]

# 合計計算（ここでエラーが出ていました）
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
                val = st.number_input(
                    f"{subj} (/{max_pt})", 
                    min_value=0, 
                    max_value=max_pt, 
                    value=int(max_pt * 0.6),
                    step=1,
                    key=f"sim_{subj}"
                )
                sim_total += val
        
        gap = sim_total - required_secondary
        st.markdown(f"**シミュレーション合計: {sim_total}点**")
        
        if gap >= 0:
            st.success(f"目標クリア (余裕: +{gap:.1f}点)")
            
            # --- 履歴保存ボタン ---
            if st.button("この結果を履歴に保存", key="save_success"):
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_record = {
                    "日時": now_str,
                    "大学": selected_univ,
                    "学部": selected_faculty,
                    "共テ換算": f"{total_center_score:.1f}",
                    "二次目標": f"{sim_total}点",
                    "合否": "合格圏"
                }
                st.session_state['history'].append(new_record)
                st.success("履歴に保存しました！")

        else:
            st.warning(f"あと {abs(gap):.1f}点 足りません")
            
            # --- 履歴保存ボタン (不合格圏でも保存可能に) ---
            if st.button("この結果を履歴に保存", key="save_fail"):
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_record = {
                    "日時": now_str,
                    "大学": selected_univ,
                    "学部": selected_faculty,
                    "共テ換算": f"{total_center_score:.1f}",
                    "二次目標": f"{sim_total}点",
                    "合否": f"不足 {abs(gap):.1f}"
                }
                st.session_state['history'].append(new_record)
                st.success("履歴に保存しました！")

# ==========================================
# 5. 履歴表示エリア
# ==========================================
if st.session_state['history']:
    st.divider()
    st.subheader(" 計算履歴 (セッション内)")
    st.caption("※ブラウザを閉じると履歴は消えます。")
    
    # 履歴をデータフレームに変換して表示
    df_history = pd.DataFrame(st.session_state['history'])
    
    # 最新が上に来るように逆順にする
    df_history = df_history.iloc[::-1]
    
    st.dataframe(df_history, use_container_width=True)
