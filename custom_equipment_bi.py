# -*- coding: utf-8 -*-
# @Time    : 2026/4/28 18:26
# @Author  : lihaizhen
# @File    : custom_equipment_bi.py
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
    page_title="智造云 - 非标设备供应商BI看板",
    page_icon="⚙️",
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

# 工业设备主题样式
st.markdown("""
<style>
    /* 工业主题色 - 深灰+科技蓝 */
    .main-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .project-card {
        background: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid;
    }

    /* 项目状态颜色 */
    .status-design { border-left-color: #3498db; }
    .status-manufacturing { border-left-color: #f39c12; }
    .status-assembly { border-left-color: #9b59b6; }
    .status-debugging { border-left-color: #e74c3c; }
    .status-acceptance { border-left-color: #2ecc71; }
    .status-completed { border-left-color: #27ae60; }
    .status-delayed { border-left-color: #7f8c8d; }

    /* 进度条样式 */
    .progress-container {
        background: #ecf0f1;
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s;
    }

    /* 风险等级 */
    .risk-low { background: #2ecc71; color: white; padding: 3px 8px; border-radius: 12px; }
    .risk-medium { background: #f39c12; color: white; padding: 3px 8px; border-radius: 12px; }
    .risk-high { background: #e74c3c; color: white; padding: 3px 8px; border-radius: 12px; }

    /* 技术难度 */
    .difficulty-low { color: #27ae60; font-weight: bold; }
    .difficulty-medium { color: #f39c12; font-weight: bold; }
    .difficulty-high { color: #e74c3c; font-weight: bold; }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(44, 62, 80, 0.3);
    }

    /* 指标卡片 */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-top: 4px solid;
        margin-bottom: 15px;
    }

    .metric-sales { border-top-color: #3498db; }
    .metric-projects { border-top-color: #2ecc71; }
    .metric-margin { border-top-color: #9b59b6; }
    .metric-delivery { border-top-color: #f39c12; }
</style>
""", unsafe_allow_html=True)


