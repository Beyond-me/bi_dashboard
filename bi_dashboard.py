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
    page_title="智造通 - 汽车管路供应商BI看板",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# 汽车行业专业样式
st.markdown("""
<style>
    /* 汽车行业主题色 - 工业蓝 */
    .main-header {
        background: linear-gradient(90deg, #0c2461 0%, #1e3799 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .client-card {
        background: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid;
    }

    .byd { border-left-color: #ff6b6b; }
    .geely { border-left-color: #1dd1a1; }
    .nissan { border-left-color: #54a0ff; }
    .dongfeng { border-left-color: #5f27cd; }
    .saic { border-left-color: #feca57; }

    /* 质量指标样式 */
    .quality-good { color: #10b981; font-weight: bold; }
    .quality-warning { color: #f59e0b; font-weight: bold; }
    .quality-bad { color: #ef4444; font-weight: bold; }

    /* 生产状态 */
    .status-on-time { background: #d1fae5; color: #065f46; padding: 3px 8px; border-radius: 12px; }
    .status-delay { background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; }
    .status-urgent { background: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 12px; }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #0c2461 0%, #1e3799 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(12, 36, 97, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# 生成汽车管路行业模拟数据
def generate_auto_parts_data():
    """生成汽车管路供应商模拟数据"""
    np.random.seed(2026)

    # 主机厂客户
    clients = ['比亚迪', '吉利', '郑州日产', '东风日产', '上汽荣威', '长城', '奇瑞', '长安']
    client_colors = {
        '比亚迪': '#ff6b6b', '吉利': '#1dd1a1', '郑州日产': '#54a0ff',
        '东风日产': '#5f27cd', '上汽荣威': '#feca57', '长城': '#00d2d3',
        '奇瑞': '#ff9ff3', '长安': '#c8d6e5'
    }

    # 产品类型
    product_types = ['制动管', '离合管', '空调管', '油管', '涡轮管', '真空管', '水管', '回油管']

    # 材料类型
    materials = ['尼龙管', '橡胶管', '金属管', '复合材料管', '硅胶管']

    # 生成月度销售数据
    months = pd.date_range(start='2025-01-01', end='2025-12-01', freq='MS')

    data = []
    for month in months:
        for client in clients:
            for product in product_types[:4]:  # 主要产品
                # 基础销量
                base_qty = np.random.randint(5000, 30000)
                # 季节性波动
                seasonal_factor = 1 + 0.2 * np.sin((month.month - 1) * np.pi / 6)
                # 客户偏好
                client_factor = np.random.uniform(0.8, 1.5)

                monthly_qty = int(base_qty * seasonal_factor * client_factor)
                unit_price = np.random.uniform(50, 300)  # 单价

                # 不良率（PPM）
                defect_rate = np.random.uniform(50, 500)  # 50-500 PPM

                data.append({
                    'month': month,
                    'client': client,
                    'product': product,
                    'material': np.random.choice(materials),
                    'quantity': monthly_qty,
                    'sales': monthly_qty * unit_price,
                    'unit_price': unit_price,
                    'defect_rate': defect_rate,
                    'on_time_delivery': np.random.uniform(0.85, 0.99)  # 准时交付率
                })

    df = pd.DataFrame(data)

    # 生成生产订单数据
    today = datetime.now()
    orders = []
    order_statuses = ['生产中', '已发货', '待检验', '已完成', '延迟']

    for i in range(50):
        order_date = today - timedelta(days=np.random.randint(1, 60))
        due_date = order_date + timedelta(days=np.random.randint(7, 30))

        orders.append({
            'order_id': f'PO{20260000 + i}',
            'client': np.random.choice(clients),
            'product': np.random.choice(product_types),
            'quantity': np.random.randint(1000, 10000),
            'order_date': order_date,
            'due_date': due_date,
            'status': np.random.choice(order_statuses, p=[0.4, 0.3, 0.1, 0.15, 0.05]),
            'urgency': np.random.choice(['正常', '加急', '特急'], p=[0.7, 0.2, 0.1])
        })

    df_orders = pd.DataFrame(orders)

    # 生成质量检测数据
    quality_data = []
    for product in product_types:
        for _ in range(20):
            quality_data.append({
                'batch_no': f'B{np.random.randint(10000, 99999)}',
                'product': product,
                'inspection_date': today - timedelta(days=np.random.randint(1, 30)),
                'pressure_test': np.random.choice(['合格', '不合格'], p=[0.97, 0.03]),
                'leak_test': np.random.choice(['合格', '不合格'], p=[0.98, 0.02]),
                'dimension_check': np.random.choice(['合格', '不合格'], p=[0.96, 0.04]),
                'overall_result': np.random.choice(['合格', '不合格', '特采'], p=[0.95, 0.03, 0.02])
            })

    df_quality = pd.DataFrame(quality_data)

    return {
        'df_sales': df,
        'df_orders': df_orders,
        'df_quality': df_quality,
        'clients': clients,
        'client_colors': client_colors,
        'products': product_types,
        'materials': materials
    }


# 加载数据
data = generate_auto_parts_data()
df_sales = data['df_sales']
df_orders = data['df_orders']
df_quality = data['df_quality']

# 计算关键指标
current_month = df_sales['month'].max()
current_month_data = df_sales[df_sales['month'] == current_month]

total_sales_current = current_month_data['sales'].sum()
total_sales_prev = df_sales[df_sales['month'] == current_month - pd.DateOffset(months=1)]['sales'].sum()
sales_growth = (total_sales_current - total_sales_prev) / total_sales_prev if total_sales_prev > 0 else 0

total_quantity = current_month_data['quantity'].sum()
avg_defect_rate = current_month_data['defect_rate'].mean()
avg_delivery_rate = current_month_data['on_time_delivery'].mean()

# 主页面
st.markdown("""
<div class="main-header">
    <h1>🚗 智造通 - 汽车管路供应商智能看板</h1>
    <p>为比亚迪、吉利、日产、荣威等主机厂提供专业的供应链数据洞察</p>
</div>
""", unsafe_allow_html=True)

# 时间筛选
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    time_range = st.selectbox("时间范围", ["本月", "本季度", "本年度", "最近12个月"], index=0)
with col2:
    view_by = st.selectbox("分析维度", ["按客户", "按产品", "按材料", "综合视图"], index=0)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 刷新数据"):
        st.rerun()

# 第一行：核心运营指标
st.markdown("### 📈 核心运营指标")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">本月销售额</div>
        <div style="font-size: 28px; font-weight: bold; color: #0c2461;">¥{total_sales_current:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            环比<span class="{'quality-good' if sales_growth > 0 else 'quality-bad'}">{sales_growth:+.1%}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">本月发货量</div>
        <div style="font-size: 28px; font-weight: bold; color: #0c2461;">{total_quantity:,.0f}件</div>
        <div style="font-size: 12px; margin-top: 5px;">
            涉及{len(data['clients'])}家主机厂
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    quality_status = "good" if avg_defect_rate < 100 else "warning" if avg_defect_rate < 300 else "bad"
    status_class = f"quality-{quality_status}"

    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">平均不良率(PPM)</div>
        <div style="font-size: 28px; font-weight: bold; color: #0c2461;">{avg_defect_rate:.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{status_class}">{'优秀' if avg_defect_rate < 100 else '达标' if avg_defect_rate < 300 else '需改善'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    delivery_status = "good" if avg_delivery_rate > 0.95 else "warning" if avg_delivery_rate > 0.90 else "bad"
    status_class = f"quality-{delivery_status}"

    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">准时交付率</div>
        <div style="font-size: 28px; font-weight: bold; color: #0c2461;">{avg_delivery_rate:.1%}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{status_class}">{'优秀' if avg_delivery_rate > 0.95 else '达标' if avg_delivery_rate > 0.90 else '需改善'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 第二行：客户分析和销售趋势
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🏭 客户销售分析")

    # 按客户销售分析
    client_sales = df_sales.groupby('client').agg({
        'sales': 'sum',
        'quantity': 'sum',
        'defect_rate': 'mean',
        'on_time_delivery': 'mean'
    }).reset_index()

    fig_clients = px.bar(
        client_sales.sort_values('sales', ascending=True),
        y='client',
        x='sales',
        orientation='h',
        color='client',
        color_discrete_map=data['client_colors'],
        labels={'client': '客户', 'sales': '销售额'},
        hover_data=['quantity', 'defect_rate', 'on_time_delivery']
    )

    fig_clients.update_layout(
        height=400,
        xaxis_title="累计销售额（元）",
        yaxis_title="",
        showlegend=False,
        plot_bgcolor='white'
    )

    fig_clients.update_traces(
        hovertemplate='<b>%{y}</b><br>销售额: ¥%{x:,.0f}<br>数量: %{customdata[0]:,.0f}件<br>不良率: %{customdata[1]:.0f}PPM<br>交付率: %{customdata[2]:.1%}'
    )

    st.plotly_chart(fig_clients, use_container_width=True)

with col2:
    st.markdown("### 📦 产品结构分析")

    # 产品销量分布
    product_sales = df_sales.groupby('product').agg({
        'sales': 'sum',
        'quantity': 'sum'
    }).reset_index()

    fig_products = px.pie(
        product_sales,
        values='sales',
        names='product',
        color='product',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )

    fig_products.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>销售额: ¥%{value:,.0f}<br>占比: %{percent}'
    )

    fig_products.update_layout(
        height=400,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(fig_products, use_container_width=True)

    # 产品利润率（模拟）
    product_sales['profit_margin'] = np.random.uniform(0.15, 0.35, len(product_sales))
    product_sales['profit'] = product_sales['sales'] * product_sales['profit_margin']

    st.dataframe(
        product_sales[['product', 'quantity', 'sales', 'profit_margin']]
        .rename(columns={'product': '产品', 'quantity': '销量', 'sales': '销售额', 'profit_margin': '毛利率'})
        .sort_values('销售额', ascending=False)
        .head(6)
        .style.format({
            '销量': '{:,.0f}',
            '销售额': '¥{:,.0f}',
            '毛利率': '{:.1%}'
        }),
        use_container_width=True,
        height=200
    )

st.divider()

# 第三行：生产订单和质量监控
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏗️ 生产订单监控")

    # 订单状态统计
    order_status = df_orders['status'].value_counts().reset_index()
    order_status.columns = ['status', 'count']

    fig_orders = px.bar(
        order_status,
        x='status',
        y='count',
        color='status',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'status': '订单状态', 'count': '订单数量'}
    )

    fig_orders.update_layout(
        height=300,
        xaxis_title="",
        yaxis_title="订单数量",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_orders, use_container_width=True)

    # 紧急订单列表
    st.markdown("##### ⚡ 紧急订单清单")
    urgent_orders = df_orders[df_orders['urgency'].isin(['加急', '特急'])]

    if not urgent_orders.empty:
        for _, order in urgent_orders.head(5).iterrows():
            status_class = f"status-{'urgent' if order['urgency'] == '特急' else 'delay'}"
            st.markdown(f"""
            <div class="client-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{order['order_id']}</strong> - {order['client']}
                        <div style="font-size: 12px; color: #666;">{order['product']} × {order['quantity']:,}件</div>
                    </div>
                    <span class="{status_class}">{order['urgency']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无紧急订单")

with col2:
    st.markdown("### ✅ 质量检测看板")

    # 质量合格率
    quality_summary = df_quality['overall_result'].value_counts().reset_index()
    quality_summary.columns = ['result', 'count']

    fig_quality = px.pie(
        quality_summary,
        values='count',
        names='result',
        color='result',
        color_discrete_map={'合格': '#10b981', '不合格': '#ef4444', '特采': '#f59e0b'},
        hole=0.5
    )

    fig_quality.update_layout(
        height=300,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
    )

    st.plotly_chart(fig_quality, use_container_width=True)

    # 不良项分析
    st.markdown("##### 🔍 不良项分布")

    defect_analysis = pd.DataFrame({
        'test_type': ['压力测试', '泄漏测试', '尺寸检测'],
        'pass_rate': [
            (df_quality['pressure_test'] == '合格').mean(),
            (df_quality['leak_test'] == '合格').mean(),
            (df_quality['dimension_check'] == '合格').mean()
        ],
        'defect_count': [
            (df_quality['pressure_test'] == '不合格').sum(),
            (df_quality['leak_test'] == '不合格').sum(),
            (df_quality['dimension_check'] == '不合格').sum()
        ]
    })

    fig_defect = px.bar(
        defect_analysis,
        x='test_type',
        y='pass_rate',
        color='test_type',
        labels={'test_type': '测试项目', 'pass_rate': '合格率'},
        hover_data=['defect_count']
    )

    fig_defect.update_layout(
        height=200,
        xaxis_title="",
        yaxis_title="合格率",
        yaxis_tickformat=',.0%',
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(fig_defect, use_container_width=True)

st.divider()

# 第四行：客户详细视图和供应链洞察
st.markdown("### 🎯 客户绩效看板")

# 按客户显示详细卡片
st.markdown("#### 客户绩效评分")

clients_performance = []
for client in data['clients'][:6]:  # 显示前6个主要客户
    client_data = df_sales[df_sales['client'] == client]

    if not client_data.empty:
        sales_total = client_data['sales'].sum()
        defect_avg = client_data['defect_rate'].mean()
        delivery_avg = client_data['on_time_delivery'].mean()

        # 计算综合评分
        defect_score = 100 - (defect_avg / 10)  # 不良率越低分越高
        delivery_score = delivery_avg * 100
        sales_score = min(100, sales_total / 1000000)  # 每100万得1分

        total_score = (defect_score + delivery_score + sales_score) / 3

        clients_performance.append({
            'client': client,
            'sales': sales_total,
            'defect_rate': defect_avg,
            'delivery_rate': delivery_avg,
            'score': total_score
        })

# 显示客户卡片
cols = st.columns(3)
for idx, perf in enumerate(clients_performance):
    with cols[idx % 3]:
        client_class = perf['client'].replace(' ', '').lower()

        st.markdown(f"""
        <div class="client-card {client_class}">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h4 style="margin: 0 0 10px 0;">{perf['client']}</h4>
                    <div style="font-size: 24px; font-weight: bold; color: #0c2461;">
                        {perf['score']:.0f}分
                    </div>
                </div>
                <div style="font-size: 12px; text-align: right;">
                    <div>销售额: ¥{perf['sales']:,.0f}</div>
                    <div>不良率: {perf['defect_rate']:.0f}PPM</div>
                    <div>交付率: {perf['delivery_rate']:.1%}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 供应链洞察
st.markdown("### 💡 供应链优化建议")

insights = [
    {
        "icon": "🚗",
        "title": "比亚迪订单增长25%",
        "content": "制动管需求显著增加，建议提前备料尼龙管原料",
        "action": "查看采购建议"
    },
    {
        "icon": "⚙️",
        "title": "空调管不良率偏高",
        "content": "近期空调管泄漏测试不合格率上升至2.1%，需检查密封工艺",
        "action": "启动质量改善"
    },
    {
        "icon": "📦",
        "title": "吉利紧急订单增加",
        "content": "吉利加急订单占比从15%升至28%，建议设立专用生产线",
        "action": "优化排产计划"
    },
    {
        "icon": "💰",
        "title": "橡胶管利润率提升",
        "content": "橡胶管毛利率达32%，高于平均28%，可适当增加产能",
        "action": "调整产品结构"
    }
]

cols = st.columns(2)
for idx, insight in enumerate(insights):
    with cols[idx % 2]:
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #0c2461;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 10px;">{insight['icon']}</span>
                <strong>{insight['title']}</strong>
            </div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 10px;">
                {insight['content']}
            </div>
            <button style="background: #0c2461; color: white; border: none; padding: 5px 15px; border-radius: 4px; font-size: 12px; cursor: pointer;">
                {insight['action']}
            </button>
        </div>
        """, unsafe_allow_html=True)

# 页脚
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p>🚗 智造通汽车零部件供应商BI系统 | 数据更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <p>💡 本系统已对接：SAP ERP | MES生产系统 | QMS质量系统 | WMS仓储系统</p>
    <p>📞 技术支持：400-800-汽车供应链 | www.auto-parts-bi.com</p>
</div>
""", unsafe_allow_html=True)

# 演示控制台
with st.sidebar:
    st.markdown("### 🎮 演示控制台")

    st.markdown("---")

    st.markdown("#### 系统对接")
    connected_systems = st.multiselect(
        "已对接系统",
        ["SAP ERP", "MES生产执行", "QMS质量管理", "WMS仓储管理", "SRM供应商管理", "CRM客户关系"],
        default=["SAP ERP", "MES生产执行", "QMS质量管理"]
    )

    st.markdown("---")

    st.markdown("#### 预警设置")
    defect_threshold = st.slider("不良率预警阈值(PPM)", 50, 500, 200)
    delivery_threshold = st.slider("交付率预警阈值", 0.8, 1.0, 0.92)

    st.markdown("---")

    st.markdown("#### 数据导出")
    if st.button("📥 生成客户报告", use_container_width=True):
        st.success("报告生成中... 包含客户绩效、质量分析、交付记录")

    if st.button("📊 导出生产数据", use_container_width=True):
        st.success("导出近30天生产订单、质量检测数据")

    st.markdown("---")

    st.markdown("""
    ### 📱 应用场景

    **生产总监**：监控生产进度、质量指标
    **销售经理**：分析客户贡献、产品利润
    **质量经理**：跟踪不良率、改进措施
    **供应链**：优化库存、提高交付率

    **演示完毕？** 联系我们定制专属版本
    """)

    if st.button("📞 获取定制方案15936507515", type="primary", use_container_width=True):
        st.success("已收到您的需求，客户经理将在1小时内联系您！")
