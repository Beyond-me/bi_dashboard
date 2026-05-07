# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (Streamlit兼容版)

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
        box-shadow: 0 2px 20px rgba(0,0,0,0.05);
        padding: 15px 0;
        margin-bottom: 80px;
    }

    /* 卡片样式 */
    .stat-card, .service-card, .project-card, .tech-card, .testimonial-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }

    .stat-card:hover, .service-card:hover, .project-card:hover, .tech-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    /* 标题样式 */
    .section-title {
        text-align: center;
        margin: 50px 0 20px;
        color: #2c3e50;
        font-weight: 700;
    }

    .section-subtitle {
        text-align: center;
        color: #7f8c8d;
        max-width: 700px;
        margin: 0 auto 40px;
    }

    /* 统计数字 */
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3498db;
        margin: 10px 0;
    }

    /* 页脚 */
    .footer {
        background: #1a2530;
        color: #ecf0f1;
        padding: 50px 0 20px;
        margin-top: 60px;
    }

    /* 咨询表单 */
    .contact-form {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }

    /* 客户评价 */
    .testimonial-content {
        font-style: italic;
        color: #555;
        margin: 15px 0;
        line-height: 1.6;
    }

    .client-info {
        display: flex;
        align-items: center;
        margin-top: 15px;
    }

    .client-avatar {
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

    /* 标签 */
    .tag {
        display: inline-block;
        background: #e0f7fa;
        color: #00838f;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 5px;
    }

    /* 按钮 */
    .btn-primary {
        background: #3498db;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        text-align: center;
    }

    .btn-primary:hover {
        background: #2980b9;
        transform: translateY(-2px);
    }

    /* 响应式调整 */
    @media (max-width: 768px) {
        .stat-number {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ========== 导航栏 ==========
def show_navbar():
    cols = st.columns([1, 3, 1])
    with cols[1]:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #2c3e50;">数智科技</div>
            <div style="display: flex; gap: 30px;">
                <a href="#services" style="text-decoration: none; color: #2c3e50; font-weight: 500;">核心服务</a>
                <a href="#projects" style="text-decoration: none; color: #2c3e50; font-weight: 500;">成功案例</a>
                <a href="#tech" style="text-decoration: none; color: #2c3e50; font-weight: 500;">技术优势</a>
                <a href="#testimonials" style="text-decoration: none; color: #2c3e50; font-weight: 500;">客户评价</a>
                <a href="#contact" style="text-decoration: none; color: #2c3e50; font-weight: 500;">立即咨询</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ========== 各部分组件 ==========

def show_hero():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%); 
                color: white; 
                padding: 80px 20px; 
                border-radius: 0 0 30px 30px; 
                margin-bottom: 50px;
                text-align: center;">
        <h1 style="font-size: 3rem; margin-bottom: 20px;">企业数字化解决方案专家</h1>
        <p style="font-size: 1.2rem; max-width: 700px; margin: 0 auto 30px;">
            提供BI商业智能、CRM客户关系管理、进销存系统等定制开发服务

        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div class="btn-primary">免费获取方案</div>
            <div style="background: white; color: #3498db; padding: 12px 25px; border-radius: 30px; font-weight: 600; cursor: pointer;">
                查看案例
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_why_choose_us():
    st.markdown("<h2 class='section-title'>为什么选择我们</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>专业的技术团队，丰富的行业经验，完善的服务体系", unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        {"number": "50+", "title": "成功项目", "desc": "覆盖制造业、零售、电商等多个行业"},
        {"number": "30+", "title": "企业客户", "desc": "服务过中小型企业到上市公司"},
        {"number": "99%", "title": "客户满意度", "desc": "完善的售后服务和持续的技术支持"},
        {"number": "7×24", "title": "小时响应", "desc": "快速响应客户需求，及时解决问题"}
    ]

    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stat['number']}</div>
                <h3>{stat['title']}</h3>
                {stat['desc']}
            </div>
            """, unsafe_allow_html=True)


def show_core_services():
    st.markdown("<h2 id='services' class='section-title'>核心服务</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>为企业提供全方位的数字化解决方案", unsafe_allow_html=True)

    services = [
        {
            "title": "BI商业智能系统",
            "icon": "📊",
            "desc": "为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。",
            "features": [
                "销售数据分析看板",
                "库存监控与预警系统",
                "客户行为分析报表",
                "实时业绩监控系统"
            ]
        },
        {
            "title": "CRM客户关系管理",
            "icon": "🤝",
            "desc": "全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。",
            "features": [
                "客户全生命周期管理",
                "销售漏斗与机会管理",
                "自动化营销工具",
                "客户服务与支持"
            ]
        },
        {
            "title": "进销存管理系统",
            "icon": "📦",
            "desc": "实现商品采购、销售、库存全流程管理，提供智能补货建议，优化库存结构，降低运营成本。",
            "features": [
                "采购订单管理",
                "销售开单系统",
                "库存预警机制",
                "多仓库管理"
            ]
        },
        {
            "title": "定制化开发",
            "icon": "🔧",
            "desc": "根据企业特定需求，量身定制专属业务系统，满足个性化业务流程和管理需求。",
            "features": [
                "业务流程梳理",
                "系统架构设计",
                "功能定制开发",
                "系统集成对接"
            ]
        }
    ]

    for service in services:
        with st.container():
            cols = st.columns([1, 5])
            with cols[0]:
                st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{service['icon']}</div>",
                            unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div class="service-card">
                    <h3 style="color: #2c3e50; margin-bottom: 15px;">{service['title']}</h3>
                    <p style="color: #666; line-height: 1.6;">{service['desc']}
                    <ul style="margin-top: 20px; color: #666; padding-left: 20px;">
                        {"".join([f"<li style='margin-bottom: 8px;'>{feature}</li>" for feature in service['features']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)


def show_projects():
    st.markdown("<h2 id='projects' class='section-title'>成功案例</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>我们为各行业客户提供定制化的数字化解决方案", unsafe_allow_html=True)

    projects = [
        {
            "title": "五金店进销存系统",
            "description": "为五金行业定制的进销存管理系统，包含商品管理、采购入库、销售开单、库存预警等功能。",
            "tags": ["Python", "Streamlit", "SQLite"],
            "duration": "开发周期：2周"
        },
        {
            "title": "企业CRM客户关系管理系统",
            "description": "完善的CRM解决方案，包含客户管理、销售机会、联系记录、任务管理、业绩分析等功能。",
            "tags": ["Python", "Streamlit", "SQLite", "Pandas"],
            "duration": "开发周期：3周"
        },
        {
            "title": "制造企业BI看板系统",
            "description": "为制造企业提供实时生产数据监控，销售数据分析，库存周转率等关键指标可视化。",
            "tags": ["Python", "Plotly", "MySQL", "Docker"],
            "duration": "开发周期：4周"
        }
    ]

    for project in projects:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                # 使用渐变背景代替图片
                st.markdown(f"""
                <div style="
                    background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                    border-radius: 15px;
                    height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                    font-weight: bold;
                ">
                    {project['title']}
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div class="project-card">
                    <h3 style="color: #2c3e50; margin-bottom: 10px;">{project['title']}</h3>
                    <p style="color: #666; margin-bottom: 15px;">{project['description']}
                    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">
                        {"".join([f"<span style='background: #e0f7fa; color: #00838f; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem;'>{tag}</span>" for tag in project['tags']])}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #667eea; font-weight: bold;">{project['duration']}</span>
                        <a href="#contact" style="color: #667eea; text-decoration: none; font-weight: bold;">了解详情 →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)


