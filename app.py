"""
================================================================================
  高考志愿智能规划与决策系统 v2.0 (Gaokao 2.0)
  极简架构 · 现代美学与微动效 · 就业实用导向 · 招生包装打假 · 全程避坑护航
================================================================================
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from core.recommend_engine import engine

# ============================================================================
# 页面基础配置与高阶美学动效样式
# ============================================================================
st.set_page_config(
    page_title="高考志愿智能规划与决策系统 2.0",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif;
}

/* 入场微动效 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulseGlow {
    0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
    70% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

.fade-in {
    animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* 顶部 Hero 渐变横幅 */
.hero-box {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #4F46E5 100%);
    border-radius: 20px;
    padding: 30px 36px;
    color: #FFFFFF;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
    animation: fadeInUp 0.35s ease-out;
}
.hero-title {
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 14.5px;
    opacity: 0.92;
    line-height: 1.6;
}

/* 步骤进度条胶囊容器 */
.step-progress-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
    background: #F3F4F6;
    border-radius: 14px;
    padding: 6px;
    gap: 8px;
}
.step-capsule {
    flex: 1;
    text-align: center;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 13.5px;
    font-weight: 600;
    color: #6B7280;
    transition: all 0.25s ease;
}
.step-capsule.active {
    background: #FFFFFF;
    color: #1E3A8A;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.step-capsule.completed {
    background: #E0E7FF;
    color: #3730A3;
}

/* 模块分段标题 */
.step-header {
    font-size: 19px;
    font-weight: 700;
    color: #111827;
    border-left: 4px solid #2563EB;
    padding-left: 12px;
    margin: 20px 0 16px 0;
}

/* 题目卡片容器 */
.question-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    animation: fadeInUp 0.3s ease-out;
}
.question-card:hover {
    border-color: #93C5FD;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.08);
}
.question-badge {
    display: inline-block;
    padding: 2px 8px;
    background: #EFF6FF;
    color: #2563EB;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 700;
    margin-bottom: 6px;
}
.question-title {
    font-size: 15px;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 10px;
    line-height: 1.5;
}

/* 专业推荐卡片 */
.major-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 22px;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    animation: fadeInUp 0.4s ease-out;
}
.major-card:hover {
    border-color: #60A5FA;
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.12);
    transform: translateY(-3px);
}

/* 标签徽章 */
.badge-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-hard { background: #EEF2FF; color: #3730A3; border: 1px solid #C7D2FE; }
.badge-warn { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.badge-good { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.badge-info { background: #F0F9FF; color: #075985; border: 1px solid #BAE6FD; }
.badge-purple { background: #FAF5FF; color: #6B21A8; border: 1px solid #E9D5FF; }

/* 招生包装打假 Truth Filter 容器 */
.truth-box {
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 13.5px;
    line-height: 1.6;
}
.truth-label {
    font-weight: 700;
    color: #B45309;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.myth-text {
    color: #92400E;
    text-decoration: line-through;
    opacity: 0.85;
}
.fact-text {
    color: #78350F;
    font-weight: 600;
}

/* 行业洞察底栏 */
.insight-box {
    background: #F8FAFC;
    border-left: 4px solid #2563EB;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-top: 10px;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.6;
}

/* 避坑拦截抽屉 */
.intercept-box {
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 18px;
    animation: fadeInUp 0.3s ease-out;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# 全局会话状态初始化
# ============================================================================
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "score": 605,
        "rank_pct": 8.0,
        "subjects": ["物理", "化学", "生物"],
        "target_goal": "大厂高薪与硬核研发（追求高起薪、凭硬技术吃饭，不靠拼爹）",
        "family_econ": "中等小康（可支持硕士深造）",
        "enable_pitfall_filter": True,
    }

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {
        "Q1": "A", "Q2": "A", "Q3": "A", "Q4": "B",
        "Q5": "A", "Q6": "A", "Q7": "A", "Q8": "A",
        "Q9": "B", "Q10": "A", "Q11": "A", "Q12": "A"
    }

# ============================================================================
# 顶部 Hero Banner
# ============================================================================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🎓 高考志愿智能规划与决策系统 2.0</div>
        <div class="hero-subtitle">
            基于真实就业大数据 · 招生简章包装打假 (Truth Filter) · 严格工科硬度分级 · 12 道微观实战情境直击底层天赋
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 阶段指示器
c_step1 = "step-capsule active" if st.session_state.current_step == 1 else ("step-capsule completed" if st.session_state.current_step > 1 else "step-capsule")
c_step2 = "step-capsule active" if st.session_state.current_step == 2 else ("step-capsule completed" if st.session_state.current_step > 2 else "step-capsule")
c_step3 = "step-capsule active" if st.session_state.current_step == 3 else "step-capsule"

st.markdown(
    f"""
    <div class="step-progress-bar">
        <div class="{c_step1}">1️⃣ 确立考生基本盘与出路诉求</div>
        <div class="{c_step2}">2️⃣ 12道微观情境评测 (测天赋/排雷)</div>
        <div class="{c_step3}">3️⃣ 终极专业大屏与打假报告</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# 侧边栏：极简模式导航与全局排雷守护
