# -*- coding: utf-8 -*-
# @Time    : 2026/5/7
# @Author  : 数智科技
# @File    : company_website_optimized.py
# @Software: PyCharm
# @Desc    : 企业官网推广页面 (优化版)

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import time

# ========== 1. 页面配置 ==========
st.set_page_config(
    page_title="数智科技 | 行业领先数字化引擎",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ========== 2. 后端逻辑接口预留 (Python Functions) ==========
# 在这里编写你的业务逻辑，点击按钮时会触发这些函数

def handle_consultation(data):
    """预留接口：处理免费方案咨询"""
    # 示例：可以将数据写入数据库或发送 API 请求
    print(f"收到咨询请求: {data}")
    time.sleep(1)  # 模拟网络延迟
    return True


def trigger_system_demo(module_name):
    """预留接口：启动演示系统"""
    st.toast(f"正在初始化 {module_name} 演示环境...", icon="🚀")
    time.sleep(1)


def fetch_case_details(case_id):
    """预留接口：获取案例详细数据"""
    return {"status": "success", "data": "详细案例报告内容"}


# ========== 3. 炫酷 CSS 样式注入 ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');

    .stApp { background: #05070a; color: #ffffff; font-family: 'Inter', sans-serif; }

    /* 霓虹边框卡片 */
    .case-card {
        background: rgba(255, 255, 255, 0.02);
        border-left: 4px solid #00f2fe;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s;
        cursor: pointer;
    }
    .case-card:hover {
        background: rgba(0, 242, 254, 0.05);
        transform: translateX(10px);
        box-shadow: -10px 0 20px rgba(0, 242, 254, 0.1);
    }

    .gradient-text {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', sans-serif;
    }

    /* 炫酷按钮样式覆盖 Streamlit */
    div.stButton > button {
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        width: 100%;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6) !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ========== 4. Hero Section ==========
col_h1, col_h2 = st.columns([1.5, 1])
with col_h1:
    st.markdown("""
    <h1 style="font-size: 4rem; margin-bottom: 10px;">数智化 <span class="gradient-text">核心引擎</span></h1>
    <p style="font-size: 1.2rem; color: #a0aec0; margin-bottom: 30px;">
        我们为企业提供不仅仅是软件，而是基于 Python 生态的深度业务进化方案。
    </p>
    """, unsafe_allow_html=True)
    if st.button("🚀 立即部署企业大脑"):
        trigger_system_demo("全平台")

with col_h2:
    # 实时数据波动展示
    st.markdown('<p style="color:#00f2fe; font-family:Orbitron; margin-bottom:5px;">SYSTEM LIVE STATUS</p>',
                unsafe_allow_html=True)
    chart_data = pd.DataFrame(np.random.randn(15, 2), columns=['CPU', 'NET'])
    st.area_chart(chart_data, height=150)

# ========== 5. 行业深度案例 (New Content) ==========
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="font-family: Orbitron; text-align: center;">INDUSTRY CASES / 行业案例</h2>',
            unsafe_allow_html=True)

case_col1, case_col2 = st.columns(2)

with case_col1:
    st.markdown("""
    <div class="case-card">
        <h3 style="color: #00f2fe;">某头部五金跨境电商</h3>
        <p style="color: #cbd5e0; font-size: 0.9rem;">
            <b>挑战：</b> 日均订单 5w+，多渠道库存同步延迟导致超卖严重。<br>
            <b>方案：</b> 部署分布式 Python 进销存引擎，引入毫秒级 Redis 锁机制。<br>
            <b>成效：</b> 库存误差率降低至 0.01%，人工盘点成本节省 70%。
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("查看此案例技术架构", key="case1"):
        st.info("正在调取 Python 后端架构图谱...")

with case_col2:
    st.markdown("""
    <div class="case-card">
        <h3 style="color: #4facfe;">华南某制造型企业 BI 项目</h3>
        <p style="color: #cbd5e0; font-size: 0.9rem;">
            <b>挑战：</b> 生产线数据孤岛化，管理层无法实时获知良品率。<br>
            <b>方案：</b> 搭建基于 Pandas 的实时数据清洗管道，Streamlit 动态看板展示。<br>
            <b>成效：</b> 异常响应速度提升 4 倍，生产损耗降低 12%。
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("查看此案例技术架构", key="case2"):
        st.info("正在调取 BI 数据流向图...")

# ========== 6. 预留功能区 (Python 接口演示) ==========
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="font-family: Orbitron; text-align: center;">TECH STACK / 技术能力</h2>', unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
with tech_col1:
    st.markdown("#### 🐍 Python 驱动")
    st.caption("高性能异步后端处理")
with tech_col2:
    st.markdown("#### 📊 实时 BI")
    st.caption("秒级响应式数据看板")
with tech_col3:
    st.markdown("#### 🤖 AI 算法")
    st.caption("销量预测与客户分类")
with tech_col4:
    st.markdown("#### ☁️ 云原生")
    st.caption("容器化部署与弹性扩容")

# ========== 7. 交互表单 (集成后端接口) ==========
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,242,254,0.05) 0%, transparent 100%); padding: 40px; border-radius: 20px; border: 1px solid rgba(0,242,254,0.1);">
        <h2 style="text-align: center; font-family: Orbitron;">CONNECT WITH US</h2>
    """, unsafe_allow_html=True)

    with st.form("main_contact"):
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("称呼")
            u_tel = st.text_input("联系电话")
        with c2:
            u_corp = st.text_input("公司名称")
            u_type = st.selectbox("意向模块", ["BI 报表", "CRM 系统", "进销存", "全案定制"])

        u_desc = st.text_area("简述您的数字化困境")

        # 按钮触发表单提交
        submitted = st.form_submit_button("发送指令至数智后端")

        if submitted:
            if u_name and u_tel:
                # 调用预留的 Python 接口
                success = handle_consultation({"name": u_name, "tel": u_tel, "corp": u_corp, "needs": u_desc})
                if success:
                    st.balloons()
                    st.success(f"已成功建立连接！系统编号：DT-{int(time.time())}。我们将尽快联系您。")
            else:
                st.warning("⚠️ 请输入关键联系信息，以便系统建立连接。")
    st.markdown("</div>", unsafe_allow_html=True)

# ========== 8. Footer ==========
st.markdown(f"""
<div style="text-align: center; padding: 40px; color: #4a5568; font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
    <p>数智科技 | NEURAL CORE ENGINE V2.0</p>
    <p>运行环境: Python 3.9+ | 实时状态: 🟢 Online</p>
</div>
""", unsafe_allow_html=True)