# 生成非标设备制造行业模拟数据
def generate_custom_equipment_data():
    """生成非标设备制造企业模拟数据"""
    np.random.seed(2026)

    # 行业客户
    industries = ['汽车制造', '消费电子', '新能源电池', '医疗器械', '航空航天', '家电制造', '半导体', '精密仪器']
    industry_colors = {
        '汽车制造': '#e74c3c', '消费电子': '#3498db', '新能源电池': '#2ecc71',
        '医疗器械': '#9b59b6', '航空航天': '#34495e', '家电制造': '#f39c12',
        '半导体': '#1abc9c', '精密仪器': '#e67e22'
    }

    # 设备类型
    equipment_types = [
        '气密检测设备', '压力检测设备', '视觉检测设备', '功能测试设备',
        '泄漏检测设备', '尺寸测量设备', '自动化装配线', '工装夹具',
        '老化测试设备', '性能测试台', '机器人工作站', '智能检测线'
    ]

    # 项目状态
    project_statuses = ['方案设计', '详细设计', '采购中', '加工制造', '装配调试', '客户验收', '已交付', '项目延期']

    # 生成项目数据
    today = datetime.now()
    projects = []

    for i in range(25):
        # 项目基础信息
        project_id = f'PJ{2026000 + i}'
        client_industry = np.random.choice(industries)
        equipment_type = np.random.choice(equipment_types)

        # 项目时间线
        start_date = today - timedelta(days=np.random.randint(30, 180))
        planned_duration = np.random.randint(60, 180)  # 计划工期60-180天
        planned_end = start_date + timedelta(days=planned_duration)

        # 实际进度
        status = np.random.choice(project_statuses)
        status_index = project_statuses.index(status)
        progress = min(100, (status_index + 1) * 12.5 + np.random.uniform(-10, 10))

        # 可能会有延期
        is_delayed = np.random.random() < 0.2
        if is_delayed and status in ['加工制造', '装配调试', '客户验收']:
            actual_end = planned_end + timedelta(days=np.random.randint(15, 60))
            delay_days = (actual_end - planned_end).days
        else:
            actual_end = planned_end
            delay_days = 0

        # 项目金额和利润
        contract_value = np.random.uniform(200000, 2000000)
        cost_rate = np.random.uniform(0.6, 0.85)
        gross_margin = 1 - cost_rate

        # 技术难度评估
        difficulty = np.random.choice(['低', '中', '高'], p=[0.3, 0.5, 0.2])

        # 项目风险
        if delay_days > 30 or difficulty == '高':
            risk_level = '高'
        elif delay_days > 15 or difficulty == '中':
            risk_level = '中'
        else:
            risk_level = '低'

        projects.append({
            'project_id': project_id,
            'project_name': f'{client_industry}{equipment_type}项目',
            'client': f'{client_industry}客户{np.random.randint(1, 10)}',
            'industry': client_industry,
            'equipment_type': equipment_type,
            'contract_value': contract_value,
            'gross_margin': gross_margin,
            'start_date': start_date,
            'planned_end': planned_end,
            'actual_end': actual_end if status == '已交付' else None,
            'status': status,
            'progress': progress,
            'difficulty': difficulty,
            'risk_level': risk_level,
            'delay_days': delay_days,
            'project_manager': f'PM{np.random.randint(1, 6)}',
            'current_phase_days': np.random.randint(5, 30)
        })

    df_projects = pd.DataFrame(projects)

    # 生成月度销售数据
    months = pd.date_range(start='2024-01-01', end='2025-12-01', freq='MS')
    monthly_sales = []

    for month in months:
        for industry in industries[:4]:  # 主要行业
            monthly_value = np.random.uniform(500000, 2000000)
            monthly_cost = monthly_value * np.random.uniform(0.65, 0.8)

            monthly_sales.append({
                'month': month,
                'industry': industry,
                'sales_value': monthly_value,
                'cost': monthly_cost,
                'gross_profit': monthly_value - monthly_cost,
                'projects_count': np.random.randint(2, 8)
            })

    df_monthly = pd.DataFrame(monthly_sales)

    # 生成资源使用数据
    resources = ['机械设计', '电气设计', '软件编程', '装配调试', '采购', '项目管理']
    resource_usage = []

    for resource in resources:
        resource_usage.append({
            'resource': resource,
            'utilization': np.random.uniform(0.6, 0.95),  # 资源利用率
            'workload': np.random.uniform(0.7, 1.2),  # 工作量负荷
            'critical_level': np.random.choice(['高', '中', '低'], p=[0.3, 0.4, 0.3])
        })

    df_resources = pd.DataFrame(resource_usage)

    # 生成问题追踪数据
    issues = []
    issue_types = ['设计变更', '采购延迟', '加工问题', '装配困难', '调试故障', '客户需求变更', '文档缺失']

    for _ in range(15):
        issue_date = today - timedelta(days=np.random.randint(1, 60))
        resolve_days = np.random.randint(1, 15) if np.random.random() > 0.3 else None

        issues.append({
            'issue_id': f'IS{np.random.randint(1000, 9999)}',
            'project_id': np.random.choice(df_projects['project_id'].tolist()),
            'issue_type': np.random.choice(issue_types),
            'severity': np.random.choice(['低', '中', '高'], p=[0.5, 0.3, 0.2]),
            'create_date': issue_date,
            'resolve_date': issue_date + timedelta(days=resolve_days) if resolve_days else None,
            'status': '已解决' if resolve_days else '处理中',
            'impact_days': np.random.randint(1, 7) if resolve_days else None
        })

    df_issues = pd.DataFrame(issues)

    return {
        'df_projects': df_projects,
        'df_monthly': df_monthly,
        'df_resources': df_resources,
        'df_issues': df_issues,
        'industries': industries,
        'industry_colors': industry_colors,
        'equipment_types': equipment_types,
        'project_statuses': project_statuses
    }


