"""
================================================================================
  高考志愿智能规划与决策系统 v2.0 (Gaokao 2.0)
  极简架构 · 现代美学与微动效 · 就业实用导向 · 招生包装打假 · 全程避坑护航
================================================================================
"""

import sys
from pathlib import Path

# 确保脚本所在目录优先加入搜索路径（支持在根目录或 github_upload 子目录独立运行）
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import time
import uuid
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from pathlib import Path
from core.recommend_engine import engine

def scroll_to_top():
    """触发浏览器主视口平滑置顶，彻底解决多题长页面切换后的滚动滞留问题"""
    nonce = f"{time.time()}_{uuid.uuid4().hex}"
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <!-- Nonce: {nonce} -->
        </head>
        <body style="margin:0;padding:0;overflow:hidden;">
            <script>
                function doScroll() {{
                    try {{
                        var p = window.parent;
                        if (!p || !p.document) return;
                        
                        // 1. 找到当前组件自身 iframe 并强制调用 scrollIntoView 让浏览器原生回滚至顶部
                        var iframes = p.document.getElementsByTagName("iframe");
                        for (var i = 0; i < iframes.length; i++) {{
                            var ifr = iframes[i];
                            if (ifr.contentWindow === window) {{
                                ifr.scrollIntoView({{ behavior: "smooth", block: "start" }});
                                break;
                            }}
                        }}

                        // 2. 双重兜底：直接重置 Streamlit 视口容器滚动距离
                        var selectors = [
                            '.main',
                            'section.main',
                            '[data-testid="stMain"]',
                            '[data-testid="stAppViewContainer"]',
                            '[data-testid="stAppViewBlockContainer"]',
                            p.document.documentElement,
                            p.document.body
                        ];
                        for (var j = 0; j < selectors.length; j++) {{
                            var item = selectors[j];
                            var el = (typeof item === 'string') ? p.document.querySelector(item) : item;
                            if (el && el.scrollTop !== undefined && el.scrollTop > 0) {{
                                el.scrollTop = 0;
                            }}
                        }}
                        p.scrollTo(0, 0);
                    }} catch (e) {{
                        console.warn("Auto scroll error:", e);
                    }}
                }}
                doScroll();
                setTimeout(doScroll, 60);
                setTimeout(doScroll, 180);
                setTimeout(doScroll, 380);
            </script>
        </body>
        </html>
        """,
        height=0,
        width=0,
    )

def render_cosmic_intro(force_replay=False):
    """
    顶级科技公司级（SpaceX / Apple Keynote / Interstellar 质感）电影级全屏引力星云与全息浑天罗盘开场
    - Retina 视网膜级高分辨率 Canvas (DPR 自动适配)
    - 60FPS 双层天体星尘系统：500+ 微光闪烁深空恒星 + 180条引力吸积流线 + 动态星座知识拓扑连线
    - 极精细 SVG 浑天经纬刻度环 (度数刻度、反向公转轨道、天文经纬流)
    - 电影级动态排版与实时星谱解算电报数据流
    - 引力坍缩与超新星漫射隐退转场 (Gravitational Collapse & Supernova Bloom)
    - 智能会话记忆 (sessionStorage) + 随时跳过 + 侧边栏一键重温
    """
    nonce = f"{time.time()}_{uuid.uuid4().hex}"
    force_str = "true" if force_replay else "false"
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <!-- Nonce: {nonce} -->
        </head>
        <body style="margin:0;padding:0;overflow:hidden;">
            <script>
                (function() {{
                    try {{
                        var p = window.parent;
                        if (!p || !p.document) return;
                        
                        var force = {force_str};
                        var SEEN_KEY = "gaokao_cosmic_intro_played_v3";
                        
                        if (!force && p.sessionStorage && p.sessionStorage.getItem(SEEN_KEY)) {{
                            return;
                        }}
                        if (p.sessionStorage) {{
                            p.sessionStorage.setItem(SEEN_KEY, "1");
                        }}
                        
                        var existing = p.document.getElementById("cosmic-warp-overlay");
                        if (existing) {{
                            existing.remove();
                        }}
                        
                        // 创建全屏宇宙全息容器
                        var overlay = p.document.createElement("div");
                        overlay.id = "cosmic-warp-overlay";
                        overlay.style.position = "fixed";
                        overlay.style.top = "0";
                        overlay.style.left = "0";
                        overlay.style.width = "100vw";
                        overlay.style.height = "100vh";
                        overlay.style.zIndex = "99999999";
                        overlay.style.backgroundColor = "#02040A";
                        overlay.style.display = "flex";
                        overlay.style.flexDirection = "column";
                        overlay.style.alignItems = "center";
                        overlay.style.justifyContent = "center";
                        overlay.style.overflow = "hidden";
                        overlay.style.userSelect = "none";
                        overlay.style.transition = "opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1), filter 0.8s ease";
                        
                        var styleEl = p.document.createElement("style");
                        styleEl.innerHTML = `
                            @keyframes astrolabeRotateCw {{
                                0% {{ transform: rotate(0deg); }}
                                100% {{ transform: rotate(360deg); }}
                            }}
                            @keyframes astrolabeRotateCcw {{
                                0% {{ transform: rotate(360deg); }}
                                100% {{ transform: rotate(0deg); }}
                            }}
                            @keyframes celestialAuraPulse {{
                                0% {{ transform: scale(0.97); opacity: 0.65; }}
                                50% {{ transform: scale(1.03); opacity: 0.95; filter: drop-shadow(0 0 28px rgba(56, 189, 248, 0.65)); }}
                                100% {{ transform: scale(0.97); opacity: 0.65; }}
                            }}
                            @keyframes titleShimmerFlow {{
                                0% {{ background-position: -200% 0; }}
                                100% {{ background-position: 200% 0; }}
                            }}
                        `;
                        overlay.appendChild(styleEl);
                        
                        // 1. Retina 高清 Canvas
                        var canvas = p.document.createElement("canvas");
                        canvas.style.position = "absolute";
                        canvas.style.top = "0";
                        canvas.style.left = "0";
                        canvas.style.width = "100%";
                        canvas.style.height = "100%";
                        canvas.style.zIndex = "1";
                        overlay.appendChild(canvas);
                        
                        // 2. 中央天文浑天仪与电影感文字中枢
                        var centerBox = p.document.createElement("div");
                        centerBox.style.position = "relative";
                        centerBox.style.zIndex = "2";
                        centerBox.style.textAlign = "center";
                        centerBox.style.display = "flex";
                        centerBox.style.flexDirection = "column";
                        centerBox.style.alignItems = "center";
                        centerBox.style.pointerEvents = "none";
                        centerBox.style.padding = "20px";
                        centerBox.style.maxWidth = "880px";
                        
                        centerBox.innerHTML = `
                            <!-- 精密 SVG 天文浑天经纬罗盘 -->
                            <div style="position:relative; width: 160px; height: 160px; margin-bottom: 24px; animation: celestialAuraPulse 4s infinite ease-in-out;">
                                <!-- 外层刻度方位环 -->
                                <svg style="position:absolute; top:0; left:0; width:100%; height:100%; animation: astrolabeRotateCw 24s linear infinite;" viewBox="0 0 160 160">
                                    <circle cx="80" cy="80" r="76" fill="none" stroke="rgba(56, 189, 248, 0.35)" stroke-width="1" stroke-dasharray="3, 5"/>
                                    <circle cx="80" cy="80" r="70" fill="none" stroke="rgba(129, 140, 248, 0.25)" stroke-width="0.8"/>
                                    <!-- 12 宿方位标记 -->
                                    <line x1="80" y1="4" x2="80" y2="10" stroke="#38BDF8" stroke-width="1.5"/>
                                    <line x1="80" y1="150" x2="80" y2="156" stroke="#38BDF8" stroke-width="1.5"/>
                                    <line x1="4" y1="80" x2="10" y2="80" stroke="#38BDF8" stroke-width="1.5"/>
                                    <line x1="150" y1="80" x2="156" y2="80" stroke="#38BDF8" stroke-width="1.5"/>
                                    <circle cx="80" cy="10" r="2" fill="#38BDF8"/>
                                    <circle cx="150" cy="80" r="2" fill="#818CF8"/>
                                    <circle cx="80" cy="150" r="2" fill="#C084FC"/>
                                    <circle cx="10" cy="80" r="2" fill="#34D399"/>
                                </svg>
                                <!-- 内层反向精密公转轨道 -->
                                <svg style="position:absolute; top:15px; left:15px; width:130px; height:130px; animation: astrolabeRotateCcw 14s linear infinite;" viewBox="0 0 130 130">
                                    <circle cx="65" cy="65" r="58" fill="none" stroke="rgba(192, 132, 252, 0.4)" stroke-width="1" stroke-dasharray="14, 8, 4, 8"/>
                                    <circle cx="65" cy="65" r="48" fill="none" stroke="rgba(56, 189, 248, 0.2)" stroke-width="0.6"/>
                                    <circle cx="115" cy="65" r="3" fill="#38BDF8" filter="drop-shadow(0 0 4px #38BDF8)"/>
                                    <circle cx="25" cy="40" r="2.5" fill="#C084FC"/>
                                </svg>
                                <!-- 中心全息引力奇点指南徽章 -->
                                <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); width:68px; height:68px; background:radial-gradient(circle, rgba(15,23,42,0.85) 0%, rgba(30,58,138,0.4) 70%, transparent 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 24px rgba(56, 189, 248, 0.4);">
                                    <span style="font-size:36px; filter: drop-shadow(0 0 14px #38BDF8);">🧭</span>
                                </div>
                            </div>
                            
                            <!-- 顶级技术电报徽标 -->
                            <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(15,23,42,0.7); border:1px solid rgba(56,189,248,0.45); color:#BAE6FD; padding:5px 18px; border-radius:999px; font-size:12px; font-weight:700; letter-spacing:1.5px; margin-bottom:16px; font-family:'JetBrains Mono', monospace; backdrop-filter:blur(14px); box-shadow:0 0 20px rgba(56,189,248,0.25);">
                                <span style="width:7px; height:7px; background:#38BDF8; border-radius:50%; box-shadow:0 0 8px #38BDF8; display:inline-block;"></span>
                                DESTINATION MATRIX // 全息引力场已校准
                            </div>
                            
                            <!-- 电影感主标题 -->
                            <div style="font-size:38px; font-weight:800; letter-spacing:0.04em; margin:0 0 12px 0; background:linear-gradient(135deg, #FFFFFF 0%, #BAE6FD 45%, #C084FC 80%, #FFFFFF 100%); background-size:200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 35px rgba(56,189,248,0.35); font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; animation: titleShimmerFlow 6s linear infinite;">
                                航向未来 · 高考专业天赋解码与现实导航系统
                            </div>
                            
                            <!-- 细腻副标题与数据流状态 -->
                            <div style="font-size:14px; color:#94A3B8; max-width:680px; line-height:1.7; font-family:'JetBrains Mono', monospace; letter-spacing:0.06em; margin-bottom:22px;">
                                <span style="color:#38BDF8;">●</span> RA 14h 29m // DEC +62°40' // 94大类高校星谱多维投射 · 12维本能引力场解析中
                            </div>
                            
                            <!-- 极细量子进度条 -->
                            <div style="width:280px; height:2px; background:rgba(56,189,248,0.18); border-radius:999px; overflow:hidden; position:relative;">
                                <div id="cosmic-pbar-fill" style="width:0%; height:100%; background:linear-gradient(90deg, #38BDF8, #818CF8, #C084FC); transition:width 2.3s cubic-bezier(0.16, 1, 0.3, 1);"></div>
                            </div>
                        `;
                        overlay.appendChild(centerBox);
                        
                        // 3. 悬浮极简科技胶囊按钮
                        var skipBtn = p.document.createElement("button");
                        skipBtn.id = "cosmic-skip-btn";
                        skipBtn.innerHTML = "⚡ 立即进入系统 (Skip) ➔";
                        skipBtn.style.position = "absolute";
                        skipBtn.style.bottom = "36px";
                        skipBtn.style.zIndex = "3";
                        skipBtn.style.background = "rgba(15, 23, 42, 0.75)";
                        skipBtn.style.border = "1px solid rgba(56, 189, 248, 0.45)";
                        skipBtn.style.color = "#BAE6FD";
                        skipBtn.style.padding = "9px 24px";
                        skipBtn.style.borderRadius = "999px";
                        skipBtn.style.fontSize = "12.5px";
                        skipBtn.style.fontWeight = "700";
                        skipBtn.style.letterSpacing = "0.8px";
                        skipBtn.style.cursor = "pointer";
                        skipBtn.style.backdropFilter = "blur(14px)";
                        skipBtn.style.boxShadow = "0 4px 20px rgba(56, 189, 248, 0.25)";
                        skipBtn.style.transition = "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)";
                        skipBtn.onmouseover = function() {{
                            skipBtn.style.background = "rgba(30, 58, 138, 0.85)";
                            skipBtn.style.borderColor = "#38BDF8";
                            skipBtn.style.transform = "translateY(-2px) scale(1.03)";
                            skipBtn.style.boxShadow = "0 8px 26px rgba(56, 189, 248, 0.5)";
                        }};
                        skipBtn.onmouseout = function() {{
                            skipBtn.style.background = "rgba(15, 23, 42, 0.75)";
                            skipBtn.style.borderColor = "rgba(56, 189, 248, 0.45)";
                            skipBtn.style.transform = "translateY(0) scale(1)";
                            skipBtn.style.boxShadow = "0 4px 20px rgba(56, 189, 248, 0.25)";
                        }};
                        overlay.appendChild(skipBtn);
                        
                        p.document.body.appendChild(overlay);
                        
                        // 4. Retina-sharp 高清 Canvas 粒子引擎
                        var ctx = canvas.getContext("2d");
                        var width, height, dpr;
                        function resize() {{
                            dpr = Math.min(p.devicePixelRatio || 1, 2);
                            width = p.innerWidth;
                            height = p.innerHeight;
                            canvas.width = width * dpr;
                            canvas.height = height * dpr;
                            ctx.scale(dpr, dpr);
                        }}
                        resize();
                        p.addEventListener("resize", resize);
                        
                        // --- 粒子群 1：深空微光闪烁星尘 (550颗细腻微光点) ---
                        var deepStars = [];
                        for (var i = 0; i < 550; i++) {{
                            deepStars.push({{
                                x: Math.random() * width,
                                y: Math.random() * height,
                                r: Math.random() * 1.3 + 0.3,
                                alpha: Math.random() * 0.7 + 0.2,
                                speed: Math.random() * 0.03 + 0.01,
                                phase: Math.random() * Math.PI * 2
                            }});
                        }}
                        
                        // --- 粒子群 2：引力吸积盘流光束 (160颗流线粒子) ---
                        var streamParticles = [];
                        for (var j = 0; j < 160; j++) {{
                            var angle = Math.random() * Math.PI * 2;
                            var dist = Math.random() * (Math.max(width, height) * 0.7) + 60;
                            streamParticles.push({{
                                angle: angle,
                                dist: dist,
                                speed: (Math.random() * 0.008 + 0.003) * (dist < 300 ? 1.5 : 1),
                                radialSpeed: Math.random() * 0.8 + 0.3,
                                r: Math.random() * 1.8 + 0.6,
                                colorType: j % 3
                            }});
                        }}
                        
                        // --- 粒子群 3：知识拓扑动态星座骨架 (28个核心节点连线) ---
                        var nodes = [];
                        for (var k = 0; k < 28; k++) {{
                            nodes.push({{
                                x: width / 2 + (Math.random() - 0.5) * 600,
                                y: height / 2 + (Math.random() - 0.5) * 400,
                                vx: (Math.random() - 0.5) * 0.6,
                                vy: (Math.random() - 0.5) * 0.6
                            }});
                        }}
                        
                        var startTime = Date.now();
                        var animFrameId;
                        var dismissed = false;
                        var shockwaveRadius = 0;
                        var collapsing = false;
                        
                        function dismiss() {{
                            if (dismissed) return;
                            dismissed = true;
                            collapsing = true;
                            
                            // 电影级超新星光晕扩散隐退
                            overlay.style.opacity = "0";
                            overlay.style.transform = "scale(1.06)";
                            overlay.style.filter = "blur(18px)";
                            
                            setTimeout(function() {{
                                cancelAnimationFrame(animFrameId);
                                p.removeEventListener("resize", resize);
                                if (overlay && overlay.parentNode) {{
                                    overlay.remove();
                                }}
                            }}, 800);
                        }}
                        
                        skipBtn.onclick = function(e) {{
                            e.stopPropagation();
                            dismiss();
                        }};
                        overlay.onclick = function() {{
                            dismiss();
                        }};
                        
                        setTimeout(function() {{
                            var pbar = p.document.getElementById("cosmic-pbar-fill");
                            if (pbar) pbar.style.width = "100%";
                        }}, 60);
                        
                        function render() {{
                            if (!overlay.parentNode) return;
                            var elapsed = Date.now() - startTime;
                            
                            if (elapsed >= 2700 && !dismissed) {{
                                dismiss();
                                return;
                            }}
                            
                            // 1. 绘制深邃背景与微弱多色星云 (Nebula Backing)
                            ctx.fillStyle = "rgba(2, 4, 10, 0.4)";
                            ctx.fillRect(0, 0, width, height);
                            
                            var cx = width / 2;
                            var cy = height / 2;
                            
                            // 柔和星云渐变 (Cyan / Indigo / Orchid)
                            var neb = ctx.createRadialGradient(cx, cy, 20, cx, cy, Math.max(width, height) * 0.55);
                            neb.addColorStop(0, "rgba(30, 58, 138, 0.22)");
                            neb.addColorStop(0.4, "rgba(56, 189, 248, 0.08)");
                            neb.addColorStop(0.7, "rgba(147, 51, 234, 0.05)");
                            neb.addColorStop(1, "transparent");
                            ctx.fillStyle = neb;
                            ctx.fillRect(0, 0, width, height);
                            
                            // 2. 绘制深空闪烁微星
                            for (var i = 0; i < deepStars.length; i++) {{
                                var ds = deepStars[i];
                                ds.phase += ds.speed;
                                var curAlpha = ds.alpha * (0.6 + 0.4 * Math.sin(ds.phase));
                                ctx.beginPath();
                                ctx.arc(ds.x, ds.y, ds.r, 0, Math.PI * 2);
                                ctx.fillStyle = "rgba(255, 255, 255, " + curAlpha + ")";
                                ctx.fill();
                            }}
                            
                            // 3. 绘制知识拓扑星座动态网格 (Constellation Network)
                            for (var a = 0; a < nodes.length; a++) {{
                                var na = nodes[a];
                                na.x += na.vx;
                                na.y += na.vy;
                                if (na.x < cx - 350 || na.x > cx + 350) na.vx *= -1;
                                if (na.y < cy - 250 || na.y > cy + 250) na.vy *= -1;
                                
                                for (var b = a + 1; b < nodes.length; b++) {{
                                    var nb = nodes[b];
                                    var dx = na.x - nb.x;
                                    var dy = na.y - nb.y;
                                    var d = Math.sqrt(dx * dx + dy * dy);
                                    if (d < 110) {{
                                        var lineAlpha = (1 - d / 110) * 0.22;
                                        ctx.beginPath();
                                        ctx.moveTo(na.x, na.y);
                                        ctx.lineTo(nb.x, nb.y);
                                        ctx.strokeStyle = "rgba(56, 189, 248, " + lineAlpha + ")";
                                        ctx.lineWidth = 0.6;
                                        ctx.stroke();
                                    }}
                                }}
                                ctx.beginPath();
                                ctx.arc(na.x, na.y, 1.8, 0, Math.PI * 2);
                                ctx.fillStyle = "rgba(129, 140, 248, 0.6)";
                                ctx.fill();
                            }}
                            
                            // 4. 绘制引力吸积盘流光束粒子 (Keplerian Orbiters)
                            for (var j = 0; j < streamParticles.length; j++) {{
                                var sp = streamParticles[j];
                                sp.angle += sp.speed;
                                sp.dist -= sp.radialSpeed * (collapsing ? 3.5 : 1);
                                if (sp.dist <= 40) {{
                                    sp.dist = Math.random() * (Math.max(width, height) * 0.7) + 200;
                                }}
                                
                                var px = cx + Math.cos(sp.angle) * sp.dist;
                                var py = cy + Math.sin(sp.angle) * (sp.dist * 0.62); // 椭圆轨道透视
                                
                                ctx.beginPath();
                                ctx.arc(px, py, sp.r, 0, Math.PI * 2);
                                if (sp.colorType === 0) {{
                                    ctx.fillStyle = "rgba(56, 189, 248, 0.85)";
                                }} else if (sp.colorType === 1) {{
                                    ctx.fillStyle = "rgba(192, 132, 252, 0.85)";
                                }} else {{
                                    ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
                                }}
                                ctx.fill();
                            }}
                            
                            // 5. 退出时的超新星光环漫射 (Supernova Shockwave)
                            if (collapsing) {{
                                shockwaveRadius += 32;
                                var waveAlpha = Math.max(0, 1 - shockwaveRadius / (Math.max(width, height) * 0.8));
                                ctx.beginPath();
                                ctx.arc(cx, cy, shockwaveRadius, 0, Math.PI * 2);
                                ctx.strokeStyle = "rgba(56, 189, 248, " + waveAlpha + ")";
                                ctx.lineWidth = 2.5;
                                ctx.stroke();
                            }}
                            
                            animFrameId = requestAnimationFrame(render);
                        }}
                        
                        animFrameId = requestAnimationFrame(render);
                    }} catch (e) {{
                        console.warn("Cosmic intro error:", e);
                    }}
                }})();
            </script>
        </body>
        </html>
        """,
        height=0,
        width=0,
    )

