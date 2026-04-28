# -*- coding: utf-8 -*-
# @Time    : 2026/4/28 17:54
# @Author  : lihaizhen
# @File    : bi_dashboard.py
# @Software: PyCharm
# @Desc    :

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="智看BI - 企业经营看板",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"  # 手机端默认收起侧边栏
)

# 隐藏streamlit默认样式
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.viewerBadge_container__1QSob {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 自定义专业样式
st.markdown("""
<style>
    /* 主标题样式 */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 指标卡片样式 */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-left: 5px solid #2a5298;
        margin-bottom: 15px;
        transition: transform 0.3s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }

    /* 增长样式 */
    .positive {
        color: #10b981;
        font-weight: bold;
    }

    .negative {
        color: #ef4444;
        font-weight: bold;
    }

    /* 标签样式 */
    .time-badge {
        background: #e0f2fe;
        color: #0369a1;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)


# 生成模拟数据
def generate_sample_data():
    """生成企业模拟数据"""
    np.random.seed(42)

    # 生成日期范围（最近30天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # 销售额数据（有增长趋势）
    base_sales = 50000
    growth_rate = 0.02
    sales = []
    for i in range(len(dates)):
        daily_sales = base_sales * (1 + growth_rate * i) + np.random.normal(0, 5000)
        sales.append(max(30000, daily_sales))

    # 生成各渠道数据
    channels = ['线上商城', '实体门店', '批发渠道', '企业客户', '跨境电商']
    channel_weights = [0.4, 0.3, 0.15, 0.1, 0.05]

    channel_data = []
    for date in dates:
        daily_total = sales[dates.get_loc(date)]
        daily_channels = np.random.dirichlet([5, 4, 3, 2, 1]) * daily_total

        for idx, channel in enumerate(channels):
            channel_data.append({
                'date': date,
                'channel': channel,
                'sales': daily_channels[idx],
                'orders': int(np.random.poisson(50 * channel_weights[idx])),
                'customers': int(np.random.poisson(30 * channel_weights[idx]))
            })

    df_channels = pd.DataFrame(channel_data)

    # 生成产品数据
    products = [
        '智能手表', '蓝牙耳机', '智能手机', '平板电脑', '笔记本电脑',
        '智能音箱', '路由器', '移动电源', '智能手环', '摄像头'
    ]

    product_data = []
    for product in products:
        product_data.append({
            'product': product,
            'sales': np.random.uniform(50000, 300000),
            'profit_rate': np.random.uniform(0.15, 0.35),
            'growth': np.random.uniform(-0.1, 0.3),
            'stock_days': np.random.randint(10, 60)
        })

    df_products = pd.DataFrame(product_data)

    # 生成地区数据
    regions = ['华北', '华东', '华南', '华中', '西北', '西南', '东北']
    region_data = []
    for region in regions:
        region_data.append({
            'region': region,
            'sales': np.random.uniform(100000, 500000),
            'growth': np.random.uniform(0.05, 0.25),
            'stores': np.random.randint(5, 50)
        })

    df_regions = pd.DataFrame(region_data)

    return {
        'dates': dates,
        'sales': sales,
        'df_channels': df_channels,
        'df_products': df_products,
        'df_regions': df_regions
    }


# 加载数据
data = generate_sample_data()

# 计算关键指标
current_sales = data['sales'][-1]
previous_sales = data['sales'][-8]  # 7天前
sales_growth = (current_sales - previous_sales) / previous_sales

total_sales_30d = sum(data['sales'])
avg_daily_sales = total_sales_30d / 30

top_product = data['df_products'].loc[data['df_products']['sales'].idxmax()]
top_region = data['df_regions'].loc[data['df_regions']['sales'].idxmax()]

# 主页面
st.markdown(
    '<div class="main-header"><h1>📈 智看BI - 企业经营数据看板</h1><p>实时监控企业核心经营指标，数据驱动决策</p></div>',
    unsafe_allow_html=True)

# 时间筛选
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    time_range = st.selectbox("时间范围", ["最近7天", "最近30天", "本季度", "本年度"], index=1)
with col2:
    compare_with = st.selectbox("对比基准", ["上周同期", "上月同期", "去年同期", "无对比"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 刷新数据"):
        st.rerun()

# 第一行：核心指标
st.markdown("### 📊 核心经营指标")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">今日销售额</div>
        <div style="font-size: 28px; font-weight: bold; color: #1e3c72;">¥{current_sales:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            环比<span class="{'positive' if sales_growth > 0 else 'negative'}">{sales_growth:+.1%}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">30天总销售额</div>
        <div style="font-size: 28px; font-weight: bold; color: #1e3c72;">¥{total_sales_30d:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            日均 ¥{avg_daily_sales:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">热销产品</div>
        <div style="font-size: 20px; font-weight: bold; color: #1e3c72;">{top_product['product']}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            销售额 ¥{top_product['sales']:,.0f} · 利润率 {top_product['profit_rate']:.1%}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">最佳销售区域</div>
        <div style="font-size: 20px; font-weight: bold; color: #1e3c72;">{top_region['region']}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            增长{top_region['growth']:+.1%} · {top_region['stores']}家门店
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 第二行：销售趋势和渠道分析
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📈 销售趋势分析")

    # 销售趋势图
    fig_sales = go.Figure()

    # 实际销售额
    fig_sales.add_trace(go.Scatter(
        x=data['dates'],
        y=data['sales'],
        mode='lines+markers',
        name='日销售额',
        line=dict(color='#1e3c72', width=3),
        marker=dict(size=6)
    ))

    # 7日移动平均
    moving_avg = pd.Series(data['sales']).rolling(window=7).mean()
    fig_sales.add_trace(go.Scatter(
        x=data['dates'],
        y=moving_avg,
        mode='lines',
        name='7日移动平均',
        line=dict(color='#10b981', width=2, dash='dash')
    ))

    fig_sales.update_layout(
        height=400,
        plot_bgcolor='white',
        hovermode='x unified',
        xaxis=dict(title='日期', gridcolor='#f0f0f0'),
        yaxis=dict(title='销售额（元）', gridcolor='#f0f0f0', tickformat=',.0f'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.markdown("### 🏪 销售渠道分布")

    # 渠道汇总
    channel_summary = data['df_channels'].groupby('channel').agg({
        'sales': 'sum',
        'orders': 'sum',
        'customers': 'sum'
    }).reset_index()

    # 渠道占比图
    fig_channels = px.pie(
        channel_summary,
        values='sales',
        names='channel',
        color='channel',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )

    fig_channels.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>销售额: ¥%{value:,.0f}<br>占比: %{percent}'
    )

    fig_channels.update_layout(
        height=400,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(fig_channels, use_container_width=True)

    # 渠道效率表
    channel_summary['客单价'] = channel_summary['sales'] / channel_summary['orders']
    channel_summary['转化率'] = channel_summary['orders'] / channel_summary['customers']

    st.dataframe(
        channel_summary.sort_values('sales', ascending=False)[['channel', 'sales', 'orders', '客单价']]
        .rename(columns={'channel': '渠道', 'sales': '销售额', 'orders': '订单数', '客单价': '客单价(元)'})
        .style.format({
            '销售额': '¥{:,.0f}',
            '订单数': '{:,.0f}',
            '客单价(元)': '¥{:,.1f}'
        }).background_gradient(subset=['销售额'], cmap='Blues'),
        use_container_width=True,
        height=200
    )

st.divider()

# 第三行：产品分析和区域分析
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 产品表现分析")

    # 产品销售额排名
    fig_products = px.bar(
        data['df_products'].sort_values('sales', ascending=True).tail(10),
        y='product',
        x='sales',
        orientation='h',
        color='profit_rate',
        color_continuous_scale='Blues',
        labels={'product': '产品', 'sales': '销售额', 'profit_rate': '利润率'},
        hover_data=['growth', 'stock_days']
    )

    fig_products.update_layout(
        height=400,
        xaxis_title="销售额（元）",
        yaxis_title="",
        coloraxis_colorbar=dict(title="利润率"),
        plot_bgcolor='white'
    )

    fig_products.update_traces(
        hovertemplate='<b>%{y}</b><br>销售额: ¥%{x:,.0f}<br>利润率: %{customdata[0]:.1%}<br>增长: %{customdata[1]:+.1%}<br>库存天数: %{customdata[2]}天'
    )

    st.plotly_chart(fig_products, use_container_width=True)

with col2:
    st.markdown("### 🗺️ 区域业绩分析")

    # 区域热力图
    fig_regions = px.bar(
        data['df_regions'].sort_values('sales', ascending=True),
        y='region',
        x='sales',
        orientation='h',
        color='growth',
        color_continuous_scale='RdYlGn',
        range_color=[-0.1, 0.3],
        labels={'region': '区域', 'sales': '销售额', 'growth': '增长率'},
        hover_data=['stores']
    )

    fig_regions.update_layout(
        height=400,
        xaxis_title="销售额（元）",
        yaxis_title="",
        coloraxis_colorbar=dict(title="增长率"),
        plot_bgcolor='white'
    )

    fig_regions.update_traces(
        hovertemplate='<b>%{y}</b><br>销售额: ¥%{x:,.0f}<br>增长: %{customdata[0]:+.1%}<br>门店数: %{customdata[1]}家'
    )

    st.plotly_chart(fig_regions, use_container_width=True)

st.divider()

# 第四行：预测和洞察
st.markdown("### 🔮 销售预测与业务洞察")

col1, col2 = st.columns([2, 1])

with col1:
    # 简单的线性预测
    last_7_days = data['sales'][-7:]
    x = np.arange(len(last_7_days))
    coeffs = np.polyfit(x, last_7_days, 1)

    # 预测未来7天
    future_days = 7
    future_x = np.arange(len(last_7_days), len(last_7_days) + future_days)
    future_sales = coeffs[0] * future_x + coeffs[1]

    # 创建预测图
    fig_forecast = go.Figure()

    # 历史数据
    fig_forecast.add_trace(go.Scatter(
        x=data['dates'][-7:],
        y=last_7_days,
        mode='lines+markers',
        name='历史数据',
        line=dict(color='#1e3c72', width=3)
    ))

    # 预测数据
    future_dates = [data['dates'][-1] + timedelta(days=i + 1) for i in range(future_days)]
    fig_forecast.add_trace(go.Scatter(
        x=future_dates,
        y=future_sales,
        mode='lines+markers',
        name='7日预测',
        line=dict(color='#10b981', width=3, dash='dot'),
        marker=dict(symbol='diamond')
    ))

    fig_forecast.update_layout(
        height=300,
        title="未来7天销售预测",
        xaxis_title="日期",
        yaxis_title="销售额预测（元）",
        plot_bgcolor='white',
        hovermode='x unified'
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

with col2:
    st.markdown("#### 💡 业务洞察")

    insights = [
        {
            "icon": "📱",
            "title": "线上渠道增长迅猛",
            "content": "线上销售额环比增长18%，建议加大数字营销投入",
            "priority": "high"
        },
        {
            "icon": "📦",
            "title": "库存优化机会",
            "content": "3款产品库存周转超过45天，建议促销清仓",
            "priority": "medium"
        },
        {
            "icon": "📍",
            "title": "区域扩张建议",
            "content": "华南市场增长25%，建议新增2家门店",
            "priority": "high"
        },
        {
            "icon": "👥",
            "title": "客户价值提升",
            "content": "企业客户客单价提升12%，建议加强大客户服务",
            "priority": "medium"
        }
    ]

    for insight in insights:
        priority_color = "#ef4444" if insight["priority"] == "high" else "#f59e0b"

        st.markdown(f"""
        <div style="border-left: 4px solid {priority_color}; padding: 10px 15px; margin: 10px 0; background: #f8fafc;">
            <div style="font-size: 16px; font-weight: bold; color: #1e293b;">
                {insight['icon']} {insight['title']}
            </div>
            <div style="font-size: 13px; color: #475569; margin-top: 5px;">
                {insight['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 页脚
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p>📊 智看BI看板系统 | 数据更新时间: {}</p>
    <p>💡 提示：本系统支持多维度数据分析、趋势预测和智能洞察，可定制对接企业ERP、CRM等业务系统</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

# 演示控制台
with st.sidebar:
    st.markdown("### 🎮 演示控制台")

    st.markdown("---")

    st.markdown("#### 数据源配置")
    data_source = st.radio(
        "选择数据源",
        ["模拟数据演示", "连接MySQL数据库", "连接Excel文件", "连接API接口"],
        index=0
    )

    st.markdown("---")

    st.markdown("#### 看板定制")
    show_forecast = st.checkbox("显示销售预测", value=True)
    show_insights = st.checkbox("显示业务洞察", value=True)
    show_details = st.checkbox("显示详细数据", value=False)

    st.markdown("---")

    st.markdown("#### 导出功能")
    if st.button("📥 导出PDF报告"):
        st.success("报告生成中...（演示功能）")

    if st.button("📊 导出Excel数据"):
        st.success("数据导出中...（演示功能）")

    st.markdown("---")

    st.markdown("""
    ### 📱 演示提示

    1. **手机端访问**：本看板完全适配手机屏幕
    2. **实时刷新**：数据每5分钟自动更新
    3. **权限控制**：支持多角色权限管理
    4. **系统对接**：可对接企业现有业务系统

    **演示完毕？** 点击下方按钮联系定制
    """)

    if st.button("📞 联系方案定制15936507515", type="primary", use_container_width=True):
        st.info("功能演示完成！可基于此框架为企业定制专属BI系统")
