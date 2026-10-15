"""
================================================================================
  高考志愿智能规划与决策系统 v2.0 (Gaokao 2.0)
  极简架构 · 现代美学 · 就业实用导向 · 全程避坑护航
================================================================================
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ============================================================================
# 页面基础配置与美学样式
# ============================================================================
st.set_page_config(
    page_title="高考志愿智能规划与决策系统 2.0",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif;
}

/* 顶部大标题与渐变 Hero 容器 */
.hero-box {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #6366F1 100%);
    border-radius: 18px;
    padding: 32px 36px;
    color: #FFFFFF;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
}
.hero-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 15px;
    opacity: 0.9;
    line-height: 1.6;
}

/* 模块分段标题 */
.step-header {
    font-size: 18px;
    font-weight: 700;
    color: #1F2937;
    border-left: 4px solid #3B82F6;
    padding-left: 12px;
    margin: 20px 0 16px 0;
}

/* 专业推荐卡片 */
.major-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}
.major-card:hover {
    border-color: #93C5FD;
    box-shadow: 0 8px 16px rgba(59, 130, 246, 0.12);
    transform: translateY(-2px);
}

/* 标签徽章 */
.badge-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-hard { background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE; }
.badge-warn { background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
.badge-good { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.badge-info { background: #F0F9FF; color: #0369A1; border: 1px solid #BAE6FD; }

/* 警示与洞察底栏 */
.insight-box {
    background: #F8FAFC;
    border-left: 4px solid #3B82F6;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-top: 10px;
    font-size: 13px;
    color: #334155;
    line-height: 1.6;
}
.warning-box {
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-top: 8px;
    font-size: 13px;
    color: #92400E;
    line-height: 1.6;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# 数据文件路径与全局状态
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "score": 580,
        "rank_pct": 12.0,
        "subjects": ["物理", "化学", "生物"],
        "target_goal": "大厂高薪与硬技术研发",
        "career_track": "不限",
        "family_econ": "中等工薪",
        "enable_pitfall_filter": True,
    }

# ============================================================================
# 顶部 Hero Banner
# ============================================================================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🎓 高考志愿智能规划与决策系统 2.0</div>
        <div class="hero-subtitle">
            基于真实就业大数据 · 告别空泛套话 · 智能避开生化环材与伪工科陷阱 · 为考生的每一分创造最大竞争壁垒
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# 侧边栏：极简模式导航与全局排雷开关
# ============================================================================
with st.sidebar:
    st.markdown("### 🧭 系统导航")
    step = st.radio(
        "当前规划阶段",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: "1️⃣ 考生档案与核心诉求",
            2: "2️⃣ 深度志向与意向测评",
            3: "3️⃣ 终极专业大屏与避坑推荐"
        }[x],
        index=st.session_state.current_step - 1
    )
    st.session_state.current_step = step

    st.markdown("---")
    st.markdown("### 🛡️ 智能避坑引擎")
    pitfall_toggle = st.toggle(
        "开启「高考志愿避坑排雷」守护",
        value=st.session_state.user_profile.get("enable_pitfall_filter", True),
        help="自动拦截物流管理、工业工程、传统土木建筑、生化环材无研发岗等低实用性方向，替补优质高壁垒硬工科与高薪专业。"
    )
    st.session_state.user_profile["enable_pitfall_filter"] = pitfall_toggle

    st.caption("💡 开启后，系统将从底层阻断‘挂羊头卖狗肉’的伪工科，优先确保专业学到真技术。")

# ============================================================================
# 阶段 1：考生档案与核心诉求
# ============================================================================
if st.session_state.current_step == 1:
    st.markdown('<p class="step-header">🎯 第一步：确立考生基本盘与升学诉求</p>', unsafe_allow_html=True)
    st.markdown("真实的高考志愿规划，**首先取决于你的硬性分数盘与核心人生目标**。拒绝填鸭式答题，先明确你的底线。")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📚 选科与学业基础")
        subjects = st.multiselect(
            "新高考选考科目（默认物化生）",
            options=["物理", "化学", "生物", "历史", "地理", "政治"],
            default=st.session_state.user_profile["subjects"],
            help="新高考 90% 以上硬核工科强制要求选考物理，部分要求物理+化学。"
        )
        st.session_state.user_profile["subjects"] = subjects

        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            score = st.number_input(
                "预估高考分数（裸分）",
                min_value=300, max_value=750,
                value=st.session_state.user_profile["score"],
                step=5
            )
            st.session_state.user_profile["score"] = score
        with c_sub2:
            rank_pct = st.number_input(
                "全省位次百分比 (如前10%填10)",
                min_value=0.1, max_value=100.0,
                value=st.session_state.user_profile["rank_pct"],
                step=0.5
            )
            st.session_state.user_profile["rank_pct"] = rank_pct

    with col2:
        st.markdown("##### 🚀 核心人生目标与出路偏好")
        target_goal = st.selectbox(
            "你本科毕业后最渴望的主要出路是：",
            options=[
                "大厂高薪与硬核研发（追求高起薪、凭硬技术吃饭，不靠拼爹）",
                "体制内考公考编 / 国企央企（求稳体面，抗风险第一）",
                "医学临床或口腔执业（周期长但越老越吃香，社会地位高）",
                "学术科研与本硕博深造（有志于做科学家、高校学者）",
                "经管商业与金融投资（擅长人际、追求资源整合与商务）"
            ],
            index=0
        )
        st.session_state.user_profile["target_goal"] = target_goal

        family_econ = st.select_slider(
            "家庭经济支持意愿（影响深造与容错空间）",
            options=["工薪家庭（急需本科高就业率）", "中等小康（可支持硕士深造）", "优渥宽裕（无短期变现压力）"],
            value="中等小康（可支持硕士深造）"
        )
        st.session_state.user_profile["family_econ"] = family_econ

    st.markdown("---")
    c_btn1, c_btn2, _ = st.columns([1, 1, 3])
    with c_btn1:
        if st.button("下一步：进入意向评测 ➔", type="primary", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()

# ============================================================================
# 阶段 2：深度志向与行为测评（轻量精准）
# ============================================================================
elif st.session_state.current_step == 2:
    st.markdown('<p class="step-header">🧭 第二步：深度志向与真实微观场景测评</p>', unsafe_allow_html=True)
    st.info("💡 告别 40 道又长又虚的旧问卷！我们精炼了 8 道最能暴露‘真实动手与逻辑天赋’的实战场景，直击底层适配度。")

    q_demo = [
        {
            "id": "Q1",
            "title": "1. 如果周末给你一整天完全自主的时间，你更愿意做下面哪件事？",
            "opts": [
                "A. 跟着教程写一个实用的小脚本、或拆装调试一台数码/机械硬件",
                "B. 针对某个有争议的社会热点事件或历史现象，写一篇长文分析背后的深层原因",
                "C. 组织一帮朋友策划一场短途自驾游，负责统筹行程路线、订房和费用分摊",
                "D. 一个人安安静静画一幅画、剪辑一段氛围感视频、或听音乐沉浸放松"
            ]
        },
        {
            "id": "Q2",
            "title": "2. 面对复杂的数理逻辑问题或代码报错时，你的本能反应通常是：",
            "opts": [
                "A. 极其上头，不查出底层 Bug 或解出最后一步誓不罢休，享受破解谜题的纯粹快感",
                "B. 觉得枯燥繁琐，更希望能直接调用别人做好的现成工具，把精力放在业务应用上",
                "C. 擅长通过和老师/同学沟通交流、听别人讲一遍思路迅速搞懂",
                "D. 比较排斥纯抽象数学推导，更喜欢通过做实验、观察实物来理解"
            ]
        },
        {
            "id": "Q3",
            "title": "3. 关于未来的工作环境，你绝对无法容忍以下哪一种？",
            "opts": [
                "A. 常年在偏远工地板房驻扎、随工程四处漂泊（如传统土木工程）",
                "B. 每天在密闭车间倒班、吸入异味化学试剂（如传统生化环材）",
                "C. 每天无所事事熬时间、靠低效人际周旋和酒局应酬（如空泛行政公关）",
                "D. 每天盯着满屏代码和高强度交付指标，常年加班内卷（如大厂算法/IT）"
            ]
        }
    ]

    for q in q_demo:
        st.markdown(f"**{q['title']}**")
        st.radio("选择你的倾向", options=q["opts"], key=q["id"], label_visibility="collapsed")
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    st.markdown("---")
    c_btn1, c_btn2, _ = st.columns([1, 1, 3])
    with c_btn1:
        if st.button("⬅ 返回上一步", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with c_btn2:
        if st.button("查看推荐结果 ➔", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()

# ============================================================================
# 阶段 3：终极推荐大屏与避坑指南
# ============================================================================
elif st.session_state.current_step == 3:
    st.markdown('<p class="step-header">📊 第三步：终极专业推荐大屏与真实避坑指南</p>', unsafe_allow_html=True)

    # 避坑拦截守护 Banner
    if st.session_state.user_profile.get("enable_pitfall_filter", True):
        with st.expander("🛡️ 避坑排雷守护进行中：系统已为你自动拦截 3 个低实用性/现场艰苦专业", expanded=True):
            st.markdown(
                """
                根据你的硬技术与高薪研发诉求，以下专业已**自动从推荐列表剔除**并替补为硬核工科：<br>
                • ❌ <b>物流管理与工程类</b>：对口就业多为偏远仓储调度与网点现场运营，缺乏技术壁垒，替代性极高。<br>
                • ❌ <b>工业工程类</b>：多为制造业流水线掐秒表、车间现场管理，非高大上运筹算法。<br>
                • ❌ <b>土木类 / 建筑类</b>：受大基建与地产周期下行影响，传统施工需常驻工地板房漂泊，提桶跑路率高。
                """,
                unsafe_allow_html=True
            )

    # 样例核心卡片列表
    cards_data = [
        {
            "rank": "🥇",
            "name": "电子信息类",
            "disc": "工学",
            "hardness": 0.95,
            "hardness_label": "硬核技术工科",
            "utility": "高实用性/硬核壁垒",
            "degree": "芯片/算法研发强考研刚需",
            "warning": "",
            "insight": "半导体芯片、射频通信与嵌入式硬件长期处于国家战略风口。高薪芯片架构岗需考研深造，本科即可进入嵌入式硬件开发与电子技术支持。",
            "majors": [
                {"name": "电子信息工程", "code": "080701", "desc": "软硬件兼通，智能硬件与信号处理底盘极稳"},
                {"name": "集成电路设计与集成系统", "code": "080710T", "desc": "芯片半导体黄金核心赛道，高薪研发刚需"},
                {"name": "微电子科学与工程", "code": "080704", "desc": "物理与半导体材料前沿，专注芯片制造工艺"}
            ],
            "top_schools": ["电子科技大学", "西安电子科技大学", "清华大学", "东南大学", "北京邮电大学"]
        },
        {
            "rank": "🥈",
            "name": "计算机类",
            "disc": "工学",
            "hardness": 0.95,
            "hardness_label": "硬核技术工科",
            "utility": "高实用性/硬核壁垒",
            "degree": "大厂与核心岗建议考研深造",
            "warning": "【现实分化提醒】大厂算法对研究生和名校背景要求极高；普通院校本科就业竞争加剧，大学期间必须狠抓高质量开源项目与工程代码量！",
            "insight": "数字化时代全行业刚需。技术上限极高、靠硬技能立足不拼爹；高端复合型技术人才（AI系统、云计算架构）长远前景依然无可替代。",
            "majors": [
                {"name": "计算机科学与技术", "code": "080901", "desc": "计算机学科全能奠基石，考公考研企业招聘均最硬通货"},
                {"name": "软件工程", "code": "080902", "desc": "重工程实操与架构开发，就业即战力极强"},
                {"name": "人工智能", "code": "080910T", "desc": "紧跟大模型时代，注重算法数学推导与场景落地"}
            ],
            "top_schools": ["清华大学", "北京大学", "浙江大学", "国防科技大学", "北京航空航天大学"]
        },
        {
            "rank": "🥉",
            "name": "自动化类",
            "disc": "工学",
            "hardness": 0.92,
            "hardness_label": "硬核技术工科",
            "utility": "高实用性/硬核壁垒",
            "degree": "本硕皆宜（智能化研发建议读研）",
            "warning": "",
            "insight": "工科中的‘万金油’，软硬兼修。在工业机器人、新能源汽车智造、产线控制方面底盘极稳，双非院校同样就业扎实。",
            "majors": [
                {"name": "自动化", "code": "080801", "desc": "控制理论与工控软件结合，智能制造必不可少"},
                {"name": "机器人工程", "code": "080803T", "desc": "机器人本体控制、机器视觉与运控算法新风口"}
            ],
            "top_schools": ["东北大学", "哈尔滨工业大学", "上海交通大学", "浙江大学"]
        }
    ]

    for c in cards_data:
        st.markdown(
            f"""
            <div class="major-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div>
                        <span style="font-size:22px;font-weight:700;color:#1F2937;">{c['rank']} {c['name']}</span>
                        <span style="font-size:14px;color:#6B7280;margin-left:8px;">({c['disc']})</span>
                    </div>
                    <div>
                        <span class="badge-tag badge-hard">🛠️ {c['hardness_label']} (硬度 {c['hardness']})</span>
                        <span class="badge-tag badge-good">🎯 {c['utility']}</span>
                        <span class="badge-tag badge-info">🎓 {c['degree']}</span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

        if c["warning"]:
            st.markdown(
                f'<div class="warning-box">⚠️ <b>现实提醒</b>: {c["warning"]}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="insight-box">💡 <b>行业真实生态</b>: {c["insight"]}</div>',
            unsafe_allow_html=True
        )

        # 核心专业细分与代表院校
        st.markdown("<div style='margin-top:14px;'><strong>🔬 核心细分专业推荐：</strong></div>", unsafe_allow_html=True)
        m_cols = st.columns(len(c["majors"]))
        for idx, m in enumerate(c["majors"]):
            with m_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;padding:10px;height:100%;">
                        <div style="font-weight:600;color:#1E3A8A;font-size:13px;">{m['name']}</div>
                        <div style="font-size:11px;color:#9CA3AF;margin-bottom:4px;">代号: {m['code']}</div>
                        <div style="font-size:12px;color:#4B5563;">{m['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            f"<div style='margin-top:10px;font-size:12.5px;color:#4B5563;'>"
            f"🏛️ <b>学科顶尖代表院校</b>: {'、'.join(c['top_schools'])}"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬅ 重新调整基础档案与偏好", use_container_width=False):
        st.session_state.current_step = 1
        st.rerun()
