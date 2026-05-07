# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_final.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (100%可用版)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== 页面配置 ==========
st.set_page_config(
    page_title="数智科技 - 企业数字化解决方案专家",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* 设置页脚的背景色 */
    .footer {
        background-color: #1a202c; /* 深色背景 */
        padding: 20px 0;
        margin-top: 50px; /* 与上方内容区隔开 */
    }

    /* 可选：优化服务列表的样式 */
    .service-list {
        list-style: none;
        padding: 0;
        color: #bdc3c7;
        line-height: 1.8;
        font-size: 0.9rem;
    }
    .service-list li::before {
        content: "•";
        color: #48bb78; /* 列表项前的绿色圆点 */
        font-weight: bold;
        display: inline-block; 
        width: 1em;
        margin-left: -1em;
    }
</style>
""", unsafe_allow_html=True)

# ========== 完整的CSS样式 ==========
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 导航栏 */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 头部区域 */
    .header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 80px 20px;
        text-align: center;
        margin-bottom: 40px;
        border-radius: 0 0 20px 20px;
    }

    /* 卡片样式 */
    .card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        padding: 25px;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    /* 统计卡片 */
    .stat-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2a5298;
        margin-bottom: 10px;
    }

    /* 按钮样式 */
    .btn-primary {
        background: linear-gradient(135deg, #3498db 0%, #1e88e5 100%);
        color: white;
        padding: 12px 25px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
        transition: all 0.3s ease;
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(52, 152, 219, 0.4);
    }

    /* 页脚 */
    .footer {
        background: #1e3c72;
        color: white;
        padding: 40px 20px;
        margin-top: 50px;
        border-radius: 20px 20px 0 0;
    }

    /* 项目卡片 */
    .project-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        overflow: hidden;
        margin-bottom: 30px;
    }

    .project-image {
        height: 200px;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .project-content {
        padding: 20px;
    }

    .tech-tag {
        display: inline-block;
        background: #e9f7fe;
        color: #3498db;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    /* 评价卡片 */
    .testimonial-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .testimonial-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }

    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #3498db;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 15px;
    }

    /* 联系表单 */
    .contact-form {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        max-width: 600px;
        margin: 0 auto;
    }

    .form-title {
        text-align: center;
        margin-bottom: 25px;
        color: #2a5298;
    }

    /* 服务列表 */
    .service-list {
        list-style: none;
        padding: 0;
    }

    .service-list li {
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
    }

    .service-list li:before {
        content: "✓";
        color: #27ae60;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ========== 页面内容 ==========

# 导航栏
st.markdown("""
<div class="navbar">
    <div style="display: flex; align-items: center;">
        <div style="font-weight: bold; font-size: 1.2rem; color: #2a5298; margin-right: 10px;">数智科技</div>
        <div style="color: #7f8c8d; font-size: 0.9rem;">企业数字化解决方案专家</div>
    </div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components

# 您的头部 HTML 代码
header_html = """
<div class="header">
    <h1 style="font-size: 2.8rem; margin-bottom: 15px; color: white;">企业数字化解决方案专家</h1>
    <p style="font-size: 1.2rem; max-width: 800px; margin: 0 auto 30px; opacity: 0.9; color: #e2e8f0;">
        提供BI商业智能、CRM客户关系管理、进销存系统等定制开发服务
    </p>

    <div style="margin-top: 20px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <div class="btn-primary">免费获取方案咨询</div>
        <div style="background: white; color: #2a5298; padding: 12px 25px; border-radius: 30px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;">
            查看案例
        </div>
    </div>
</div>
"""

# 使用 st.components.v1.html 来嵌入 HTML
components.html(header_html, height=300)

# 为什么选择我们
st.markdown("""
## 为什么选择我们
<p style="text-align: center; color: #666; margin-bottom: 30px;">专业的技术团队，丰富的行业经验，完善的服务体系

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
""", unsafe_allow_html=True)

# 统计卡片
stats = [
    {"number": "50+", "title": "成功项目", "desc": "覆盖制造业、零售、电商等多个行业"},
    {"number": "30+", "title": "企业客户", "desc": "服务过中小型企业到上市公司"},
    {"number": "99%", "title": "客户满意度", "desc": "完善的售后服务和持续的技术支持"},
    {"number": "7×24", "title": "小时响应", "desc": "快速响应客户需求，及时解决问题"}
]

for stat in stats:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stat['number']}</div>
        <h3 style="margin-bottom: 10px;">{stat['title']}</h3>
        <p style="color: #666;">{stat['desc']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 核心服务
st.markdown("""
## 核心服务
<p style="text-align: center; color: #666; margin-bottom: 30px;">为企业提供全方位的数字化解决方案

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 40px;">
""", unsafe_allow_html=True)

# 服务卡片
services = [
    {
        "icon": "📊",
        "title": "BI商业智能系统",
        "desc": "为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。",
        "features": ["销售数据分析看板", "库存监控与预警系统", "客户行为分析报表", "实时业绩监控系统"]
    },
    {
        "icon": "👥",
        "title": "CRM客户关系管理",
        "desc": "全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。",
        "features": ["客户全生命周期管理", "销售漏斗与机会管理", "自动化营销工具", "客户服务与支持"]
    },
    {
        "icon": "📦",
        "title": "智能进销存系统",
        "desc": "整合采购、销售、库存流程，实现商品全程追踪，智能预警补货，提升供应链效率。",
        "features": ["采购订单管理", "销售出库管理", "库存实时盘点", "供应商评估系统"]
    }
]

for service in services:
    features_html = "".join([f"<li>{feature}</li>" for feature in service["features"]])
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">{service['icon']}</div>
        <h3 style="margin-bottom: 15px; color: #333;">{service['title']}</h3>
        <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">{service['desc']}
        <ul class="service-list">
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 成功案例
st.markdown("""
## 成功案例
<p style="text-align: center; color: #666; margin-bottom: 30px;">我们为各行业客户提供定制化的数字化解决方案

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 40px;">
""", unsafe_allow_html=True)

# 项目卡片
projects = [
    {
        "title": "五金店进销存系统",
        "desc": "为五金行业定制的进销存管理系统，包含商品管理、采购入库、销售开单、库存预警等功能。",
        "tech": ["Python", "Streamlit", "SQLite"],
        "duration": "2周"
    },
    {
        "title": "企业CRM客户关系管理系统",
        "desc": "为销售团队打造的CRM系统，实现客户跟进自动化、销售漏斗管理、业绩分析等功能。",
        "tech": ["Python", "Pandas", "Plotly"],
        "duration": "3周"
    },
    {
        "title": "BI销售数据分析平台",
        "desc": "为零售企业构建的数据分析平台，实时监控销售数据，提供多维度分析报表。",
        "tech": ["Python", "SQLAlchemy", "Dash"],
        "duration": "4周"
    }
]

for project in projects:
    tech_tags = "".join([f'<span class="tech-tag">{tech}</span>' for tech in project["tech"]])
    st.markdown(f"""
    <div class="project-card">
        <div class="project-image">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📈</div>
                {project['title']}
            </div>
        </div>
        <div class="project-content">
            <h3 style="margin-bottom: 10px;">{project['title']}</h3>
            <p style="color: #666; margin-bottom: 15px;">{project['desc']}
            <div style="margin-bottom: 15px;">
                {tech_tags}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: #2a5298;">开发周期: {project['duration']}</span>
                <a href="#contact" style="color: #2a5298; text-decoration: none; font-weight: bold;">了解详情 →</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 技术优势
st.markdown("""
## 技术优势
<p style="text-align: center; color: #666; margin-bottom: 30px;">我们采用先进的技术栈，确保系统稳定、安全、高效

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
""", unsafe_allow_html=True)

# 优势卡片
advantages = [
    {"icon": "⚡", "title": "快速开发", "desc": "使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。"},
    {"icon": "🔒", "title": "安全可靠", "desc": "完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。"},
    {"icon": "📱", "title": "多端适配", "desc": "响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。"},
    {"icon": "🔄", "title": "持续迭代", "desc": "根据业务发展需求，持续优化升级，确保系统与企业一同成长。"}
]

for adv in advantages:
    st.markdown(f"""
    <div class="stat-card" style="text-align: center;">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">{adv['icon']}</div>
        <h3 style="margin-bottom: 10px;">{adv['title']}</h3>
        <p style="color: #666;">{adv['desc']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 客户评价
st.markdown("""
## 客户评价
<p style="text-align: center; color: #666; margin-bottom: 30px;">听听我们的客户怎么说

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px;">
""", unsafe_allow_html=True)

# 评价卡片
testimonials = [
    {
        "name": "张总",
        "position": "某制造企业 总经理",
        "quote": "数智科技为我们开发的BI看板系统，让我们的销售数据一目了然，管理决策更加科学高效。团队专业，服务周到。"
    },
    {
        "name": "李经理",
        "position": "某科技公司 销售总监",
        "quote": "CRM系统极大地提升了我们的销售效率，客户跟进更加及时，销售漏斗清晰可见。强烈推荐！"
    },
    {
        "name": "王女士",
        "position": "某零售企业 运营总监",
        "quote": "进销存系统解决了我们库存混乱的问题，现在可以实时掌握库存情况，大大减少了资金占用。"
    }
]

for testimonial in testimonials:
    st.markdown(f"""
    <div class="testimonial-card">
        <div class="testimonial-header">
            <div class="avatar">{testimonial['name'][0]}</div>
            <div>
                <h4 style="margin: 0;">{testimonial['name']}</h4>
                <p style="opacity: 0.8; margin: 0; font-size: 0.9rem;">{testimonial['position']}</p>
            </div>
        </div>
        <p style="font-style: italic; color: #555; margin-top: 10px;">"{testimonial['quote']}"
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 立即咨询
st.markdown("""
## 立即咨询
<p style="text-align: center; color: #666; margin-bottom: 30px;">留下您的需求，我们将尽快与您联系

<div class="contact-form">
    <div class="form-title">
        <h3 style="color: #2a5298;">免费获取方案咨询</h3>
    </div>
    <form>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500;">您的姓名</label>
            <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入姓名">
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500;">联系电话</label>
            <input type="tel" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入联系电话">
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500;">企业名称</label>
            <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入企业名称">
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500;">需求描述</label>
            <textarea style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; height: 120px;" placeholder="请描述您的具体需求"></textarea>
        </div>
        <button type="submit" class="btn-primary" style="width: 100%; border: none; cursor: pointer;">提交咨询</button>
    </form>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components

# 您的页脚 HTML 代码
footer_html = """
<div class="footer">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.1rem;">数智科技</h4>
            <p style="color: #bdc3c7; line-height: 1.6; font-size: 0.9rem;">
                专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务。
            </p>
        </div>

        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.1rem;">服务项目</h4>
            <ul style="list-style: none; padding: 0; color: #bdc3c7; line-height: 1.8; font-size: 0.9rem;">
                <li>BI商业智能系统</li>
                <li>CRM客户关系管理</li>
                <li>ERP企业资源计划</li>
                <li>定制化开发</li>
            </ul>
        </div>

        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.1rem;">联系我们</h4>
            <ul style="list-style: none; padding: 0; color: #bdc3c7; line-height: 1.8; font-size: 0.9rem;">
                <li style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="margin-right: 10px;">📧</span> contact@datech.com
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="margin-right: 10px;">📞</span> 400-888-8888
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="margin-right: 10px;">📍</span> 北京市朝阳区科技园A座12层
                </li>
            </ul>
        </div>

        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.1rem;">关注我们</h4>
            <div style="display: flex; gap: 15px;">
                <div style="width: 40px; height: 40px; background: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">微</div>
                <div style="width: 40px; height: 40px; background: #1da1f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">Q</div>
                <div style="width: 40px; height: 40px; background: #0077b5; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">领</div>
            </div>
        </div>
    </div>

    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); color: #bdc3c7; font-size: 0.85rem;">
        © 2026 数智科技有限公司 版权所有 | 京ICP备12345678号
    </div>
</div>
"""

# 使用 st.components.v1.html 来嵌入 HTML
components.html(footer_html, height=350)

# ========== 侧边栏 ==========
with st.sidebar:
    st.title("数智科技")
    st.markdown("企业数字化解决方案专家")
    st.markdown("---")
    st.markdown("### 快速导航")
    st.markdown("[首页](#home)")
    st.markdown("[服务案例](#services)")
    st.markdown("[成功案例](#projects)")
    st.markdown("[技术优势](#advantages)")
    st.markdown("[客户评价](#testimonials)")
    st.markdown("[联系我们](#contact)")
    st.markdown("---")
    st.markdown("### 联系咨询")
    st.markdown("📞 400-888-8888")
    st.markdown("📧 contact@datech.com")
    st.markdown("📍 北京市朝阳区科技园A座12层")