def show_tech_advantages():
    st.markdown("<h2 id='tech' class='section-title'>技术优势</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>我们采用先进的技术栈，确保系统稳定、安全、高效", unsafe_allow_html=True)

    advantages = [
        {"icon": "⚡", "title": "快速开发", "desc": "使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。"},
        {"icon": "🔒", "title": "安全可靠", "desc": "完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。"},
        {"icon": "📱", "title": "多端适配", "desc": "响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。"},
        {"icon": "🔄", "title": "持续迭代", "desc": "根据业务发展需求，持续优化升级，确保系统与企业一同成长。"}
    ]

    cols = st.columns(4)
    for i, adv in enumerate(advantages):
        with cols[i]:
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 3rem; text-align: center; margin-bottom: 15px;">{adv['icon']}</div>
                <h3 style="color: #2c3e50; text-align: center; margin-bottom: 10px;">{adv['title']}</h3>
                <p style="color: #666; text-align: center; line-height: 1.6;">{adv['desc']}
            </div>
            """, unsafe_allow_html=True)


def show_testimonials():
    st.markdown("<h2 id='testimonials' class='section-title'>客户评价</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>听听我们的客户怎么说", unsafe_allow_html=True)

    testimonials = [
        {
            "quote": "数智科技为我们开发的BI看板系统，让我们的销售数据一目了然，管理决策更加科学高效。团队专业，服务周到！",
            "name": "张总",
            "position": "某制造企业 总经理"
        },
        {
            "quote": "CRM系统极大地提升了我们的销售效率，客户跟进更加及时，销售漏斗清晰可见。强烈推荐！",
            "name": "李经理",
            "position": "某科技公司 销售总监"
        },
        {
            "quote": "进销存系统解决了我们多年的库存管理难题，操作简单但功能强大，真正帮我们降低了15%的库存成本。",
            "name": "王女士",
            "position": "某零售企业 运营总监"
        }
    ]

    cols = st.columns(3)
    for i, testimonial in enumerate(testimonials):
        with cols[i]:
            st.markdown(f"""
            <div class="testimonial-card">
                <p class="testimonial-content">"{testimonial['quote']}"
                <div class="client-info">
                    <div class="client-avatar">{testimonial['name'][0]}</div>
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">{testimonial['name']}</h4>
                        <p style="opacity: 0.8; margin: 0; font-size: 0.9rem;">{testimonial['position']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def show_contact():
    st.markdown("<h2 id='contact' class='section-title'>立即咨询</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>留下您的需求，我们将尽快与您联系", unsafe_allow_html=True)

    cols = st.columns([1, 1])
    with cols[0]:
        st.markdown("""
        <div class="contact-form">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">获取免费方案</h3>
            <form>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #555;">您的姓名</label>
                    <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入姓名">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #555;">联系电话</label>
                    <input type="tel" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入电话">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #555;">公司名称</label>
                    <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;" placeholder="请输入公司名称">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #555;">需求描述</label>
                    <textarea style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; height: 120px;" placeholder="请描述您的具体需求"></textarea>
                </div>
                <button type="submit" class="btn-primary" style="width: 100%;">提交需求</button>
            </form>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown("""
        <div style="padding: 30px; background: #f8f9fa; border-radius: 15px; height: 100%;">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">联系我们</h3>
            <div style="margin-bottom: 25px;">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="width: 40px; height: 40px; background: #e3f2fd; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; color: #1976d2;">
                        ✉️
                    </div>
                    <div>
                        <div style="font-weight: 500;">contact@datatech.com</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="width: 40px; height: 40px; background: #e8f5e9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; color: #388e3c;">
                        📞
                    </div>
                    <div>
                        <div style="font-weight: 500;">400-888-8888</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 40px; height: 40px; background: #fff3e0; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; color: #f57c00;">
                        📍
                    </div>
                    <div>
                        <div style="font-weight: 500;">北京市朝阳区科技园A座12层</div>
                    </div>
                </div>
            </div>

            <h3 style="color: #2c3e50; margin-bottom: 20px;">关注我们</h3>
            <div style="display: flex; gap: 15px;">
                <div style="width: 40px; height: 40px; background: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                    微
                </div>
                <div style="width: 40px; height: 40px; background: #1da1f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                    Q
                </div>
                <div style="width: 40px; height: 40px; background: #0077b5; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                    领
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_footer():
    st.markdown("""
    <div class="footer">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-bottom: 40px;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 20px; color: white;">数智科技</div>
                    <p style="color: #bdc3c7; line-height: 1.6;">
                        专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务。

                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 20px;">服务项目</h4>
                    <ul style="list-style: none; padding: 0; color: #bdc3c7;">
                        <li style="margin-bottom: 10px;">BI商业智能系统</li>
                        <li style="margin-bottom: 10px;">CRM客户关系管理</li>
                        <li style="margin-bottom: 10px;">ERP企业资源计划</li>
                        <li style="margin-bottom: 10px;">定制化开发</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 20px;">联系我们</h4>
                    <ul style="list-style: none; padding: 0; color: #bdc3c7;">
                        <li style="margin-bottom: 10px;">✉️ contact@datatech.com</li>
                        <li style="margin-bottom: 10px;">📞 400-888-8888</li>
                        <li style="margin-bottom: 10px;">📍 北京市朝阳区科技园A座12层</li>
                        <li style="margin-bottom: 10px;">🕒 周一至周五 9:00-18:00</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 20px;">关注我们</h4>
                    <div style="display: flex; gap: 15px;">
                        <div style="width: 40px; height: 40px; background: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                            微
                        </div>
                        <div style="width: 40px; height: 40px; background: #1da1f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                            Q
                        </div>
                        <div style="width: 40px; height: 40px; background: #0077b5; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; cursor: pointer;">
                            领
                        </div>
                    </div>
                </div>
            </div>
            <div style="border-top: 1px solid #34495e; padding-top: 20px; text-align: center; color: #7f8c8d; font-size: 0.9rem;">
                © 2026 数智科技有限公司 版权所有 | 京ICP备12345678号
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ========== 主程序 ==========
def main():
    show_navbar()
    show_hero()
    show_why_choose_us()
    show_core_services()
    show_projects()
    show_tech_advantages()
    show_testimonials()
    show_contact()
    show_footer()


if __name__ == "__main__":
    main()