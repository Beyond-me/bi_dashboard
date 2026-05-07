# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_optimized.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面（优化版）

import streamlit as st

# ========== 1. 页面配置 ==========
st.set_page_config(
    page_title="数智科技 | 未来数字化引擎",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 2. 动态粒子背景 & 核心样式 ==========
# 注入 JavaScript 粒子背景和高级 CSS
st.markdown("""
<style>
    /* 引入极简科技字体 */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');

    .stApp {
        background: #0a0e17; /* 深邃太空黑 */
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* 隐藏默认元素 */
    header, footer, .stDeployButton {visibility: hidden;}

    /* 霓虹发光卡片 */
    .neon-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }

    .neon-card:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: #00f2fe;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.3);
    }

    /* 渐变文字 */
    .gradient-text {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
    }

    /* 炫酷按钮 */
    .glow-button {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        border: none;
        color: white;
        padding: 15px 40px;
        border-radius: 50px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        transition: 0.3s;
        text-decoration: none;
        display: inline-block;
    }

    .glow-button:hover {
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.7);
        transform: scale(1.05);
    }

    /* 浮动动画 */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    .floating-icon {
        animation: float 4s ease-in-out infinite;
        font-size: 4rem;
    }
</style>

<!-- 粒子背景 Canvas -->
<canvas id="canvas" style="position: fixed; top: 0; left: 0; z-index: -1;"></canvas>
<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    let particlesArray = [];
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.1;
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.size > 0.2) this.size -= 0.01;
        }
        draw() {
            ctx.fillStyle = 'rgba(0, 242, 254, 0.8)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    function init() {
        for (let i = 0; i < 100; i++) { particlesArray.push(new Particle()); }
    }
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
            if (particlesArray[i].size <= 0.3) {
                particlesArray.splice(i, 1);
                i--;
                particlesArray.push(new Particle());
            }
        }
        requestAnimationFrame(animate);
    }
    init(); animate();
</script>
""", unsafe_allow_html=True)

# ========== 3. 头部 Hero 区域 ==========
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
col_hero1, col_hero2 = st.columns([1.2, 0.8])

with col_hero1:
    st.markdown("""
    <h3 style="color: #00f2fe; letter-spacing: 5px; margin-bottom: 0;">DIGITAL TRANSFORMATION</h3>
    <h1 style="font-size: 5rem; line-height: 1.1; margin-bottom: 20px;">
        定义 <span class="gradient-text">未来管理</span><br>新范式
    </h1>
    <p style="font-size: 1.25rem; color: #a0aec0; max-width: 600px; line-height: 1.6; margin-bottom: 40px;">
        我们不只是在写代码，我们是在为您构建数字世界的“神经系统”。从 BI 洞察到 AI 驱动的 CRM，数智科技让您的企业拥有思考的能力。
    </p>
    <a href="#contact" class="glow-button">开启数字化之旅 →</a>
    """, unsafe_allow_html=True)

with col_hero2:
    st.markdown('<div class="floating-icon" style="text-align: center;">🚀</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(0, 242, 254, 0.1); border-radius: 50%; width: 300px; height: 300px; margin: 0 auto; filter: blur(60px); position: absolute; z-index: -1;"></div>
    """, unsafe_allow_html=True)

# ========== 4. 核心技术展示 (Grid 布局) ==========
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-family: Orbitron;">核心引擎模块</h2>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

service_items = [
    {
        "title": "BI 智能决策",
        "icon": "⚡",
        "desc": "秒级处理千万量级数据，将枯燥的表格转化为直观的业务洞察，让决策不再靠猜。",
        "color": "#00f2fe"
    },
    {
        "title": "AI 客户大脑",
        "icon": "🧠",
        "desc": "基于机器学习的客户画像系统，精准预测流失与转化，实现真正的自动化私域运营。",
        "color": "#4facfe"
    },
    {
        "title": "数字孪生进销存",
        "icon": "🌐",
        "desc": "物理库存与数字世界的实时映射，供应链全链路可视化，效率提升翻倍。",
        "color": "#706fd3"
    }
]

for i, item in enumerate(service_items):
    with [c1, c2, c3][i]:
        st.markdown(f"""
        <div class="neon-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">{item['icon']}</div>
            <h3 style="color: {item['color']};">{item['title']}</h3>
            <p style="color: #cbd5e0; font-size: 0.95rem;">{item['desc']}</p>
            <div style="margin-top: 20px; font-size: 0.8rem; color: {item['color']}; font-weight: bold;">查看技术文档 ></div>
        </div>
        """, unsafe_allow_html=True)

# ========== 5. 炫酷的数据动效展示 ==========
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
st.write("---")
col_data1, col_data2 = st.columns([1, 1])

with col_data1:
    st.markdown("""
    <h2 style="font-family: Orbitron;">我们用数据说话</h2>
    <div style="margin-top: 40px;">
        <div style="margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>决策效率提升</span><span>85%</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;">
                <div style="background: #00f2fe; width: 85%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px #00f2fe;"></div>
            </div>
        </div>
        <div style="margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>运营成本降低</span><span>40%</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;">
                <div style="background: #4facfe; width: 40%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px #4facfe;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_data2:
    # 嵌入一个简单的炫酷图表
    import pandas as pd
    import numpy as np

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['AI预测', '实际销售', '库存水位']
    )
    st.line_chart(chart_data)

# ========== 6. 交互式联系表单 ==========
st.markdown('<div id="contact" style="height: 100px;"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="neon-card" style="max-width: 800px; margin: 0 auto; border: 2px solid #00f2fe;">
    <h2 style="text-align: center; color: #00f2fe; font-family: Orbitron;">预约您的数字蓝图</h2>
    <p style="text-align: center; color: #a0aec0; margin-bottom: 40px;">填写下方信息，我们的架构师将在 1 小时内为您提供初步方案</p>
""", unsafe_allow_html=True)

with st.form("fancy_contact"):
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        name = st.text_input("您的尊称", placeholder="例如：王总")
        phone = st.text_input("私密电话", placeholder="仅用于方案对接")
    with f_c2:
        company = st.text_input("企业全称", placeholder="例如：某某集团")
        budget = st.select_slider("项目预期规模", options=["初创版", "成长版", "企业版", "旗舰定制"])

    msg = st.text_area("您面临的业务挑战", placeholder="描述您最想解决的问题...")

    submit = st.form_submit_button("立即获取数智方案")
    if submit:
        if name and phone:
            st.balloons()
            st.success("🚀 指令已接收！系统已将您的需求分配给首席架构师，请保持电话畅通。")

st.markdown("</div>", unsafe_allow_html=True)

# ========== 7. 页脚 ==========
st.markdown("""
<div style="text-align: center; padding: 60px 0; color: #4a5568; font-size: 0.8rem;">
    <p>数智科技 - NEURAL INTELLIGENCE TECH © 2026</p>
    <p style="letter-spacing: 2px;">POWERED BY STREAMLIT & AI ENGINE</p>
</div>
""", unsafe_allow_html=True)