# 加载数据
data = generate_custom_equipment_data()
df_projects = data['df_projects']
df_monthly = data['df_monthly']

# 计算关键指标
current_year_data = df_monthly[df_monthly['month'].dt.year == 2025]
current_month_data = df_monthly[df_monthly['month'] == df_monthly['month'].max()]

total_contract_value = df_projects['contract_value'].sum()
total_projects = len(df_projects)
avg_gross_margin = df_projects['gross_margin'].mean()

# 进行中项目
active_projects = df_projects[~df_projects['status'].isin(['已交付', '项目延期'])]
active_project_value = active_projects['contract_value'].sum()
delayed_projects = df_projects[df_projects['status'] == '项目延期']

# 计算交付准时率
delivered_projects = df_projects[df_projects['status'] == '已交付']
if not delivered_projects.empty:
    on_time_delivery = (delivered_projects['delay_days'] == 0).mean()
else:
    on_time_delivery = 0

# 主页面
st.markdown("""
<div class="main-header">
    <h1>⚙️ 智造云 - 非标设备制造BI看板</h1>
    <p>为气密检测、压力测试、自动化设备供应商提供全流程项目管理与数据分析</p>
</div>
""", unsafe_allow_html=True)

# 时间筛选
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    time_range = st.selectbox("时间范围", ["本月", "本季度", "本年度", "所有项目"], index=2)
with col2:
    view_by = st.selectbox("分析维度", ["按行业", "按设备类型", "按项目状态", "综合视图"], index=0)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 刷新数据"):
        st.rerun()

