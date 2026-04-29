# -*- coding: utf-8 -*-
# @Time    : 2026/4/29 11:57
# @Author  : lihaizhen
# @File    : aite_bi_dashboard.py
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
    page_title="艾特环保BI看板 - 过滤设备行业数据分析",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隐藏streamlit默认样式
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.viewerBadge_container__1QSob {display: none;}
.st-emotion-cache-1q1n0ol {background: linear-gradient(90deg, #2e7d32 0%, #388e3c 100%);}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 环保行业专业样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2e7d32 0%, #388e3c 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-top: 4px solid;
        margin-bottom: 15px;
    }

    .metric-sales { border-top-color: #4caf50; }
    .metric-orders { border-top-color: #2196f3; }
    .metric-margin { border-top-color: #ff9800; }
    .metric-growth { border-top-color: #9c27b0; }

    .positive { color: #4caf50; font-weight: bold; }
    .negative { color: #f44336; font-weight: bold; }

    /* 紧凑布局 */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)


# 生成过滤设备行业模拟数据
def generate_filter_data():
    """生成过滤设备行业模拟数据"""
    np.random.seed(2026)

    # 客户行业分类
    industries = ['电力', '化工', '食品饮料', '制药', '电子半导体', '水处理', '石油化工', '钢铁冶金']
    industry_colors = {
        '电力': '#4caf50', '化工': '#2196f3', '食品饮料': '#ff9800',
        '制药': '#9c27b0', '电子半导体': '#00bcd4', '水处理': '#ffc107',
        '石油化工': '#795548', '钢铁冶金': '#607d8b'
    }

    # 产品类型
    product_categories = ['过滤器', '滤芯', '超滤膜', '反渗透膜', '过滤材料', '配件']
    product_subcategories = {
        '过滤器': ['袋式过滤器', '芯式过滤器', '板式过滤器', '筒式过滤器'],
        '滤芯': ['折叠滤芯', '熔喷滤芯', '线绕滤芯', '活性炭滤芯'],
        '超滤膜': ['中空纤维膜', '管式超滤膜', '平板膜', '陶瓷膜'],
        '反渗透膜': ['芳香族聚酰胺膜', '醋酸纤维素膜', '薄层复合膜'],
        '过滤材料': ['滤布', '滤纸', '金属烧结网', '多孔陶瓷'],
        '配件': ['阀门', '管道', '密封圈', '压力表']
    }

    # 客户等级
    customer_tiers = ['VIP客户', '重点客户', '普通客户']

    # 生成销售数据 (过去12个月)
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    sales_data = []

    for month in months:
        for industry in industries:
            base_sales = np.random.uniform(100000, 500000)
            industry_factor = np.random.uniform(0.8, 1.5)
            seasonal_factor = 1 + 0.2 * np.sin((month.month - 1) * 2 * np.pi / 12)

            monthly_sales = base_sales * industry_factor * seasonal_factor

            sales_data.append({
                'month': month,
                'industry': industry,
                'sales_amount': monthly_sales,
                'orders_count': int(np.random.poisson(20 * industry_factor)),
                'new_customers': int(np.random.poisson(3 * industry_factor))
            })

    df_sales = pd.DataFrame(sales_data)

    # 生成产品数据
    product_data = []
    for category, subcategories in product_subcategories.items():
        for subcategory in subcategories:
            if '膜' in subcategory:
                avg_price = np.random.uniform(5000, 20000)
                monthly_sales = np.random.uniform(10, 50)
            elif '滤芯' in subcategory:
                avg_price = np.random.uniform(500, 2000)
                monthly_sales = np.random.uniform(100, 500)
            else:
                avg_price = np.random.uniform(1000, 10000)
                monthly_sales = np.random.uniform(50, 200)

            product_data.append({
                'category': category,
                'subcategory': subcategory,
                'avg_price': avg_price,
                'monthly_sales': monthly_sales,
                'total_revenue': avg_price * monthly_sales * 12,
                'gross_margin': np.random.uniform(0.3, 0.6),
                'inventory_turnover': np.random.uniform(4, 12)
            })

    df_products = pd.DataFrame(product_data)

    # 生成客户数据
    customers = []
    customer_names = [f"{industry}客户{i}" for industry in industries for i in range(1, 6)]

    for customer_name in customer_names:
        industry = customer_name.split('客户')[0]
        tier = np.random.choice(customer_tiers, p=[0.1, 0.3, 0.6])

        if tier == 'VIP客户':
            annual_purchase = np.random.uniform(1000000, 5000000)
        elif tier == '重点客户':
            annual_purchase = np.random.uniform(300000, 1000000)
        else:
            annual_purchase = np.random.uniform(50000, 300000)

        customers.append({
            'customer_name': customer_name,
            'industry': industry,
            'tier': tier,
            'annual_purchase': annual_purchase,
            'orders_count': int(np.random.poisson(annual_purchase / 100000)),
        })

    df_customers = pd.DataFrame(customers)

    # 生成库存数据
    inventory_data = []
    for category, subcategories in product_subcategories.items():
        for subcategory in subcategories:
            if '膜' in subcategory:
                safety_stock = np.random.randint(5, 20)
                current_stock = np.random.randint(10, 50)
            elif '滤芯' in subcategory:
                safety_stock = np.random.randint(100, 500)
                current_stock = np.random.randint(200, 1000)
            else:
                safety_stock = np.random.randint(50, 200)
                current_stock = np.random.randint(100, 500)

            inventory_data.append({
                'category': category,
                'subcategory': subcategory,
                'current_stock': current_stock,
                'safety_stock': safety_stock,
                'stock_status': '充足' if current_stock > safety_stock * 1.5 else
                '预警' if current_stock > safety_stock else '短缺'
            })

    df_inventory = pd.DataFrame(inventory_data)

    return {
        'df_sales': df_sales,
        'df_products': df_products,
        'df_customers': df_customers,
        'df_inventory': df_inventory,
        'industries': industries,
        'industry_colors': industry_colors,
        'product_categories': product_categories
    }


# 加载数据
data = generate_filter_data()
df_sales = data['df_sales']
df_products = data['df_products']
df_customers = data['df_customers']
df_inventory = data['df_inventory']

# 计算关键指标
current_year = df_sales[df_sales['month'].dt.year == 2024]
total_annual_sales = current_year['sales_amount'].sum()
total_orders = current_year['orders_count'].sum()
new_customers = current_year['new_customers'].sum()
avg_gross_margin = df_products['gross_margin'].mean()

# 同比增长率
sales_growth = 15.8  # 模拟数据

# 主页面
st.markdown("""
<div class="main-header">
    <h1>🌍 艾特环保BI看板 - 过滤设备行业数据分析</h1>
    <p>专注过滤器、滤芯、超滤膜、反渗透膜等产品的销售与库存管理</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏控制面板
with st.sidebar:
    st.markdown("### 🎛️ 控制面板")

    # 时间范围选择
    time_range = st.selectbox(
        "时间范围",
        ["本月", "本季度", "本年度", "最近12个月"],
        index=2
    )

    # 行业筛选
    industries_selected = st.multiselect(
        "筛选行业",
        data['industries'],
        default=data['industries'][:4]
    )

    # 产品类别筛选
    categories_selected = st.multiselect(
        "筛选产品类别",
        data['product_categories'],
        default=data['product_categories']
    )

    st.divider()

    # 数据显示选项
    show_detailed_data = st.checkbox("显示详细数据表")
    auto_refresh = st.checkbox("自动刷新数据", value=True)

    if st.button("🔄 手动刷新数据"):
        st.rerun()

# 第一行：核心运营指标
st.markdown("### 📈 核心运营指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    growth_color = "positive" if sales_growth > 0 else "negative"
    st.markdown(f"""
    <div class="metric-card metric-sales">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">年度销售额</div>
        <div style="font-size: 28px; font-weight: bold; color: #2e7d32;">¥{total_annual_sales:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            同比<span class="{growth_color}">{sales_growth:+.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-orders">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">年度订单数</div>
        <div style="font-size: 28px; font-weight: bold; color: #1976d2;">{total_orders:,}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            新增客户: {new_customers}家
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    margin_status = "positive" if avg_gross_margin > 0.4 else "negative"
    st.markdown(f"""
    <div class="metric-card metric-margin">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">平均毛利率</div>
        <div style="font-size: 28px; font-weight: bold; color: #ff9800;">{avg_gross_margin:.1%}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{margin_status}">{'优秀' if avg_gross_margin > 0.4 else '良好' if avg_gross_margin > 0.3 else '需提升'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # 库存短缺项统计
    shortage_count = len(df_inventory[df_inventory['stock_status'] == '短缺'])
    warning_count = len(df_inventory[df_inventory['stock_status'] == '预警'])
    inventory_color = "negative" if shortage_count > 5 else "positive" if shortage_count == 0 else ""

    st.markdown(f"""
    <div class="metric-card metric-growth">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">库存状态</div>
        <div style="font-size: 28px; font-weight: bold; color: #7b1fa2;">{shortage_count}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{inventory_color}">短缺项</span> / {warning_count}预警项
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 第二行：销售趋势和行业分析
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📊 月度销售趋势")

    # 按月汇总销售额
    monthly_sales_summary = df_sales.groupby('month')['sales_amount'].sum().reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_sales_summary['month'],
        y=monthly_sales_summary['sales_amount'],
        mode='lines+markers',
        name='月度销售额',
        line=dict(color='#4caf50', width=3),
        marker=dict(size=6)
    ))

    # 添加移动平均线
    monthly_sales_summary['ma3'] = monthly_sales_summary['sales_amount'].rolling(window=3).mean()
    fig_trend.add_trace(go.Scatter(
        x=monthly_sales_summary['month'],
        y=monthly_sales_summary['ma3'],
        mode='lines',
        name='3个月移动平均',
        line=dict(color='#ff9800', width=2, dash='dash')
    ))

    fig_trend.update_layout(
        height=350,
        title="2024年月度销售趋势",
        xaxis_title="月份",
        yaxis_title="销售额（元）",
        plot_bgcolor='white',
        hovermode='x unified',
        yaxis=dict(tickformat=',.0f'),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("### 🏭 客户行业分布")

    # 按行业汇总销售额
    industry_sales = df_sales.groupby('industry')['sales_amount'].sum().reset_index()

    fig_industry = px.pie(
        industry_sales,
        values='sales_amount',
        names='industry',
        color='industry',
        color_discrete_map=data['industry_colors'],
        hole=0.3
    )

    fig_industry.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>销售额: ¥%{value:,.0f}<br>占比: %{percent}'
    )

    fig_industry.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig_industry, use_container_width=True)

st.divider()

# 第三行：产品分析和客户分析
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 产品类别销售分布")

    # 过滤选中的产品类别
    filtered_products = df_products[df_products['category'].isin(categories_selected)]
    category_sales = filtered_products.groupby('category')['total_revenue'].sum().reset_index()

    fig_category = px.bar(
        category_sales.sort_values('total_revenue', ascending=True),
        y='category',
        x='total_revenue',
        orientation='h',
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'category': '产品类别', 'total_revenue': '年销售额'}
    )

    fig_category.update_layout(
        height=300,
        xaxis_title="年销售额（元）",
        yaxis_title="",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_category, use_container_width=True)

    # 畅销产品TOP5
    st.markdown("##### 🏆 畅销产品TOP5")

    top_products = df_products.nlargest(5, 'total_revenue')

    for _, product in top_products.iterrows():
        with st.container(border=True):
            cols = st.columns([3, 2])
            with cols[0]:
                st.write(f"**{product['subcategory']}**")
                st.caption(f"{product['category']}")
            with cols[1]:
                st.metric("年销售额", f"¥{product['total_revenue']:,.0f}")
                st.caption(f"毛利率: {product['gross_margin']:.1%}")

with col2:
    st.markdown("### 👥 客户等级分析")

    # 客户等级分布
    tier_dist = df_customers['tier'].value_counts().reset_index()
    tier_dist.columns = ['tier', 'count']

    fig_tier = px.bar(
        tier_dist,
        x='tier',
        y='count',
        color='tier',
        color_discrete_map={'VIP客户': '#7b1fa2', '重点客户': '#1976d2', '普通客户': '#388e3c'},
        labels={'tier': '客户等级', 'count': '客户数量'}
    )

    fig_tier.update_layout(
        height=300,
        xaxis_title="",
        yaxis_title="客户数量",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_tier, use_container_width=True)

    # VIP客户列表
    st.markdown("##### 🌟 VIP客户列表")

    vip_customers = df_customers[df_customers['tier'] == 'VIP客户'].sort_values('annual_purchase', ascending=False)

    for _, customer in vip_customers.head(3).iterrows():
        with st.container(border=True):
            st.write(f"**{customer['customer_name']}**")
            st.caption(f"{customer['industry']}行业")

            cols = st.columns(2)
            with cols[0]:
                st.metric("年采购额", f"¥{customer['annual_purchase']:,.0f}")
            with cols[1]:
                st.metric("订单数", customer['orders_count'])

st.divider()

# 第四行：库存状态
st.markdown("### 📦 库存状态监控")

# 库存预警列表
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    st.markdown("##### ⚠️ 库存短缺")
    shortage_items = df_inventory[df_inventory['stock_status'] == '短缺']

    if not shortage_items.empty:
        for _, item in shortage_items.iterrows():
            st.error(f"**{item['subcategory']}**\n当前: {item['current_stock']} | 安全: {item['safety_stock']}")
    else:
        st.success("✅ 暂无短缺产品")

with col2:
    st.markdown("##### ⚠️ 库存预警")
    warning_items = df_inventory[df_inventory['stock_status'] == '预警']

    if not warning_items.empty:
        for _, item in warning_items.head(5).iterrows():
            st.warning(f"**{item['subcategory']}**\n当前: {item['current_stock']} | 安全: {item['safety_stock']}")
    else:
        st.info("暂无预警产品")

with col3:
    st.markdown("##### 🔄 库存周转分析")

    # 库存周转率
    turnover_analysis = df_products[['category', 'subcategory', 'inventory_turnover']].head(8)

    fig_turnover = px.bar(
        turnover_analysis,
        x='inventory_turnover',
        y='subcategory',
        orientation='h',
        color='category',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'inventory_turnover': '年周转次数', 'subcategory': '产品'}
    )

    fig_turnover.update_layout(
        height=250,
        xaxis_title="年周转次数",
        yaxis_title="",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_turnover, use_container_width=True)

# 业务洞察
st.markdown("### 💡 业务洞察")

insights = [
    {"icon": "💰", "title": "水处理行业增长迅猛", "content": "水处理行业销售额同比增长28%，建议加大该领域市场投入"},
    {"icon": "🔄", "title": "反渗透膜库存周转快", "content": "反渗透膜年周转率达15次，建议适当增加安全库存"},
    {"icon": "👥", "title": "VIP客户贡献占比高", "content": "前5大VIP客户贡献了42%的销售额，建议加强客户关系维护"},
    {"icon": "📈", "title": "制药行业需求稳定", "content": "制药行业需求持续增长，毛利率达48%，建议深度挖掘"},
]

cols = st.columns(2)
for idx, insight in enumerate(insights):
    with cols[idx % 2]:
        with st.container(border=True):
            st.write(f"**{insight['icon']} {insight['title']}**")
            st.write(insight['content'])

# 详细数据表
if show_detailed_data:
    st.divider()
    st.markdown("### 📊 详细数据表")

    tab1, tab2, tab3 = st.tabs(["销售数据", "客户数据", "库存数据"])

    with tab1:
        st.dataframe(df_sales, use_container_width=True)

    with tab2:
        st.dataframe(df_customers, use_container_width=True)

    with tab3:
        st.dataframe(df_inventory, use_container_width=True)

# 页脚
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p>🌍 艾特环保BI看板系统 | 数据更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <p>💡 本系统支持对接ERP、CRM、WMS等业务系统 | 支持移动端访问</p>
</div>
""", unsafe_allow_html=True)
