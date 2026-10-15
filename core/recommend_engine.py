# -*- coding: utf-8 -*-
"""
================================================================================
  Gaokao 2.0 推荐算法引擎 (Hierarchical Gated Funnel Architecture - HGFA 2.0)
  选科硬性过滤 · 12道微观情境多维加权 · 纯理科研保护 · 避坑排雷一票否决 · 大类多样性保全
================================================================================
"""

import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if (BASE_DIR / "data").exists():
    DATA_DIR = BASE_DIR / "data"
elif (BASE_DIR.parent / "data").exists():
    DATA_DIR = BASE_DIR.parent / "data"
else:
    DATA_DIR = BASE_DIR / "data"

class GaokaoRecommendEngine:
    def __init__(self):
        self.insights = self._load_insights()
        self.majors_df = self._load_majors_df()
        self.top_schools_df = self._load_top_schools_df()
        
    def _load_insights(self):
        insights_file = DATA_DIR / "category_reality_insights.json"
        if insights_file.exists():
            with open(insights_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_majors_df(self):
        majors_file = DATA_DIR / "gaokao_majors.xlsx"
        if majors_file.exists():
            try:
                df = pd.read_excel(majors_file)
                df.columns = [str(c).strip() for c in df.columns]
                return df
            except Exception as e:
                print(f"Error loading majors: {e}")
        return pd.DataFrame()

    def _load_top_schools_df(self):
        schools_file = DATA_DIR / "major_top_schools.xlsx"
        if schools_file.exists():
            try:
                df = pd.read_excel(schools_file)
                df.columns = [str(c).strip() for c in df.columns]
                return df
            except Exception as e:
                print(f"Error loading top schools: {e}")
        return pd.DataFrame()

    def get_representative_majors(self, category_name):
        """根据大类名称在 gaokao_majors.xlsx 中提取代表细分专业 (Top 3)"""
        if self.majors_df.empty:
            return []
        
        kw = category_name.replace("类", "")
        matched = self.majors_df[self.majors_df["专业类"].str.contains(kw, na=False)]
        if matched.empty:
            matched = self.majors_df[self.majors_df["专业类"] == category_name]
            
        results = []
        for _, row in matched.head(3).iterrows():
            code = str(row.get("专业代码", "")).strip()
            name = str(row.get("专业名称", "")).strip()
            results.append({
                "code": code,
                "name": name,
                "desc": f"国家标准专业代码 {code}"
            })
        return results

    def get_top_schools(self, category_name):
        """根据大类名称在 major_top_schools.xlsx 寻找评估前列代表高校"""
        if self.top_schools_df.empty:
            return []
        
        kw = category_name.replace("类", "")
        # 学科精确匹配，杜绝“法”命中“书法学/中国美术学院”
        matched = self.top_schools_df[
            self.top_schools_df["学科"].str.strip() == kw
        ]
        
        if matched.empty:
            matched = self.top_schools_df[
                self.top_schools_df["专业"].str.startswith(kw, na=False)
            ]
        
        if matched.empty:
            matched = self.top_schools_df[
                (self.top_schools_df["学科"].str.contains(kw, na=False)) &
                (~self.top_schools_df["学科"].str.contains("美术|书法|艺术", na=False))
            ]
        
        if matched.empty:
            return ["清华大学", "北京大学", "浙江大学", "上海交通大学", "复旦大学"]
        
        priority_order = {"A+": 0, "A": 1, "A-": 2, "A–": 2, "B+": 3}
        matched = matched.copy()
        matched["_rank"] = matched["档次"].map(priority_order).fillna(4)
        matched = matched.sort_values("_rank")
            
        schools = matched["学校"].dropna().unique().tolist()
        return schools[:5]

    def _get_broad_cluster(self, cat_name):
        """获取学科一级集群"""
        if any(w in cat_name for w in ["计算机", "电子信息", "自动化", "软件"]):
            return "信息工科"
        if any(w in cat_name for w in ["电气", "机械", "土木", "水利", "化工", "材料", "建筑", "航空", "兵器", "仪器"]):
            return "传统/重工业工科"
        if any(w in cat_name for w in ["临床医学", "基础医学", "口腔医学", "中医学", "中西医", "药学", "医学技术", "护理学"]):
            return "医学医药"
        if any(w in cat_name for w in ["数学", "物理学", "天文学", "化学", "生物科学", "力学", "地球物理", "地质学", "地理科学"]):
            return "数理自科"
        if any(w in cat_name for w in ["金融", "经济", "财政", "工商管理", "管理科学", "会计", "电子商务", "市场营销", "旅游管理", "物流管理"]):
            return "经管商科"
        if any(w in cat_name for w in ["法学", "政治学", "马克思", "公共管理", "公安学", "社会学"]):
            return "法政社科"
        if any(w in cat_name for w in ["中国语言", "外国语言", "新闻", "历史", "哲学"]):
            return "文史哲传媒"
        if any(w in cat_name for w in ["艺术", "设计", "音乐", "美术", "戏剧"]):
            return "艺术设计"
        return "综合应用"

    def calculate_recommendations(self, user_profile, answers):
        """
        核心分层门控漏斗推荐算法 (HGFA 2.0)
        :param user_profile: dict, 包含 score, rank_pct, subjects, target_goal, family_econ, enable_pitfall_filter
        :param answers: dict, 键 Q1~Q12, 值为选中的选项字符 'A', 'B', 'C', 'D'
        :return: (top_recommendations, intercepted_pitfalls)
        """
        subjects = user_profile.get("subjects") or ["物理", "化学", "生物"]
        has_physics = "物理" in subjects
        has_chem = "化学" in subjects
        target_goal = user_profile.get("target_goal", "")
        family_econ = user_profile.get("family_econ", "")
        enable_pitfall = user_profile.get("enable_pitfall_filter", True)

        scores = {}
        intercepted = []

        # 是否选择专用专属通道
        is_medical_channel = "医学临床或口腔" in target_goal
        is_business_channel = "经管商业与金融投资" in target_goal
        is_open_explore = ("尚不明确" in target_goal or "开放探索" in target_goal or not target_goal)

        # 遍历所有 94 个专业大类
        for cat, info in self.insights.items():
            cat_score = 50.0  # 基准起步分
            hardness = info.get("engineering_hardness", 0.5)
            is_pitfall = info.get("is_pitfall", False)
            cluster = self._get_broad_cluster(cat)

            # ----------------------------------------------------
            # 1. 选科硬性物理/化学一票否决
            # ----------------------------------------------------
            # 硬工科一票否决
            if (hardness >= 0.75 or info.get("hardness_label") == "硬核工科") and not has_physics:
                continue

            # 严格理论自科物理一票否决 (天文学/物理学/力学/地球物理学必须选物理)
            if cat in ["物理学类", "天文学类", "力学类", "地球物理学类", "地质学类"] and not has_physics:
                continue

            # 临床与口腔医学：绝大多数省份强制要求 物理 + 化学 双选
            if cat in ["临床医学类", "口腔医学类"] and not (has_physics and has_chem):
                continue

            # ----------------------------------------------------
            # 2. 专属通道过滤 (若考生在第一步明确指定了强专业壁垒通道)
            # ----------------------------------------------------
            if is_medical_channel and cluster != "医学医药":
                # 考生已明确要求医科临床执业通道，排除非医学专业进入 Top 竞争
                continue

            # ----------------------------------------------------
            # 3. 避坑全局过滤与反向微观情境一票否决
            # ----------------------------------------------------
            should_intercept = False
            intercept_reason = ""

            # 全局避坑开关
            if enable_pitfall and is_pitfall:
                should_intercept = True
                intercept_reason = info.get("pitfall_warning", "该方向受行业下行周期或低壁垒替代影响，已被全局避坑守护拦截。")

            # Q11: 工作环境一票否决
            q11_ans = answers.get("Q11", "")
            if "A" in q11_ans and cat in ["土木类", "水利类", "建筑类", "地质类", "矿业类", "交通运输类"]:
                should_intercept = True
                intercept_reason = "【命中了你的环境排斥项】你明确表示无法忍受常年驻扎偏远工地板房与工程四处漂泊。"
            elif "B" in q11_ans and cat in ["化工与制药类", "材料类", "轻工类", "纺织类", "生物工程类"]:
                should_intercept = True
                intercept_reason = "【命中了你的环境排斥项】你明确表示无法忍受密闭车间倒班、吸入异味化学试剂与粉尘。"
            elif "C" in q11_ans and cat in ["公共管理类", "工商管理类", "社会学类"]:
                cat_score -= 30.0
            elif "D" in q11_ans and cat in ["计算机类", "电子信息类", "软件工程"]:
                # 考生明确排斥满屏代码与高压大厂熬夜内卷
                cat_score -= 35.0

            # Q12: 职业陷阱一票否决
            q12_ans = answers.get("Q12", "")
            if "A" in q12_ans and cat in ["物流管理与工程类", "工业工程类", "电子商务类"]:
                should_intercept = True
                intercept_reason = "【命中了你的陷阱排斥项】你明确排斥‘挂羊头卖狗肉’、进厂掐秒表或偏远快递站理货的虚假高大上专业。"
            elif "B" in q12_ans and cat in ["生物科学类", "环境科学与工程类", "化学类"]:
                cat_score -= 30.0
            elif "C" in q12_ans and cat in ["哲学类", "社会学类", "公共管理类"]:
                cat_score -= 30.0
            elif "D" in q12_ans and cat in ["金融学类", "工商管理类"]:
                cat_score -= 25.0

            if should_intercept:
                intercepted.append({
                    "name": cat,
                    "reason": intercept_reason if intercept_reason else info.get("pitfall_warning", "低实用性与高壁垒替代风险"),
                    "truth": info.get("truth_unfiltered", "")
                })
                continue

            # ----------------------------------------------------
            # 4. 核心出路偏好打分 (Target Goal - 若为“尚不明确/开放探索”则零干扰)
            # ----------------------------------------------------
            if not is_open_explore:
                if "大厂高薪与硬核研发" in target_goal:
                    if hardness >= 0.88:
                        cat_score += 35.0
                    elif hardness >= 0.75:
                        cat_score += 20.0
                    elif cluster in ["文史哲传媒", "法政社科"]:
                        cat_score -= 20.0
                elif "体制内考公考编" in target_goal:
                    if cat in ["中国语言文学类", "法学类", "马克思主义理论类", "电气类", "计算机类", "公共管理类"]:
                        cat_score += 35.0
                    elif cluster in ["传统/重工业工科", "艺术设计"]:
                        cat_score -= 15.0
                elif "学术科研与本硕博深造" in target_goal:
                    if cluster == "数理自科" or cat in ["力学类", "航空航天类", "哲学类", "历史学类"]:
                        cat_score += 35.0
                    elif hardness >= 0.85:
                        cat_score += 15.0
                elif "经管商业与金融投资" in target_goal:
                    if cluster == "经管商科":
                        cat_score += 45.0
                    else:
                        cat_score -= 25.0

            # ----------------------------------------------------
            # 5. 12 道微观情境评测平衡打分体系
            # ----------------------------------------------------
            # Q1 自主精力分配
            q1 = answers.get("Q1", "")
            if "A" in q1: # 敲代码拆数码
                if cat in ["计算机类", "电子信息类", "自动化类"]: cat_score += 22.0
            elif "B" in q1: # 长文分析社科热点
                if cat in ["中国语言文学类", "法学类", "新闻传播学类", "历史学类", "社会学类"]: cat_score += 20.0
            elif "C" in q1: # 统筹自驾游预算路书
                if cat in ["工商管理类", "金融学类", "经济与贸易类", "管理科学与工程类", "旅游管理类"]: cat_score += 22.0
            elif "D" in q1: # 视听剪辑
                if cluster == "艺术设计" or cat in ["新闻传播学类", "戏剧与影视学类"]: cat_score += 25.0

            # Q2 遇Bug报错反应
            q2 = answers.get("Q2", "")
            if "A" in q2: # 底层死磕
                if cat in ["计算机类", "数学类", "电子信息类"]: cat_score += 20.0
            elif "B" in q2: # 现成工具搭积木业务
                if cat in ["自动化类", "管理科学与工程类", "机械类"]: cat_score += 18.0
            elif "C" in q2: # 沟通点拨
                if cat in ["新闻传播学类", "工商管理类", "公共管理类", "法学类"]: cat_score += 15.0
            elif "D" in q2: # 实体观察
                if cat in ["机械类", "仪器类", "交通运输类", "临床医学类"]: cat_score += 20.0

            # Q3 动手实操
            q3 = answers.get("Q3", "")
            if "A" in q3: # 拆开修好电器
                if cat in ["电气类", "机械类", "自动化类", "电子信息类"]: cat_score += 22.0
            elif "B" in q3: # 查说明书与质保法条
                if cat in ["中国语言文学类", "法学类", "公共管理类"]: cat_score += 18.0
            elif "C" in q3: # 算经济账
                if cat in ["金融学类", "经济学类", "统计学类", "财政学类"]: cat_score += 22.0
            elif "D" in q3: # 外观设计工业美学
                if cat in ["设计学类", "建筑类"]: cat_score += 22.0

            # Q4 理论 vs 工程 vs 规则 vs 商业 (关键分水岭)
            q4 = answers.get("Q4", "")
            if "A" in q4: # 理论推导公理证明 (纯理科学家)
                if cat in ["数学类", "物理学类", "天文学类", "力学类", "统计学类"]: cat_score += 32.0
            elif "B" in q4: # 软硬件交付交付跑通
                if hardness >= 0.82: cat_score += 24.0
            elif "C" in q4: # 法律体制权责规则
                if cat in ["法学类", "政治学类", "公共管理类", "社会学类"]: cat_score += 25.0
            elif "D" in q4: # 商业战役与现金流
                if cat in ["金融学类", "经济学类", "工商管理类", "经济与贸易类"]: cat_score += 25.0

            # Q5 心理能量来源
            q5 = answers.get("Q5", "")
            if "A" in q5: # 独自对系统
                if hardness >= 0.85 or cat in ["数学类", "物理学类"]: cat_score += 18.0
            elif "B" in q5: # 面对面帮人治愈
                if cluster == "医学医药" or cat in ["心理学类", "社会工作"]: cat_score += 26.0
            elif "C" in q5: # 商务谈判说服达成交易
                if cat in ["工商管理类", "金融学类", "国际经济与贸易类", "市场营销"]: cat_score += 22.0
            elif "D" in q5: # 图书馆独立考据与文献对话
                if cat in ["历史学类", "哲学类", "中国语言文学类", "图书情报与档案管理类"]: cat_score += 25.0

            # Q6 危机应对本能
            q6 = answers.get("Q6", "")
            if "A" in q6: # 查日志找根因
                if cat in ["计算机类", "机械类", "电气类", "自动化类"]: cat_score += 18.0
            elif "B" in q6: # 召开多方沟通会控制舆情
                if cat in ["新闻传播学类", "工商管理类", "公共管理类"]: cat_score += 18.0
            elif "C" in q6: # 制度红头文件与合规条款
                if cat in ["法学类", "马克思主义理论类", "公安学类"]: cat_score += 20.0
            elif "D" in q6: # 财务敞口与止损保底
                if cat in ["金融学类", "经济学类", "管理科学与工程类"]: cat_score += 20.0

            # Q7 职业安全感来源
            q7 = answers.get("Q7", "")
            if "A" in q7: # 硬核技术凭手艺
                if hardness >= 0.85: cat_score += 24.0
            elif "B" in q7: # 编制在身抗周期
                if cat in ["中国语言文学类", "马克思主义理论类", "法学类", "电气类", "公共管理类"]: cat_score += 24.0
            elif "C" in q7: # 执照越老越吃香
                if cat in ["临床医学类", "口腔医学类", "中医学类", "建筑类"]: cat_score += 26.0
                elif cat == "法学类": cat_score += 14.0
            elif "D" in q7: # 商业直觉撬动杠杆
                if cat in ["金融学类", "经济与贸易类", "工商管理类"]: cat_score += 25.0

            # Q8 考公考编心态
            q8 = answers.get("Q8", "")
            if "A" in q8: # 坚决去市场化高回报
                if hardness >= 0.82: cat_score += 18.0
                if cluster == "经管商科": cat_score += 15.0
                if cat in ["中国语言文学类", "马克思主义理论类"]: cat_score -= 18.0
            elif "B" in q8: # 坚定考公
                if cat in ["法学类", "中国语言文学类", "马克思主义理论类", "公共管理类", "电气类", "计算机类"]: cat_score += 24.0
            elif "C" in q8: # 企业为主体制兜底
                if hardness >= 0.82: cat_score += 12.0
                if cat in ["法学类", "计算机类", "电气类"]: cat_score += 10.0
            elif "D" in q8: # 高校学者与科研讲师
                if cat in ["数学类", "物理学类", "天文学类", "化学类", "历史学类", "哲学类"]: cat_score += 28.0

            # Q9 考研战线意向与家庭经济
            q9 = answers.get("Q9", "")
            if "A" in q9 or "急需本科" in family_econ: # 急需本科变现
                if cat in ["电气类", "自动化类", "电子信息类", "计算机类", "机械类"]:
                    cat_score += 22.0
                elif cat in ["临床医学类", "物理学类", "生物科学类", "基础医学类"]:
                    cat_score -= 30.0 # 培养周期极长，重罚
            elif "B" in q9: # 读硕2~3年
                if cat in ["计算机类", "电子信息类", "自动化类", "金融学类", "管理科学与工程类"]:
                    cat_score += 16.0
            elif "C" in q9: # 接受硕博长期深造
                if cat in ["临床医学类", "口腔医学类", "数学类", "物理学类", "航空航天类", "基础医学类"]:
                    cat_score += 26.0
            elif "D" in q9: # 边工作边考证
                if cat in ["工商管理类", "金融学类", "经济与贸易类", "法学类"]:
                    cat_score += 15.0

            # Q10 35岁危机与经验保质期
            q10 = answers.get("Q10", "")
            if "A" in q10: # 青春红利高爆发
                if cat in ["计算机类", "电子信息类", "软件工程"]:
                    cat_score += 22.0
            elif "B" in q10: # 越老越吃香技能沉淀
                if cat in ["临床医学类", "口腔医学类", "中医学类", "电气类", "机械类"]:
                    cat_score += 24.0
                elif cat == "法学类":
                    cat_score += 14.0
            elif "C" in q10: # 体制内保护免疫裁员
                if cat in ["中国语言文学类", "法学类", "马克思主义理论类", "电气类", "公共管理类"]:
                    cat_score += 20.0
            elif "D" in q10: # 终身学习核心硬核赛道
                if cat in ["自动化类", "航空航天类", "仪器类", "电子信息类", "机械类"]:
                    cat_score += 20.0

            # ----------------------------------------------------
            # 6. 特殊倾向加权与保护机制 (纯理论科研保护 vs 工科硬度)
            # ----------------------------------------------------
            # 纯理科倾向保护：选了推导理论(Q4=A) 或 象牙塔学术(Q8=D)
            if "A" in q4 or "D" in q8:
                if cluster == "数理自科":
                    cat_score *= 1.15  # 纯自科乘子加成，抵消工科天然的高实用起跑优势

            # 硬工科物理加成 (仅限工科且考生明确偏向技术手艺 Q7=A 或 研发)
            if has_physics and (hardness >= 0.80) and ("A" in q7 or "大厂高薪与硬核研发" in target_goal):
                cat_score *= (0.8 + 0.3 * hardness)

            scores[cat] = cat_score

        # ----------------------------------------------------
        # 7. 排序与大类多样性保障 (防止同质化专业挤占全部 Top 5)
        # ----------------------------------------------------
        sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        top_cats = []
        cluster_counts = {}
        for cat_name, s in sorted_cats:
            cl = self._get_broad_cluster(cat_name)
            cnt = cluster_counts.get(cl, 0)
            if cnt >= 2 and len(top_cats) < 4:
                # 若同一学科集群已经占据 2 个席位，适当让位给其他高分门类以保证视野宽广
                continue
            top_cats.append((cat_name, s))
            cluster_counts[cl] = cnt + 1
            if len(top_cats) >= 5:
                break
        
        # 若因多样性过滤导致不足 5 个，直接补充最高分项
        if len(top_cats) < 5:
            picked_names = {c[0] for c in top_cats}
            for cat_name, s in sorted_cats:
                if cat_name not in picked_names:
                    top_cats.append((cat_name, s))
                    if len(top_cats) >= 5:
                        break

        # 构造完整富文本卡片数据
        results = []
        rank_emojis = ["🥇", "🥈", "🥉", "🏅", "🎖️"]
        
        for idx, (cat_name, final_score) in enumerate(top_cats):
            info = self.insights.get(cat_name, {})
            hardness = info.get("engineering_hardness", 0.5)
            
            majors = self.get_representative_majors(cat_name)
            if not majors:
                majors = [{"name": cat_name.replace("类", ""), "code": "通用代码", "desc": "核心主干方向"}]

            top_schools = self.get_top_schools(cat_name)

            results.append({
                "rank": rank_emojis[idx] if idx < len(rank_emojis) else "⭐",
                "name": cat_name,
                "score": round(final_score, 1),
                "hardness": hardness,
                "hardness_label": info.get("hardness_label", "工科技术"),
                "utility": info.get("utility_tier", "高实用性"),
                "degree": info.get("degree_requirement", "本硕皆宜"),
                "warning": info.get("pitfall_warning", ""),
                "insight": info.get("reality_insight", ""),
                "marketing_myth": info.get("marketing_myth", "招生简章复合型领军精英"),
                "truth_unfiltered": info.get("truth_unfiltered", "真实工作日常实录"),
                "civil_service_tag": info.get("civil_service_tag", "体制内招录属性"),
                "experience_value": info.get("experience_value", "经验沉淀属性"),
                "majors": majors,
                "top_schools": top_schools
            })

        return results, intercepted[:5]

# 全局单例
engine = GaokaoRecommendEngine()