# 第一行：核心运营指标
st.markdown("### 📈 核心运营指标")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-sales">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">在执合同总额</div>
        <div style="font-size: 28px; font-weight: bold; color: #2c3e50;">¥{total_contract_value:,.0f}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            {total_projects}个项目执行中
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-projects">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">进行中项目</div>
        <div style="font-size: 28px; font-weight: bold; color: #2c3e50;">{len(active_projects)}个</div>
        <div style="font-size: 12px; margin-top: 5px;">
            合同额 ¥{active_project_value:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    margin_class = "difficulty-low" if avg_gross_margin > 0.3 else "difficulty-medium" if avg_gross_margin > 0.2 else "difficulty-high"

    st.markdown(f"""
    <div class="metric-card metric-margin">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">平均毛利率</div>
        <div style="font-size: 28px; font-weight: bold; color: #2c3e50;">{avg_gross_margin:.1%}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{margin_class}">{'优秀' if avg_gross_margin > 0.3 else '良好' if avg_gross_margin > 0.2 else '需提升'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    delivery_class = "difficulty-low" if on_time_delivery > 0.85 else "difficulty-medium" if on_time_delivery > 0.7 else "difficulty-high"

    st.markdown(f"""
    <div class="metric-card metric-delivery">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">准时交付率</div>
        <div style="font-size: 28px; font-weight: bold; color: #2c3e50;">{on_time_delivery:.0%}</div>
        <div style="font-size: 12px; margin-top: 5px;">
            <span class="{delivery_class}">{len(delayed_projects)}个项目延期</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 第二行：项目概览和行业分析
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📊 项目状态概览")

    # 项目状态分布
    status_dist = df_projects['status'].value_counts().reset_index()
    status_dist.columns = ['status', 'count']

    fig_status = px.bar(
        status_dist,
        x='status',
        y='count',
        color='status',
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'status': '项目状态', 'count': '项目数量'}
    )

    fig_status.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="项目数量",
        plot_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    st.markdown("### 🏭 行业分布分析")

    # 按行业合同额分布
    industry_sales = df_projects.groupby('industry').agg({
        'contract_value': 'sum',
        'project_id': 'count'
    }).reset_index()

    fig_industry = px.pie(
        industry_sales,
        values='contract_value',
        names='industry',
        color='industry',
        color_discrete_map=data['industry_colors'],
        hole=0.4
    )

    fig_industry.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>合同额: ¥%{value:,.0f}<br>项目数: %{customdata[0]}个'
    )

    fig_industry.update_layout(
        height=400,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(fig_industry, use_container_width=True)

    # 行业项目数量
    st.dataframe(
        industry_sales.rename(columns={
            'industry': '行业',
            'contract_value': '合同额',
            'project_id': '项目数'
        }).sort_values('合同额', ascending=False)
        .head(5)
        .style.format({
            '合同额': '¥{:,.0f}',
            '项目数': '{:,.0f}'
        }),
        use_container_width=True,
        height=200
    )

st.divider()

# 第三行：项目列表和资源分析
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 重点项目监控")

    # 高风险项目筛选
    high_risk_projects = df_projects[df_projects['risk_level'] == '高'].sort_values('contract_value', ascending=False)

    if not high_risk_projects.empty:
        # 使用紧凑的项目卡片容器
        projects_container = st.container()

        with projects_container:
            for idx, (_, project) in enumerate(high_risk_projects.head(3).iterrows()):
                # 使用紧凑的卡片布局
                with st.container(border=True):  # 使用border参数创建有边界的容器
                    # 顶部：项目ID和名称
                    title_cols = st.columns([4, 1])
                    with title_cols[0]:
                        st.markdown(f"**⚠️ {project['project_id']} - {project['project_name']}**")
                    with title_cols[1]:
                        st.error("高风险", help="高风险项目需重点监控")

                    # 项目信息
                    st.caption(f"{project['industry']} · {project['equipment_type']} · {project['project_manager']}")

                    # 进度条 - 更紧凑
                    progress_cols = st.columns([1, 4])
                    with progress_cols[0]:
                        st.metric("进度", f"{project['progress']:.0f}%", delta=None)
                    with progress_cols[1]:
                        st.progress(project['progress'] / 100, text="")

                    # 底部指标 - 紧凑排列
                    metric_cols = st.columns(3)
                    with metric_cols[0]:
                        st.metric("合同额", f"¥{project['contract_value']:,.0f}", delta=None, help="项目合同金额")
                    with metric_cols[1]:
                        difficulty = project['difficulty']
                        if difficulty == "高":
                            st.metric("难度", "高", delta=None, help="项目技术难度")
                        elif difficulty == "中":
                            st.metric("难度", "中", delta=None, help="项目技术难度")
                        else:
                            st.metric("难度", "低", delta=None, help="项目技术难度")
                    with metric_cols[2]:
                        delay = project['delay_days']
                        if delay > 0:
                            st.metric("延期", f"{delay}天", delta=None, help="项目延期天数")
                        else:
                            st.metric("状态", "按时", delta=None, help="项目交付状态")

                    # 如果不是最后一个项目，添加分隔线
                    if idx < min(2, len(high_risk_projects.head(3)) - 1):
                        st.divider()
    else:
        st.info("暂无高风险项目")

    # 设备类型分布 - 调整高度，更紧凑
    st.markdown("##### ⚙️ 设备类型分布")
    equipment_dist = df_projects['equipment_type'].value_counts().reset_index()
    equipment_dist.columns = ['equipment_type', 'count']

    fig_equipment = px.bar(
        equipment_dist.head(8),
        x='count',
        y='equipment_type',
        orientation='h',
        color='equipment_type',
        color_discrete_sequence=px.colors.sequential.Greys_r
    )

    fig_equipment.update_layout(
        height=200,  # 减少高度
        xaxis_title="项目数量",
        yaxis_title="",
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0, pad=0)  # 减少边距
    )

    st.plotly_chart(fig_equipment, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("### 👥 资源负荷分析")

    # 资源利用率图表 - 调整高度
    fig_resources = px.bar(
        data['df_resources'],
        x='resource',
        y='utilization',
        color='critical_level',
        color_discrete_map={'高': '#e74c3c', '中': '#f39c12', '低': '#2ecc71'},
        labels={'resource': '资源类型', 'utilization': '利用率', 'critical_level': '关键程度'},
        hover_data=['workload']
    )

    fig_resources.update_layout(
        height=220,  # 减少高度
        xaxis_title="",
        yaxis_title="资源利用率",
        yaxis_tickformat=',.0%',
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=0, b=0, pad=0)  # 减少边距
    )

    st.plotly_chart(fig_resources, use_container_width=True, config={'displayModeBar': False})

    # 问题追踪 - 使用Streamlit组件替代HTML
    st.markdown("##### 🔧 问题追踪")

    active_issues = data['df_issues'][data['df_issues']['status'] == '处理中']

    if not active_issues.empty:
        issues_container = st.container()

        with issues_container:
            for idx, (_, issue) in enumerate(active_issues.head(3).iterrows()):
                # 使用Streamlit组件创建问题卡片
                with st.container(border=True):
                    # 问题标题和严重程度
                    issue_cols = st.columns([3, 1])
                    with issue_cols[0]:
                        st.markdown(f"**{issue['issue_id']}**")
                        st.caption(f"{issue['issue_type']} · {issue['project_id']}")
                    with issue_cols[1]:
                        severity = issue['severity']
                        if severity == '高':
                            st.error(f"{severity}级")
                        elif severity == '中':
                            st.warning(f"{severity}级")
                        else:
                            st.success(f"{severity}级")

                    # 创建时间
                    st.caption(f"创建: {issue['create_date'].strftime('%m-%d')} · 处理中")

                    # 如果不是最后一个问题，添加分隔线
                    if idx < min(2, len(active_issues.head(3)) - 1):
                        st.divider()
    else:
        st.success("✅ 暂无待处理问题")