def load_pitfall_encyclopedia():
    p = Path(__file__).resolve().parent / "data" / "pitfall_majors_encyclopedia.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ============================================================================
# 页面基础配置与高阶美学动效样式
# ============================================================================
st.set_page_config(
    page_title="航向未来 · 高考专业天赋解码与现实导航系统",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

/* 全局字体与科技感底色 */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* 页面背景微光科技氛围 + 蓝图网格脉动 */
.stApp {
    background-color: #F8FAFC;
    background-image: 
        radial-gradient(circle at 50% -10%, rgba(37, 99, 235, 0.12) 0%, rgba(14, 165, 233, 0.05) 45%, transparent 75%),
        linear-gradient(rgba(226, 232, 240, 0.45) 1px, transparent 1px),
        linear-gradient(90deg, rgba(226, 232, 240, 0.45) 1px, transparent 1px);
    background-size: 100% 100%, 36px 36px, 36px 36px;
    background-position: 0 0, -1px -1px, -1px -1px;
}

/* 高阶光影聚焦与阶梯滑入动效体系 (Optical Blur & Spring Cascading) */
@keyframes cyberEntrance {
    0% {
        opacity: 0;
        transform: translateY(28px) scale(0.97);
        filter: blur(6px);
    }
    60% {
        filter: blur(0.5px);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
        filter: blur(0px);
    }
}

@keyframes heroGlowPulse {
    0% {
        box-shadow: 0 16px 40px -10px rgba(30, 58, 138, 0.4), 0 0 0 1px rgba(96, 165, 250, 0.25) inset;
    }
    50% {
        box-shadow: 0 22px 55px -8px rgba(37, 99, 235, 0.6), 0 0 0 1px rgba(56, 189, 248, 0.5) inset;
    }
    100% {
        box-shadow: 0 16px 40px -10px rgba(30, 58, 138, 0.4), 0 0 0 1px rgba(96, 165, 250, 0.25) inset;
    }
}

@keyframes beaconPulse {
    0% { transform: scale(0.92); opacity: 0.8; filter: drop-shadow(0 0 4px #06B6D4); }
    50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 10px #38BDF8); }
    100% { transform: scale(0.92); opacity: 0.8; filter: drop-shadow(0 0 4px #06B6D4); }
}

@keyframes scannerPass {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(250%); }
}

@keyframes borderGlowSweep {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 顶部全息深空 Hero 横幅 */
.hero-box {
    background: linear-gradient(135deg, #050814 0%, #0B132B 35%, #1C2E68 70%, #1D4ED8 100%);
    border-radius: 24px;
    padding: 36px 42px;
    color: #FFFFFF;
    margin-bottom: 24px;
    border: 1px solid rgba(96, 165, 250, 0.35);
    animation: cyberEntrance 0.65s cubic-bezier(0.16, 1, 0.3, 1) both, heroGlowPulse 6s infinite ease-in-out;
    position: relative;
    overflow: hidden;
}
.hero-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 80%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38BDF8, #818CF8, transparent);
    animation: scannerPass 3.6s infinite linear;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.45);
    color: #BAE6FD;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 14px;
    letter-spacing: 0.8px;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);
    animation: beaconPulse 3.5s infinite ease-in-out;
}
.hero-title {
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -0.6px;
    line-height: 1.25;
    background: linear-gradient(135deg, #FFFFFF 30%, #BAE6FD 80%, #7DD3FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 14.5px;
    color: #CBD5E1;
    line-height: 1.65;
    margin-bottom: 16px;
    max-width: 950px;
}
.hero-features {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 12px;
}
.feature-pill {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(147, 197, 253, 0.3);
    backdrop-filter: blur(10px);
    border-radius: 999px;
    padding: 5px 13px;
    font-size: 12px;
    color: #F1F5F9;
    font-weight: 600;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}
.feature-pill:hover {
    background: rgba(30, 58, 138, 0.65);
    border-color: #38BDF8;
    color: #38BDF8;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.45);
    transform: translateY(-2px);
}

/* 步骤进度条 HUD 轨道 */
.step-progress-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 26px;
    background: rgba(241, 245, 249, 0.9);
    border: 1px solid #E2E8F0;
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 6px;
    gap: 10px;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03);
    animation: cyberEntrance 0.55s cubic-bezier(0.16, 1, 0.3, 1) 0.08s both;
}
.step-capsule {
    flex: 1;
    text-align: center;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 13.5px;
    font-weight: 700;
    color: #64748B;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}
.step-capsule.active {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    color: #FFFFFF !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
    transform: translateY(-1px);
}
.step-capsule.completed {
    background: #EEF2FF;
    color: #3730A3;
    border: 1px solid #C7D2FE;
}

/* 模块分段标题 */
.step-header {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    border-left: 5px solid #2563EB;
    padding-left: 14px;
    margin: 22px 0 18px 0;
    display: flex;
    align-items: center;
    letter-spacing: -0.3px;
    animation: cyberEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* 12道微观情境评测 — 阶梯式科技座舱 Radio 选项卡 */
div[data-testid="stRadio"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 20px 24px;
    box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
    animation: cyberEntrance 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}
/* 12道题阶梯式微延迟流式滑入 (Staggered Cascading Entrance) */
div[data-testid="stRadio"]:nth-of-type(1) { animation-delay: 0.03s; }
div[data-testid="stRadio"]:nth-of-type(2) { animation-delay: 0.07s; }
div[data-testid="stRadio"]:nth-of-type(3) { animation-delay: 0.11s; }
div[data-testid="stRadio"]:nth-of-type(4) { animation-delay: 0.15s; }
div[data-testid="stRadio"]:nth-of-type(5) { animation-delay: 0.19s; }
div[data-testid="stRadio"]:nth-of-type(6) { animation-delay: 0.23s; }
div[data-testid="stRadio"]:nth-of-type(7) { animation-delay: 0.27s; }
div[data-testid="stRadio"]:nth-of-type(8) { animation-delay: 0.31s; }
div[data-testid="stRadio"]:nth-of-type(9) { animation-delay: 0.35s; }
div[data-testid="stRadio"]:nth-of-type(10) { animation-delay: 0.39s; }
div[data-testid="stRadio"]:nth-of-type(11) { animation-delay: 0.43s; }
div[data-testid="stRadio"]:nth-of-type(12) { animation-delay: 0.47s; }

div[data-testid="stRadio"]:hover {
    border-color: #93C5FD;
    box-shadow: 0 10px 24px -4px rgba(37, 99, 235, 0.1);
}
div[data-testid="stRadio"] > label {
    font-size: 15.5px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin-bottom: 10px !important;
    line-height: 1.5 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 9px;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    position: relative;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 12px 18px 12px 20px;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    overflow: hidden;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label::before {
    content: '';
    position: absolute;
    left: 0;
    top: 25%;
    height: 50%;
    width: 3.5px;
    background: #38BDF8;
    border-radius: 0 4px 4px 0;
    opacity: 0;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    background: #EFF6FF;
    border-color: #60A5FA;
    transform: translateX(6px);
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.1);
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:hover::before {
    opacity: 1;
    height: 70%;
    top: 15%;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #EFF6FF 0%, #E0E7FF 100%) !important;
    border-color: #2563EB !important;
    box-shadow: 0 0 0 1px #2563EB, 0 6px 18px rgba(37, 99, 235, 0.2) !important;
}

/* 量子全息神经元解码状态卡 (Step 3 专属) */
.cyber-decode-card {
    position: relative;
    background: linear-gradient(135deg, #050814 0%, #0F172A 40%, #1E3A8A 100%);
    border-radius: 20px;
    padding: 24px 30px;
    color: #FFFFFF;
    margin-bottom: 24px;
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 16px 36px -6px rgba(14, 165, 233, 0.28), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
    overflow: hidden;
    animation: cyberEntrance 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.cyber-scanner-sweep {
    position: absolute;
    top: 0;
    left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.22), transparent);
    transform: skewX(-25deg);
    animation: scannerPass 3.2s infinite ease-in-out;
    pointer-events: none;
}
.cyber-pulse-dot {
    width: 10px;
    height: 10px;
    background: #38BDF8;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px #38BDF8;
    animation: beaconPulse 2s infinite ease-in-out;
}
.cyber-decode-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.cyber-chip {
    font-size: 12px;
    font-weight: 600;
    color: #E2E8F0;
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 4px 12px;
    border-radius: 999px;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}
.cyber-chip:hover {
    border-color: #38BDF8;
    color: #38BDF8;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
}

/* 终极专业推荐卡片 — 阶梯滑入全息仓与机甲边角 HUD Bracket */
.major-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 26px;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 6px 22px -4px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
    animation: cyberEntrance 0.65s cubic-bezier(0.16, 1, 0.3, 1) both;
}
/* 卡片阶梯式滑入延迟 (Staggered Entrance) */
.major-card:nth-of-type(1) { animation-delay: 0.08s; }
.major-card:nth-of-type(2) { animation-delay: 0.18s; }
.major-card:nth-of-type(3) { animation-delay: 0.28s; }
.major-card:nth-of-type(4) { animation-delay: 0.38s; }
.major-card:nth-of-type(5) { animation-delay: 0.48s; }

/* 顶端全息流光激光线 */
.major-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563EB 0%, #06B6D4 50%, #8B5CF6 100%);
    opacity: 0.85;
    transition: all 0.3s ease;
}
/* 卡片右上角赛博机甲指示角标 HUD Bracket */
.major-card::after {
    content: '';
    position: absolute;
    top: 14px;
    right: 14px;
    width: 14px;
    height: 14px;
    border-top: 2px solid rgba(56, 189, 248, 0.4);
    border-right: 2px solid rgba(56, 189, 248, 0.4);
    border-top-right-radius: 6px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.major-card:hover {
    transform: translateY(-6px) scale(1.006);
    border-color: #60A5FA;
    box-shadow: 0 22px 48px -10px rgba(37, 99, 235, 0.22), 0 0 0 1px rgba(56, 189, 248, 0.35);
}
.major-card:hover::before {
    height: 4px;
    opacity: 1;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.6);
}
.major-card:hover::after {
    width: 26px;
    height: 26px;
    border-color: #06B6D4;
    box-shadow: 2px -2px 10px rgba(6, 182, 212, 0.5);
}

/* 高阶等离子能量徽章 (Mono风格) */
.badge-tag {
    display: inline-block;
    padding: 4px 11px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
    margin-bottom: 4px;
    font-family: 'JetBrains Mono', monospace, sans-serif;
    transition: all 0.2s ease;
}
.badge-hard { background: #EEF2FF; color: #3730A3; border: 1px solid #818CF8; box-shadow: 0 0 8px rgba(129, 140, 248, 0.18); }
.badge-warn { background: #FEF3C7; color: #92400E; border: 1px solid #FBBF24; box-shadow: 0 0 8px rgba(251, 191, 36, 0.18); }
.badge-good { background: #ECFDF5; color: #065F46; border: 1px solid #34D399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.18); }
.badge-info { background: #F0F9FF; color: #0369A1; border: 1px solid #38BDF8; box-shadow: 0 0 8px rgba(56, 189, 248, 0.18); }
.badge-purple { background: #FAF5FF; color: #6B21A8; border: 1px solid #C084FC; box-shadow: 0 0 8px rgba(192, 132, 252, 0.18); }

/* 专属量身推荐理由 — AI 神经解码舱 */
.reason-box {
    background: linear-gradient(135deg, rgba(239, 246, 255, 0.85) 0%, rgba(240, 249, 255, 0.95) 100%);
    border-left: 5px solid #0284C7;
    border-top: 1px solid rgba(186, 230, 253, 0.5);
    border-right: 1px solid rgba(186, 230, 253, 0.5);
    border-bottom: 1px solid rgba(186, 230, 253, 0.5);
    border-radius: 0 14px 14px 0;
    padding: 13px 18px;
    margin-top: 10px;
    margin-bottom: 12px;
    font-size: 13.5px;
    color: #0C4A6E;
    line-height: 1.65;
    box-shadow: 0 2px 10px rgba(2, 132, 199, 0.08);
}

/* 招生包装打假 Truth Filter — 赛博打假扫描室 */
.truth-box {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-left: 5px solid #D97706;
    border-radius: 0 14px 14px 0;
    padding: 14px 18px;
    margin-top: 12px;
    font-size: 13.5px;
    line-height: 1.65;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.08);
}
.truth-label {
    font-weight: 800;
    color: #92400E;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
}
.myth-text {
    color: #B91C1C;
    text-decoration: line-through;
    background: rgba(254, 226, 226, 0.65);
    padding: 2px 7px;
    border-radius: 5px;
    font-weight: 600;
}
.fact-text {
    color: #14532D;
    font-weight: 700;
    background: rgba(220, 252, 231, 0.65);
    padding: 2px 7px;
    border-radius: 5px;
}

/* 行业真实生态底栏 */
.insight-box {
    background: #F8FAFC;
    border-left: 5px solid #2563EB;
    border-radius: 0 14px 14px 0;
    padding: 13px 18px;
    margin-top: 10px;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.65;
    border-top: 1px solid #F1F5F9;
    border-bottom: 1px solid #F1F5F9;
    border-right: 1px solid #F1F5F9;
}

/* 孪生备选对标台 — 全息对接舱 */
.sister-card-box {
    background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
    border: 1px solid #A7F3D0;
    border-left: 5px solid #059669;
    border-radius: 0 14px 14px 0;
    padding: 16px 20px;
    margin-top: 14px;
    margin-bottom: 10px;
    font-size: 13px;
    line-height: 1.65;
    box-shadow: 0 4px 18px -3px rgba(5, 150, 105, 0.12);
}
.sister-header {
    font-weight: 800;
    color: #065F46;
    font-size: 14.5px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sister-item {
    background: #FFFFFF;
    border: 1px solid #D1FAE5;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 10px;
    transition: all 0.25s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}
.sister-item:hover {
    border-color: #34D399;
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.12);
    transform: translateX(4px);
}

/* 避坑拦截抽屉 */
.intercept-box {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border: 1px solid #FCA5A5;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
    animation: cyberEntrance 0.5s ease-out;
}

/* 全局主次按钮科技化升级 */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 45%, #2563EB 80%, #06B6D4 100%) !important;
    background-size: 200% 200% !important;
    border: none !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 11px 24px !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.38) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    animation: borderGlowSweep 6s ease infinite !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) scale(1.015) !important;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.55), 0 0 16px rgba(6, 182, 212, 0.4) !important;
}
.stButton > button[kind="secondary"] {
    border-radius: 12px !important;
    border: 1px solid #CBD5E1 !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #3B82F6 !important;
    color: #2563EB !important;
    background: #EFF6FF !important;
    transform: translateY(-1px) !important;
}

/* 屏幕右下角悬浮置顶按钮 (等离子流光浮动) */
.float-scroll-btn {
    position: fixed;
    bottom: 28px;
    right: 30px;
    z-index: 999999;
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
    color: #FFFFFF !important;
    text-decoration: none !important;
    padding: 10px 18px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(30, 58, 138, 0.45), 0 0 0 1px rgba(96, 165, 250, 0.3) inset;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.25s ease-in-out;
    animation: beaconPulse 4s infinite ease-in-out;
}
.float-scroll-btn:hover {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #06B6D4 100%);
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6), 0 0 16px rgba(6, 182, 212, 0.5);
    color: #FFFFFF !important;
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
        "target_goal": "🧭 尚不明确 / 开放探索（根据后续12道实战情境题，测出我的真实天赋与兴趣）",
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
# 宇宙全息穿梭引力跃迁动效 (首次访问自动震撼呈现 / 侧边栏支持随时重温)
# ============================================================================
if "replay_cosmic_intro" not in st.session_state:
    st.session_state.replay_cosmic_intro = False

render_cosmic_intro(force_replay=st.session_state.replay_cosmic_intro)
if st.session_state.replay_cosmic_intro:
    st.session_state.replay_cosmic_intro = False

# ============================================================================
# 顶部锚点与自动置顶控制
# ============================================================================
st.markdown('<div id="page-top-anchor" style="position:absolute;top:0;left:0;height:0;width:0;opacity:0;"></div>', unsafe_allow_html=True)
st.markdown('<a href="#page-top-anchor" class="float-scroll-btn" target="_self">⬆️ 回到顶部</a>', unsafe_allow_html=True)

if "last_rendered_step" not in st.session_state:
    st.session_state.last_rendered_step = st.session_state.current_step

if st.session_state.current_step != st.session_state.last_rendered_step or st.session_state.get("need_scroll_top", False):
    scroll_to_top()
    st.session_state.last_rendered_step = st.session_state.current_step
    st.session_state.need_scroll_top = False

# ============================================================================
# 顶部 Hero Banner
# ============================================================================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-badge">⚡ 2026 新高考专属 · 穿透招生包装 · 让底层天赋自然浮现</div>
        <div class="hero-title">🧭 航向未来 · 高考专业天赋解码与现实导航系统</div>
        <div class="hero-subtitle">
            不问抽象空话，用 12 个真实微观生活冲突直击动手韧性与抗压底线；深度穿透 94 个大类真实现实生态，让契合你的最优职业路径清晰呈现。
        </div>
        <div class="hero-features">
            <span class="feature-pill">🛡️ 94 大类招生包装打假</span>
            <span class="feature-pill">🧭 12 道微观生活情境评测</span>
            <span class="feature-pill">🔄 35 个孪生备选对标台</span>
            <span class="feature-pill">🚨 19 大下行赛道全景避雷</span>
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
        st.session_state.need_scroll_top = True
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

    st.markdown("---")
    st.markdown("### 🌌 全息视觉特效")
    if st.button("🚀 重温星际穿梭引力跃迁", use_container_width=True):
        st.session_state.replay_cosmic_intro = True
        st.rerun()

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
            "本科毕业后你最渴望的主要出路是（若现阶段不明确，建议保留默认开放探索）：",
            options=[
                "🧭 尚不明确 / 开放探索（根据后续12道实战情境题，测出我的真实天赋与兴趣）",
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
            st.session_state.need_scroll_top = True
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
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:10px;margin:28px 0 16px 0;">
                    <span style="height:2px;width:24px;background:#38BDF8;border-radius:2px;"></span>
                    <span style="font-size:16px;font-weight:800;color:#1E3A8A;letter-spacing:-0.2px;">🏷️ {current_module}</span>
                    <span style="flex:1;height:1px;background:linear-gradient(90deg, rgba(56,189,248,0.4), transparent);"></span>
                </div>
                """,
                unsafe_allow_html=True
            )

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
            st.session_state.need_scroll_top = True
            st.rerun()
    with c_btn2:
        if st.button("动态计算并查看推荐大屏 ➔", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.session_state.need_scroll_top = True
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

    # 量子神经元矩阵运算状态全息卡 (动态光影扫描)
    st.markdown(
        """
        <div class="cyber-decode-card">
            <div class="cyber-scanner-sweep"></div>
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span class="cyber-pulse-dot"></span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800;letter-spacing:1px;color:#38BDF8;">
                        QUANTUM NEURAL ENGINE · 天赋拓扑全息矩阵解算完成
                    </span>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#BAE6FD;background:rgba(15,23,42,0.65);padding:3px 12px;border-radius:999px;border:1px solid rgba(56,189,248,0.3);letter-spacing:0.5px;">
                    STATUS: OPTIMAL · 94 MAJORS PARSED
                </div>
            </div>
            <div style="font-size:18px;font-weight:800;margin-bottom:10px;background:linear-gradient(135deg, #FFFFFF 0%, #BAE6FD 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🎯 多维天赋与行业生态耦合成功：已为你匹配出 Top 5 最优攻守平衡方案
            </div>
            <div class="cyber-decode-chips">
                <span class="cyber-chip">⚡ 12道微观情境本能推演</span>
                <span class="cyber-chip">🛡️ 19大高危下行赛道已严密熔断</span>
                <span class="cyber-chip">🔄 35组孪生备选对标池已挂载</span>
                <span class="cyber-chip">🎓 招生简章包装谎言滤镜已穿透</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================================
    # 专属【19 大高危与下行避坑专业深度全景剖析专区】（独立专属按键专区）
    # ========================================================================
    pitfall_encyclopedia = load_pitfall_encyclopedia()
    if pitfall_encyclopedia:
        with st.expander("🚨 【志愿避坑排雷指南 / 19 大高危与下行专业深度全景剖析专区】（点击展开查阅为何劝退、详细优劣势与唯一生存路径）", expanded=False):
            st.markdown(
                """
                <div style="font-size:13px;color:#991B1B;background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;padding:10px 14px;margin-bottom:14px;line-height:1.6;">
                    🛡️ <b>独立排雷专区说明</b>：以下 19 个专业受<b>行业周期断崖、生化环材毒害倒班、偏远野外极端艰苦或纯管理低壁垒</b>影响，已彻底移出算法推荐榜。在此专区中，我们为你<b>客观剖析每个专业的招生宣称、残酷日常、唯一优点及极少数适合人群</b>，帮助你与家庭理性决策，坚决不踩暗坑！
                </div>
                """,
                unsafe_allow_html=True
            )
            tab_p1, tab_p2, tab_p3 = st.tabs([
                "🏗️ 偏远野外与周期断崖 (5个)",
                "🧪 传统生化环材高危 (5个)",
                "📋 虚假高大上与低壁垒行政 (9个)"
            ])

            def render_pitfall_cards(target_group):
                for p_name, p_info in pitfall_encyclopedia.items():
                    if target_group in p_info.get("group", ""):
                        st.markdown(
                            f"""
                            <div style="background:#FFFFFF;border:1px solid #E5E7EB;border-left:4px solid #DC2626;border-radius:8px;padding:14px 16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:8px;">
                                    <span style="font-size:16px;font-weight:800;color:#991B1B;">⚠️ {p_info['name']}</span>
                                    <span style="background:#FEE2E2;color:#991B1B;font-weight:700;font-size:11.5px;padding:2px 8px;border-radius:6px;">风险评级: {p_info['risk_level']}</span>
                                </div>
                                <div style="font-size:12.5px;margin-bottom:4px;">
                                    <span style="font-weight:700;color:#92400E;">🔥 招生宣传包装: </span>
                                    <span style="text-decoration:line-through;color:#B45309;opacity:0.9;">“{p_info['marketing_myth']}”</span>
                                </div>
                                <div style="font-size:12.5px;margin-bottom:6px;color:#78350F;">
                                    <span style="font-weight:700;color:#166534;">🥊 真实日常打假: </span>{p_info['truth_unfiltered']}
                                </div>
                                <div style="font-size:12px;color:#065F46;background:#F0FDF4;padding:6px 10px;border-radius:6px;margin-bottom:4px;border:1px solid #DCFCE7;">
                                    ✅ <b>唯一优点与极少数适合人群</b>: {p_info['pros']}
                                </div>
                                <div style="font-size:12px;color:#991B1B;background:#FEF2F2;padding:6px 10px;border-radius:6px;margin-bottom:6px;border:1px solid #FEE2E2;">
                                    ❌ <b>致命硬伤与劝退根因</b>: {p_info['cons']}
                                </div>
                                <div style="font-size:12px;color:#1E3A8A;background:#EFF6FF;padding:6px 10px;border-radius:6px;border:1px dashed #93C5FD;">
                                    🧭 <b>报考避坑忠告</b>: {p_info['verdict']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with tab_p1:
                render_pitfall_cards("偏远艰苦野外与周期断崖组")
            with tab_p2:
                render_pitfall_cards("传统‘生化环材’高危替代组")
            with tab_p3:
                render_pitfall_cards("虚假高大上与低壁垒行政组")

    st.markdown("### 🏆 专属精准推荐专业 Top 5")

    # 循环渲染 Top 推荐卡片
    for c in top_recommendations:
        st.markdown(
            f"""
            <div class="major-card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:14px;gap:8px;">
                    <div style="display:flex;align-items:center;flex-wrap:wrap;gap:8px;">
                        <span style="font-size:24px;font-weight:800;color:#0F172A;letter-spacing:-0.5px;">{c['rank']} {c['name']}</span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:12.5px;background:linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(6,182,212,0.15) 100%);color:#0284C7;border:1px solid rgba(14,165,233,0.35);padding:4px 12px;border-radius:999px;font-weight:800;box-shadow:0 0 14px rgba(14,165,233,0.18);display:inline-flex;align-items:center;gap:4px;">⚡ 匹配度 {c['score']} 分</span>
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
            <div style="margin-bottom:10px;font-size:13px;color:#475569;">
                🏛️ <b>体制内考公考编真实属性</b>: <span style="font-weight:700;color:#1E3A8A;background:#EEF2FF;padding:2px 8px;border-radius:6px;border:1px solid #C7D2FE;">{c['civil_service_tag']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 专属量身推荐理由
        if c.get("recommend_reason"):
            st.markdown(
                f"""
                <div class="reason-box">
                    🎯 <b>为你量身推荐的专属理由</b>: {c['recommend_reason']}
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
                    <span style="font-weight:700;color:#92400E;">宣称包装: </span>
                    <span class="myth-text">“{c['marketing_myth']}”</span>
                </div>
                <div>
                    <span style="font-weight:700;color:#166534;">真实日常打假: </span>
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

        # 孪生备选对标台 / 考生分流对比
        if c.get("sister_benchmarks") and len(c["sister_benchmarks"]) > 0:
            sisters_html = ""
            for s in c["sister_benchmarks"][:2]:
                sisters_html += f"""
                <div class="sister-item">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:5px;">
                        <span style="font-weight:800;font-size:14px;color:#166534;">🔄 孪生对标：{s['sister_name']}</span>
                        <span style="background:#DCFCE7;color:#15803D;font-weight:700;font-size:11.5px;padding:2px 8px;border-radius:6px;border:1px solid #86EFAC;">{s['relation_tag']}</span>
                    </div>
                    <div style="font-size:12.5px;color:#374151;margin-bottom:4px;">
                        📊 <b>录取分差预估</b>: <span style="color:#B45309;font-weight:700;">{s['score_diff']}</span>
                    </div>
                    <div style="font-size:12.5px;color:#1F2937;margin-bottom:4px;">
                        ✅ <b>对标优势</b>: {s['pros']}
                    </div>
                    <div style="font-size:12.5px;color:#4B5563;margin-bottom:5px;">
                        ⚠️ <b>现实代价</b>: {s['cons']}
                    </div>
                    <div style="font-size:12px;color:#1E3A8A;background:#F0FDF4;padding:7px 12px;border-radius:8px;border:1px dashed #86EFAC;line-height:1.5;">
                        🧭 <b>考生报考分流建议</b>: {s['verdict']}
                    </div>
                </div>
                """
            st.markdown(
                f"""
                <div class="sister-card-box">
                    <div class="sister-header">🔄 【孪生备选对标台 / 考生自主分流选择】</div>
                    <div style="font-size:12.5px;color:#15803D;margin-bottom:6px;">
                        💡 <b>专业不应非此即彼，把选择权交给你</b>：若你对该大类感兴趣但担忧分数过高、或追求不同变现路径，可对比以下孪生备选赛道：
                    </div>
                    {sisters_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        # 核心细分专业
        if c.get("majors") and len(c["majors"]) > 0:
            st.markdown("<div style='margin-top:16px;font-size:14px;'><strong>🔬 核心细分推荐专业：</strong></div>", unsafe_allow_html=True)
            m_cols = st.columns(len(c["majors"]))
            for idx, m in enumerate(c["majors"]):
                with m_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;height:100%;box-shadow:0 2px 6px rgba(0,0,0,0.02);transition:all 0.2s ease;">
                            <div style="font-weight:800;color:#1E3A8A;font-size:14px;">{m['name']}</div>
                            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#64748B;margin-bottom:4px;">代码: {m['code']}</div>
                            <div style="font-size:12px;color:#475569;line-height:1.5;">{m['desc']}</div>
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
            <div style="margin-top:14px;font-size:13px;color:#334155;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);border:1px solid #E2E8F0;padding:10px 14px;border-radius:10px;gap:8px;">
                <div>🏛️ <b>第四轮学科评估顶尖代表院校</b>: <span style="font-weight:700;color:#1E3A8A;">{top_schools_str}</span></div>
                <div>🎯 <b>结合位次 (前{user_rank}%) 报考策略</b>: <span style="font-weight:800;color:#2563EB;background:rgba(37,99,235,0.08);padding:2px 8px;border-radius:6px;">{tier_tip}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 底部院校层级实情与报考提示（给考生清晰标注现实情况）
        if c.get("tier_alert"):
            st.markdown(
                f"""
                <div style="margin-top:12px;font-size:13px;color:#92400E;background:linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);border-left:5px solid #F59E0B;padding:12px 16px;border-radius:0 12px 12px 0;line-height:1.6;box-shadow:0 2px 8px rgba(245,158,11,0.08);">
                    {c['tier_alert']}
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
            st.session_state.need_scroll_top = True
            st.rerun()
