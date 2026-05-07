# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_optimized.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面（优化版）

import streamlit as st

# ========== 1. 页面配置 ==========
st.set_page_config(
    page_title="数智科技 - 企业数字化解决方案专家",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 2. 注入全局 CSS 样式 ==========
# 统一管理样式，避免 iframe 隔离导致的样式失效
st.markdown("""
<style>
    /* 全局背景与字体 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }

    /* 自定义容器 */
    .custom-container {
        padding: 2rem 5rem;
    }
    @media (max-width: 768px) {
        .custom-container { padding: 1rem; }
    }

    /* 头部 Hero 区域 */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 100px 20px;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(30, 60, 114, 0.2);
    }

    /* 卡片通用样式 */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 30px;
        height: 100%;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-10px);
    }

    /* 统计数字 */
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#1e3c72, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 标签样式 */
    .tech-tag {
        background: #e9f7fe;
        color: #3498db;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        margin-right: 5px;
        border: 1px solid #d1e9f7;
    }

    /* 隐藏 Streamlit 默认页眉页脚（可选） */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ========== 3. 页面内容渲染 ==========

# --- 导航锚点 ---
st.markdown('<div id="home"></div>', unsafe_allow_html=True)

# --- Hero Header ---
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 20px;">数智科技</h1>
    <h2 style="font-size: 1.8rem; font-weight: 300; opacity: 0.9; margin-bottom: 40px;">企业数字化解决方案专家</h2>
    <p style="max-width: 700px; margin: 0 auto 40px; line-height: 1.8; font-size: 1.1rem; color: #e2e8f0;">
        专注 BI 商业智能、定制化 CRM 与 智能进销存系统。我们用数据驱动您的业务增长，助力企业实现全流程数字化转型。
    </p>
    <div style="display: flex; justify-content: center; gap: 15px;">
        <a href="#contact" style="text-decoration: none;">
            <div style="background: #3498db; color: white; padding: 15px 35px; border-radius: 50px; font-weight: 600;">免费方案咨询</div>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 核心统计 ---
st.markdown('<div id="stats" style="padding-top: 50px;"></div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
stats_data = [
    ("50+", "成功项目"), ("30+", "标杆客户"),
    ("99%", "满意度"), ("7×24", "技术支持")
]
for i, (num, title) in enumerate(stats_data):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="stat-number">{num}</div>
            <div style="color: #2c3e50; font-weight: 600;">{title}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 核心服务 ---
st.markdown('<h2 style="text-align: center; margin: 80px 0 40px;">核心服务模块</h2>', unsafe_allow_html=True)
s_col1, s_col2, s_col3 = st.columns(3)

services = [
    {"icon": "📊", "title": "BI 商业智能", "desc": "多维度数据看板，实时监控业务核心指标，支持决策透明化。"},
    {"icon": "🤝", "title": "CRM 客户管理", "desc": "全生命周期客户追踪，自动化营销漏斗，提升转化与留存。"},
    {"icon": "📦", "title": "智能进销存", "desc": "毫秒级库存同步，智能补货预警，优化供应链周转效率。"}
]

for i, s in enumerate(services):
    with [s_col1, s_col2, s_col3][i]:
        st.markdown(f"""
        <div class="glass-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">{s['icon']}</div>
            <h3 style="color: #1e3c72;">{s['title']}</h3>
            <p style="color: #666; line-height: 1.7;">{s['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- 成功案例 (使用原生组件增强交互) ---
st.markdown('<h2 style="text-align: center; margin: 80px 0 40px;">行业解决方案案例</h2>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["零售进销存", "科技CRM", "制造BI平台"])

with tab1:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.image("https://img.icons8.com/clouds/500/shipped.png", width=300)
    with col_b:
        st.subheader("五金零售进销存系统")
        st.markdown("""
        - **挑战**：手工记账混乱，库存积压严重。
        - **方案**：基于 Python 构建的轻量化进销存，支持扫码入库与自动盘点。
        - **结果**：库存周转率提升 **35%​**，财务对账时间缩短至分钟级。
        """)
        st.markdown('<span class="tech-tag">Streamlit</span><span class="tech-tag">SQLite</span>',
                    unsafe_allow_html=True)

# --- 联系我们 (真正可用的表单) ---
st.markdown('<div id="contact" style="padding-top: 80px;"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; margin-bottom: 10px;">立即获取定制方案</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 40px;">我们的技术顾问将在24小时内联系您</p>',
            unsafe_allow_html=True)

with st.container():
    # 使用 Streamlit 原生表单，保证数据安全收集
    with st.form("contact_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("您的姓名")
            phone = st.text_input("联系电话")
        with c2:
            company = st.text_input("企业名称")
            industry = st.selectbox("所属行业", ["制造业", "零售/电商", "服务业", "其他"])

        needs = st.text_area("需求描述（如：我想做一个BI看板...）")

        submit_button = st.form_submit_button("提交咨询请求")

        if submit_button:
            if name and phone:
                st.success(f"感谢您的信任，{name}！您的需求已收到，我们会尽快拨打 {phone} 与您联系。")
                # 这里可以添加发送邮件或存入数据库的代码
            else:
                st.error("请填写姓名和联系电话以便我们联系您。")

# --- 页脚 ---
st.markdown("""
<div style="background: #1e3c72; color: white; padding: 60px 20px 20px; margin-top: 100px; border-radius: 40px 40px 0 0;">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; max-width: 1200px; margin: 0 auto;">
        <div style="flex: 1; min-width: 250px; margin-bottom: 30px;">
            <h4 style="font-size: 1.5rem; margin-bottom: 20px;">数智科技</h4>
            <p style="opacity: 0.7; font-size: 0.9rem;">为中坚力量提供数字武器</p>
        </div>
        <div style="flex: 1; min-width: 250px; margin-bottom: 30px;">
            <h4 style="margin-bottom: 20px;">联系方式</h4>
            <p style="opacity: 0.7; font-size: 0.9rem;">📧 contact@datech.com</p>
            <p style="opacity: 0.7; font-size: 0.9rem;">📞 400-888-8888</p>
        </div>
    </div>
    <div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; margin-top: 40px; font-size: 0.8rem; opacity: 0.5;">
        © 2026 数智科技有限公司 版权所有 | 京ICP备12345678号
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 4. 侧边栏优化 ==========
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)
    st.title("数智科技导航")
    st.info("专注企业级数字化转型")

    st.markdown("### 快速跳转")
    # 注意：Streamlit 侧边栏跳转原生支持较弱，建议配合锚点或 st.radio 模拟页面切换
    st.markdown("- [首页](#home)")
    st.markdown("- [核心服务](#stats)")
    st.markdown("- [获取方案](#contact)")

    st.divider()
    st.write("📞 咨询热线：400-888-8888")
