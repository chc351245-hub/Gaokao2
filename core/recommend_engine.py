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
        self.sister_majors = self._load_sister_majors()
        
    def _load_insights(self):
        insights_file = DATA_DIR / "category_reality_insights.json"
        if insights_file.exists():
            with open(insights_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_sister_majors(self):
        sister_file = DATA_DIR / "sister_majors_comparison.json"
        if sister_file.exists():
            with open(sister_file, "r", encoding="utf-8") as f:
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

    def _generate_recommend_reason(self, cat_name, user_profile, answers, info):
        """根据考生答题倾向 (Q1~Q12) 动态生成专属个性化推荐理由"""
        traits = []
        cluster = self._get_broad_cluster(cat_name)
        hardness = info.get("engineering_hardness", 0.5)
        econ = user_profile.get("family_econ", "")

        q1 = answers.get("Q1", "")
        q2 = answers.get("Q2", "")
        q3 = answers.get("Q3", "")
        q4 = answers.get("Q4", "")
        q5 = answers.get("Q5", "")
        q7 = answers.get("Q7", "")
        q8 = answers.get("Q8", "")
        q9 = answers.get("Q9", "")
        q10 = answers.get("Q10", "")
        q11 = answers.get("Q11", "")

        # 工科与技术信息类
        if cluster in ["信息工科", "传统/重工业工科"]:
            if "A" in q1: traits.append("对数码硬件与代码底层的本能探究欲")
            if "A" in q2: traits.append("遇复杂报错底层死磕的技术韧性")
            if "A" in q3: traits.append("亲手拆装电路与机械实操的动手力")
            if "B" in q4: traits.append("交付真实工程系统跑通的极高成就感")
            if "A" in q7: traits.append("‘凭一身硬手艺安身立命、跳槽不看脸色’的底气诉求")
            if "D" in q10: traits.append("扎根硬核工业标准与不可轻易替代的技术壁垒")
        # 法政社科与文史
        elif cluster in ["法政社科", "文史哲传媒"]:
            if "B" in q1: traits.append("对深度社科与人文长文的研读钻研耐性")
            if "B" in q3: traits.append("善于溯源法规条款、厘清权责红线的严谨秩序感")
            if "C" in q4: traits.append("对社会运行机制与制度规矩的深刻洞察")
            if "D" in q5: traits.append("享受文献考据、耐得住寂寞的治学沉静心性")
            if "B" in q7 or "B" in q8: traits.append("立志体制求稳、在公务员/国企编制招录上的显著优势")
            if "C" in q10: traits.append("依靠体制合规体系保护、免疫市场波动的长效安全感")
        # 经管商科
        elif cluster == "经管商科":
            if "C" in q1: traits.append("善于统筹多方资源与精细化规划预算的调度直觉")
            if "C" in q3: traits.append("精打细算、权衡折旧与维修成本的敏锐商业嗅觉")
            if "D" in q4: traits.append("沉醉于市场现金流博弈与商业运转的进取心")
            if "C" in q5: traits.append("在商务谈判博弈中说服多方促成合作的社交说服力")
            if "D" in q7: traits.append("善用商业直觉与资产杠杆撬动超额溢价的财富观")
        # 医学医药
        elif cluster == "医学医药":
            if "D" in q2: traits.append("对生命实体生理构造与实物观察的敏锐直觉")
            if "B" in q5: traits.append("面对面解除他人病痛、践行救死扶伤的崇高利他心")
            if "C" in q7: traits.append("‘考取国家终身执业牌照、经验越老越吃香’的长坡厚雪赛道诉求")
            if "B" in q10: traits.append("技能经验不随技术迭代淘汰、年资沉淀越久护城河越宽")
        # 数理自科
        elif cluster == "数理自科":
            if "A" in q4: traits.append("偏好第一性原理推导与追求数学定理证明的纯粹求知欲")
            if "A" in q5: traits.append("习惯沉浸在抽象逻辑系统之中获得心流充能的思维习惯")
            if "D" in q8: traits.append("深耕高校与科研院所象牙塔、做科研学者的纯粹志向")
        # 艺术设计
        elif cluster == "艺术设计":
            if "D" in q1: traits.append("对视听审美与内容策划的创意直觉")
            if "D" in q3: traits.append("对产品外观质感与工业造型设计的审美敏感度")

        econ_trait = ""
        if "A" in q9 or "急需本科" in econ:
            if hardness >= 0.75 or cluster == "经管商科" or cat_name == "电气类":
                econ_trait = "具备较强本科直接高质量就业变现能力，契合你的家庭深造容错边界"
        elif "C" in q9 or "优渥" in econ:
            econ_trait = "你与家庭做好了长线深造作战准备，能平稳跨过该领域的名校硕博硬门槛"

        avoid_trait = ""
        if "A" in q11 and cat_name not in ["土木类", "水利类", "建筑类", "地质类", "矿业类", "交通运输类"]:
            avoid_trait = "完全规避了你排斥的偏远野外工地驻场环境"
        elif "B" in q11 and cat_name not in ["化工与制药类", "材料类", "轻工类", "纺织类", "生物工程类"]:
            avoid_trait = "完全绕开了你排斥的密闭车间与化学异味倒班环境"

        if traits:
            core_str = "、".join(traits[:2])
            reason = f"契合你在此前评测中表现出的【{core_str}】"
        else:
            reason = f"综合匹配了你在此前多项生活情境中的思维本能与能力倾向"

        if econ_trait:
            reason += f"；且{econ_trait}"
        if avoid_trait:
            reason += f"；同时{avoid_trait}"

        reason += "，是契合你天赋秉性与避坑诉求的最优解之一。"
        return reason

    def _generate_tier_alert(self, cat_name, user_profile):
        """根据考生位次与专业现实属性生成卡片底部的真实就读与报考提示"""
        rank_pct = user_profile.get("rank_pct", 10.0)
        score = user_profile.get("score", 600)
        subjects = user_profile.get("subjects") or []
        has_physics = "物理" in subjects
        has_chem = "化学" in subjects

        # 选科特别提醒：新高考选了物理但未选化学的工科风险提示
        chem_warning = ""
        if has_physics and not has_chem and cat_name in ["机械类", "电气类", "自动化类", "电子信息类", "航空航天类", "仪器类"]:
            chem_warning = "⚠️【选科新规重要提醒】：2024起多数主流高校工科要求‘物化双选’。你未选化学，填报时请务必在省招生专业目录中优先筛选‘仅限物理’即可报考的代码，避免无效选填！\n"

        base_alert = ""
        if cat_name in ["金融学类", "经济与贸易类"]:
            if rank_pct >= 15.0 or score < 580:
                base_alert = "⚠️【院校层级与求职实情警示】：金融行业高度看重‘第一学历名校光环’与家庭人脉资源。若在普通二本/双非就读，进投行券商核心组门槛极高，毕业多偏向基层银行网点拉存款柜员或销售，建议以扎实考研或转战公考为主要目标。"
            else:
                base_alert = "💡【名校资源赋能提示】：以你的预估位次有望进入头部高水平大学，该专业名校光环附加值极大，适合深耕券商投行、公募资管等核心金融业务。"

        elif cat_name == "法学类":
            if rank_pct >= 18.0 or score < 560:
                base_alert = "⚠️【院校层级与法考警示】：法学极度看重‘五院四系’名校背景与司法考试（法考）。若就读于普通院校，务必在本科期间全力拿下法考 A 证，提早锚定公务员省考国考或基层法检选调。"
            else:
                base_alert = "💡【法学精英提示】：高位次进入顶尖法学院，法检系统选调与红圈所律师助理门槛通畅，建议本硕连读深造。"

        elif cat_name in ["临床医学类", "口腔医学类"]:
            if rank_pct >= 12.0:
                base_alert = "⚠️【学制战线与医院门槛警示】：地级市以上三甲医院招聘普遍要求‘名校医学博士 + 规范化培训’（8~11年漫长周期）。普通本科临床大多面向县级医院或基层社区卫生院，求稳建议规划专硕规培并轨。"
            else:
                base_alert = "💡【医学长周期提示】：适合冲刺顶尖医学院 5+3 本硕一体化或本博贯通培养，家庭需具备支持 8 年以上长线深造的耐心与经济容错。"

        elif cat_name in ["计算机类", "电子信息类", "软件工程"]:
            if rank_pct >= 18.0:
                base_alert = "💡【硬技能逆袭提示】：技术类专业相对更看重真实代码能力与工程项目经验，双非普通院校只要技术扎实、积极参与开源开发与算法竞赛，依然能获得极高质量的起薪。"
            else:
                base_alert = "💡【高端架构规划】：名校背景在互联网与芯片外企具备极高简历初筛豁免权，建议在校期间多进导师核心实验室攻坚前沿项目。"

        elif cat_name == "电气类":
            if rank_pct >= 15.0:
                base_alert = "💡【电网特色院校报考技巧】：进国家电网不仅看 985，原电力部直属双非高校（如沈阳工程、南京工程、上海电力等）在本地电网招录通过率极高，择校时可重点关注电力行业老牌强校！"
            else:
                base_alert = "💡【电网总部梯队提示】：顶尖 985 电气毕业生是各省电力调度中心与电科院研发专家的首选储备人才。"

        elif cat_name == "机械类":
            if rank_pct >= 15.0 or score < 560:
                base_alert = "💡【应用型工科求职策略】：机械底子扎实，不挑名校光环。在新能源汽车产线、精密制造装备与非标自动化领域，掌握SolidWorks/CAD三维建模与机电一体化调试的毕业生极为抢手，先积累2~3年项目经验是核心跳板。"
            else:
                base_alert = "💡【高端重器与研发深造】：高位次考生建议本硕直通，锚定航空航天动力、高端数控机床与机器人伺服机构等国家核心研发方向。"

        elif cat_name == "教育学类":
            if rank_pct >= 18.0 or score < 560:
                base_alert = "💡【公立教师编与地方师范技巧】：普通院校师范生建议优先报考本省老牌省属师范大学（如本省师范大学/师专升本院校），其在各地市县教育局招考、特岗教师及地方公费师范生中认可度极高，就业确定性远超普通综合性二本。"
            else:
                base_alert = "💡【部属六所与高中教师精英】：高分建议直冲教育部直属六所师范大学公费师范生或优师计划，毕业免试认定教资且直接落实事业编制与岗位！"

        elif cat_name == "管理科学与工程类":
            base_alert = "💡【工管复合型优势】：该专业既有信息管理、大数据与供应链系统等硬技能，又覆盖项目管理与工程造价，考取一造/二造造价师或信息系统项目管理师证书可在国企与科技企业快速立足。"

        elif cat_name == "中国语言文学类":
            base_alert = "💡【体制公文与教育提示】：中文核心竞争力在‘笔杆子’。体制内公文材料岗招录体量极大；同时考取教资证书走公立中小学语文教师编制是极具确定性的托底退路。"

        elif cat_name in ["数学类", "物理学类", "天文学类", "力学类"]:
            base_alert = "⚠️【学术耐受度提示】：纯自科类专业本科直接就业对口度低，大多需继续攻读硕士或博士，适合立志从事科研、高校讲师，或研究生阶段转金融工程/算法研究的考生。"

        elif cat_name == "中医学类":
            base_alert = "💡【老中医时间沉淀提示】：技能不随技术更新淘汰，越老越吃香，但前期需耐得住跟师抄方与长线轮转寂寞，基层社区与特色专科医院需求长期旺盛。"

        else:
            base_alert = "💡【报考综合提示】：该专业属于稳健发展门类，建议结合自身兴趣特长，提早在大一期间明确考研深造或求职考编的发展主线。"

        return chem_warning + base_alert

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
            # 3. 避坑大类彻底解耦出算法（由专属避坑避雷指南专区全景承载）
            # ----------------------------------------------------
            if is_pitfall:
                # 19 个避坑大类不参与主流算法排名，由专属【19大高危与下行专业全景剖析专区】深度解读
                continue

            should_intercept = False
            intercept_reason = ""

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
                    if cat in ["马克思主义理论类", "哲学类", "历史学类", "社会学类"]:
                        cat_score -= 100.0  # 大厂完全无对口业务研发岗，强力熔断脱离大厂现实的推荐
                    elif hardness >= 0.88:
                        cat_score += 35.0
                    elif hardness >= 0.75:
                        cat_score += 20.0
                    elif not has_physics:
                        # 文科生渴望大厂研发/私企高薪，精准对标互联网产品运营、交互设计与数据分析
                        if cat in ["新闻传播学类", "设计学类", "管理科学与工程类"]:
                            cat_score += 32.0
                        elif cat in ["外国语言文学类", "法学类"]:
                            cat_score += 15.0
                        else:
                            cat_score -= 25.0
                    elif cluster in ["文史哲传媒", "法政社科"]:
                        cat_score -= 25.0
                elif "体制内考公考编" in target_goal:
                    if cat in ["中国语言文学类", "法学类", "马克思主义理论类", "电气类", "计算机类", "公共管理类", "教育学类"]:
                        cat_score += 35.0
                    elif cat in ["航空航天类", "天文学类", "兵器类"]:
                        cat_score -= 15.0  # 科研院所为主，普通公务员招考极少
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
            # 4.1 位次与分数层级耐受度 (Tier Risk Calibration)
            # ----------------------------------------------------
            user_score = user_profile.get("score", 600)
            user_rank_pct = user_profile.get("rank_pct", 10.0)
            # 普通二本/中低分位次（rank_pct >= 18% 或 score < 560）且工薪家庭：
            # 对极度看重名校光环与资源的纯金融与纯理论类适度降权，托举硬技能工科、管科与带编师范
            if (user_rank_pct >= 18.0 or user_score < 560) and ("工薪" in family_econ or "急需本科" in family_econ):
                if cat in ["金融学类", "经济与贸易类", "天文学类"]:
                    cat_score -= 32.0  # 二本工薪适度避让极度依赖名校光环与资源的纯金融
                elif cat in ["电气类", "自动化类", "机械类", "计算机类", "管理科学与工程类", "教育学类"]:
                    cat_score += 12.0

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
            recommend_reason = self._generate_recommend_reason(cat_name, user_profile, answers, info)
            tier_alert = self._generate_tier_alert(cat_name, user_profile)

            results.append({
                "rank": rank_emojis[idx] if idx < len(rank_emojis) else "⭐",
                "name": cat_name,
                "score": round(final_score, 1),
                "hardness": hardness,
                "hardness_label": info.get("hardness_label", "工科技术"),
                "utility": info.get("utility_tier", "高实用性"),
                "degree": info.get("degree_requirement", "本硕皆宜"),
                "tier_risk": info.get("tier_risk", "本硕皆宜/梯队分化"),
                "warning": info.get("pitfall_warning", ""),
                "insight": info.get("reality_insight", ""),
                "recommend_reason": recommend_reason,
                "tier_alert": tier_alert,
                "marketing_myth": info.get("marketing_myth", "招生简章复合型领军精英"),
                "truth_unfiltered": info.get("truth_unfiltered", "真实工作日常实录"),
                "civil_service_tag": info.get("civil_service_tag", "体制内招录属性"),
                "experience_value": info.get("experience_value", "经验沉淀属性"),
                "majors": majors,
                "top_schools": top_schools,
                "sister_benchmarks": self.sister_majors.get(cat_name, [])
            })

        return results, intercepted[:5]

# 全局单例
engine = GaokaoRecommendEngine()
