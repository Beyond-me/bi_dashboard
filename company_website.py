# -*- coding: utf-8 -*-
# @Time    : 2026/5/7 20:02
# @Author  : lihaizhen
# @File    : company_website.py
# @Software: PyCharm
# @Desc    :


# -*- coding: utf-8 -*-
# @Time    : 2026/5/6
# @Author  : 数智科技
# @File    : company_website.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        padding: 15px 5%;
    }

    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }

    .logo {
        font-size: 24px;
        font-weight: bold;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nav-links {
        display: flex;
        gap: 30px;
    }

    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }

    .nav-link:hover {
        color: #667eea;
    }

    .cta-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 10px 25px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        color: white;
    }

    /* 英雄区域 */
    .hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 100px 5% 50px;
    }

    .hero-content {
        max-width: 1200px;
        margin: 0 auto;
    }

    .hero h1 {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 20px;
        line-height: 1.2;
    }

    .hero p {
        font-size: 1.2rem;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* 卡片样式 */
    .card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }

    .card-icon {
        font-size: 40px;
        margin-bottom: 20px;
    }

    /* 项目展示 */
    .project-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }

    .project-card:hover {
        transform: translateY(-5px);
    }

    .project-image {
        height: 200px;
        background-size: cover;
        background-position: center;
    }

    .project-content {
        padding: 20px;
    }

    /* 统计数字 */
    .stat-card {
        text-align: center;
        padding: 30px;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 页脚 */
    .footer {
        background: #1a1a2e;
        color: white;
        padding: 60px 5%;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.5rem;
        }

        .nav-links {
            display: none;
        }
    }
</style>

<!-- 导航栏 -->
<div class="navbar">
    <div class="nav-container">
        <div class="logo">🚀 数智科技</div>
        <div class="nav-links">
            <a href="#home" class="nav-link">首页</a>
            <a href="#services" class="nav-link">服务</a>
            <a href="#projects" class="nav-link">项目案例</a>
            <a href="#about" class="nav-link">关于我们</a>
            <a href="#contact" class="nav-link">联系我们</a>
        </div>
        <a href="#contact" class="cta-button">免费咨询</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 首页英雄区域 ==========
