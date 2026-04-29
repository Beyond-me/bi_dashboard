# -*- coding: utf-8 -*-
# @Time    : 2026/4/29 14:41
# @Author  : lihaizhen
# @File    : tuoweisi_bi_dashboard_fixed.py
# @Software: PyCharm
# @Desc    : 拓威斯自动化BI看板 - 侧边栏稳定版

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# ========== 1. 页面配置 ==========
# 关键修改：完全移除 initial_sidebar_state 参数，让 Streamlit 使用默认行为
st.set_page_config(
    page_title="拓威斯自动化 - 智能管理驾驶舱",
    page_icon="⚙️",
    layout="wide"
    # 注意：这里不设置 initial_sidebar_state
)

# ========== 2. 最小化的样式 ==========
# 只保留必要的样式，避免与 Streamlit 原生样式冲突
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a237e 0%, #283593 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-top: 4px solid;
        margin-bottom: 10px;
    }

    .metric-sales { border-top-color: #1a237e; }
    .metric-projects { border-top-color: #3949ab; }
    .metric-regions { border-top-color: #5c6bc0; }
    .metric-growth { border-top-color: #7986cb; }

    .positive { color: #4caf50; font-weight: bold; }
    .negative { color: #f44336; font-weight: bold; }
    .warning { color: #ff9800; font-weight: bold; }

    /* 隐藏 Streamlit 的默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# ========== 3. 生成模拟数据 ==========
def generate_tuoweisi_data():
    """生成自动化设备制造商模拟数据"""
    np.random.seed(2026)

    regions = ['深圳总公司', '广州办事处', '苏州办事处', '天津办事处',
               '温州办事处', '宁波办事处', '厦门办事处', '青岛办事处', '成都办事处']
    region_colors = {
        '深圳总公司': '#1a237e', '广州办事处': '#3949ab', '苏州办事处': '#5c6bc0',
        '天津办事处': '#7986cb', '温州办事处': '#9575cd', '宁波办事处': '#7e57c2',
        '厦门办事处': '#673ab7', '青岛办事处': '#5e35b1', '成都办事处': '#512da8'
    }

    product_lines = ['自动冲针机', '自动锁螺丝机', '机器人集成', '非标定制线']
    product_models = {
        '自动冲针机': ['TO-901手持式', 'TO-902单轴式', 'TO-905平台式', 'TO-908机器人式'],
        '自动锁螺丝机': ['TO-801手持式', 'TO-802多轴式', 'TO-803转盘式', 'TO-805桌面式'],
        '机器人集成': ['四轴机器人线', '六轴机器人线', '协作机器人线'],
        '非标定制线': ['检测专机', '组装专机', '包装专机']
    }

    industries = ['消费电子', '家用电器', '汽车零部件', '通讯设备',
                  '新能源', '医疗器械', '玩具礼品', '仪器仪表']

    project_statuses = ['线索跟进', '方案报价', '设计阶段', '生产制造',
                        '调试交付', '售后服务', '项目结案']

    # 生成销售机会数据
    today = datetime.now()
    opportunities = []

    for i in range(50):
        region = np.random.choice(regions)
        industry = np.random.choice(industries)
        product_line = np.random.choice(product_lines)
        product_model = np.random.choice(product_models[product_line])

        if '机器人' in product_line:
            contract_value = np.random.uniform(200000, 800000)
        elif '定制线' in product_line:
            contract_value = np.random.uniform(300000, 1000000)
        else:
            contract_value = np.random.uniform(50000, 300000)

        status = np.random.choice(project_statuses, p=[0.2, 0.15, 0.1, 0.15, 0.1, 0.2, 0.1])
        status_index = project_statuses.index(status)
        progress = (status_index + 1) * 100 / len(project_statuses)

        create_date = today - timedelta(days=np.random.randint(10, 180))
        if status in ['调试交付', '售后服务', '项目结案']:
            delivery_date = create_date + timedelta(days=np.random.randint(60, 120))
        else:
            delivery_date = None

        opportunities.append({
            'opp_id': f'OPP{2026000 + i}',
            'customer_name': f'{industry}客户{np.random.randint(1, 20)}',
            'industry': industry,
            'region': region,
            'product_line': product_line,
            'product_model': product_model,
            'contract_value': contract_value,
            'status': status,
            'progress': progress,
            'create_date': create_date,
            'expected_delivery': delivery_date,
            'sales_person': f'销售{np.random.randint(1, 6)}',
            'probability': np.random.uniform(0.3, 0.9) if status in ['线索跟进', '方案报价'] else 1.0
        })

    df_opps = pd.DataFrame(opportunities)

    # 生成月度销售数据
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    monthly_sales = []

    for month in months:
        for region in regions[:4]:
            for product_line in product_lines:
                monthly_sales.append({
                    'month': month,
                    'region': region,
                    'product_line': product_line,
                    'sales_amount': np.random.uniform(100000, 500000),
                    'projects_count': np.random.randint(1, 6)
                })

    df_monthly = pd.DataFrame(monthly_sales)

    # 生成售后服务数据
    service_data = []
    service_types = ['安装调试', '操作培训', '配件更换', '故障维修', '预防保养']

    for _ in range(30):
        region = np.random.choice(regions)
        product_line = np.random.choice(product_lines)

        service_data.append({
            'service_id': f'SVC{np.random.randint(1000, 9999)}',
            'region': region,
            'product_line': product_line,
            'service_type': np.random.choice(service_types),
            'create_date': today - timedelta(days=np.random.randint(1, 90)),
            'status': np.random.choice(['待处理', '处理中', '已完成'], p=[0.1, 0.3, 0.6]),
            'response_days': np.random.randint(1, 7),
            'customer_rating': np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.2, 0.4, 0.25])
        })

    df_service = pd.DataFrame(service_data)

    return {
        'df_opps': df_opps,
        'df_monthly': df_monthly,
        'df_service': df_service,
        'regions': regions,
        'region_colors': region_colors,
        'product_lines': product_lines,
        'project_statuses': project_statuses
    }


# 加载数据
data = generate_tuoweisi_data()
df_opps = data['df_opps']
df_monthly = data['df_monthly']
df_service = data['df_service']

today = datetime.now()

# 计算关键指标
current_year = df_monthly[df_monthly['month'].dt.year == 2024]
total_annual_sales = current_year['sales_amount'].sum()
total_projects = current_year['projects_count'].sum()

active_projects = df_opps[~df_opps['status'].isin(['项目结案'])]
active_projects_value = active_projects['contract_value'].sum()

if not df_opps.empty:
    df_opps_delivered = df_opps[df_opps['status'].isin(['调试交付', '售后服务', '项目结案'])]
    if not df_opps_delivered.empty:
        avg_delivery_days = (df_opps_delivered['expected_delivery'] - df_opps_delivered['create_date']).dt.days.mean()
    else:
        avg_delivery_days = 0
else:
    avg_delivery_days = 0

avg_service_rating = df_service['customer_rating'].mean()

# ========== 4. 侧边栏 ==========
# 关键：确保侧边栏有足够内容和明确的标题
st.sidebar.title("⚙️ 拓威斯自动化")

# 在侧边栏中添加足够的控件，确保其稳定显示
st.sidebar.markdown("### 🎛️ 控制面板")

# 添加一些实际控件
time_range = st.sidebar.selectbox(
    "时间范围",
    ["本月", "本季度", "本年度", "最近12个月"],
    index=2
)

regions_selected = st.sidebar.multiselect(
    "选择办事处",
    data['regions'],
    default=data['regions'][:4]
)

products_selected = st.sidebar.multiselect(
    "选择产品线",
    data['product_lines'],
    default=data['product_lines']
)

st.sidebar.divider()

# 添加一个刷新按钮
if st.sidebar.button("🔄 刷新数据", use_container_width=True):
    st.rerun()

# 添加一个简单的提示
with st.sidebar.expander("💡 使用提示"):
    st.write("""
    1. 点击图表可交互
    2. 鼠标悬停查看详情
    3. 使用筛选器查看不同维度
    """)

# ========== 5. 主页面内容 ==========
# 主标题
st.markdown("""
<div class="main-header">
    <h1>⚙️ 拓威斯自动化 - 智能管理驾驶舱</h1>
    <p>专注自动螺丝机、冲针机、非标自动化设备的销售与项目管理</p>
</div>
""", unsafe_allow_html=True)

# 第一行：核心运营指标
st.markdown("### 📈 核心运营指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-sales">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">年度销售额</div>
        <div style="font-size: 28px; font-weight: bold; color: #1a237e;">¥{total_annual_sales:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">项目数: {total_projects:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-projects">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">在执项目</div>
        <div style="font-size: 28px; font-weight: bold; color: #3949ab;">{len(active_projects)}</div>
        <div style="font-size: 12px; margin-top: 5px;">合同额: ¥{active_projects_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-regions">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">平均交付周期</div>
        <div style="font-size: 28px; font-weight: bold; color: #5c6bc0;">{avg_delivery_days:.0f}天</div>
        <div style="font-size: 12px; margin-top: 5px;">当前进行中: {len(df_opps[df_opps['status'] == '生产制造'])}个</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    rating_color = "positive" if avg_service_rating >= 4 else "warning" if avg_service_rating >= 3 else "negative"
    st.markdown(f"""
    <div class="metric-card metric-growth">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">服务满意度</div>
        <div style="font-size: 28px; font-weight: bold; color: #7986cb;">{avg_service_rating:.1f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            评分<span class="{rating_color}">{'优秀' if avg_service_rating >= 4 else '良好' if avg_service_rating >= 3 else '需改进'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 第二行：销售漏斗和区域分析
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📊 销售漏斗分析")
    status_dist = df_opps['status'].value_counts().reindex(data['project_statuses']).fillna(0)

    fig_funnel = go.Figure(go.Funnel(
        y=status_dist.index.tolist(),
        x=status_dist.values.tolist(),
        textinfo="value+percent initial",
        opacity=0.8,
        marker=dict(color=['#e3f2fd', '#e8eaf6', '#f3e5f5', '#fff3e0', '#e8f5e9', '#f1f8e9', '#f5f5f5'])
    ))

    fig_funnel.update_layout(
        height=400,
        title="销售漏斗 - 项目状态分布",
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    st.markdown("### 🗺️ 区域业绩分布")
    region_sales = df_monthly.groupby('region')['sales_amount'].sum().reset_index()

    fig_region = px.pie(
        region_sales,
        values='sales_amount',
        names='region',
        color='region',
        color_discrete_map=data['region_colors'],
        hole=0.3
    )

    fig_region.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>销售额: ¥%{value:,.0f}'
    )

    fig_region.update_layout(
        height=400,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# 第三行：项目监控和产品分析
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 重点项目监控")
    high_value_projects = df_opps[df_opps['contract_value'] > 300000].sort_values('contract_value', ascending=False)

    if not high_value_projects.empty:
        for _, project in high_value_projects.head(3).iterrows():
            with st.container(border=True):
                title_cols = st.columns([3, 1])
                with title_cols[0]:
                    st.write(f"**{project['opp_id']} - {project['customer_name']}**")
                with title_cols[1]:
                    st.write(f"**{project['status']}**")

                st.caption(f"{project['industry']} · {project['product_model']} · {project['region']}")
                st.progress(project['progress'] / 100)
                st.caption(f"进度: {project['progress']:.0f}%")

                metric_cols = st.columns(3)
                with metric_cols[0]:
                    st.metric("合同额", f"¥{project['contract_value']:,.0f}")
                with metric_cols[1]:
                    st.metric("负责人", project['sales_person'])
                with metric_cols[2]:
                    days_open = (today - project['create_date']).days
                    st.metric("已进行", f"{days_open}天")
    else:
        st.info("暂无高价值项目")

    st.markdown("##### ⚙️ 产品线销售分布")
    product_sales = df_monthly.groupby('product_line')['sales_amount'].sum().reset_index()

    fig_product = px.bar(
        product_sales.sort_values('sales_amount', ascending=True),
        y='product_line',
        x='sales_amount',
        orientation='h',
        color='product_line',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig_product.update_layout(
        height=250,
        xaxis_title="销售额（元）",
        yaxis_title="",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_product, use_container_width=True)

with col2:
    st.markdown("### 🔧 售后服务看板")
    service_dist = df_service['service_type'].value_counts().reset_index()
    service_dist.columns = ['service_type', 'count']

    fig_service = px.bar(
        service_dist,
        x='service_type',
        y='count',
        color='service_type',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_service.update_layout(
        height=300,
        xaxis_title="服务类型",
        yaxis_title="数量",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_service, use_container_width=True)

    st.markdown("##### ⏳ 待处理服务单")
    pending_service = df_service[df_service['status'] == '待处理']

    if not pending_service.empty:
        for _, service in pending_service.head(3).iterrows():
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"**{service['service_id']}**")
                    st.caption(f"{service['service_type']} · {service['product_line']}")
                with cols[1]:
                    st.warning("待处理")
    else:
        st.success("✅ 无待处理服务单")

st.divider()

# 第四行：月度趋势和业务洞察
st.markdown("### 📈 月度销售趋势")
monthly_trend = df_monthly.groupby('month')['sales_amount'].sum().reset_index()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=monthly_trend['month'],
    y=monthly_trend['sales_amount'],
    mode='lines+markers',
    name='月度销售额',
    line=dict(color='#1a237e', width=3),
    marker=dict(size=6)
))

fig_trend.update_layout(
    height=300,
    title="2024年月度销售趋势",
    xaxis_title="月份",
    yaxis_title="销售额（元）",
    plot_bgcolor='white',
    hovermode='x unified',
    yaxis=dict(tickformat=',.0f')
)

st.plotly_chart(fig_trend, use_container_width=True)

# 业务洞察
st.markdown("### 💡 业务洞察")

insights = [
    {"icon": "💰", "title": "机器人集成订单增长",
     "content": "机器人集成线订单额同比增长35%，毛利率达42%，建议加大该产品线推广"},
    {"icon": "📍", "title": "长三角地区需求旺盛", "content": "苏州、宁波办事处业绩增长显著，建议增加该区域技术支持人员"},
    {"icon": "⏱️", "title": "设计阶段周期偏长", "content": "项目在'设计阶段'平均停留21天，建议优化设计评审流程"},
    {"icon": "🔧", "title": "配件更换服务频次高", "content": "配件更换占服务总量的38%，建议优化易损件设计和备货策略"},
]

cols = st.columns(2)
for idx, insight in enumerate(insights):
    with cols[idx % 2]:
        with st.container(border=True):
            st.write(f"**{insight['icon']} {insight['title']}**")
            st.write(insight['content'])

# 页脚
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p>⚙️ 拓威斯自动化BI看板系统 | 数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p>💡 本系统支持对接CRM、项目管理系统、售后服务系统 | 全国9大办事处数据实时同步</p>
</div>
""", unsafe_allow_html=True)
