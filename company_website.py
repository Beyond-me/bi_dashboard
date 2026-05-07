# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_optimized.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (优化版)

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ========== 页面配置 ==========
st.set_page_config(
    page_title="数智科技 - 企业数字化解决方案专家",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 优化的CSS样式 ==========
st.markdown("""
<style>
    /* 全局样式优化 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    }

    /* 导航栏优化 */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        padding: 12px 0;
        width: 100%;
    }

    /* 头部区域优化 */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 100px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
        opacity: 0.1;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        line-height: 1.1;
        background: linear-gradient(45deg, #fff, rgba(255,255,255,0.8));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto 40px;
        line-height: 1.6;
    }

    /* 按钮优化 */
    .cta-button {
        display: inline-block;
        padding: 16px 32px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }

    .cta-primary {
        background: white;
        color: #2a5298;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .cta-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.2);
    }

    .cta-secondary {
        background: transparent;
        color: white;
        border: 2px solid white;
    }

    .cta-secondary:hover {
        background: rgba(255,255,255,0.1);
        transform: translateY(-3px);
    }

    /* 卡片优化 */
    .service-card, .project-card, .stat-card, .testimonial-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        padding: 30px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0,0,0,0.05);
    }

    .service-card:hover, .project-card:hover, .stat-card:hover, .testimonial-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }

    /* 统计数字优化 */
    .stat-number {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #3498db, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* 技术标签优化 */
    .tech-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #f1f8ff, #e3f2fd);
        color: #1976d2;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 5px;
        transition: all 0.3s;
    }

    .tech-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
    }

    /* 表单优化 */
    .contact-form {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
    }

    .form-input {
        width: 100%;
        padding: 16px 20px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s;
        background: #f8fafc;
    }

    .form-input:focus {
        outline: none;
        border-color: #3498db;
        background: white;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    /* 页脚优化 */
    .footer-section {
        background: linear-gradient(135deg, #1a2536 0%, #2c3e50 100%);
        color: white;
        padding: 60px 20px 30px;
        margin-top: 80px;
        position: relative;
    }

    .footer-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }

    .footer-column h4 {
        font-size: 1.2rem;
        margin-bottom: 20px;
        color: white;
        position: relative;
        padding-bottom: 10px;
    }

    .footer-column h4::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 3px;
        background: #3498db;
        border-radius: 2px;
    }

    .social-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        color: white;
        transition: all 0.3s;
        cursor: pointer;
    }

    .social-icon:hover {
        background: #3498db;
        transform: translateY(-3px);
    }

    /* 响应式优化 */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .hero-subtitle {
            font-size: 1.1rem;
        }

        .stat-number {
            font-size: 2.5rem;
        }

        .cta-button {
            padding: 14px 28px;
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== 优化的页面内容 ==========

# 导航栏优化
st.markdown("""
<div class="navbar">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #2a5298; display: flex; align-items: center; gap: 8px;">
                <span style="background: linear-gradient(45deg, #2a5298, #3498db); padding: 6px 12px; border-radius: 8px; color: white;">🚀</span>
                <span>数智科技</span>
            </div>
            <div style="color: #64748b; font-size: 0.9rem; padding-left: 10px; border-left: 2px solid #e2e8f0;">
                企业数字化解决方案专家
            </div>
        </div>
        <div style="display: flex; gap: 30px;">
            <a href="#services" style="text-decoration: none; color: #475569; font-weight: 500; transition: color 0.3s;">服务</a>
            <a href="#projects" style="text-decoration: none; color: #475569; font-weight: 500; transition: color 0.3s;">案例</a>
            <a href="#contact" style="text-decoration: none; color: #475569; font-weight: 500; transition: color 0.3s;">联系我们</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 优化头部区域
header_html = f"""
<div class="hero-section">
    <div style="max-width: 1200px; margin: 0 auto; position: relative; z-index: 2;">
        <h1 class="hero-title">企业数字化解决方案专家</h1>
        <p class="hero-subtitle">
            专注于BI商业智能、CRM客户关系管理、进销存系统等企业级数字化解决方案定制开发，
            助力企业实现数据驱动的智能化管理
        </p>

        <div style="margin-top: 40px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <a href="#contact" class="cta-button cta-primary" onclick="trackCTA('header_primary')">
                免费获取方案咨询
            </a>
            <a href="#projects" class="cta-button cta-secondary" onclick="trackCTA('header_secondary')">
                查看成功案例
            </a>
        </div>

        <div style="margin-top: 50px; display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: white; margin-bottom: 5px;">50+</div>
                <div style="color: rgba(255,255,255,0.8);">成功项目</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: white; margin-bottom: 5px;">30+</div>
                <div style="color: rgba(255,255,255,0.8);">企业客户</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: white; margin-bottom: 5px;">99%</div>
                <div style="color: rgba(255,255,255,0.8);">满意度</div>
            </div>
        </div>
    </div>
</div>
"""

components.html(header_html, height=500)

# 为什么选择我们
st.markdown("""
<div style="max-width: 1200px; margin: 60px auto; padding: 0 20px;">
    <div style="text-align: center; margin-bottom: 60px;">
        <h2 style="color: #1e293b; font-size: 2.5rem; margin-bottom: 20px;">为什么选择数智科技</h2>
        <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            专业的技术团队，丰富的行业经验，完善的服务体系，为客户提供全方位的数字化解决方案
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
""", unsafe_allow_html=True)

stats = [
    {"number": "50+", "title": "成功项目", "desc": "覆盖制造业、零售、电商等多个行业，丰富的行业经验"},
    {"number": "30+", "title": "企业客户", "desc": "服务过中小型企业到上市公司，深谙企业需求"},
    {"number": "99%", "title": "客户满意度", "desc": "完善的售后服务和持续的技术支持，赢得客户信赖"},
    {"number": "7×24", "title": "小时响应", "desc": "快速响应客户需求，及时解决问题，确保系统稳定运行"}
]

for stat in stats:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stat['number']}</div>
        <h3 style="color: #1e293b; margin-bottom: 10px; font-size: 1.3rem;">{stat['title']}</h3>
        <p style="color: #64748b; line-height: 1.6;">{stat['desc']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 核心服务
st.markdown("""
<div id="services" style="max-width: 1200px; margin: 80px auto; padding: 0 20px;">
    <div style="text-align: center; margin-bottom: 60px;">
        <h2 style="color: #1e293b; font-size: 2.5rem; margin-bottom: 20px;">核心服务</h2>
        <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            为企业提供全方位的数字化解决方案，从咨询到开发，从部署到运维
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
""", unsafe_allow_html=True)

services = [
    {
        "icon": "📊",
        "title": "BI商业智能系统",
        "desc": "为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。",
        "features": ["销售数据分析看板", "库存监控与预警", "客户行为分析", "实时业绩监控"]
    },
    {
        "icon": "👥",
        "title": "CRM客户关系管理",
        "desc": "全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。",
        "features": ["客户生命周期管理", "销售漏斗管理", "自动化营销", "客户服务支持"]
    },
    {
        "icon": "🏭",
        "title": "ERP企业资源计划",
        "desc": "整合企业资源，优化业务流程，实现财务、采购、销售、库存等模块的一体化管理。",
        "features": ["财务管理", "供应链管理", "生产计划", "人力资源"]
    }
]

for service in services:
    features_html = "".join([
                                f'<li style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center;"><span style="color: #10b981; margin-right: 8px;">✓</span> {feature}</li>'
                                for feature in service["features"]])

    st.markdown(f"""
    <div class="service-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; color: white;">
                {service['icon']}
            </div>
            <h3 style="color: #1e293b; font-size: 1.4rem; margin: 0;">{service['title']}</h3>
        </div>
        <p style="color: #64748b; line-height: 1.7; margin-bottom: 25px;">{service['desc']}
        <ul style="list-style: none; padding: 0; margin: 0;">
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 成功案例
st.markdown(f"""
<div id="projects" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 80px 20px;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="color: #1e293b; font-size: 2.5rem; margin-bottom: 20px;">成功案例</h2>
            <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                我们为各行业客户提供定制化的数字化解决方案
            </p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
""", unsafe_allow_html=True)

projects = [
    {
        "title": "五金店进销存系统",
        "desc": "为五金行业定制的进销存管理系统，实现商品、采购、销售、库存全流程数字化管理。",
        "tech": ["Python", "Streamlit", "SQLite", "Pandas"],
        "duration": "开发周期：2周"
    },
    {
        "title": "企业CRM管理系统",
        "desc": "为企业量身定制的客户关系管理系统，优化销售流程，提升客户满意度和转化率。",
        "tech": ["Python", "FastAPI", "PostgreSQL", "React"],
        "duration": "开发周期：4周"
    },
    {
        "title": "BI数据分析平台",
        "desc": "为零售企业构建的数据分析平台，提供多维度数据分析和可视化报表。",
        "tech": ["Python", "Plotly", "MySQL", "Docker"],
        "duration": "开发周期：6周"
    }
]

for project in projects:
    tech_tags = "".join([f'<span class="tech-badge">{tech}</span>' for tech in project["tech"]])

    st.markdown(f"""
    <div class="project-card">
        <div style="height: 200px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; color: white;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">🚀</div>
                <div style="font-size: 1.3rem; font-weight: 600;">{project['title']}</div>
            </div>
        </div>
        <h3 style="color: #1e293b; margin-bottom: 15px; font-size: 1.4rem;">{project['title']}</h3>
        <p style="color: #64748b; margin-bottom: 20px; line-height: 1.6;">{project['desc']}
        <div style="margin-bottom: 20px;">
            {tech_tags}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 20px; border-top: 1px solid #e2e8f0;">
            <span style="color: #3b82f6; font-weight: 600;">{project['duration']}</span>
            <button onclick="showProjectDetail('{project['title']}')" style="
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                color: white;
                padding: 8px 20px;
                border-radius: 20px;
                border: none;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            ">了解详情 →</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div></div>", unsafe_allow_html=True)

# 技术优势
st.markdown("""
<div style="max-width: 1200px; margin: 80px auto; padding: 0 20px;">
    <div style="text-align: center; margin-bottom: 60px;">
        <h2 style="color: #1e293b; font-size: 2.5rem; margin-bottom: 20px;">技术优势</h2>
        <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            我们采用先进的技术栈，确保系统稳定、安全、高效
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
""", unsafe_allow_html=True)

advantages = [
    {"icon": "⚡", "title": "快速开发", "desc": "使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。"},
    {"icon": "🔐", "title": "安全可靠", "desc": "完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。"},
    {"icon": "📱", "title": "多端适配", "desc": "响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。"},
    {"icon": "🔄", "title": "持续迭代", "desc": "根据业务发展需求，持续优化升级，确保系统与企业一同成长。"}
]

for adv in advantages:
    st.markdown(f"""
    <div class="service-card" style="text-align: center; padding: 40px 20px;">
        <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 2rem; color: white;">
            {adv['icon']}
        </div>
        <h3 style="color: #1e293b; margin-bottom: 15px; font-size: 1.3rem;">{adv['title']}</h3>
        <p style="color: #64748b; line-height: 1.6;">{adv['desc']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 联系表单
st.markdown("""
<div id="contact" style="max-width: 800px; margin: 80px auto; padding: 0 20px;">
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="color: #1e293b; font-size: 2.5rem; margin-bottom: 20px;">立即咨询</h2>
        <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            留下您的需求，我们将在24小时内与您联系
        </p>
    </div>

    <div class="contact-form">
        <h3 style="color: #1e293b; margin-bottom: 30px; text-align: center;">免费获取方案咨询</h3>

        <form id="consultForm" style="margin-bottom: 20px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div>
                    <label style="display: block; margin-bottom: 8px; color: #475569; font-weight: 500;">您的姓名 *</label>
                    <input type="text" class="form-input" placeholder="请输入姓名" required>
                </div>
                <div>
                    <label style="display: block; margin-bottom: 8px; color: #475569; font-weight: 500;">联系电话 *</label>
                    <input type="tel" class="form-input" placeholder="请输入联系电话" required>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div>
                    <label style="display: block; margin-bottom: 8px; color: #475569; font-weight: 500;">企业名称</label>
                    <input type="text" class="form-input" placeholder="请输入企业名称">
                </div>
                <div>
                    <label style="display: block; margin-bottom: 8px; color: #475569; font-weight: 500;">邮箱</label>
                    <input type="email" class="form-input" placeholder="请输入邮箱">
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <label style="display: block; margin-bottom: 8px; color: #475569; font-weight: 500;">需求描述 *</label>
                <textarea class="form-input" placeholder="请描述您的具体需求，包括行业、规模、预算等信息" style="height: 120px; resize: vertical;" required></textarea>
            </div>

            <button type="button" onclick="submitConsultForm()" style="
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                color: white;
                width: 100%;
                padding: 16px;
                border: none;
                border-radius: 12px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            ">
                提交咨询
            </button>
        </form>

        <div style="text-align: center; margin-top: 30px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px; color: #64748b;">
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 8px;">📞</span> 400-888-8888
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 8px;">📧</span> contact@datech.com
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 优化页脚
footer_html = f"""
<div class="footer-section">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-bottom: 40px;">
            <div class="footer-column">
                <h4>数智科技</h4>
                <p style="color: #94a3b8; line-height: 1.7; margin-top: 15px;">
                    专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务，
                    助力企业实现数字化转型和业务增长。
                </p>
            </div>

            <div class="footer-column">
                <h4>服务项目</h4>
                <ul style="list-style: none; padding: 0; margin-top: 15px; color: #94a3b8;">
                    <li style="padding: 8px 0; display: flex; align-items: center;">
                        <span style="color: #3498db; margin-right: 8px;">•</span> BI商业智能系统
                    </li>
                    <li style="padding: 8px 0; display: flex; align-items: center;">
                        <span style="color: #3498db; margin-right: 8px;">•</span> CRM客户关系管理
                    </li>
                    <li style="padding: 8px 0; display: flex; align-items: center;">
                        <span style="color: #3498db; margin-right: 8px;">•</span> ERP企业资源计划
                    </li>
                    <li style="padding: 8px 0; display: flex; align-items: center;">
                        <span style="color: #3498db; margin-right: 8px;">•</span> 定制化开发
                    </li>
                </ul>
            </div>

            <div class="footer-column">
                <h4>联系我们</h4>
                <ul style="list-style: none; padding: 0; margin-top: 15px; color: #94a3b8;">
                    <li style="padding: 10px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #3498db;">📧</span> contact@datech.com
                    </li>
                    <li style="padding: 10px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #3498db;">📞</span> 400-888-8888
                    </li>
                    <li style="padding: 10px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #3498db;">📍</span> 北京市朝阳区科技园A座12层
                    </li>
                </ul>
            </div>

            <div class="footer-column">
                <h4>关注我们</h4>
                <div style="display: flex; gap: 15px; margin-top: 20px;">
                    <div class="social-icon" onclick="window.open('https://weixin.qq.com/')">微</div>
                    <div class="social-icon" onclick="window.open('https://qzone.qq.com/')">Q</div>
                    <div class="social-icon" onclick="window.open('https://linkedin.com/')">领</div>
                </div>
            </div>
        </div>

        <div style="text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 0.9rem;">
            <p style="margin: 5px 0;">© 2026 数智科技有限公司 版权所有</p>
            <p style="margin: 5px 0;">京ICP备12345678号 | 企业数字化解决方案专家</p>
        </div>
    </div>
</div>

<script>
function submitConsultForm() {{
    alert('咨询表单已提交！我们将在24小时内与您联系。');
    document.getElementById('consultForm').reset();
}}

function trackCTA(ctaType) {{
    console.log('CTA点击: ' + ctaType);
}}

function showProjectDetail(projectName) {{
    alert('即将展示' + projectName + '的详细案例信息');
}}
</script>
"""

components.html(footer_html, height=400)

# ========== 侧边栏优化 ==========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 1.8rem; font-weight: 800; color: #2a5298; margin-bottom: 10px;">
            🚀 数智科技
        </div>
        <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 30px;">
            企业数字化解决方案专家
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📋 快速导航")
    nav_cols = st.columns(2)
    with nav_cols[0]:
        if st.button("🏠 首页", use_container_width=True):
            st.session_state.page = "home"
    with nav_cols[1]:
        if st.button("📊 服务", use_container_width=True):
            st.session_state.page = "services"

    nav_cols2 = st.columns(2)
    with nav_cols2[0]:
        if st.button("💼 案例", use_container_width=True):
            st.session_state.page = "projects"
    with nav_cols2[1]:
        if st.button("📞 联系", use_container_width=True):
            st.session_state.page = "contact"

    st.markdown("---")

    st.markdown("### 📱 联系咨询")
    st.markdown("**电话:** 400-888-8888")
    st.markdown("**邮箱:** contact@datech.com")
    st.markdown("**地址:** 北京市朝阳区科技园A座12层")

    st.markdown("---")

    st.markdown("### ⏰ 工作时间")
    st.markdown("周一至周五: 9:00-18:00")
    st.markdown("周六: 9:00-12:00")
    st.markdown("周日: 休息")

    st.markdown("---")

    st.info("💡 专业的企业级数字化解决方案，助力您的业务增长！")