# ============================================================================
with st.sidebar:
    st.markdown("### 🧭 规划阶段")
    nav_step = st.radio(
        "切换阶段",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: "1️⃣ 考生档案与核心诉求",
            2: "2️⃣ 12道微观情境测评",
            3: "3️⃣ 终极推荐与打假大屏"
        }[x],
        index=st.session_state.current_step - 1,
        label_visibility="collapsed"
    )
    if nav_step != st.session_state.current_step:
        st.session_state.current_step = nav_step
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛡️ 全局排雷守护引擎")
    pitfall_toggle = st.toggle(
        "开启「高考志愿避坑排雷」守护",
        value=st.session_state.user_profile.get("enable_pitfall_filter", True),
        help="自动拦截物流管理、工业工程、传统土木建筑、生化环材车间等低实用性或艰苦方向，替补优质高壁垒硬工科与高薪专业。"
    )
    st.session_state.user_profile["enable_pitfall_filter"] = pitfall_toggle

    st.caption("💡 **避坑排雷已启动**：系统将从底层阻断‘挂羊头卖狗肉’的伪工科与夕阳方向，优先确保专业能学到真技术。")

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
            help="新高考 90% 以上硬核工科强制要求选考物理，医学多数强制物化双选。"
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
                "全省位次百分比 (如前8%填8.0)",
                min_value=0.1, max_value=100.0,
                value=st.session_state.user_profile["rank_pct"],
                step=0.5
            )
            st.session_state.user_profile["rank_pct"] = rank_pct

    with col2:
        st.markdown("##### 🚀 核心人生目标与出路偏好")
        target_goal = st.selectbox(
            "本科毕业后你最渴望的主要出路是：",
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
            "家庭经济支持意愿（影响深造容错与战线长短）",
            options=["工薪家庭（急需本科高质量就业赚钱）", "中等小康（可支持硕士深造）", "优渥宽裕（无短期变现压力）"],
            value=st.session_state.user_profile.get("family_econ", "中等小康（可支持硕士深造）")
        )
        st.session_state.user_profile["family_econ"] = family_econ

    st.markdown("---")
    c_btn1, c_btn2, _ = st.columns([1.2, 1.2, 3])
    with c_btn1:
        if st.button("进入 12 道微观实战情境评测 ➔", type="primary", use_container_width=True):
            if not st.session_state.user_profile["subjects"]:
                st.warning("⚠️ 请至少选择 3 门新高考选考科目！已为你重置为默认组合【物理、化学、生物】。")
                st.session_state.user_profile["subjects"] = ["物理", "化学", "生物"]
            st.session_state.current_step = 2
            st.rerun()

