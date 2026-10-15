# -*- coding: utf-8 -*-
"""
================================================================================
  Gaokao 2.0 推荐算法引擎 (Recommendation Engine)
  选科硬性过滤 · 12道微观情境多维加权 · 工科硬度乘子 · 避坑排雷一票否决
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
                # 规范化列名
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
        
        # 寻找匹配的大类行 (专业类字段)
        matched = self.majors_df[self.majors_df["专业类"].str.contains(category_name.replace("类", ""), na=False)]
        if matched.empty:
            # 尝试名称包含
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
        # 使用学科字段精确匹配，避免关键词碰撞（如'法'命中'书法学'）
        matched = self.top_schools_df[
            self.top_schools_df["学科"].str.strip() == kw
        ]
        
        # 若学科精确匹配无结果，尝试专业字段精确前缀匹配
        if matched.empty:
            matched = self.top_schools_df[
                self.top_schools_df["专业"].str.startswith(kw, na=False)
            ]
        
        # 若仍无结果，回退关键词包含但排除明显不相关
        if matched.empty:
            matched = self.top_schools_df[
                (self.top_schools_df["学科"].str.contains(kw, na=False)) &
                (~self.top_schools_df["学科"].str.contains("美术|书法|艺术", na=False))
            ]
        
        if matched.empty:
            # 回退通用代表学校
            return ["清华大学", "浙江大学", "上海交通大学", "华中科技大学"]
        
        # 优先取 A+ 和 A 档次
        priority_order = {"A+": 0, "A": 1, "A-": 2, "A–": 2, "B+": 3}
        matched = matched.copy()
        matched["_rank"] = matched["档次"].map(priority_order).fillna(4)
        matched = matched.sort_values("_rank")
            
        schools = matched["学校"].dropna().unique().tolist()
        return schools[:5]

    def calculate_recommendations(self, user_profile, answers):
        """
        核心综合推荐计算函数
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

        # 遍历所有 94 个专业大类
        for cat, info in self.insights.items():
            cat_score = 50.0  # 基准起步分
            hardness = info.get("engineering_hardness", 0.5)
            is_pitfall = info.get("is_pitfall", False)
            # 门类归属判断（用于后续差异化打分）
            if hardness >= 0.7:
                disc = "工学"
            elif "医" in cat or "药" in cat or "护" in cat:
                disc = "医学"
            elif "学类" in cat and ("数" in cat or "物" in cat or "天" in cat or "地球" in cat or "大气" in cat or "海洋科学" in cat):
                disc = "理学"
            elif "化学类" == cat:
                disc = "理学"
            elif "经济" in cat or "金融" in cat or "管理" in cat or "工商" in cat or "旅游" in cat or "农林经济" in cat:
                disc = "经管"
            elif "法" in cat or "政治" in cat or "马克思" in cat or "公安学" in cat:
                disc = "法政"
            else:
                disc = "人文社科"

            # ----------------------------------------------------
            # 1. 选科硬性过滤 (物理一票否决硬工科)
            # ----------------------------------------------------
            if hardness >= 0.8 and not has_physics:
                # 考生没有选物理，无法报考绝大部分硬核工科
                continue

            if ("临床医学" in cat or "口腔医学" in cat) and not (has_physics and has_chem):
                # 临床医学强制要求物理+化学双选（绝大多数省份硬性要求）
                continue

            # ----------------------------------------------------
            # 2. 避坑全局过滤与反向情境一票否决
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
                cat_score -= 35.0
            elif "D" in q11_ans and cat in ["计算机类", "电子信息类"]:
                # 考生明确排斥满屏代码与高压大厂熬夜内卷
                cat_score -= 40.0

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
            # 3. 核心出路偏好打分 (Target Goal)
            # ----------------------------------------------------
            if "大厂高薪与硬核研发" in target_goal:
                if hardness >= 0.90:
                    cat_score += 40.0
                elif hardness >= 0.80:
                    cat_score += 25.0
                elif "理学" in disc:
                    cat_score += 15.0
                else:
                    cat_score -= 25.0
            elif "体制内考公考编" in target_goal:
                if cat in ["中国语言文学类", "法学类", "马克思主义理论类", "电气类", "计算机类"]:
                    cat_score += 45.0
                elif "管理" in cat or "经济" in cat:
                    cat_score += 15.0
                elif hardness >= 0.85:
                    cat_score += 10.0
                else:
                    cat_score -= 10.0
            elif "医学临床或口腔" in target_goal:
                if cat in ["临床医学类", "口腔医学类", "中医学类", "中西医结合类"]:
                    cat_score += 55.0
                elif "医学" in cat or "药学" in cat:
                    cat_score += 20.0
                else:
                    cat_score -= 30.0
            elif "学术科研与本硕博深造" in target_goal:
                if "理学" in disc or cat in ["数学类", "物理学类", "力学类", "航空航天类", "计算机类"]:
                    cat_score += 40.0
                elif hardness >= 0.85:
                    cat_score += 20.0
            elif "经管商业与金融投资" in target_goal:
                if cat in ["金融学类", "经济学类", "经济与贸易类", "统计学类", "管理科学与工程类"]:
                    cat_score += 45.0
                else:
                    cat_score -= 15.0

            # ----------------------------------------------------
            # 4. 12 道微观情境评测多维加权
            # ----------------------------------------------------
            # Q1 自主精力分配
            q1 = answers.get("Q1", "")
            if "A" in q1: # 敲代码拆数码
                if cat in ["计算机类", "电子信息类", "自动化类"]: cat_score += 25.0
            elif "B" in q1: # 长文分析社科热点
                if cat in ["中国语言文学类", "法学类", "新闻传播学类", "社会学类"]: cat_score += 25.0
            elif "C" in q1: # 统筹自驾游
                if cat in ["工商管理类", "金融学类", "管理科学与工程类"]: cat_score += 20.0
            elif "D" in q1: # 艺术视听
                if "艺术" in cat or "设计" in cat: cat_score += 25.0

            # Q2 遇Bug报错反应
            q2 = answers.get("Q2", "")
            if "A" in q2: # 底层死磕
                if cat in ["计算机类", "数学类", "电子信息类"]: cat_score += 20.0
            elif "B" in q2: # 现成工具业务
                if cat in ["自动化类", "软件工程", "管理科学与工程类"]: cat_score += 15.0
            elif "C" in q2: # 沟通点拨
                if cat in ["法学类", "新闻传播学类", "工商管理类"]: cat_score += 15.0
            elif "D" in q2: # 实体观察
                if cat in ["机械类", "仪器类", "临床医学类"]: cat_score += 20.0

            # Q3 动手实操
            q3 = answers.get("Q3", "")
            if "A" in q3: # 拆开修好电器
                if cat in ["电气类", "机械类", "自动化类", "电子信息类"]: cat_score += 25.0
            elif "B" in q3: # 查软件叫售后
                if cat in ["计算机类", "中国语言文学类", "法学类"]: cat_score += 10.0
            elif "C" in q3: # 算经济账
                if cat in ["金融学类", "经济学类", "统计学类"]: cat_score += 20.0
            elif "D" in q3: # 外观工业设计
                if cat in ["设计学类", "美术学类"]: cat_score += 20.0

            # Q4 理论 vs 工程
            q4 = answers.get("Q4", "")
            if "A" in q4: # 理论公理推导
                if cat in ["数学类", "物理学类"]: cat_score += 25.0
            elif "B" in q4: # 零件与代码交付跑通
                if hardness >= 0.85: cat_score += 25.0
            elif "C" in q4: # 法律体制
                if cat in ["法学类", "政治学类"]: cat_score += 25.0
            elif "D" in q4: # 商业战役
                if "经济" in cat or "金融" in cat: cat_score += 25.0

            # Q5 心理能量来源
            q5 = answers.get("Q5", "")
            if "A" in q5: # 独自对系统
                if hardness >= 0.90: cat_score += 15.0
            elif "B" in q5: # 面对面帮人治愈
                if "医" in cat or "护" in cat: cat_score += 30.0
            elif "C" in q5: # 商务谈判说服
                if disc == "经管" or disc == "法政": cat_score += 20.0
            elif "D" in q5: # 图书馆独立考据
                if cat in ["历史学类", "哲学类", "图书情报与档案管理类", "中国语言文学类"]: cat_score += 20.0

            # Q6 危机应对本能
            q6 = answers.get("Q6", "")
            if "A" in q6 and hardness >= 0.85: cat_score += 15.0
            elif "B" in q6 and ("管理" in cat or "新闻" in cat): cat_score += 15.0
            elif "C" in q6 and cat in ["法学类", "马克思主义理论类", "公安学类"]: cat_score += 18.0
            elif "D" in q6 and disc == "经管": cat_score += 15.0

            # Q7 职业安全感来源
            q7 = answers.get("Q7", "")
            if "A" in q7: # 硬核技术凭手艺
                if hardness >= 0.90: cat_score += 25.0
            elif "B" in q7: # 编制在身抗周期
                if cat in ["电气类", "中国语言文学类", "法学类", "马克思主义理论类"]: cat_score += 25.0
            elif "C" in q7: # 执照越老越吃香
                if cat in ["临床医学类", "口腔医学类", "中医学类", "法学类"]: cat_score += 30.0
            elif "D" in q7: # 商业直觉撬动杠杆
                if cat in ["金融学类", "经济与贸易类", "工商管理类"]: cat_score += 25.0

            # Q8 考公考编心态
            q8 = answers.get("Q8", "")
            if "A" in q8: # 坚决不去体制
                if hardness >= 0.85: cat_score += 20.0
                if cat in ["中国语言文学类", "马克思主义理论类"]: cat_score -= 20.0
            elif "B" in q8: # 坚定考公
                if cat in ["法学类", "中国语言文学类", "马克思主义理论类", "电气类", "计算机类"]: cat_score += 30.0
            elif "C" in q8: # 企业为主体制兜底
                if hardness >= 0.85: cat_score += 10.0
                if cat in ["法学类", "中国语言文学类"]: cat_score += 8.0
            elif "D" in q8: # 高校学者
                if cat in ["数学类", "物理学类", "历史学类", "哲学类"]: cat_score += 25.0

            # Q9 考研战线意向与家庭经济
            q9 = answers.get("Q9", "")
            if "A" in q9 or "急需本科" in family_econ: # 急需本科变现
                if cat in ["电气类", "自动化类", "电子信息类", "计算机类"]:
                    cat_score += 20.0
                elif cat in ["临床医学类", "物理学类", "生物科学类"]:
                    cat_score -= 25.0 # 读研周期太长
            elif "B" in q9: # 读硕2~3年
                if cat in ["计算机类", "电子信息类", "自动化类", "金融学类"]:
                    cat_score += 15.0
            elif "C" in q9: # 接受硕博长期深造
                if cat in ["临床医学类", "口腔医学类", "数学类", "物理学类", "航空航天类"]:
                    cat_score += 25.0
            elif "D" in q9: # 边工作边考证
                if cat in ["工商管理类", "金融学类", "经济与贸易类"]:
                    cat_score += 10.0

            # Q10 35岁危机与经验保质期
            q10 = answers.get("Q10", "")
            if "A" in q10: # 青春红利高爆发
                if cat in ["计算机类", "电子信息类"]:
                    cat_score += 20.0
            elif "B" in q10: # 越老越吃香
                if cat in ["临床医学类", "口腔医学类", "电气类", "法学类", "中医学类"]:
                    cat_score += 25.0
            elif "C" in q10: # 体制内保护免疫裁员
                if cat in ["中国语言文学类", "法学类", "马克思主义理论类", "电气类"]:
                    cat_score += 20.0
            elif "D" in q10: # 终身学习核心技术赛道
                if cat in ["电子信息类", "自动化类", "航空航天类", "计算机类"]:
                    cat_score += 20.0

            # ----------------------------------------------------
            # 5. 工科硬度乘子增强 (若用户偏好硬科技，工科硬度加权)
            # ----------------------------------------------------
            if has_physics and ("研发" in target_goal or "A" in q1 or "A" in q7):
                cat_score *= (0.6 + 0.5 * hardness)

            scores[cat] = cat_score

        # 排序并取 Top 5
        sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_cats = sorted_cats[:5]

        # 构造完整富文本卡片数据
        results = []
        rank_emojis = ["🥇", "🥈", "🥉", "🏅", "🎖️"]
        
        for idx, (cat_name, final_score) in enumerate(top_cats):
            info = self.insights.get(cat_name, {})
            hardness = info.get("engineering_hardness", 0.5)
            
            # 代表专业
            majors = self.get_representative_majors(cat_name)
            if not majors:
                majors = [{"name": cat_name.replace("类", ""), "code": "通用代码", "desc": "核心主干方向"}]

            # 顶尖大学
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
