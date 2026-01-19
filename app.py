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
            # 理科重視(100点)、社会圧縮(50点)
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
        "工学部": {
            # 英語1:1配点
            "center_max": 225, "secondary_max": 800,
            "secondary_subjects": {"数学": 250, "理科①": 125, "理科②": 125, "英語": 200, "国語": 100},
            "weights": {"jap": 0.125, "math": 0.125, "eng": 0.25, "soc": 0.5, "sci": 0.125, "info": 0.5},
            "pass_score_mean": 630, 
            "eng_rule": "normal_sum"
        },
        "理学部": {
            # 全科目0.25倍
            "center_max": 250, "secondary_max": 975,
            "secondary_subjects": {"数学": 300, "理科①": 150, "理科②": 150, "英語": 225, "国語": 150},
            "weights": {"jap": 0.25, "math": 0.25, "eng": 0.25, "soc": 0.25, "sci": 0.25, "info": 0.25},
            "pass_score_mean": 750,
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
            "center_max": 350, "secondary_max": 700,
            "secondary_subjects": {"数学": 200, "理科①": 100, "理科②": 100, "英語": 200, "国語": 100},
            "weights": {"jap": 0.35, "math": 0.25, "eng": 0.25, "soc": 1.0, "sci": 0.25, "info": 0.3},
            "pass_score_mean": 660,
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
        }
    },

    # ---------------------------------------------------------
    # 北海道大学 (文系) - 目標点を情報分(+11点)修正
    # ---------------------------------------------------------
    "北海道大学 (文系)": {
        "総合入試 (文系)": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 528, # +11
            "eng_rule": "normal_sum"
        },
        "文学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 533, # +11
            "eng_rule": "normal_sum"
        },
        "法学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15}, 
            "pass_score_mean": 531, # +11
            "eng_rule": "normal_sum"
        },
        "経済学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 531, # +11
            "eng_rule": "normal_sum"
        },
        "教育学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"国語": 150, "数学": 150, "英語": 150},
            "weights": {"jap": 0.3, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.4, "info": 0.15},
            "pass_score_mean": 513, # +11
            "eng_rule": "normal_sum"
        }
    },
    
    # ---------------------------------------------------------
    # 北海道大学 (理系) - 目標点を情報分(+11点)修正
    # ---------------------------------------------------------
    "北海道大学 (理系)": {
        "総合入試 (理系) - 標準": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 541,
            "eng_rule": "normal_sum"
        },
        "総合入試 (理系) - 数学重点": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学": 225, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 585,
            "eng_rule": "normal_sum"
        },
        "総合入試 (理系) - 物理重点": {
            "center_max": 315, "secondary_max": 487.5,
            "secondary_subjects": {"数学": 150, "理科①(重点)": 112.5, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 565,
            "eng_rule": "normal_sum"
        },
        "総合入試 (理系) - 化学重点": {
            "center_max": 315, "secondary_max": 487.5,
            "secondary_subjects": {"数学": 150, "理科①(重点)": 112.5, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 565,
            "eng_rule": "normal_sum"
        },
        "総合入試 (理系) - 生物重点": {
            "center_max": 315, "secondary_max": 487.5,
            "secondary_subjects": {"数学": 150, "理科①(重点)": 112.5, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 565,
            "eng_rule": "normal_sum"
        },
        "医学部 (医学科)": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150, "面接": 75},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 681,
            "eng_rule": "normal_sum"
        },
        "歯学部": {
            "center_max": 315, "secondary_max": 525,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150, "面接/小論": 75},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 571,
            "eng_rule": "normal_sum"
        },
        "獣医学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 621,
            "eng_rule": "normal_sum"
        },
        "水産学部": {
            "center_max": 315, "secondary_max": 450,
            "secondary_subjects": {"数学": 150, "理科①": 75, "理科②": 75, "英語": 150},
            "weights": {"jap": 0.4, "math": 0.3, "eng": 0.3, "soc": 0.4, "sci": 0.3, "info": 0.15},
            "pass_score_mean": 501,
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
            "eng_