st.divider()

# 第四行：财务分析和项目健康度
st.markdown("### 💰 财务趋势分析")

# 月度销售趋势
monthly_trend = df_monthly.groupby('month').agg({
    'sales_value': 'sum',
    'gross_profit': 'sum',
    'projects_count': 'sum'
}).reset_index()

fig_monthly = go.Figure()

fig_monthly.add_trace(go.Scatter(
    x=monthly_trend['month'],
    y=monthly_trend['sales_value'],
    mode='lines+markers',
    name='合同额',
    line=dict(color='#3498db', width=3),
    yaxis='y'
))

fig_monthly.add_trace(go.Scatter(
    x=monthly_trend['month'],
    y=monthly_trend['gross_profit'],
    mode='lines+markers',
    name='毛利',
    line=dict(color='#2ecc71', width=2, dash='dot'),
    yaxis='y'
))

fig_monthly.update_layout(
    height=300,
    title="月度合同额与毛利趋势",
    xaxis_title="月份",
    yaxis_title="金额（元）",
    plot_bgcolor='white',
    hovermode='x unified',
    yaxis=dict(tickformat=',.0f')
)

st.plotly_chart(fig_monthly, use_container_width=True)

# 项目健康度分析
st.markdown("### 📊 项目健康度评分")


# 计算每个项目的健康度评分
def calculate_project_health(project):
    """计算项目健康度评分"""
    score = 100

    # 进度得分
    if project['progress'] < 30:
        progress_score = 30
    elif project['progress'] < 70:
        progress_score = 60
    else:
        progress_score = 100

    # 延期扣分
    delay_penalty = min(30, project['delay_days'] * 2)

    # 风险扣分
    risk_penalty = {'高': 20, '中': 10, '低': 0}[project['risk_level']]

    # 难度扣分
    difficulty_penalty = {'高': 15, '中': 5, '低': 0}[project['difficulty']]

    final_score = (progress_score + score) / 2 - delay_penalty - risk_penalty - difficulty_penalty
    return max(0, min(100, final_score))


df_projects['health_score'] = df_projects.apply(calculate_project_health, axis=1)

