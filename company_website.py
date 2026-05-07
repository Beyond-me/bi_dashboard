# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (完整修复版)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from pathlib import Path
import json

# ========== 页面配置 ==========
st.set_page_config(
    page_title="数智科技 - 企业数字化解决方案专家",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 自定义CSS样式 ==========
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }

    /* 导航栏 */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        padding: 15px 0;
        margin-bottom: 80px;
    }

    .navbar-container {
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
        display: flex;
        align-items: center;
    }

    .logo-icon {
        margin-right: 10px;
        color: #3498db;
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

    /* 英雄区域 */
    .hero {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        padding: 100px 20px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin-bottom: 60px;
    }

    .hero h1 {
        font-size: 3.5rem;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .hero p {
        font-size: 1.5rem;
        max-width: 800px;
        margin: 0 auto 40px;
        opacity: 0.9;
    }

    .hero-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }

    .btn {
        padding: 14px 32px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-align: center;
        border: none;
        outline: none;
    }

    .btn-primary {
        background: white;
        color: #3498db;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }

    .btn-secondary {
        background: transparent;
        color: white;
        border: 2px solid white;
    }

    .btn-secondary:hover {
        background: rgba(255,255,255,0.1);
        transform: translateY(-3px);
    }

    /* 通用卡片样式 */
    .card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        padding: 30px;
        margin-bottom: 30px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }

    .section-title {
        text-align: center;
        margin: 60px 0 30px;
        color: #2c3e50;
        font-size: 2.5rem;
        position: relative;
    }

    .section-title:after {
        content: '';
        display: block;
        width: 80px;
        height: 4px;
        background: #3498db;
        margin: 15px auto 0;
        border-radius: 2px;
    }

    .section-subtitle {
        text-align: center;
        color: #7f8c8d;
        max-width: 700px;
        margin: 0 auto 50px;
        font-size: 1.2rem;
        line-height: 1.6;
    }

    /* 为什么选择我们 */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }

    .stat-card {
        text-align: center;
        padding: 30px 20px;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: #3498db;
        margin-bottom: 10px;
    }

    .stat-label {
        font-size: 1.2rem;
        color: #2c3e50;
        margin-bottom: 15px;
    }

    .stat-desc {
        color: #7f8c8d;
        line-height: 1.6;
    }

    /* 核心服务 */
    .services-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }

    .service-card {
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .service-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        color: #3498db;
    }

    .service-title {
        font-size: 1.5rem;
        margin-bottom: 15px;
        color: #2c3e50;
    }

    .service-desc {
        color: #7f8c8d;
        line-height: 1.7;
        margin-bottom: 20px;
        flex-grow: 1;
    }

    .service-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .service-features li {
        padding: 8px 0;
        padding-left: 25px;
        position: relative;
        color: #555;
    }

    .service-features li:before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #27ae60;
        font-weight: bold;
    }

    /* 成功案例 */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }

    .project-card {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }

    .project-card:hover {
        transform: translateY(-5px);
    }

    .project-image {
        height: 200px;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }

    .project-content {
        padding: 25px;
        background: white;
    }

    .project-title {
        font-size: 1.4rem;
        margin-bottom: 12px;
        color: #2c3e50;
    }

    .project-desc {
        color: #7f8c8d;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .project-tech {
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
        font-weight: 500;
    }

    .project-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #7f8c8d;
        font-size: 0.95rem;
    }

    /* 技术优势 */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }

    .feature-card {
        text-align: center;
        padding: 30px 20px;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        color: #3498db;
    }

    .feature-title {
        font-size: 1.4rem;
        margin-bottom: 15px;
        color: #2c3e50;
    }

    .feature-desc {
        color: #7f8c8d;
        line-height: 1.6;
    }

    /* 客户评价 */
    .testimonials-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 50px 30px;
        margin: 60px 0;
        color: white;
    }

    .testimonials-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 40px;
    }

    .testimonial-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .testimonial-text {
        font-style: italic;
        line-height: 1.8;
        margin-bottom: 25px;
        position: relative;
    }

    .testimonial-text:before {
        content: '"';
        position: absolute;
        top: -20px;
        left: -10px;
        font-size: 4rem;
        color: rgba(255,255,255,0.2);
        font-family: Georgia, serif;
    }

    .testimonial-author {
        display: flex;
        align-items: center;
    }

    .author-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: white;
        margin-right: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3498db;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .author-info {
        flex-grow: 1;
    }

    .author-name {
        font-weight: 600;
        margin-bottom: 5px;
    }

    .author-position {
        opacity: 0.8;
        font-size: 0.9rem;
    }

    /* 立即咨询 */
    .cta-container {
        background: white;
        border-radius: 20px;
        padding: 50px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 60px auto;
        text-align: center;
    }

    .cta-title {
        font-size: 2.2rem;
        color: #2c3e50;
        margin-bottom: 20px;
    }

    .cta-desc {
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 30px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* 页脚 */
    .footer {
        background: #2c3e50;
        color: white;
        padding: 60px 20px 30px;
        margin-top: 60px;
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
        margin-bottom: 25px;
        position: relative;
        padding-bottom: 10px;
    }

    .footer-column h4:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 50px;
        height: 3px;
        background: #3498db;
    }

    .footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .footer-links li {
        margin-bottom: 12px;
    }

    .footer-links a {
        color: #bdc3c7;
        text-decoration: none;
        transition: color 0.3s;
    }

    .footer-links a:hover {
        color: #3498db;
    }

    .contact-info {
        display: flex;
        align-items: flex-start;
        margin-bottom: 20px;
    }

    .contact-icon {
        margin-right: 15px;
        color: #3498db;
        font-size: 1.2rem;
        min-width: 24px;
    }

    .social-links {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }

    .social-link {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        color: white;
        transition: all 0.3s;
    }

    .social-link:hover {
        background: #3498db;
        transform: translateY(-3px);
    }

    .copyright {
        text-align: center;
        padding-top: 30px;
        margin-top: 40px;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: #95a5a6;
        font-size: 0.9rem;
    }

    /* 响应式调整 */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.5rem;
        }

        .hero p {
            font-size: 1.2rem;
        }

        .section-title {
            font-size: 2rem;
        }

        .navbar-container {
            flex-direction: column;
            gap: 15px;
        }

        .nav-links {
            flex-wrap: wrap;
            justify-content: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== 页面内容 ==========

# 导航栏
st.markdown("""
<div class="navbar">
    <div class="navbar-container">
        <div class="logo">
            <span class="logo-icon">🚀</span>
            <span>数智科技</span>
        </div>
        <div class="nav-links">
            <a href="#home" class="nav-link">首页</a>
            <a href="#why-us" class="nav-link">为什么选择我们</a>
            <a href="#services" class="nav-link">核心服务</a>
            <a href="#projects" class="nav-link">成功案例</a>
            <a href="#testimonials" class="nav-link">客户评价</a>
            <a href="#contact" class="nav-link">联系我们</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 英雄区域
st.markdown("""
<div class="hero" id="home">
    <h1>企业数字化解决方案专家</h1>
    提供BI商业智能、CRM客户关系管理、进销存系统等定制开发服务
    <div class="hero-buttons">
        <a href="#contact" class="btn btn-primary">免费获取方案咨询</a>
        <a href="#projects" class="btn btn-secondary">查看案例</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 为什么选择我们
st.markdown("""
<div id="why-us">
    <h2 class="section-title">为什么选择我们</h2>
    <p class="section-subtitle">专业的技术团队，丰富的行业经验，完善的服务体系

    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">50+</div>
            <h3 class="stat-label">成功项目</h3>
            <p class="stat-desc">覆盖制造业、零售、电商等多个行业
        </div>
        <div class="stat-card">
            <div class="stat-number">30+</div>
            <h3 class="stat-label">企业客户</h3>
            <p class="stat-desc">服务过中小型企业到上市公司
        </div>
        <div class="stat-card">
            <div class="stat-number">99%</div>
            <h3 class="stat-label">客户满意度</h3>
            <p class="stat-desc">完善的售后服务和持续的技术支持
        </div>
        <div class="stat-card">
            <div class="stat-number">7×24</div>
            <h3 class="stat-label">小时响应</h3>
            <p class="stat-desc">快速响应客户需求，及时解决问题
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 核心服务
st.markdown("""
<div id="services">
    <h2 class="section-title">核心服务</h2>
    <p class="section-subtitle">为企业提供全方位的数字化解决方案

    <div class="services-grid">
        <div class="card service-card">
            <div class="service-icon">📊</div>
            <h3 class="service-title">BI商业智能系统</h3>
            <p class="service-desc">为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。
            <ul class="service-features">
                <li>销售数据分析看板</li>
                <li>库存监控与预警系统</li>
                <li>客户行为分析报表</li>
                <li>实时业绩监控系统</li>
            </ul>
        </div>

        <div class="card service-card">
            <div class="service-icon">👥</div>
            <h3 class="service-title">CRM客户关系管理</h3>
            <p class="service-desc">全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。
            <ul class="service-features">
                <li>客户全生命周期管理</li>
                <li>销售漏斗与机会管理</li>
                <li>自动化营销工具</li>
                <li>客户服务与支持</li>
            </ul>
        </div>

        <div class="card service-card">
            <div class="service-icon">📦</div>
            <h3 class="service-title">进销存管理系统</h3>
            <p class="service-desc">整合采购、销售、库存流程，实现供应链数字化管理，优化库存结构，提高运营效率。
            <ul class="service-features">
                <li>智能采购管理</li>
                <li>销售订单跟踪</li>
                <li>库存实时监控</li>
                <li>财务报表分析</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 成功案例
st.markdown("""
<div id="projects">
    <h2 class="section-title">成功案例</h2>
    <p class="section-subtitle">我们为各行业客户提供定制化的数字化解决方案

    <div class="projects-grid">
        <div class="project-card">
            <div class="project-image">五金店进销存系统</div>
            <div class="project-content">
                <h3 class="project-title">五金店进销存管理系统</h3>
                <p class="project-desc">为五金行业定制的进销存管理系统，包含商品管理、采购入库、销售开单、库存预警等功能。
                <div class="project-tech">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Streamlit</span>
                    <span class="tech-tag">SQLite</span>
                </div>
                <div class="project-meta">
                    <span>开发周期: 2周</span>
                    <a href="#contact" style="color: #3498db; font-weight: 600;">了解详情 →</a>
                </div>
            </div>
        </div>

        <div class="project-card">
            <div class="project-image">CRM管理系统</div>
            <div class="project-content">
                <h3 class="project-title">企业CRM客户关系管理系统</h3>
                <p class="project-desc">专为B2B企业设计的客户关系管理系统，优化销售流程，提升团队协作效率，实现客户资源最大化利用。
                <div class="project-tech">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Flask</span>
                    <span class="tech-tag">MySQL</span>
                </div>
                <div class="project-meta">
                    <span>开发周期: 3周</span>
                    <a href="#contact" style="color: #3498db; font-weight: 600;">了解详情 →</a>
                </div>
            </div>
        </div>

        <div class="project-card">
            <div class="project-image">BI数据分析平台</div>
            <div class="project-content">
                <h3 class="project-title">零售BI数据分析平台</h3>
                <p class="project-desc">为连锁零售企业构建的数据分析平台，整合线上线下数据，提供销售预测、库存优化、会员分析等深度洞察。
                <div class="project-tech">
                    <span class="tech-tag">Python</span>
                    <span class="tech-tag">Power BI</span>
                    <span class="tech-tag">SQL Server</span>
                </div>
                <div class="project-meta">
                    <span>开发周期: 4周</span>
                    <a href="#contact" style="color: #3498db; font-weight: 600;">了解详情 →</a>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 技术优势
st.markdown("""
<div id="features">
    <h2 class="section-title">技术优势</h2>
    <p class="section-subtitle">我们采用先进的技术栈，确保系统稳定、安全、高效

    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">快速开发</h3>
            <p class="feature-desc">使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">安全可靠</h3>
            <p class="feature-desc">完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。
        </div>
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">多端适配</h3>
            <p class="feature-desc">响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <h3 class="feature-title">持续迭代</h3>
            <p class="feature-desc">根据业务发展需求，持续优化升级，确保系统与企业一同成长。
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 客户评价
st.markdown("""
<div id="testimonials" class="testimonials-container">
    <h2 class="section-title" style="color: white;">客户评价</h2>
    <p class="section-subtitle" style="color: rgba(255,255,255,0.8);">听听我们的客户怎么说

    <div class="testimonials-grid">
        <div class="testimonial-card">
            <p class="testimonial-text">"数智科技为我们开发的BI看板系统，让我们的销售数据一目了然，管理决策更加科学高效。团队专业，服务周到，强烈推荐！"
            <div class="testimonial-author">
                <div class="author-avatar">张</div>
                <div class="author-info">
                    <div class="author-name">张总</div>
                    <div class="author-position">某制造企业 总经理</div>
                </div>
            </div>
        </div>

        <div class="testimonial-card">
            <p class="testimonial-text">"CRM系统极大地提升了我们的销售效率，客户跟进更加及时，销售漏斗清晰可见。从需求沟通到系统上线，全程服务专业贴心。"
            <div class="testimonial-author">
                <div class="author-avatar">李</div>
                <div class="author-info">
                    <div class="author-name">李经理</div>
                    <div class="author-position">某科技公司 销售总监</div>
                </div>
            </div>
        </div>

        <div class="testimonial-card">
            <p class="testimonial-text">"进销存系统解决了我们多年的库存管理难题，操作简单，功能实用。技术人员响应迅速，后期维护也很到位，非常满意！"
            <div class="testimonial-author">
                <div class="author-avatar">王</div>
                <div class="author-info">
                    <div class="author-name">王老板</div>
                    <div class="author-position">某商贸公司 创始人</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 立即咨询
st.markdown("""
<div id="contact">
    <div class="cta-container">
        <h2 class="cta-title">立即咨询</h2>
        <p class="cta-desc">留下您的需求，我们将尽快与您联系

        <div style="background: #f8f9fa; border-radius: 15px; padding: 30px; margin-top: 30px;">
            <h3 style="text-align: center; color: #2c3e50; margin-bottom: 25px;">免费获取方案咨询</h3>
            <form>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; color: #555;">姓名</label>
                        <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="您的姓名">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; color: #555;">公司</label>
                        <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="您的公司">
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; color: #555;">电话</label>
                        <input type="tel" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="您的电话">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; color: #555;">邮箱</label>
                        <input type="email" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="您的邮箱">
                    </div>
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #555;">需求描述</label>
                    <textarea style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; height: 120px;" placeholder="请描述您的具体需求"></textarea>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">提交咨询</button>
            </form>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 页脚
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="footer-column">
            <h4>数智科技</h4>
            专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务。
            <div class="social-links">
                <a href="#" class="social-link">微</a>
                <a href="#" class="social-link">Q</a>
                <a href="#" class="social-link">领</a>
            </div>
        </div>

        <div class="footer-column">
            <h4>服务项目</h4>
            <ul class="footer-links">
                <li><a href="#services">BI商业智能系统</a></li>
                <li><a href="#services">CRM客户关系管理</a></li>
                <li><a href="#services">ERP企业资源计划</a></li>
                <li><a href="#services">定制化开发</a></li>
            </ul>
        </div>

        <div class="footer-column">
            <h4>联系我们</h4>
            <div class="contact-info">
                <div class="contact-icon">✉️</div>
                <div>contact@datech.com</div>
            </div>
            <div class="contact-info">
                <div class="contact-icon">📞</div>
                <div>400-888-8888</div>
            </div>
            <div class="contact-info">
                <div class="contact-icon">📍</div>
                <div>北京市朝阳区科技园A座12层</div>
            </div>
            <div class="contact-info">
                <div class="contact-icon">⏰</div>
                <div>周一至周五 9:00-18:00</div>
            </div>
        </div>
    </div>

    <div class="copyright">
        &copy; 2026 数智科技 版权所有 | 企业数字化解决方案专家
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://via.placeholder.com/150x150?text=Logo", use_column_width=True)
    st.title("数智科技")
    st.write("企业数字化解决方案专家")

    st.markdown("---")

    st.subheader("快速导航")
    st.markdown("[首页](#home)")
    st.markdown("[为什么选择我们](#why-us)")
    st.markdown("[核心服务](#services)")
    st.markdown("[成功案例](#projects)")
    st.markdown("[客户评价](#testimonials)")
    st.markdown("[联系我们](#contact)")

    st.markdown("---")

    st.subheader("联系方式")
    st.markdown("📧 contact@datech.com")
    st.markdown("📞 400-888-8888")
    st.markdown("📍 北京市朝阳区科技园A座12层")

    st.markdown("---")

    st.subheader("关注我们")
    st.markdown("<div style='display: flex; gap: 15px;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='width: 40px; height: 40px; background: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;'>微</div>",
        unsafe_allow_html=True)
    st.markdown(
        "<div style='width: 40px; height: 40px; background: #1da1f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;'>Q</div>",
        unsafe_allow_html=True)
    st.markdown(
        "<div style='width: 40px; height: 40px; background: #0077b5; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;'>领</div>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)