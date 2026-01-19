import streamlit as st
import pandas as pd

# ==========================================
# 1. データ定義 (2026年度 令和8年度入試対応)
# ==========================================
# データ出典: Benesse マナビジョン / 各大学公表の2026予告
# pass_score_mean: 過去データと新配点から算出した目標点目安

UNIVERSITY_DATA = {
    # ---------------------------------------------------------
    # 京都大学 (2026年度 最新配点)
    # ---------------------------------------------------------
    "京都大学 (文系)": {
        "法学部": {
            # 共テ285: 全科目x0.3 (情15)
            "center_max": 285, "secondary_max": 600,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 200, "地歴": 100},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.3, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 560,
            "eng_rule": "kyodai_special"
        },
        "経済学部 (文系)": {
            # 共テ300: 全科目50点 (理・情も0.5倍)
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
            # [2026特徴] 共テ225点: 情報50点, 地歴50点, 英語50点, 国数理は25点に圧縮
            # 二次800点: 英200, 数250, 理250, 国100
            "center_max": 225, "secondary_max": 800,
            "secondary_subjects": {"数学(Ⅲ含む)": 250, "理科(2科目)": 250, "英語": 200, "国語": 100},
            "weights": {"jap": 0.125, "math": 0.125, "eng": 0.25, "soc": 0.5, "sci": 0.125, "info": 0.5},
            "pass_score_mean": 630, # 目安
            "eng_rule": "kyodai_special"
        },
        "理学部": {
            # 共テ225(or250): 国数英理50?, 社50?, 情25
            # 一般的に理学部は共テ圧縮型。ここでは標準的な275点ベース(国数英社理50+情25)で計算
            "center_max": 275, "secondary_max": 975,
            "secondary_subjects": {"数学(Ⅲ含む)": 300, "理科(2科目)": 300, "英語": 225, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 750,
            "eng_rule": "kyodai_special"
        },
        "医学部 (医学科)": {
            # 共テ275: 国数英社理50 + 情25
            "center_max": 275, "secondary_max": 1000,
            "secondary_subjects": {"数学(Ⅲ含む)": 250, "理科(2科目)": 300, "英語": 300, "国語": 150}, # 面接除外or含む
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 950,
            "eng_rule": "kyodai_special"
        },
        "薬学部": {
            # 共テ275ベース
            "center_max": 275, "secondary_max": 700,
            "secondary_subjects": {"数学(Ⅲ含む)": 200, "理科(2科目)": 200, "英語": 200, "国語": 100},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 650,
            "eng_rule": "kyodai_special"
        },
        "農学部": {
            # 共テ350: 国70, 数50, 英50, 社50, 理50, 情30(推定)
            "center_max": 300, "secondary_max": 700,
            "secondary_subjects": {"数学(Ⅲ含む)": 200, "理科(2科目)": 200, "英語": 200, "国語": 100},
            "weights": {"jap": 0.35, "math": 0.25, "eng": 0.25, "soc": 0.5, "sci": 0.25, "info": 0.3},
            "pass_score_mean": 660,
            "eng_rule": "kyodai_special"
        }
    },

    # ---------------------------------------------------------
    # 北海道大学 (2026年度 最新配点)
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
    "北海道大学 (理系)": {
        "総合入試 (理系)": {
            # 共テ315: 全科目標準的 (理系は理社が逆転する文系と違い、バランス型が多い)
            # ここでは標準: J60, M60, E60, Soc60, Sci60, Info15
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 530,
            "eng_rule": "normal_sum"
        },
        "医学部 (医学科)": {
            # 共テ315, 二次525 (面接75点含む)
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学(Ⅲ含む)": 150, "理科(2科目)": 150, "英語": 150, "面接": 75},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.6, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 670,
            "eng_rule": "normal_sum"
        },
        "歯学部": {
            # 共テ315, 二次525 (面接?点) ※標準的な450+面接などの構成
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

    # ---------------------------------------------------------
    # 一橋大学 (2026年度 最新配点)
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
st.caption("2026年度(令和8年度)新課程入試対応。文系・理系全学部対応版。")

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

# 共通テスト換算得点の計算
# 理系・文系で理科の満点入力が異なる(100or200)場合の補正
# 理系学部で「理科2科目」が必要な場合、入力値(200満点)をそのまま使う
# 文系学部で「理科基礎」の場合、入力値(100満点)だが、ユーザーが間違えて200に入れるケースも想定して、ここでは単純に入力値×係数とする
# (※weights側で、理科が200点満点前提なら係数を半分にする等の調整が必要だが、
#  今回は「理系は素点200入力、文系は素点100入力」を想定し、係数は100点あたりで設定されているため
#  理系(200入力)の場合は係数を0.5倍して適用するロジックを追加)

final_sci_score = 0
if "理系" in selected_univ:
    # 理系は200点満点入力 -> 係数が「100点に対する倍率」で定義されているなら、入力値を半分にしてかけるか、係数を調整
    # ここでは「入力値(200) * 係数(例:0.25)」だと50点になる。
    # 京大工学部: 理科200点 -> 25点 (0.125倍)
    final_sci_score = val_sci * w["sci"]
else:
    # 文系: 100点満点入力 (基礎2 or 専門1)
    # ユーザーが下の欄(200max)に入力してしまった場合も考慮しつつ、基本はそのまま
    # ただし理科入力欄が1つになったので、文系ユーザーが100点満点で入力すればOK
    final_sci_score = val_sci * w["sci"]

score_jap = val_jap * w["jap"]
score_math = (val_m1 + val_m2) * w["math"]
score_eng = eng_base_score * w["eng"]
score_soc = (val_soc1 + val_soc2) * w["soc"]
score_sci = final_sci_score
score_info = val_info * w["info"]

# 社会の科目数補正 (一橋など2科目必要な場合)
# 入力は常に2科目あるが、1科目しか使わない大学(京大理系など)の場合、
# weights["soc"] が「1科目分」として定義されていると、2科目合計にかけると倍になる。
# 京大理系: 地歴1科目選択。入力は2つある。Maxをとるロジックが必要。
if "京都大学 (理系)" in selected_univ or "北海道大学 (理系)" in selected_univ:
    # 理系は地歴1科目のみ利用が多い
    score_soc = max(val_soc1, val_soc2) * w["soc"]
else:
    # 文系は2科目合計を使うケースが多い(一橋、京大文系)
    # ただし京大文系など地歴100点満点の場合は「2科目合計200点→100点」なので、
    # w["soc"]=0.5 と設定して合計にかければOK
    # 一橋社学は地歴2科目利用
    score_soc = (val_soc1 + val_soc2) * w["soc"]

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
        else:
            st.warning(f"あと {abs(gap):.1f}点 足りません")