# ============================================================================
# 阶段 2：12 道深度微观实战情境评测
# ============================================================================
elif st.session_state.current_step == 2:
    st.markdown('<p class="step-header">🧭 第二步：12 道微观实战情境评测（直击天赋与排雷一票否决）</p>', unsafe_allow_html=True)
    st.info("💡 **评测设计准则**：不问抽象概念，通过 12 个真实生活微观冲突与选择，测算你的数理死磕耐受、动手本能、考公适配与避坑底线。")

    # 12 道题目定义
    quiz_data = [
        # --- 模块一 ---
        {
            "id": "Q1",
            "module": "模块一：认知本能与动手天赋",
            "title": "1. 周末给你一整天完全自主的时间，没有任何外部打扰，你最愿意沉浸在哪件事中？",
            "opts": [
                ("A", "A. 跟着教程写一个实用的小脚本/爬虫，或拆装调试一台数码/机械硬件"),
                ("B", "B. 针对某个有争议的社会热点事件或历史现象，写一篇长文分析背后的深层原因"),
                ("C", "C. 组织一帮朋友策划一场短途自驾游，负责统筹行程路线、订房和费用分摊"),
                ("D", "D. 一个人安安静静画一幅画、剪辑一段精细的氛围感视频、或听音乐沉浸创作")
            ]
        },
        {
            "id": "Q2",
            "module": "模块一：认知本能与动手天赋",
            "title": "2. 面对极其复杂的数理逻辑难题或一段报错连连的代码时，你的本能情绪通常是：",
            "opts": [
                ("A", "A. 极其上头，不查出底层 Bug 或推导出最后一步誓不罢休，享受破解谜题的纯粹快感"),
                ("B", "B. 觉得枯燥繁琐，更希望能直接调用别人做好的现成工具，把精力放在业务功能实现上"),
                ("C", "C. 擅长通过和老师/同学沟通交流，听别人把思路拆解一遍自己就能迅速搞懂"),
                ("D", "D. 比较排斥纯纸面抽象数学推导，更喜欢通过做实验、观察实物和物理模型来理解")
            ]
        },
        {
            "id": "Q3",
            "module": "模块一：认知本能与动手天赋",
            "title": "3. 面对家里一台发生故障的电器、机械设备或自行车，你的第一反应是：",
            "opts": [
                ("A", "A. 兴奋地拿起螺丝刀拆开，研究内部机械构件或电路板，动手修好极具成就感"),
                ("B", "B. 完全不想弄脏手，倾向于上网查软件设置或直接叫售后专业师傅来修"),
                ("C", "C. 习惯性计算这台设备的折旧成本、维修费用与买新机器的性价比账本"),
                ("D", "D. 对内部机械构件不感冒，只关注该设备的外观工业美学设计与人机交互手感")
            ]
        },
        {
            "id": "Q4",
            "module": "模块一：认知本能与动手天赋",
            "title": "4. 如果进入大学深入学习，你更期待哪种知识带来的成就感？",
            "opts": [
                ("A", "A. 纸面上严谨优美的公理定理证明，探究宇宙底层物理法则或前沿数学猜想"),
                ("B", "B. 亲手把图纸零件车出来、电路焊出来、代码部署上线跑通解决实际工程问题"),
                ("C", "C. 深入研读法律条款、社会体制演进与公共政策制定逻辑"),
                ("D", "D. 拆解经典的商业战役案例、资本运作杠杆与企业战略博弈")
            ]
        },
        # --- 模块二 ---
        {
            "id": "Q5",
            "module": "模块二：人际博弈与职业出路诉求",
            "title": "5. 一整天高强度学习或工作后，以下哪种情境最能让你感到充实而不是内耗？",
            "opts": [
                ("A", "A. 独自一人对着电脑或实验仪器，安静地把一套复杂系统/功能搭顺畅了"),
                ("B", "B. 面对面为一个具体的受助者解决实际疾苦（如解答疑难、排忧解难、治愈痛苦）"),
                ("C", "C. 在商务谈判、组织协调或公开演讲中成功说服并引导了大家"),
                ("D", "D. 独自坐在图书馆查阅海量档案文献，整理出一份严谨的考据报告")
            ]
        },
        {
            "id": "Q6",
            "module": "模块二：人际博弈与职业出路诉求",
            "title": "6. 团队负责的核心项目突然在交付前夜发生重大紧急事故，你的第一反应是：",
            "opts": [
                ("A", "A. 极度冷静，第一时间抓包查看系统底层日志，定位具体代码或硬件短路点"),
                ("B", "B. 第一时间安抚受影响各方情绪，迅速建立跨部门协同沟通链协调资源"),
                ("C", "C. 严格对照应急预案条例与责任清单，按合规程序向上汇报与处置"),
                ("D", "D. 迅速研判可能带来的商业利润损失，寻找最低成本的折中商业止损方案")
            ]
        },
        {
            "id": "Q7",
            "module": "模块二：人际博弈与职业出路诉求",
            "title": "7. 你最希望依靠什么建立自己抵御中年危机的人生护城河？",
            "opts": [
                ("A", "A. 掌握不可替代的硬核工程技术壁垒，走到哪里都凭真本事吃饭，不看任何人脸色"),
                ("B", "B. 考入国家核心体制内或大型垄断央国企，编制在身，旱涝保收抗周期"),
                ("C", "C. 考取准入门槛极高、具有法定排他性的行业执业牌照（如医生/律师），越老越吃香"),
                ("D", "D. 凭借敏锐的商业直觉撬动资本与资源杠杆，博取高爆发的财富回报")
            ]
        },
        {
            "id": "Q8",
            "module": "模块二：人际博弈与职业出路诉求",
            "title": "8. 关于未来进入体制内考公务员或事业单位编制，你的真实心态是：",
            "opts": [
                ("A", "A. 绝对不想进体制，厌烦按资排辈与繁文缛节，渴望在硬核技术市场竞争中拿高薪"),
                ("B", "B. 坚定追求考公考编，希望大学所选专业是体制内招考岗位最多的‘硬通货大户’"),
                ("C", "C. 将体制内视为兜底选项，优先去大厂或企业闯荡，若行业受阻再考虑考编"),
                ("D", "D. 渴望进入大学或高端智库当编制内学者/高校教师，享受学术殿堂声誉")
            ]
        },
        # --- 模块三 ---
        {
            "id": "Q9",
            "module": "模块三：长期主义与避坑一票否决",
            "title": "9. 关于大学毕业后的学历提升与深造规划，你的家庭与个人心理承受力是：",
            "opts": [
                ("A", "A. 必须本科毕业立即高质量变现就业，家庭需要我尽快产生稳定现金流"),
                ("B", "B. 乐意读硕士（2~3年），希望靠硕士学历敲开头部大厂或中高端研发院所的大门"),
                ("C", "C. 坚定接受硕博连读长周期深造（5~8年），无惧长达数年的学术冷板凳"),
                ("D", "D. 边工作边考在职研究生或行业认证，更看重真实职场摸爬滚打")
            ]
        },
        {
            "id": "Q10",
            "module": "模块三：长期主义与避坑一票否决",
            "title": "10. 你如何看待现代职场的技能半衰期与‘35岁危机’？",
            "opts": [
                ("A", "A. 能接受年轻时高强度吃青春饭赚取高额起薪和第一桶金，后续靠资产积累或管理转型"),
                ("B", "B. 极度看重‘资产沉淀属性’，宁可起步阶段起薪平平，但必须每一年经验都在增加自身议价权"),
                ("C", "C. 追求体制内或大型央企的制度性保护，彻底免疫外部裁员与技能过时风暴"),
                ("D", "D. 坚信持续终身学习能力，只要扎根在国家战略急需的底层核心技术赛道就不会被淘汰")
            ]
        },
        {
            "id": "Q11",
            "module": "模块三：长期主义与避坑一票否决",
            "title": "11. 【工作环境一票否决】如果以下工作环境要求你必须呆满 5 年以上，你绝对无法容忍哪一个？",
            "opts": [
                ("A", "A. 常年在偏远山区项目板房驻扎、随工程四处漂泊无固定住所（传统土木/水利工程）"),
                ("B", "B. 每天在密闭车间倒班、吸入异味化学试剂/粉尘（传统化工/生化环材车间）"),
                ("C", "C. 每天处理低效繁琐的人际周旋、端茶倒水写空话汇报、看领导脸色熬资历（空泛文秘行政）"),
                ("D", "D. 每天对着满屏代码与高强度交付指标，常年熬夜内卷、严重透支睡眠（高压大厂IT）")
            ]
        },
        {
            "id": "Q12",
            "module": "模块三：长期主义与避坑一票否决",
            "title": "12. 【职业生态陷阱排雷】在大学学习与后续就业中，你最害怕掉入以下哪种‘现实陷阱’？",
            "opts": [
                ("A", "A. ‘挂羊头卖狗肉’陷阱：名字听起来是现代高科技，进厂实则是流水线掐秒表或偏远快递站理货"),
                ("B", "B. ‘学历严重贬值’陷阱：本科毕业根本找不到对口研发岗，必须卷到名校博士，否则只能干销售质检"),
                ("C", "C. ‘考公炮灰’陷阱：听信文科好考公，毕业才发现没有定向招考岗位，只能去卷上千人争一个的‘三不限’"),
                ("D", "D. ‘重度看背景人脉’陷阱：行业天花板极度依赖家庭背景与社会关系网，平民子弟很难出头")
            ]
        }
    ]

    current_module = ""
    for q in quiz_data:
        if q["module"] != current_module:
            current_module = q["module"]
            st.markdown(f"#### 🏷️ {current_module}")

        default_opt_index = 0
        current_saved = st.session_state.quiz_answers.get(q["id"], "A")
        for idx, (opt_val, opt_label) in enumerate(q["opts"]):
            if opt_val == current_saved:
                default_opt_index = idx
                break

        chosen = st.radio(
            q["title"],
            options=[opt[0] for opt in q["opts"]],
            format_func=lambda x, opts=dict(q["opts"]): opts[x],
            index=default_opt_index,
            key=f"widget_{q['id']}"
        )
        st.session_state.quiz_answers[q["id"]] = chosen
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    st.markdown("---")
    c_btn1, c_btn2, _ = st.columns([1, 1.4, 2.6])
    with c_btn1:
        if st.button("⬅ 返回第一步", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with c_btn2:
        if st.button("动态计算并查看推荐大屏 ➔", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()

# ============================================================================
# 阶段 3：终极推荐大屏与招生包装打假报告 (动态计算)
# ============================================================================
elif st.session_state.current_step == 3:
    st.markdown('<p class="step-header">📊 第三步：终极专业推荐大屏与招生打假报告</p>', unsafe_allow_html=True)

    # 动态调用推荐算法引擎
    top_recommendations, intercepted_pitfalls = engine.calculate_recommendations(
        st.session_state.user_profile,
        st.session_state.quiz_answers
    )

    # 避坑拦截守护 Banner
    if st.session_state.user_profile.get("enable_pitfall_filter", True) and intercepted_pitfalls:
        with st.expander(f"🛡️ 避坑排雷守护进行中：系统已为你自动拦截 {len(intercepted_pitfalls)} 个低实用性/艰苦/伪工科专业", expanded=True):
            st.markdown("根据你的选科、硬技术诉求及 **Q11/Q12 一票否决排斥项**，以下专业已被**底层拦截**并替补为硬核高壁垒专业：")
            for item in intercepted_pitfalls:
                st.markdown(
                    f"""
                    <div style="margin-bottom:8px;font-size:13.5px;">
                        • ❌ <b>{item['name']}</b>：<span style="color:#B91C1C;">{item['reason']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("### 🏆 专属精准推荐专业 Top 5")

    # 循环渲染 Top 推荐卡片
    for c in top_recommendations:
        st.markdown(
            f"""
            <div class="major-card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:12px;gap:8px;">
                    <div>
                        <span style="font-size:23px;font-weight:800;color:#111827;">{c['rank']} {c['name']}</span>
                        <span style="font-size:13px;color:#6B7280;margin-left:8px;">(综合匹配评分: {c['score']})</span>
                    </div>
                    <div>
                        <span class="badge-tag badge-hard">🛠️ {c['hardness_label']} (硬度 {c['hardness']})</span>
                        <span class="badge-tag badge-good">🎯 {c['utility']}</span>
                        <span class="badge-tag badge-info">🎓 {c['degree']}</span>
                        <span class="badge-tag badge-purple">⏳ {c['experience_value']}</span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

        # 考公真实属性标签
        st.markdown(
            f"""
            <div style="margin-bottom:8px;font-size:13px;color:#4B5563;">
                🏛️ <b>体制内考公考编真实属性</b>: <span style="font-weight:600;color:#1E3A8A;">{c['civil_service_tag']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 招生包装打假 (Truth Filter) 核心特色区域
        st.markdown(
            f"""
            <div class="truth-box">
                <div class="truth-label">🔥 【招生简章包装打假 / 谎言滤镜】</div>
                <div style="margin-bottom:4px;">
                    <span style="font-weight:600;color:#92400E;">宣称包装: </span>
                    <span class="myth-text">“{c['marketing_myth']}”</span>
                </div>
                <div>
                    <span style="font-weight:600;color:#166534;">真实日常打假: </span>
                    <span class="fact-text">{c['truth_unfiltered']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 行业真实生态与生命周期
        st.markdown(
            f"""
            <div class="insight-box">
                💡 <b>行业真实生态与出路</b>: {c['insight']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 核心细分专业
        if c.get("majors") and len(c["majors"]) > 0:
            st.markdown("<div style='margin-top:14px;font-size:13.5px;'><strong>🔬 核心细分推荐专业：</strong></div>", unsafe_allow_html=True)
            m_cols = st.columns(len(c["majors"]))
            for idx, m in enumerate(c["majors"]):
                with m_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:10px 12px;height:100%;">
                            <div style="font-weight:700;color:#1E3A8A;font-size:13.5px;">{m['name']}</div>
                            <div style="font-size:11px;color:#9CA3AF;margin-bottom:3px;">代码: {m['code']}</div>
                            <div style="font-size:12px;color:#4B5563;">{m['desc']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # 学科评估前列代表院校与择校梯队提示
        top_schools_str = "、".join(c["top_schools"]) if c.get("top_schools") else "清华大学、浙江大学、上海交通大学"
        user_rank = st.session_state.user_profile.get("rank_pct", 10.0)
        tier_tip = "冲刺全国顶尖 985" if user_rank <= 3.0 else ("主打强势 985 与 头部 211 稳妥" if user_rank <= 10.0 else "关注骨干 211 与强势特色单科院校保底")

        st.markdown(
            f"""
            <div style="margin-top:12px;font-size:13px;color:#374151;display:flex;justify-content:space-between;flex-wrap:wrap;background:#F8FAFC;padding:8px 12px;border-radius:8px;">
                <div>🏛️ <b>第四轮学科评估顶尖代表院校</b>: <span style="font-weight:600;color:#1E3A8A;">{top_schools_str}</span></div>
                <div>🎯 <b>结合位次 (前{user_rank}%) 报考策略</b>: <span style="font-weight:700;color:#2563EB;">{tier_tip}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    c_back1, c_back2 = st.columns([1.2, 3])
    with c_back1:
        if st.button("⬅ 重新调整问卷与选项", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