# 显示项目健康度分布
fig_health = px.histogram(
    df_projects,
    x='health_score',
    nbins=10,
    color_discrete_sequence=['#3498db'],
    labels={'health_score': '健康度得分', 'count': '项目数量'}
)

fig_health.update_layout(
    height=250,
    xaxis_title="健康度得分",
    yaxis_title="项目数量",
    plot_bgcolor='white',
    bargap=0.1
)

st.plotly_chart(fig_health, use_container_width=True)

# 管理洞察
st.markdown("### 💡 管理洞察与建议")

insights = [
    {
        "icon": "⚙️",
        "title": "机械设计资源紧张",
        "content": "机械设计资源利用率达92%，负荷过重，建议增加设计人员或优化工作流程",
        "priority": "high"
    },
    {
        "icon": "📅",
        "title": "汽车行业项目集中交付",
        "content": "3个汽车行业项目将在下月同时进入调试阶段，需提前协调调试资源",
        "priority": "high"
    },
    {
        "icon": "💰",
        "title": "医疗器械项目利润率高",
        "content": "医疗器械类项目平均毛利率达38%，高于公司平均32%，建议加大该行业拓展",
        "priority": "medium"
    },
    {
        "icon": "🔧",
        "title": "视觉检测设备需求增长",
        "content": "视觉检测设备项目数量同比增长45%，建议加强相关技术储备",
        "priority": "medium"
    }
]

cols = st.columns(2)
for idx, insight in enumerate(insights):
    with cols[idx % 2]:
        priority_color = "#e74c3c" if insight["priority"] == "high" else "#f39c12"

        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid {priority_color};">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 10px;">{insight['icon']}</span>
                <strong>{insight['title']}</strong>
            </div>
            <div style="color: #475569; font-size: 14px; margin-bottom: 10px;">
                {insight['content']}
            </div>
            <button style="background: {priority_color}; color: white; border: none; padding: 5px 15px; border-radius: 4px; font-size: 12px; cursor: pointer;">
                查看详情
            </button>
        </div>
        """, unsafe_allow_html=True)

# 页脚
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p>⚙️ 智造云非标设备制造BI系统 | 数据更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <p>💡 本系统已对接：Project项目管理 | SolidWorks/UG设计 | 用友ERP | 金蝶财务 | OA办公</p>
    <p>📞 技术支持：400-800-非标设备 | www.custom-equipment-bi.com</p>
</div>
""", unsafe_allow_html=True)

# 演示控制台
with st.sidebar:
    st.markdown("### 🎮 演示控制台")

    st.markdown("---")

    st.markdown("#### 系统对接")
    connected_systems = st.multiselect(
        "已对接系统",
        ["Project项目管理", "SolidWorks设计", "UG/NX设计", "用友U8 ERP", "金蝶K3", "OA办公", "PDM图档"],
        default=["Project项目管理", "SolidWorks设计", "用友U8 ERP"]
    )

    st.markdown("---")

    st.markdown("#### 预警设置")
    margin_threshold = st.slider("毛利率预警阈值", 0.1, 0.5, 0.25)
    delay_threshold = st.slider("延期预警阈值(天)", 7, 30, 15)

    st.markdown("---")

    st.markdown("#### 数据导出")
    if st.button("📥 生成项目周报", use_container_width=True):
        st.success("周报生成中... 包含项目进度、问题汇总、资源安排")

    if st.button("📊 导出财务数据", use_container_width=True):
        st.success("导出合同台账、成本明细、收款计划")

    st.markdown("---")

    st.markdown("""
    ### 📱 应用场景

    **总经理**：监控公司整体运营、利润率
    **项目经理**：跟踪项目进度、协调资源
    **设计主管**：管理设计任务、技术难点
    **生产经理**：安排生产计划、控制成本

    **演示完毕？** 联系我们定制专属版本
    """)

    if st.button("📞 获取定制方案15936507515", type="primary", use_container_width=True):
        st.success("已收到您的需求，技术顾问将在1小时内联系您！")
