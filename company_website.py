# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_final.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (完整可用版)

import streamlit as st
import pandas as pd
from datetime import datetime

# ========== 页面配置 ==========
st.set_page_config(
    page_title="数智科技 - 企业数字化解决方案专家",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 完整的CSS样式 ==========
st.markdown("""
<style>
    /* 全局样式重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* 主体容器 */
    .main-content {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
    }

    /* 导航栏样式 */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        padding: 15px 0;
    }

    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
    }

    .logo {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
    }

    .nav-links {
        display: flex;
        gap: 30px;
    }

    .nav-link {
        text-decoration: none;
        color: #2c3e50;
        font-weight: 500;
        transition: color 0.3s;
    }

    .nav-link:hover {
        color: #3498db;
    }

    .cta-button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
    }

    /* 英雄区域样式 */
    .hero-section {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        padding: 100px 20px;
        text-align: center;
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-content {
        max-width: 800px;
        margin: 0 auto;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 20px;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 40px;
    }

    .hero-buttons {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .hero-btn {
        padding: 15px 30px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        border: none;
        font-size: 1rem;
    }

    .hero-btn-primary {
        background: white;
        color: #3498db;
    }

    .hero-btn-secondary {
        background: transparent;
        color: white;
        border: 2px solid white;
    }

    .hero-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }

    /* 通用卡片样式 */
    .card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        padding: 30px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }

    /* 统计卡片 */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        padding: 50px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .stat-card {
        text-align: center;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 10px;
    }

    .stat-title {
        font-size: 1.2rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .stat-desc {
        color: #7f8c8d;
    }

    /* 服务卡片 */
    .services-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        padding: 50px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .service-card {
        padding: 30px;
    }

    .service-icon {
        font-size: 3rem;
        margin-bottom: 20px;
    }

    .service-title {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 15px;
    }

    .service-desc {
        color: #7f8c8d;
        margin-bottom: 20px;
        line-height: 1.6;
    }

    .features-list {
        list-style: none;
    }

    .features-list li {
        padding: 8px 0;
        position: relative;
        padding-left: 25px;
    }

    .features-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #27ae60;
        font-weight: bold;
    }

    /* 项目卡片 */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        padding: 50px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .project-card {
        border-radius: 15px;
        overflow: hidden;
    }

    .project-image {
        height: 200px;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }

    .project-content {
        padding: 25px;
        background: white;
    }

    .project-title {
        font-size: 1.4rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .project-desc {
        color: #7f8c8d;
        margin-bottom: 20px;
        line-height: 1.6;
    }

    .tech-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }

    .tech-tag {
        background: #eef7ff;
        color: #3498db;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
    }

    .project-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* 表单样式 */
    .contact-form {
        max-width: 600px;
        margin: 0 auto;
        padding: 50px 20px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-label {
        display: block;
        margin-bottom: 8px;
        color: #2c3e50;
        font-weight: 500;
    }

    .form-input {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
    }

    .form-textarea {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        min-height: 120px;
        resize: vertical;
    }

    /* 页脚样式 */
    .footer {
        background: #2c3e50;
        color: white;
        padding: 60px 20px 30px;
    }

    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 40px;
    }

    .footer-column h4 {
        font-size: 1.3rem;
        margin-bottom: 20px;
        color: white;
    }

    .footer-links {
        list-style: none;
    }

    .footer-links li {
        margin-bottom: 10px;
    }

    .footer-links a {
        color: #bdc3c7;
        text-decoration: none;
    }

    .footer-links a:hover {
        color: #3498db;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .nav-links {
            display: none;
        }

        .hero-buttons {
            flex-direction: column;
            align-items: center;
        }

        .hero-btn {
            width: 100%;
            max-width: 300px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== 导航栏 ==========
st.markdown("""
<div class="navbar">
    <div class="nav-container">
        <div class="logo">🚀 数智科技</div>
        <div class="nav-links">
            <a href="#home" class="nav-link">首页</a>
            <a href="#services" class="nav-link">服务</a>
            <a href="#projects" class="nav-link">项目案例</a>
            <a href="#contact" class="nav-link">联系我们</a>
        </div>
        <a href="#contact" class="cta-button">免费咨询</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 首页英雄区域 ==========
st.markdown("""
<div class="hero-section" id="home">
    <div class="hero-content">
        <h1 class="hero-title">用数据驱动企业增长<br>用技术赋能业务创新</h1>
        <p class="hero-subtitle">专业的企业级BI系统、CRM系统定制开发，为您的业务提供智能化、可视化的管理解决方案</p>
        <div class="hero-buttons">
            <button class="hero-btn hero-btn-primary">查看案例</button>
            <button class="hero-btn hero-btn-secondary">立即咨询</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 公司亮点统计 ==========
st.markdown("""
<div style="background: #f8f9fa; padding: 20px 0 60px;">
    <div style="text-align: center; margin-bottom: 50px;">
        <h2 style="color: #2c3e50; font-size: 2.5rem; margin-bottom: 15px;">为什么选择我们</h2>
        <p style="color: #7f8c8d; font-size: 1.2rem;">专业的技术团队，丰富的行业经验，完善的服务体系</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">50+</div>
            <h3 class="stat-title">成功项目</h3>
            <p class="stat-desc">覆盖制造业、零售、电商等多个行业</p>
        </div>
        <div class="stat-card">
            <div class="stat-number">30+</div>
            <h3 class="stat-title">企业客户</h3>
            <p class="stat-desc">服务过中小型企业到上市公司</p>
        </div>
        <div class="stat-card">
            <div class="stat-number">99%</div>
            <h3 class="stat-title">客户满意度</h3>
            <p class="stat-desc">完善的售后服务和持续的技术支持</p>
        </div>
        <div class="stat-card">
            <div class="stat-number">7×24</div>
            <h3 class="stat-title">小时响应</h3>
            <p class="stat-desc">快速响应客户需求，及时解决问题</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 服务项目 ==========
st.markdown("""
<div id="services" style="padding: 20px 0 60px;">
    <div style="text-align: center; margin-bottom: 50px;">
        <h2 style="color: #2c3e50; font-size: 2.5rem; margin-bottom: 15px;">核心服务</h2>
        <p style="color: #7f8c8d; font-size: 1.2rem;">为企业提供全方位的数字化解决方案</p>
    </div>

    <div class="services-grid">
        <div class="service-card card">
            <div class="service-icon">📊</div>
            <h3 class="service-title">BI商业智能系统</h3>
            <p class="service-desc">为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。</p>
            <ul class="features-list">
                <li>销售数据分析看板</li>
                <li>库存监控与预警系统</li>
                <li>客户行为分析报表</li>
                <li>实时业绩监控系统</li>
            </ul>
        </div>

        <div class="service-card card">
            <div class="service-icon">🤝</div>
            <h3 class="service-title">CRM客户关系管理</h3>
            <p class="service-desc">全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。</p>
            <ul class="features-list">
                <li>客户全生命周期管理</li>
                <li>销售漏斗与机会管理</li>
                <li>自动化营销工具</li>
                <li>客户服务与支持</li>
            </ul>
        </div>

        <div class="service-card card">
            <div class="service-icon">🛠️</div>
            <h3 class="service-title">定制化管理系统</h3>
            <p class="service-desc">根据企业特定需求，定制开发ERP、OA、进销存等管理系统，完美匹配业务流程。</p>
            <ul class="features-list">
                <li>ERP企业资源计划</li>
                <li>OA办公自动化</li>
                <li>进销存管理系统</li>
                <li>生产制造执行系统</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 项目案例展示 ==========
st.markdown("""
<div id="projects" style="background: #f8f9fa; padding: 20px 0 60px;">
    <div style="text-align: center; margin-bottom: 50px;">
        <h2 style="color: #2c3e50; font-size: 2.5rem; margin-bottom: 15px;">成功案例</h2>
        <p style="color: #7f8c8d; font-size: 1.2rem;">我们为各行业客户提供定制化的数字化解决方案</p>
    </div>

    <div class="projects-grid">
        <div class="project-card card">
            <div class="project-image">五金店进销存系统</div>
            <div class="project-content">
                <h3 class="project-title">五金店进销存管理系统</h3>
                <p class="project-desc">为五金行业定制的进销存管理系统，包含商品管理、采购入库、销售开单、库存预警等功能。</p>
                <div class="tech-tags">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Streamlit</span>
                    <span class="tech-tag">SQLite</span>
                </div>
                <div class="project-meta">
                    <span style="color: #3498db; font-weight: bold;">开发周期：2周</span>
                    <a href="#contact" style="color: #3498db; text-decoration: none; font-weight: bold;">了解详情 →</a>
                </div>
            </div>
        </div>

        <div class="project-card card">
            <div class="project-image">CRM管理系统</div>
            <div class="project-content">
                <h3 class="project-title">企业CRM客户关系管理系统</h3>
                <p class="project-desc">完整的CRM解决方案，包含客户管理、销售机会、联系记录、任务管理、业绩分析等功能。</p>
                <div class="tech-tags">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Streamlit</span>
                    <span class="tech-tag">SQLite</span>
                </div>
                <div class="project-meta">
                    <span style="color: #3498db; font-weight: bold;">开发周期：3周</span>
                    <a href="#contact" style="color: #3498db; text-decoration: none; font-weight: bold;">了解详情 →</a>
                </div>
            </div>
        </div>

        <div class="project-card card">
            <div class="project-image">制造企业BI看板</div>
            <div class="project-content">
                <h3 class="project-title">制造企业BI智能看板</h3>
                <p class="project-desc">为制造企业定制的BI数据分析平台，实时监控生产、销售、库存等关键指标，支持多维度分析。</p>
                <div class="tech-tags">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Plotly</span>
                    <span class="tech-tag">MySQL</span>
                </div>
                <div class="project-meta">
                    <span style="color: #3498db; font-weight: bold;">开发周期：4周</span>
                    <a href="#contact" style="color: #3498db; text-decoration: none; font-weight: bold;">了解详情 →</a>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 技术优势 ==========
st.markdown("""
<div style="padding: 20px 0 60px;">
    <div style="text-align: center; margin-bottom: 50px;">
        <h2 style="color: #2c3e50; font-size: 2.5rem; margin-bottom: 15px;">技术优势</h2>
        <p style="color: #7f8c8d; font-size: 1.2rem;">我们采用先进的技术栈，确保系统稳定、安全、高效</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">⚡</div>
            <h3 class="stat-title">快速开发</h3>
            <p class="stat-desc">使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。</p>
        </div>

        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">🔐</div>
            <h3 class="stat-title">安全可靠</h3>
            <p class="stat-desc">完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。</p>
        </div>

        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">📱</div>
            <h3 class="stat-title">多端适配</h3>
            <p class="stat-desc">响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。</p>
        </div>

        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 20px;">🔄</div>
            <h3 class="stat-title">持续迭代</h3>
            <p class="stat-desc">根据业务发展需求，持续优化升级，确保系统与企业一同成长。</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 在线咨询表单 ==========
st.markdown("""
<div id="contact" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px;">
    <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <h2 style="font-size: 2.5rem; margin-bottom: 20px;">立即咨询</h2>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 40px;">留下您的需求，我们将尽快与您联系</p>

        <div class="contact-form">
            <div style="background: white; border-radius: 15px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                <h3 style="color: #2c3e50; margin-bottom: 30px; text-align: center;">免费获取方案咨询</h3>

                <form>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                        <div class="form-group">
                            <label class="form-label" style="color: #333;">姓名</label>
                            <input type="text" class="form-input" placeholder="请输入您的姓名">
                        </div>
                        <div class="form-group">
                            <label class="form-label" style="color: #333;">公司名称</label>
                            <input type="text" class="form-input" placeholder="请输入公司名称">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                        <div class="form-group">
                            <label class="form-label" style="color: #333;">联系电话</label>
                            <input type="tel" class="form-input" placeholder="请输入您的手机号">
                        </div>
                        <div class="form-group">
                            <label class="form-label" style="color: #333;">邮箱</label>
                            <input type="email" class="form-input" placeholder="请输入您的邮箱">
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 20px;">
                        <label class="form-label" style="color: #333;">具体需求</label>
                        <textarea class="form-textarea" placeholder="请详细描述您的需求，如：需要管理客户信息、需要数据分析功能等"></textarea>
                    </div>

                    <button type="submit" style="
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        color: white;
                        width: 100%;
                        padding: 15px;
                        border: none;
                        border-radius: 8px;
                        font-size: 1.1rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s;
                    ">提交咨询</button>
                </form>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 页脚 ==========
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div>
            <h4>🚀 数智科技</h4>
            <p style="color: #bdc3c7; line-height: 1.6;">专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务。</p>
        </div>

        <div>
            <h4>服务项目</h4>
            <ul class="footer-links">
                <li><a href="#services">BI商业智能系统</a></li>
                <li><a href="#services">CRM客户关系管理</a></li>
                <li><a href="#services">ERP企业资源计划</a></li>
                <li><a href="#services">定制化开发</a></li>
            </ul>
        </div>

        <div>
            <h4>联系我们</h4>
            <ul class="footer-links">
                <li><a href="mailto:contact@datatech.com">📧 contact@datatech.com</a></li>
                <li><a href="tel:4008888888">📞 400-888-8888</a></li>
                <li>📍 北京市朝阳区科技园</li>
                <li>🕐 周一至周五 9:00-18:00</li>
            </ul>
        </div>
    </div>

    <div style="
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 20px;
        text-align: center;
        color: #95a5a6;
        font-size: 0.9rem;
        max-width: 1200px;
        margin: 40px auto 0;
    ">
        © 2026 数智科技 版权所有 京ICP备12345678号
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 侧边栏信息 ==========
with st.sidebar:
    st.title("数智科技")
    st.markdown("企业数字化解决方案专家")

    st.markdown("---")
    st.subheader("📞 联系方式")
    st.write("**电话:** 400-888-8888")
    st.write("**邮箱:** contact@datatech.com")
    st.write("**地址:** 北京市朝阳区科技园")

    st.markdown("---")
    st.subheader("⏰ 工作时间")
    st.write("周一至周五: 9:00-18:00")
    st.write("周六: 9:00-12:00")
    st.write("周日: 休息")

    st.markdown("---")
    st.subheader("📱 关注我们")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("微信", use_container_width=True)
    with col2:
        st.button("QQ", use_container_width=True)
    with col3:
        st.button("领英", use_container_width=True)

    st.markdown("---")
    st.info("💡 专业的企业级数字化解决方案，助力您的业务增长！")