st.markdown("""
<a id="home"></a>
<div class="hero">
    <div class="hero-content">
        <h1>用数据驱动企业增长<br>用技术赋能业务创新</h1>
        <p>专业的企业级BI系统、CRM系统定制开发，为您的业务提供智能化、可视化的管理解决方案</p>
        <div style="display: flex; gap: 20px; margin-top: 40px;">
            <a href="#projects" class="cta-button" style="background: white; color: #667eea;">查看案例</a>
            <a href="#contact" class="cta-button">立即咨询</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 公司亮点统计 ==========
st.markdown("""
<div style="background: #f8f9fa; padding: 60px 5%;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 50px;">
            <h2 style="color: #333; font-size: 2.5rem; margin-bottom: 15px;">为什么选择我们</h2>
            <p style="color: #666; font-size: 1.1rem;">专业的技术团队，丰富的行业经验，完善的服务体系</p>
        </div>

        <div class="row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
            <div class="stat-card">
                <div class="stat-number">50+</div>
                <h3>成功项目</h3>
                <p style="color: #666;">覆盖制造业、零售、电商等多个行业</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">30+</div>
                <h3>企业客户</h3>
                <p style="color: #666;">服务过中小型企业到上市公司</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">99%</div>
                <h3>客户满意度</h3>
                <p style="color: #666;">完善的售后服务和持续的技术支持</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">7×24</div>
                <h3>小时响应</h3>
                <p style="color: #666;">快速响应客户需求，及时解决问题</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 服务项目 ==========
st.markdown("""
<a id="services"></a>
<div style="padding: 100px 5%; background: white;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="color: #333; font-size: 2.5rem; margin-bottom: 15px;">核心服务</h2>
            <p style="color: #666; font-size: 1.1rem;">为企业提供全方位的数字化解决方案</p>
        </div>

        <div class="row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
            <div class="card">
                <div class="card-icon">📊</div>
                <h3 style="color: #333; margin-bottom: 15px;">BI商业智能系统</h3>
                <p style="color: #666; line-height: 1.6;">为企业提供数据可视化分析，实时监控业务指标，支持多维度数据分析，助力企业数据驱动决策。</p>
                <ul style="margin-top: 20px; color: #666;">
                    <li>销售数据分析看板</li>
                    <li>库存监控与预警系统</li>
                    <li>客户行为分析报表</li>
                    <li>实时业绩监控系统</li>
                </ul>
            </div>

            <div class="card">
                <div class="card-icon">🤝</div>
                <h3 style="color: #333; margin-bottom: 15px;">CRM客户关系管理</h3>
                <p style="color: #666; line-height: 1.6;">全面管理客户信息，跟踪销售机会，自动化营销流程，提升客户满意度和销售转化率。</p>
                <ul style="margin-top: 20px; color: #666;">
                    <li>客户全生命周期管理</li>
                    <li>销售漏斗与机会管理</li>
                    <li>自动化营销工具</li>
                    <li>客户服务与支持</li>
                </ul>
            </div>

            <div class="card">
                <div class="card-icon">🛠️</div>
                <h3 style="color: #333; margin-bottom: 15px;">定制化管理系统</h3>
                <p style="color: #666; line-height: 1.6;">根据企业特定需求，定制开发ERP、OA、进销存等管理系统，完美匹配业务流程。</p>
                <ul style="margin-top: 20px; color: #666;">
                    <li>ERP企业资源计划</li>
                    <li>OA办公自动化</li>
                    <li>进销存管理系统</li>
                    <li>生产制造执行系统</li>
                </ul>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 项目案例展示 ==========
st.markdown("""
<a id="projects"></a>
<div style="padding: 100px 5%; background: #f8f9fa;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="color: #333; font-size: 2.5rem; margin-bottom: 15px;">成功案例</h2>
            <p style="color: #666; font-size: 1.1rem;">我们为各行业客户提供定制化的数字化解决方案</p>
        </div>

        <div class="row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
            <!-- 项目1：五金店进销存系统 -->
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(45deg, #4facfe, #00f2fe);"></div>
                <div class="project-content">
                    <h3 style="color: #333; margin-bottom: 10px;">五金店进销存管理系统</h3>
                    <p style="color: #666; margin-bottom: 20px;">为五金行业定制的进销存管理系统，包含商品管理、采购入库、销售开单、库存预警等功能。</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                        <span style="background: #e3f2fd; color: #1565c0; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">Python</span>
                        <span style="background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">Streamlit</span>
                        <span style="background: #f3e5f5; color: #7b1fa2; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">SQLite</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #667eea; font-weight: bold;">开发周期：2周</span>
                        <a href="#contact" style="color: #667eea; text-decoration: none; font-weight: bold;">了解详情 →</a>
                    </div>
                </div>
            </div>

            <!-- 项目2：CRM管理系统 -->
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(45deg, #667eea, #764ba2);"></div>
                <div class="project-content">
                    <h3 style="color: #333; margin-bottom: 10px;">企业CRM客户关系管理系统</h3>
                    <p style="color: #666; margin-bottom: 20px;">完整的CRM解决方案，包含客户管理、销售机会、联系记录、任务管理、业绩分析等功能。</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                        <span style="background: #e3f2fd; color: #1565c0; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">多角色权限</span>
                        <span style="background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">数据可视化</span>
                        <span style="background: #f3e5f5; color: #7b1fa2; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">销售漏斗</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #667eea; font-weight: bold;">开发周期：4周</span>
                        <a href="#contact" style="color: #667eea; text-decoration: none; font-weight: bold;">了解详情 →</a>
                    </div>
                </div>
            </div>

            <!-- 项目3：BI看板系统 -->
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(45deg, #f093fb, #f5576c);"></div>
                <div class="project-content">
                    <h3 style="color: #333; margin-bottom: 10px;">制造业BI智能看板</h3>
                    <p style="color: #666; margin-bottom: 20px;">为制造企业定制的BI数据分析平台，实时监控生产、销售、库存等关键指标，支持多维度分析。</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                        <span style="background: #e3f2fd; color: #1565c0; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">实时数据</span>
                        <span style="background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">预警监控</span>
                        <span style="background: #f3e5f5; color: #7b1fa2; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem;">移动适配</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #667eea; font-weight: bold;">开发周期：3周</span>
                        <a href="#contact" style="color: #667eea; text-decoration: none; font-weight: bold;">了解详情 →</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 技术优势 ==========
st.markdown("""
<div style="padding: 100px 5%; background: white;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="color: #333; font-size: 2.5rem; margin-bottom: 15px;">技术优势</h2>
            <p style="color: #666; font-size: 1.1rem;">我们采用先进的技术栈，确保系统稳定、安全、高效</p>
        </div>

        <div class="row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 50px; margin-bottom: 20px;">⚡</div>
                <h3 style="color: #333; margin-bottom: 15px;">快速开发</h3>
                <p style="color: #666;">使用Streamlit快速原型开发，大幅缩短项目周期，快速响应需求变化。</p>
            </div>

            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 50px; margin-bottom: 20px;">🔐</div>
                <h3 style="color: #333; margin-bottom: 15px;">安全可靠</h3>
                <p style="color: #666;">完善的安全机制，数据加密传输，权限分级管理，保障企业数据安全。</p>
            </div>

            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 50px; margin-bottom: 20px;">📱</div>
                <h3 style="color: #333; margin-bottom: 15px;">多端适配</h3>
                <p style="color: #666;">响应式设计，完美适配PC、平板、手机等多种设备，随时随地办公。</p>
            </div>

            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 50px; margin-bottom: 20px;">🔄</div>
                <h3 style="color: #333; margin-bottom: 15px;">持续迭代</h3>
                <p style="color: #666;">根据业务发展需求，持续优化升级，确保系统与企业一同成长。</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 客户评价 ==========
st.markdown("""
<div style="padding: 100px 5%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; margin-bottom: 15px;">客户评价</h2>
            <p style="opacity: 0.9; font-size: 1.1rem;">听听我们的客户怎么说</p>
        </div>

        <div class="row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 30px;">
                <p style="font-style: italic; margin-bottom: 20px;">"数智科技为我们开发的BI看板系统，让我们的销售数据一目了然，管理决策更加科学高效。团队专业，服务到位。"</p>
                <div style="display: flex; align-items: center;">
                    <div style="width: 50px; height: 50px; background: white; border-radius: 50%; margin-right: 15px;"></div>
                    <div>
                        <h4 style="margin: 0;">张总</h4>
                        <p style="opacity: 0.8; margin: 0; font-size: 0.9rem;">某制造企业 总经理</p>
                    </div>
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 30px;">
                <p style="font-style: italic; margin-bottom: 20px;">"CRM系统极大地提升了我们的销售效率，客户跟进更加及时，销售漏斗清晰可见。强烈推荐！"</p>
                <div style="display: flex; align-items: center;">
                    <div style="width: 50px; height: 50px; background: white; border-radius: 50%; margin-right: 15px;"></div>
                    <div>
                        <h4 style="margin: 0;">李经理</h4>
                        <p style="opacity: 0.8; margin: 0; font-size: 0.9rem;">某科技公司 销售总监</p>
                    </div>
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 30px;">
                <p style="font-style: italic; margin-bottom: 20px;">"进销存系统操作简单，功能实用，帮助我们规范了库存管理，减少了库存积压。服务响应很快。"</p>
                <div style="display: flex; align-items: center;">
                    <div style="width: 50px; height: 50px; background: white; border-radius: 50%; margin-right: 15px;"></div>
                    <div>
                        <h4 style="margin: 0;">王老板</h4>
                        <p style="opacity: 0.8; margin: 0; font-size: 0.9rem;">某五金店 店主</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 在线咨询表单 ==========
st.markdown("""
<a id="contact"></a>
<div style="padding: 100px 5%; background: white;">
    <div style="max-width: 800px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="color: #333; font-size: 2.5rem; margin-bottom: 15px;">立即咨询</h2>
            <p style="color: #666; font-size: 1.1rem;">留下您的需求，我们将尽快与您联系</p>
        </div>

        <div class="card" style="max-width: 600px; margin: 0 auto;">
            <h3 style="color: #333; margin-bottom: 30px; text-align: center;">免费获取方案咨询</h3>
""", unsafe_allow_html=True)

# 咨询表单
with st.form("consult_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名*", placeholder="请输入您的姓名")
        company = st.text_input("公司名称", placeholder="请输入公司名称")
    with col2:
        phone = st.text_input("联系电话*", placeholder="请输入您的手机号")
        email = st.text_input("邮箱", placeholder="请输入您的邮箱")

    industry = st.selectbox("所属行业", ["", "制造业", "零售业", "电商", "服务业", "教育", "医疗", "其他"])

    service_type = st.multiselect(
        "感兴趣的服务",
        ["BI商业智能系统", "CRM客户关系管理", "ERP企业资源计划", "OA办公自动化", "进销存管理系统", "定制开发"]
    )

    budget = st.selectbox(
        "预算范围",
        ["", "1-3万元", "3-5万元", "5-10万元", "10万元以上", "待评估"]
    )

    requirements = st.text_area("具体需求*", placeholder="请详细描述您的需求，如：需要管理客户信息、需要数据分析功能等",
                                height=150)

    submitted = st.form_submit_button("提交咨询", type="primary", use_container_width=True)

    if submitted:
        if not name or not phone or not requirements:
            st.error("请填写带*的必填项")
        else:
            # 这里可以添加将数据保存到数据库或发送邮件的逻辑
            st.success("✅ 咨询已提交！我们将在24小时内与您联系。")

            # 显示提交的内容
            st.info(f"""
            **提交信息：**
            - 姓名：{name}
            - 公司：{company or '未填写'}
            - 电话：{phone}
            - 邮箱：{email or '未填写'}
            - 行业：{industry or '未选择'}
            - 服务类型：{', '.join(service_type) if service_type else '未选择'}
            - 预算：{budget or '未选择'}
            - 需求：{requirements}
            """)

st.markdown("""
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 页脚 ==========
st.markdown("""
<div class="footer">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-bottom: 40px;">
            <div>
                <h3 style="color: white; margin-bottom: 20px;">🚀 数智科技</h3>
                <p style="color: #aaa; line-height: 1.6;">专注于企业级数字化解决方案，为企业提供智能化、可视化的管理系统定制开发服务。</p>
            </div>

            <div>
                <h4 style="color: white; margin-bottom: 20px;">服务项目</h4>
                <ul style="list-style: none; padding: 0; color: #aaa;">
                    <li style="margin-bottom: 10px;">BI商业智能系统</li>
                    <li style="margin-bottom: 10px;">CRM客户关系管理</li>
                    <li style="margin-bottom: 10px;">ERP企业资源计划</li>
                    <li style="margin-bottom: 10px;">定制化开发</li>
                </ul>
            </div>

            <div>
                <h4 style="color: white; margin-bottom: 20px;">联系我们</h4>
                <ul style="list-style: none; padding: 0; color: #aaa;">
                    <li style="margin-bottom: 10px;">📧 contact@datatech.com</li>
                    <li style="margin-bottom: 10px;">📞 400-888-8888</li>
                    <li style="margin-bottom: 10px;">📍 北京市朝阳区科技园</li>
                    <li style="margin-bottom: 10px;">🕐 周一至周五 9:00-18:00</li>
                </ul>
            </div>

            <div>
                <h4 style="color: white; margin-bottom: 20px;">关注我们</h4>
                <div style="display: flex; gap: 15px;">
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white;">微</span>
                    </div>
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white;">Q</span>
                    </div>
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white;">抖</span>
                    </div>
                </div>
            </div>
        </div>

        <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; text-align: center; color: #aaa;">
            <p>© 2026 数智科技 版权所有 京ICP备12345678号</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 在线聊天工具 ==========
st.markdown("""
<script>
// 简单的在线聊天工具
document.addEventListener('DOMContentLoaded', function() {
    // 创建聊天按钮
    const chatBtn = document.createElement('div');
    chatBtn.innerHTML = `
        <style>
            .chat-button {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
                z-index: 1000;
                transition: transform 0.3s;
            }
            .chat-button:hover {
                transform: scale(1.1);
            }
            .chat-button span {
                color: white;
                font-size: 24px;
            }
        </style>
        <div class="chat-button">
            <span>💬</span>
        </div>
    `;
    document.body.appendChild(chatBtn);

    // 点击事件
    chatBtn.addEventListener('click', function() {
        document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
    });
});
</script>
""", unsafe_allow_html=True)
