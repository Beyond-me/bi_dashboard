# -*- coding: utf-8 -*-
# @Time    : 2026/5/6 08:25
# @Author  : lihaizhen
# @File    : crm_system.py
# @Software: PyCharm
# @Desc    :

# -*- coding: utf-8 -*-
# @Time    : 2026/4/30
# @Author  : CRM系统
# @File    : crm_system.py
# @Software: PyCharm
# @Desc    : 完整的CRM客户关系管理系统

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import warnings
import hashlib
import json
from io import BytesIO

warnings.filterwarnings('ignore')

# ========== 1. 页面配置 ==========
st.set_page_config(
    page_title="智能CRM管理系统",
    page_icon="🤝",
    layout="wide"
)

# ========== 2. 自定义样式 ==========
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
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
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid;
        margin-bottom: 15px;
    }

    .metric-clients { border-left-color: #1e3c72; }
    .metric-opportunities { border-left-color: #3498db; }
    .metric-sales { border-left-color: #2ecc71; }
    .metric-activities { border-left-color: #9b59b6; }

    .status-new { background: #e3f2fd; color: #1565c0; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .status-qualified { background: #e8f5e9; color: #2e7d32; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .status-proposal { background: #fff3e0; color: #ef6c00; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .status-negotiation { background: #f3e5f5; color: #7b1fa2; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .status-closed { background: #f5f5f5; color: #424242; padding: 3px 8px; border-radius: 12px; font-size: 12px; }

    .priority-high { background: #ffebee; color: #c62828; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .priority-medium { background: #fff3e0; color: #ef6c00; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
    .priority-low { background: #e8f5e9; color: #2e7d32; padding: 3px 8px; border-radius: 12px; font-size: 12px; }

    .source-website { background: #e3f2fd; color: #1565c0; }
    .source-referral { background: #f3e5f5; color: #7b1fa2; }
    .source-campaign { background: #e8f5e9; color: #2e7d32; }
    .source-social { background: #fff3e0; color: #ef6c00; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 5px 5px 0 0;
        padding: 10px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e3c72;
        color: white;
    }

    /* 卡片样式 */
    .client-card {
        background: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #1e3c72;
        transition: transform 0.2s;
    }

    .client-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)


# ========== 3. 数据库初始化 ==========
def init_database():
    """初始化CRM数据库"""
    conn = sqlite3.connect('crm_system.db', check_same_thread=False)
    c = conn.cursor()

    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (
                     id
                     INTEGER
                     PRIMARY
                     KEY
                     AUTOINCREMENT,
                     username
                     TEXT
                     UNIQUE
                     NOT
                     NULL,
                     password
                     TEXT
                     NOT
                     NULL,
                     full_name
                     TEXT,
                     email
                     TEXT,
                     role
                     TEXT
                     DEFAULT
                     '销售',
                     department
                     TEXT,
                     phone
                     TEXT,
                     created_at
                     TIMESTAMP
                     DEFAULT
                     CURRENT_TIMESTAMP,
                     is_active
                     INTEGER
                     DEFAULT
                     1
                 )''')

    # 客户表
    c.execute('''CREATE TABLE IF NOT EXISTS clients
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        client_code
        TEXT
        UNIQUE
        NOT
        NULL,
        company_name
        TEXT
        NOT
        NULL,
        contact_name
        TEXT,
        contact_title
        TEXT,
        phone
        TEXT,
        email
        TEXT,
        industry
        TEXT,
        city
        TEXT,
        province
        TEXT,
        address
        TEXT,
        source
        TEXT,
        status
        TEXT
        DEFAULT
        '潜在客户',
        level
        TEXT
        DEFAULT
        'C级',
        assigned_to
        INTEGER,
        created_by
        INTEGER,
        created_at
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        last_contact
        DATE,
        notes
        TEXT,
        FOREIGN
        KEY
                 (
        assigned_to
                 ) REFERENCES users
                 (
                     id
                 ),
        FOREIGN KEY
                 (
                     created_by
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # 联系记录表
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        client_id
        INTEGER
        NOT
        NULL,
        contact_type
        TEXT,
        contact_date
        DATE
        NOT
        NULL,
        contact_time
        TEXT,
        contact_person
        TEXT,
        summary
        TEXT,
        details
        TEXT,
        next_step
        TEXT,
        next_date
        DATE,
        created_by
        INTEGER,
        created_at
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        FOREIGN
        KEY
                 (
        client_id
                 ) REFERENCES clients
                 (
                     id
                 ),
        FOREIGN KEY
                 (
                     created_by
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # 销售机会表
    c.execute('''CREATE TABLE IF NOT EXISTS opportunities
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        opp_code
        TEXT
        UNIQUE
        NOT
        NULL,
        client_id
        INTEGER
        NOT
        NULL,
        name
        TEXT
        NOT
        NULL,
        description
        TEXT,
        product_line
        TEXT,
        estimated_value
        REAL,
        probability
        INTEGER
        DEFAULT
        30,
        stage
        TEXT
        DEFAULT
        '初步接触',
        priority
        TEXT
        DEFAULT
        '中',
        expected_close
        DATE,
        assigned_to
        INTEGER,
        created_by
        INTEGER,
        created_at
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        last_updated
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        notes
        TEXT,
        FOREIGN
        KEY
                 (
        client_id
                 ) REFERENCES clients
                 (
                     id
                 ),
        FOREIGN KEY
                 (
                     assigned_to
                 ) REFERENCES users
                 (
                     id
                 ),
        FOREIGN KEY
                 (
                     created_by
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # 任务表
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        title
        TEXT
        NOT
        NULL,
        description
        TEXT,
        related_to
        TEXT,
        related_id
        INTEGER,
        assigned_to
        INTEGER,
        due_date
        DATE,
        priority
        TEXT
        DEFAULT
        '中',
        status
        TEXT
        DEFAULT
        '待处理',
        reminder_date
        DATE,
        created_by
        INTEGER,
        created_at
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        completed_at
        TIMESTAMP,
        FOREIGN
        KEY
                 (
        assigned_to
                 ) REFERENCES users
                 (
                     id
                 ),
        FOREIGN KEY
                 (
                     created_by
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # 插入默认管理员用户
    c.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if c.fetchone()[0] == 0:
        # 使用简单的密码哈希
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        c.execute('''INSERT INTO users (username, password, full_name, email, role, department)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  ('admin', password_hash, '系统管理员', 'admin@crm.com', '管理员', '管理部'))

        # 插入示例销售用户
        sales_hash = hashlib.sha256('sales123'.encode()).hexdigest()
        c.execute('''INSERT INTO users (username, password, full_name, email, role, department)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  ('sales1', sales_hash, '张三', 'zhangsan@company.com', '销售', '销售部'))

    # 插入示例客户数据
    c.execute("SELECT COUNT(*) FROM clients")
    if c.fetchone()[0] == 0:
        example_clients = [
            ('CLT20240001', '华为技术有限公司', '任先生', '采购总监', '13800138001', 'ren@huawei.com',
             '通信设备', '深圳', '广东', '深圳市龙岗区坂田华为基地', '官网咨询', '重点客户', 'A级', 2, 1,
             '2024-01-15', '对5G设备有采购需求'),
            ('CLT20240002', '阿里巴巴集团', '马女士', '采购经理', '13900139002', 'ma@alibaba.com',
             '互联网', '杭州', '浙江', '杭州市余杭区文一西路969号', '客户推荐', '活跃客户', 'A级', 2, 1,
             '2024-02-10', '需要企业级云服务'),
            ('CLT20240003', '腾讯科技', '张先生', '技术总监', '13700137003', 'zhang@tencent.com',
             '互联网', '深圳', '广东', '深圳市南山区科技园', '市场活动', '活跃客户', 'A级', 2, 1,
             '2024-02-20', '对AI解决方案感兴趣'),
            ('CLT20240004', '字节跳动', '李先生', '采购专员', '13600136004', 'li@bytedance.com',
             '互联网', '北京', '北京', '北京市海淀区中航广场', '社交媒体', '潜在客户', 'B级', 2, 1,
             '2024-03-05', '需要海外服务器'),
            ('CLT20240005', '小米科技', '王先生', '供应链经理', '13500135005', 'wang@xiaomi.com',
             '消费电子', '北京', '北京', '北京市海淀区清河中街', '官网咨询', '重点客户', 'A级', 2, 1,
             '2024-03-12', 'IoT设备采购'),
        ]

        for client in example_clients:
            c.execute('''INSERT INTO clients
                         (client_code, company_name, contact_name, contact_title, phone, email,
                          industry, city, province, address, source, status, level, assigned_to,
                          created_by, last_contact, notes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', client)

    # 插入示例销售机会
    c.execute("SELECT COUNT(*) FROM opportunities")
    if c.fetchone()[0] == 0:
        example_opps = [
            ('OPP20240001', 1, '华为5G基站采购项目', '为华为提供新一代5G基站设备', '通信设备',
             5000000, 80, '商务谈判', '高', '2024-06-30', 2, 1, '项目已进入最后谈判阶段'),
            ('OPP20240002', 2, '阿里云企业服务', '提供企业级云存储解决方案', '云服务',
             1200000, 60, '方案提交', '中', '2024-07-15', 2, 1, '正在准备技术方案'),
            ('OPP20240003', 3, '腾讯AI实验室设备', 'AI训练服务器采购', 'AI硬件',
             3000000, 40, '需求分析', '高', '2024-08-30', 2, 1, '客户需求还在确认中'),
            ('OPP20240004', 4, '字节海外数据中心', '海外服务器设备供应', '服务器',
             2500000, 30, '初步接触', '中', '2024-09-15', 2, 1, '刚建立联系，需深入沟通'),
            ('OPP20240005', 5, '小米IoT设备采购', '智能家居设备供应', 'IoT设备',
             1800000, 70, '方案提交', '高', '2024-06-15', 2, 1, '方案已提交，等待反馈'),
        ]

        for opp in example_opps:
            c.execute('''INSERT INTO opportunities
                         (opp_code, client_id, name, description, product_line, estimated_value,
                          probability, stage, priority, expected_close, assigned_to, created_by, notes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', opp)

    # 插入示例联系记录
    c.execute("SELECT COUNT(*) FROM contacts")
    if c.fetchone()[0] == 0:
        example_contacts = [
            (1, '电话沟通', '2024-04-01', '10:30', '任先生', '讨论5G设备需求',
             '客户对设备性能有较高要求，需要提供详细技术参数', '准备技术方案', '2024-04-10', 2),
            (2, '视频会议', '2024-04-02', '14:00', '马女士', '云服务需求沟通',
             '客户需要定制化的云存储解决方案，讨论具体需求', '提交初步方案', '2024-04-12', 2),
            (3, '上门拜访', '2024-04-03', '15:30', '张先生', 'AI服务器需求调研',
             '参观了客户实验室，了解具体应用场景', '准备需求分析报告', '2024-04-15', 2),
        ]

        for contact in example_contacts:
            c.execute('''INSERT INTO contacts
                         (client_id, contact_type, contact_date, contact_time, contact_person,
                          summary, details, next_step, next_date, created_by)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', contact)

    # 插入示例任务
    c.execute("SELECT COUNT(*) FROM tasks")
    if c.fetchone()[0] == 0:
        example_tasks = [
            ('准备华为技术方案', '准备5G设备技术参数和报价方案', '客户', 1, 2, '2024-04-10',
             '高', '进行中', '2024-04-08', 1),
            ('联系阿里确认需求', '电话确认云服务的具体技术需求', '客户', 2, 2, '2024-04-05',
             '中', '待处理', '2024-04-04', 1),
            ('拜访腾讯技术团队', '上门了解AI服务器具体应用', '客户', 3, 2, '2024-04-12',
             '高', '已完成', '2024-04-10', 1),
        ]

        for task in example_tasks:
            c.execute('''INSERT INTO tasks
                         (title, description, related_to, related_id, assigned_to, due_date,
                          priority, status, reminder_date, created_by)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', task)

    conn.commit()
    return conn


# 初始化数据库
conn = init_database()


# ========== 4. 用户认证系统 ==========
def login(username, password):
    """用户登录"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    df = pd.read_sql_query(
        "SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1",
        conn, params=(username, password_hash)
    )
    return df.iloc[0] if not df.empty else None


def check_auth():
    """检查用户认证状态"""
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        return show_login_page()
    else:
        return True


def show_login_page():
    """显示登录页面"""
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; min-height: 80vh;">
        <div style="width: 100%; max-width: 400px;">
            <div class="main-header" style="text-align: center;">
                <h2>🤝 CRM管理系统</h2>
                <p>客户关系管理平台</p>
            </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("用户名", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", placeholder="请输入密码")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("登录", type="primary")

        if submit:
            user = login(username, password)
            if user is not None:
                st.session_state.user = {
                    'id': int(user['id']),
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role'],
                    'department': user['department']
                }
                st.success(f"欢迎回来，{user['full_name']}！")
                st.rerun()
            else:
                st.error("用户名或密码错误")

    # 显示默认账户信息
    with st.expander("测试账户"):
        st.write("**管理员账户**")
        st.write("用户名: admin")
        st.write("密码: admin123")
        st.write("**销售账户**")
        st.write("用户名: sales1")
        st.write("密码: sales123")

    return False


# ========== 5. 侧边栏导航 ==========
def show_sidebar():
    """显示侧边栏导航"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3>🤝 CRM系统</h3>
            <p style="color: #666; font-size: 14px;">欢迎，{st.session_state.user['full_name']}</p>
            <p style="color: #888; font-size: 12px;">{st.session_state.user['role']} | {st.session_state.user['department']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 定义菜单选项
        menu_options = [
            ("📊 仪表盘", "dashboard"),
            ("👥 客户管理", "clients"),
            ("💼 销售机会", "opportunities"),
            ("📞 联系记录", "contacts"),
            ("📅 任务日程", "tasks"),
            ("📈 业绩分析", "analytics"),
            ("👤 用户管理", "users")
        ]

        # 根据用户角色过滤菜单
        if st.session_state.user['role'] != '管理员':
            menu_options = [m for m in menu_options if m[1] != 'users']

        # 创建菜单选择器
        selected_index = 0
        for i, (name, _) in enumerate(menu_options):
            if st.session_state.get('page', 'dashboard') == menu_options[i][1]:
                selected_index = i

        selected = st.selectbox(
            "导航菜单",
            options=[m[0] for m in menu_options],
            index=selected_index,
            label_visibility="collapsed",
            key="sidebar_menu"  # 添加key
        )

        # 获取对应的页面标识
        selected_page = dict(menu_options)[selected]

        # 如果菜单选择发生了变化，更新session state
        if st.session_state.get('page') != selected_page:
            st.session_state.page = selected_page
            st.session_state.subpage = ""
            st.rerun()

        st.divider()

        # 快速操作按钮
        st.markdown("### ⚡ 快速操作")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ 新增客户", use_container_width=True, key="add_client_btn"):
                st.session_state.page = "clients"
                st.session_state.subpage = "add"
                st.rerun()

        with col2:
            if st.button("🎯 新增商机", use_container_width=True, key="add_opp_btn"):
                st.session_state.page = "opportunities"
                st.session_state.subpage = "add"
                st.rerun()

        st.divider()

        # 登出按钮
        if st.button("🚪 退出登录", use_container_width=True, key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "dashboard"
            st.session_state.subpage = ""
            st.rerun()

        return selected_page


# ========== 6. 仪表盘页面 ==========
def show_dashboard():
    """显示仪表盘"""
    st.markdown("""
    <div class="main-header">
        <h1>📊 CRM仪表盘</h1>
        <p>实时掌握客户动态与销售进展</p>
    </div>
    """, unsafe_allow_html=True)

    # 获取统计数据
    today = datetime.now().strftime('%Y-%m-%d')

    # 客户统计
    client_stats = pd.read_sql_query("""
                                     SELECT status,
                                            level,
                                            COUNT(*) as count
                                     FROM clients
                                     WHERE assigned_to = ? OR ? = '管理员'
                                     GROUP BY status, level
                                     """, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    # 销售机会统计
    opp_stats = pd.read_sql_query("""
                                  SELECT stage,
                                         priority,
                                         COUNT(*) as count,
            SUM(estimated_value) as total_value
                                  FROM opportunities
                                  WHERE assigned_to = ? OR ? = '管理员'
                                  GROUP BY stage, priority
                                  """, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    # 任务统计
    task_stats = pd.read_sql_query("""
                                   SELECT status,
                                          priority,
                                          COUNT(*) as count
                                   FROM tasks
                                   WHERE assigned_to = ? OR ? = '管理员'
                                   GROUP BY status, priority
                                   """, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    # 联系记录统计
    contact_stats = pd.read_sql_query("""
                                      SELECT strftime('%Y-%m', contact_date) as month,
            COUNT(*) as count
                                      FROM contacts
                                      WHERE created_by = ? OR ? = '管理员'
                                      GROUP BY strftime('%Y-%m', contact_date)
                                      ORDER BY month DESC
                                          LIMIT 6
                                      """, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    # 第一行：关键指标
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_clients = client_stats['count'].sum() if not client_stats.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-clients">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">我的客户总数</div>
            <div style="font-size: 28px; font-weight: bold; color: #1e3c72;">{total_clients}</div>
            <div style="font-size: 12px; margin-top: 5px;">
                重点客户: {client_stats[client_stats['level'] == 'A级']['count'].sum() if not client_stats.empty else 0}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        active_opps = opp_stats['count'].sum() if not opp_stats.empty else 0
        opp_value = opp_stats['total_value'].sum() if not opp_stats.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-opportunities">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">进行中商机</div>
            <div style="font-size: 28px; font-weight: bold; color: #3498db;">{active_opps}</div>
            <div style="font-size: 12px; margin-top: 5px;">
                预计金额: ¥{opp_value:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        pending_tasks = task_stats[task_stats['status'] == '待处理']['count'].sum() if not task_stats.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-sales">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">待处理任务</div>
            <div style="font-size: 28px; font-weight: bold; color: #2ecc71;">{pending_tasks}</div>
            <div style="font-size: 12px; margin-top: 5px;">
                高优先级: {task_stats[(task_stats['status'] == '待处理') & (task_stats['priority'] == '高')]['count'].sum() if not task_stats.empty else 0}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        recent_contacts = contact_stats['count'].sum() if not contact_stats.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-activities">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">近期联系</div>
            <div style="font-size: 28px; font-weight: bold; color: #9b59b6;">{recent_contacts}</div>
            <div style="font-size: 12px; margin-top: 5px;">
                最近6个月联系记录
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 第二行：图表分析
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 客户状态分布")
        if not client_stats.empty:
            fig = px.pie(
                client_stats,
                values='count',
                names='status',
                color='status',
                hole=0.4
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("暂无客户数据")

    with col2:
        st.markdown("### 📈 销售漏斗")
        if not opp_stats.empty:
            stage_order = ['初步接触', '需求分析', '方案提交', '商务谈判', '合同签订', '关闭']
            stage_data = opp_stats.groupby('stage')['count'].sum().reindex(stage_order).fillna(0)

            fig = go.Figure(go.Funnel(
                y=stage_data.index.tolist(),
                x=stage_data.values.tolist(),
                textinfo="value+percent initial"
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("暂无销售机会数据")

    st.divider()

    # 第三行：近期任务和活动
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📅 近期任务")
        recent_tasks = pd.read_sql_query("""
                                         SELECT t.*, u.full_name as assigned_name
                                         FROM tasks t
                                                  LEFT JOIN users u ON t.assigned_to = u.id
                                         WHERE (t.assigned_to = ? OR ? = '管理员')
                                           AND t.due_date >= date ('now')
                                         ORDER BY
                                             CASE priority
                                             WHEN '高' THEN 1
                                             WHEN '中' THEN 2
                                             WHEN '低' THEN 3
                                         END
                                         ,
                due_date
            LIMIT 10
                                         """, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

        if not recent_tasks.empty:
            for _, task in recent_tasks.iterrows():
                with st.container(border=True):
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.write(f"**{task['title']}**")
                        st.caption(f"截止: {task['due_date']} | 负责人: {task['assigned_name']}")
                    with cols[1]:
                        priority_class = f"priority-{task['priority']}"
                        st.markdown(f'<span class="{priority_class}">{task["priority"]}优先级</span>',
                                    unsafe_allow_html=True)
        else:
            st.info("暂无近期任务")

    with col2:
        st.markdown("### 📞 近期联系")
        recent_contacts = pd.read_sql_query("""
                                            SELECT c.*, cl.company_name, u.full_name as created_name
                                            FROM contacts c
                                                     LEFT JOIN clients cl ON c.client_id = cl.id
                                                     LEFT JOIN users u ON c.created_by = u.id
                                            WHERE (c.created_by = ? OR ? = '管理员')
                                            ORDER BY c.contact_date DESC, c.contact_time DESC LIMIT 10
                                            """, conn,
                                            params=(st.session_state.user['id'], st.session_state.user['role']))

        if not recent_contacts.empty:
            for _, contact in recent_contacts.iterrows():
                with st.container(border=True):
                    st.write(f"**{contact['company_name']}**")
                    st.caption(f"{contact['contact_date']} {contact['contact_time']} | {contact['contact_type']}")
                    st.write(contact['summary'])
        else:
            st.info("暂无联系记录")


# ========== 7. 客户管理页面 ==========
def show_clients():
    """显示客户管理页面"""
    st.markdown("""
    <div class="main-header">
        <h1>👥 客户管理</h1>
        <p>管理客户信息，跟进客户状态</p>
    </div>
    """, unsafe_allow_html=True)

    # 子页面选择
    subpage = st.radio(
        "功能选择",
        ["客户列表", "新增客户", "客户分析"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if subpage == "客户列表":
        show_client_list()
    elif subpage == "新增客户":
        add_client()
    elif subpage == "客户分析":
        show_client_analysis()


def show_client_list():
    """显示客户列表"""
    # 搜索和筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 搜索客户", placeholder="公司名称/联系人/电话")
    with col2:
        status_filter = st.selectbox("客户状态", ["全部", "潜在客户", "活跃客户", "重点客户", "流失客户"])
    with col3:
        level_filter = st.selectbox("客户等级", ["全部", "A级", "B级", "C级"])

    # 构建查询
    query = """
            SELECT c.*, u.full_name as assigned_name
            FROM clients c
                     LEFT JOIN users u ON c.assigned_to = u.id
            WHERE 1 = 1 \
            """
    params = []

    if st.session_state.user['role'] != '管理员':
        query += " AND c.assigned_to = ?"
        params.append(st.session_state.user['id'])

    if search:
        query += " AND (c.company_name LIKE ? OR c.contact_name LIKE ? OR c.phone LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if status_filter != "全部":
        query += " AND c.status = ?"
        params.append(status_filter)

    if level_filter != "全部":
        query += " AND c.level = ?"
        params.append(level_filter)

    query += " ORDER BY c.last_contact DESC, c.created_at DESC"

    df_clients = pd.read_sql_query(query, conn, params=params)

    if not df_clients.empty:
        # 显示数据表格
        display_cols = ['client_code', 'company_name', 'contact_name', 'phone', 'industry',
                        'city', 'status', 'level', 'assigned_name', 'last_contact']

        st.dataframe(
            df_clients[display_cols],
            column_config={
                "client_code": "客户编号",
                "company_name": "公司名称",
                "contact_name": "联系人",
                "phone": "电话",
                "industry": "行业",
                "city": "城市",
                "status": "状态",
                "level": "等级",
                "assigned_name": "负责人",
                "last_contact": "最后联系"
            },
            width='stretch'
        )

        # 客户详情
        st.markdown("### 📋 客户详情")
        selected_id = st.selectbox("选择客户查看详情", df_clients['id'].tolist(),
                                   format_func=lambda
                                       x: f"{df_clients[df_clients['id'] == x]['company_name'].iloc[0]} (ID: {x})")

        if selected_id:
            client = df_clients[df_clients['id'] == selected_id].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**公司名称:** {client['company_name']}")
                st.markdown(f"**联系人:** {client['contact_name']} ({client['contact_title']})")
                st.markdown(f"**电话:** {client['phone']}")
                st.markdown(f"**邮箱:** {client['email']}")
                st.markdown(f"**行业:** {client['industry']}")

            with col2:
                st.markdown(f"**地址:** {client['province']}{client['city']}{client['address']}")
                st.markdown(f"**来源:** {client['source']}")
                status_class = f"status-{client['status'].replace('客户', '')}"
                st.markdown(f"**状态:** <span class='{status_class}'>{client['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**等级:** {client['level']}")
                st.markdown(f"**负责人:** {client['assigned_name']}")

            # 客户备注
            if client['notes']:
                with st.expander("客户备注"):
                    st.write(client['notes'])
    else:
        st.info("暂无客户数据")


def add_client():
    """新增客户"""
    st.subheader("➕ 新增客户")

    with st.form("add_client_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("公司名称*", placeholder="请输入公司全称")
            contact_name = st.text_input("联系人*", placeholder="请输入联系人姓名")
            contact_title = st.text_input("联系人职位", placeholder="如：采购经理")
            phone = st.text_input("联系电话*", placeholder="11位手机号")
            email = st.text_input("邮箱", placeholder="联系人邮箱")

        with col2:
            industry = st.selectbox("所属行业*",
                                    ["", "互联网", "金融", "制造", "教育", "医疗", "零售", "房地产", "其他"])
            province = st.selectbox("省份*", ["", "北京", "上海", "广东", "浙江", "江苏", "山东", "四川", "其他"])
            city = st.text_input("城市*", placeholder="如：深圳")
            address = st.text_area("详细地址", placeholder="街道门牌号")

        col3, col4 = st.columns(2)
        with col3:
            source = st.selectbox("客户来源*", ["", "官网咨询", "客户推荐", "市场活动", "社交媒体", "电话销售", "其他"])
            status = st.selectbox("客户状态*", ["潜在客户", "活跃客户", "重点客户", "流失客户"])

        with col4:
            level = st.selectbox("客户等级*", ["A级", "B级", "C级"])
            # 获取可分配的用户
            users = pd.read_sql_query("SELECT id, full_name FROM users WHERE role = '销售'", conn)
            assigned_to = st.selectbox("负责人*", users['id'].tolist(),
                                       format_func=lambda x: users[users['id'] == x]['full_name'].iloc[0])

        notes = st.text_area("客户备注", placeholder="可填写客户特点、需求等信息")
        last_contact = st.date_input("最后联系日期", value=datetime.now())

        submitted = st.form_submit_button("✅ 添加客户", type="primary")

        if submitted:
            if not all([company_name, contact_name, phone, industry, province, city, source]):
                st.error("请填写所有带*的必填项")
            else:
                try:
                    # 生成客户编号
                    client_code = f"CLT{datetime.now().strftime('%Y%m%d%H%M%S')}"

                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO clients
                                      (client_code, company_name, contact_name, contact_title, phone, email,
                                       industry, province, city, address, source, status, level,
                                       assigned_to, created_by, last_contact, notes)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (client_code, company_name, contact_name, contact_title, phone, email,
                                    industry, province, city, address, source, status, level,
                                    assigned_to, st.session_state.user['id'], last_contact, notes or None))
                    conn.commit()

                    st.success(f"✅ 客户 '{company_name}' 添加成功！")
                    st.balloons()
                except Exception as e:
                    st.error(f"添加失败: {str(e)}")


def show_client_analysis():
    """显示客户分析"""
    st.subheader("📊 客户分析")

    # 获取客户数据
    query = """
            SELECT * \
            FROM clients
            WHERE assigned_to = ? \
               OR ? = '管理员' \
            """
    df_clients = pd.read_sql_query(query, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    if not df_clients.empty:
        col1, col2 = st.columns(2)

        with col1:
            # 客户行业分布
            st.markdown("##### 🏢 客户行业分布")
            industry_dist = df_clients['industry'].value_counts()
            fig1 = px.pie(
                values=industry_dist.values,
                names=industry_dist.index,
                hole=0.3
            )
            st.plotly_chart(fig1, width='stretch')

        with col2:
            # 客户地区分布
            st.markdown("##### 🗺️ 客户地区分布")
            region_dist = df_clients['province'].value_counts().head(10)
            fig2 = px.bar(
                x=region_dist.values,
                y=region_dist.index,
                orientation='h'
            )
            st.plotly_chart(fig2, width='stretch')

        # 客户状态趋势
        st.markdown("##### 📈 客户状态趋势")
        df_clients['created_month'] = pd.to_datetime(df_clients['created_at']).dt.strftime('%Y-%m')
        status_trend = df_clients.pivot_table(
            index='created_month',
            columns='status',
            values='id',
            aggfunc='count',
            fill_value=0
        )

        fig3 = go.Figure()
        for status in status_trend.columns:
            fig3.add_trace(go.Scatter(
                x=status_trend.index,
                y=status_trend[status],
                mode='lines+markers',
                name=status
            ))

        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')
    else:
        st.info("暂无客户数据进行分析")


# ========== 8. 销售机会页面 ==========
def show_opportunities():
    """显示销售机会页面"""
    st.markdown("""
    <div class="main-header">
        <h1>💼 销售机会管理</h1>
        <p>跟踪销售机会，预测销售业绩</p>
    </div>
    """, unsafe_allow_html=True)

    subpage = st.radio(
        "功能选择",
        ["机会列表", "新增机会", "漏斗分析"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if subpage == "机会列表":
        show_opportunity_list()
    elif subpage == "新增机会":
        add_opportunity()
    elif subpage == "漏斗分析":
        show_funnel_analysis()


def show_opportunity_list():
    """显示销售机会列表"""
    # 筛选条件
    col1, col2, col3 = st.columns(3)
    with col1:
        stage_filter = st.selectbox("阶段筛选",
                                    ["全部", "初步接触", "需求分析", "方案提交", "商务谈判", "合同签订", "关闭"])
    with col2:
        priority_filter = st.selectbox("优先级筛选", ["全部", "高", "中", "低"])
    with col3:
        month_filter = st.selectbox("预计成交月", ["全部", "本月", "下月", "本季度", "下季度"])

    # 构建查询
    query = """
            SELECT o.*, c.company_name, u.full_name as assigned_name
            FROM opportunities o
                     LEFT JOIN clients c ON o.client_id = c.id
                     LEFT JOIN users u ON o.assigned_to = u.id
            WHERE 1 = 1 \
            """
    params = []

    if st.session_state.user['role'] != '管理员':
        query += " AND o.assigned_to = ?"
        params.append(st.session_state.user['id'])

    if stage_filter != "全部":
        query += " AND o.stage = ?"
        params.append(stage_filter)

    if priority_filter != "全部":
        query += " AND o.priority = ?"
        params.append(priority_filter)

    if month_filter != "全部":
        if month_filter == "本月":
            query += " AND strftime('%Y-%m', o.expected_close) = strftime('%Y-%m', 'now')"
        elif month_filter == "下月":
            query += " AND strftime('%Y-%m', o.expected_close) = strftime('%Y-%m', 'now', '+1 month')"
        elif month_filter == "本季度":
            query += " AND strftime('%Y-%m', o.expected_close) BETWEEN strftime('%Y-%m', 'now', 'start of month') AND strftime('%Y-%m', 'now', '+2 months')"
        elif month_filter == "下季度":
            query += " AND strftime('%Y-%m', o.expected_close) BETWEEN strftime('%Y-%m', 'now', '+3 months') AND strftime('%Y-%m', 'now', '+5 months')"

    query += " ORDER BY o.priority DESC, o.expected_close"

    df_opps = pd.read_sql_query(query, conn, params=params)

    if not df_opps.empty:
        # 计算预计金额
        df_opps['expected_amount'] = df_opps['estimated_value'] * df_opps['probability'] / 100

        # 显示统计信息
        total_value = df_opps['estimated_value'].sum()
        expected_amount = df_opps['expected_amount'].sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("机会总数", len(df_opps))
        with col2:
            st.metric("总金额", f"¥{total_value:,.0f}")
        with col3:
            st.metric("预计收入", f"¥{expected_amount:,.0f}")

        st.divider()

        # 显示机会列表
        for _, opp in df_opps.iterrows():
            with st.container(border=True):
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.write(f"**{opp['name']}**")
                    st.caption(f"{opp['company_name']} | {opp['product_line']}")
                    st.write(f"阶段: {opp['stage']} | 概率: {opp['probability']}%")

                with cols[1]:
                    st.write(f"**金额**")
                    st.write(f"¥{opp['estimated_value']:,.0f}")

                with cols[2]:
                    priority_class = f"priority-{opp['priority']}"
                    st.markdown(f'<span class="{priority_class}">{opp["priority"]}优先级</span>',
                                unsafe_allow_html=True)
                    st.write(f"预计: {opp['expected_close']}")
                    st.write(f"负责人: {opp['assigned_name']}")
    else:
        st.info("暂无销售机会数据")


def add_opportunity():
    """新增销售机会"""
    st.subheader("🎯 新增销售机会")

    with st.form("add_opportunity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            # 选择客户
            query = "SELECT id, company_name FROM clients WHERE assigned_to = ? OR ? = '管理员'"
            df_clients = pd.read_sql_query(query, conn,
                                           params=(st.session_state.user['id'], st.session_state.user['role']))
            client_options = {f"{row['company_name']} (ID: {row['id']})": row['id'] for _, row in df_clients.iterrows()}

            if client_options:
                selected_client = st.selectbox("选择客户*", list(client_options.keys()))
                client_id = client_options[selected_client]
            else:
                st.warning("请先添加客户")
                client_id = None

            name = st.text_input("机会名称*", placeholder="如：XX公司ERP系统采购")
            description = st.text_area("机会描述", placeholder="详细描述客户需求和解决方案")
            product_line = st.selectbox("产品线*", ["软件", "硬件", "服务", "解决方案", "其他"])

        with col2:
            estimated_value = st.number_input("预估金额(元)*", min_value=0.0, value=0.0, format="%.2f")
            probability = st.slider("成交概率(%)*", 0, 100, 30)
            stage = st.selectbox("当前阶段*", ["初步接触", "需求分析", "方案提交", "商务谈判", "合同签订", "关闭"])
            priority = st.selectbox("优先级*", ["高", "中", "低"])
            expected_close = st.date_input("预计成交日期*", value=datetime.now() + timedelta(days=30))

        # 获取可分配的用户
        users = pd.read_sql_query("SELECT id, full_name FROM users WHERE role = '销售'", conn)
        assigned_to = st.selectbox("负责人*", users['id'].tolist(),
                                   format_func=lambda x: users[users['id'] == x]['full_name'].iloc[0],
                                   index=0)

        notes = st.text_area("备注", placeholder="可填写注意事项、关键信息等")

        submitted = st.form_submit_button("✅ 添加机会", type="primary")

        if submitted:
            if not all([client_id, name, product_line, estimated_value > 0]):
                st.error("请填写所有带*的必填项，且金额必须大于0")
            elif not client_options:
                st.error("请先添加客户")
            else:
                try:
                    # 生成机会编号
                    opp_code = f"OPP{datetime.now().strftime('%Y%m%d%H%M%S')}"

                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO opportunities
                                      (opp_code, client_id, name, description, product_line, estimated_value,
                                       probability, stage, priority, expected_close, assigned_to, created_by, notes)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (opp_code, client_id, name, description, product_line, estimated_value,
                                    probability, stage, priority, expected_close, assigned_to,
                                    st.session_state.user['id'], notes or None))
                    conn.commit()

                    st.success(f"✅ 销售机会 '{name}' 添加成功！")
                    st.balloons()
                except Exception as e:
                    st.error(f"添加失败: {str(e)}")


def show_funnel_analysis():
    """显示销售漏斗分析"""
    st.subheader("📊 销售漏斗分析")

    # 获取销售机会数据
    query = """
            SELECT stage, priority, estimated_value, probability
            FROM opportunities
            WHERE assigned_to = ? \
               OR ? = '管理员' \
            """
    df_opps = pd.read_sql_query(query, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    if not df_opps.empty:
        # 阶段分布
        stage_order = ['初步接触', '需求分析', '方案提交', '商务谈判', '合同签订', '关闭']
        stage_data = df_opps.groupby('stage').agg({
            'estimated_value': 'sum',
            'probability': 'mean'
        }).reindex(stage_order).fillna(0)

        col1, col2 = st.columns(2)

        with col1:
            # 销售漏斗图
            fig1 = go.Figure(go.Funnel(
                y=stage_data.index.tolist(),
                x=stage_data['estimated_value'].tolist(),
                textinfo="value+percent initial"
            ))
            fig1.update_layout(
                title="销售金额漏斗",
                height=400
            )
            st.plotly_chart(fig1, width='stretch')

        with col2:
            # 阶段金额分布
            fig2 = px.bar(
                x=stage_data.index.tolist(),
                y=stage_data['estimated_value'].tolist(),
                labels={'x': '阶段', 'y': '预估金额'},
                title="各阶段预估金额"
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, width='stretch')

        # 预计收入分析
        df_opps['expected_value'] = df_opps['estimated_value'] * df_opps['probability'] / 100
        expected_by_stage = df_opps.groupby('stage')['expected_value'].sum().reindex(stage_order).fillna(0)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=expected_by_stage.index.tolist(),
            y=expected_by_stage.values.tolist(),
            name='预计收入'
        ))
        fig3.add_trace(go.Bar(
            x=stage_data.index.tolist(),
            y=stage_data['estimated_value'].tolist(),
            name='预估金额'
        ))

        fig3.update_layout(
            title="预估金额 vs 预计收入",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig3, width='stretch')
    else:
        st.info("暂无销售机会数据")


# ========== 9. 联系记录页面 ==========
def show_contacts():
    """显示联系记录页面"""
    st.markdown("""
    <div class="main-header">
        <h1>📞 联系记录</h1>
        <p>记录客户沟通，跟踪跟进进度</p>
    </div>
    """, unsafe_allow_html=True)

    subpage = st.radio(
        "功能选择",
        ["记录列表", "新增记录"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if subpage == "记录列表":
        show_contact_list()
    elif subpage == "新增记录":
        add_contact()


def show_contact_list():
    """显示联系记录列表"""
    # 日期范围筛选
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("开始日期", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("结束日期", value=datetime.now())

    # 构建查询
    query = """
            SELECT c.*, cl.company_name, u.full_name as created_name
            FROM contacts c
                     LEFT JOIN clients cl ON c.client_id = cl.id
                     LEFT JOIN users u ON c.created_by = u.id
            WHERE c.contact_date BETWEEN ? AND ? \
            """
    params = [start_date, end_date]

    if st.session_state.user['role'] != '管理员':
        query += " AND c.created_by = ?"
        params.append(st.session_state.user['id'])

    query += " ORDER BY c.contact_date DESC, c.contact_time DESC"

    df_contacts = pd.read_sql_query(query, conn, params=params)

    if not df_contacts.empty:
        # 统计信息
        total_contacts = len(df_contacts)
        today_contacts = len(df_contacts[df_contacts['contact_date'] == datetime.now().strftime('%Y-%m-%d')])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("总联系记录", total_contacts)
        with col2:
            st.metric("今日联系", today_contacts)

        st.divider()

        # 显示联系记录
        for _, contact in df_contacts.iterrows():
            with st.container(border=True):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"**{contact['company_name']}**")
                    st.caption(
                        f"{contact['contact_date']} {contact['contact_time']} | {contact['contact_type']} | 联系人: {contact['contact_person']}")
                    st.write(f"**摘要:** {contact['summary']}")
                    if contact['details']:
                        with st.expander("查看详情"):
                            st.write(contact['details'])
                with cols[1]:
                    st.write(f"记录人: {contact['created_name']}")
                    if contact['next_step']:
                        st.write(f"**下一步:** {contact['next_step']}")
                        if contact['next_date']:
                            st.write(f"计划日期: {contact['next_date']}")
    else:
        st.info("该时间段内无联系记录")


def add_contact():
    """新增联系记录"""
    st.subheader("📝 新增联系记录")

    with st.form("add_contact_form", clear_on_submit=True):
        # 选择客户
        query = "SELECT id, company_name FROM clients WHERE assigned_to = ? OR ? = '管理员'"
        df_clients = pd.read_sql_query(query, conn, params=(st.session_state.user['id'], st.session_state.user['role']))
        client_options = {f"{row['company_name']} (ID: {row['id']})": row['id'] for _, row in df_clients.iterrows()}

        if not client_options:
            st.warning("暂无负责的客户，请先添加客户或联系管理员分配客户")
            client_id = None
        else:
            selected_client = st.selectbox("选择客户*", list(client_options.keys()))
            client_id = client_options[selected_client]

        col1, col2 = st.columns(2)
        with col1:
            contact_type = st.selectbox("联系类型*",
                                        ["电话沟通", "视频会议", "上门拜访", "邮件沟通", "微信联系", "其他"])
            contact_date = st.date_input("联系日期*", value=datetime.now())
            contact_time = st.time_input("联系时间*", value=datetime.now().time())
            contact_person = st.text_input("客户联系人*", placeholder="与您沟通的客户方人员")

        with col2:
            summary = st.text_area("联系摘要*", placeholder="简要描述沟通内容", height=100)
            details = st.text_area("详细记录", placeholder="详细记录沟通内容、客户反馈等", height=150)

        col3, col4 = st.columns(2)
        with col3:
            next_step = st.text_input("下一步计划", placeholder="下一步行动计划")
        with col4:
            next_date = st.date_input("计划日期", value=datetime.now() + timedelta(days=7))

        submitted = st.form_submit_button("✅ 保存记录", type="primary")

        if submitted:
            if not all([client_id, contact_person, summary]):
                st.error("请填写所有带*的必填项")
            elif not client_options:
                st.error("请先添加客户")
            else:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO contacts
                                      (client_id, contact_type, contact_date, contact_time, contact_person,
                                       summary, details, next_step, next_date, created_by)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (client_id, contact_type, contact_date, contact_time.strftime('%H:%M'),
                                    contact_person, summary, details or None, next_step or None,
                                    next_date if next_step else None, st.session_state.user['id']))

                    # 更新客户最后联系时间
                    cursor.execute("UPDATE clients SET last_contact = ? WHERE id = ?",
                                   (contact_date, client_id))

                    conn.commit()

                    st.success("✅ 联系记录保存成功！")

                    # 如果有下一步计划，创建任务
                    if next_step:
                        try:
                            task_title = f"跟进：{next_step}"
                            cursor.execute('''INSERT INTO tasks
                                              (title, description, related_to, related_id, assigned_to,
                                               due_date, priority, created_by)
                                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                           (task_title, details or next_step, '客户', client_id,
                                            st.session_state.user['id'], next_date, '中', st.session_state.user['id']))
                            conn.commit()
                            st.success("✅ 已自动创建跟进任务")
                        except:
                            pass

                    st.balloons()
                except Exception as e:
                    st.error(f"保存失败: {str(e)}")


# ========== 10. 任务日程页面 ==========
def show_tasks():
    """显示任务日程页面"""
    st.markdown("""
    <div class="main-header">
        <h1>📅 任务日程</h1>
        <p>管理待办任务，提高工作效率</p>
    </div>
    """, unsafe_allow_html=True)

    subpage = st.radio(
        "功能选择",
        ["我的任务", "新增任务", "任务统计"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if subpage == "我的任务":
        show_my_tasks()
    elif subpage == "新增任务":
        add_task()
    elif subpage == "任务统计":
        show_task_stats()


def show_my_tasks():
    """显示我的任务"""
    # 任务筛选
    status_filter = st.selectbox("任务状态", ["全部", "待处理", "进行中", "已完成", "已延期"])

    # 构建查询
    query = """
            SELECT t.*, u.full_name as assigned_name
            FROM tasks t
                     LEFT JOIN users u ON t.assigned_to = u.id
            WHERE t.assigned_to = ? \
            """
    params = [st.session_state.user['id']]

    if status_filter != "全部":
        query += " AND t.status = ?"
        params.append(status_filter)

    query += " ORDER BY t.priority, t.due_date"

    df_tasks = pd.read_sql_query(query, conn, params=params)

    if not df_tasks.empty:
        # 按状态分组显示
        for status in ['待处理', '进行中', '已完成', '已延期']:
            status_tasks = df_tasks[df_tasks['status'] == status]
            if not status_tasks.empty:
                st.subheader(f"{status} ({len(status_tasks)})")

                for _, task in status_tasks.iterrows():
                    with st.container(border=True):
                        cols = st.columns([4, 1])
                        with cols[0]:
                            st.write(f"**{task['title']}**")
                            if task['description']:
                                st.caption(task['description'])

                            # 显示关联信息
                            if task['related_to'] and task['related_id']:
                                if task['related_to'] == '客户':
                                    client_info = pd.read_sql_query(
                                        "SELECT company_name FROM clients WHERE id = ?",
                                        conn, params=(task['related_id'],)
                                    )
                                    if not client_info.empty:
                                        st.caption(f"关联客户: {client_info.iloc[0]['company_name']}")

                        with cols[1]:
                            priority_class = f"priority-{task['priority']}"
                            st.markdown(f'<span class="{priority_class}">{task["priority"]}优先级</span>',
                                        unsafe_allow_html=True)
                            st.write(f"截止: {task['due_date']}")

                            # 任务操作
                            if status != '已完成':
                                if st.button("完成", key=f"complete_{task['id']}"):
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "UPDATE tasks SET status = '已完成', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                                        (task['id'],))
                                    conn.commit()
                                    st.success(f"任务 '{task['title']}' 已完成！")
                                    st.rerun()
    else:
        st.info("暂无任务")


def add_task():
    """新增任务"""
    st.subheader("➕ 新增任务")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("任务标题*", placeholder="请输入任务标题")
        description = st.text_area("任务描述", placeholder="详细描述任务内容")

        col1, col2 = st.columns(2)
        with col1:
            related_to = st.selectbox("关联对象", ["无", "客户", "销售机会"])
            if related_to != "无":
                if related_to == "客户":
                    query = "SELECT id, company_name FROM clients WHERE assigned_to = ? OR ? = '管理员'"
                    df_related = pd.read_sql_query(query, conn,
                                                   params=(st.session_state.user['id'], st.session_state.user['role']))
                    related_options = {f"{row['company_name']} (ID: {row['id']})": row['id'] for _, row in
                                       df_related.iterrows()}
                else:  # 销售机会
                    query = "SELECT id, name FROM opportunities WHERE assigned_to = ? OR ? = '管理员'"
                    df_related = pd.read_sql_query(query, conn,
                                                   params=(st.session_state.user['id'], st.session_state.user['role']))
                    related_options = {f"{row['name']} (ID: {row['id']})": row['id'] for _, row in
                                       df_related.iterrows()}

                if related_options:
                    selected_related = st.selectbox(f"选择{related_to}", list(related_options.keys()))
                    related_id = related_options[selected_related]
                else:
                    related_id = None
            else:
                related_id = None

        with col2:
            due_date = st.date_input("截止日期*", value=datetime.now() + timedelta(days=7))
            priority = st.selectbox("优先级*", ["高", "中", "低"])
            reminder_date = st.date_input("提醒日期", value=datetime.now() + timedelta(days=5))

        # 如果是管理员，可以选择分配给别人
        if st.session_state.user['role'] == '管理员':
            users = pd.read_sql_query("SELECT id, full_name FROM users", conn)
            assigned_to = st.selectbox("负责人*", users['id'].tolist(),
                                       format_func=lambda x: users[users['id'] == x]['full_name'].iloc[0])
        else:
            assigned_to = st.session_state.user['id']

        submitted = st.form_submit_button("✅ 添加任务", type="primary")

        if submitted:
            if not title or not due_date:
                st.error("请填写所有带*的必填项")
            else:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO tasks
                                      (title, description, related_to, related_id, assigned_to,
                                       due_date, priority, reminder_date, created_by)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (title, description or None, related_to if related_to != "无" else None,
                                    related_id, assigned_to, due_date, priority,
                                    reminder_date if reminder_date else None, st.session_state.user['id']))
                    conn.commit()

                    st.success(f"✅ 任务 '{title}' 添加成功！")
                    st.balloons()
                except Exception as e:
                    st.error(f"添加失败: {str(e)}")


def show_task_stats():
    """显示任务统计"""
    st.subheader("📊 任务统计")

    # 获取任务数据
    query = """
            SELECT * \
            FROM tasks
            WHERE assigned_to = ? \
               OR ? = '管理员' \
            """
    df_tasks = pd.read_sql_query(query, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    if not df_tasks.empty:
        col1, col2 = st.columns(2)

        with col1:
            # 任务状态分布
            st.markdown("##### 📈 任务状态分布")
            status_dist = df_tasks['status'].value_counts()
            fig1 = px.pie(
                values=status_dist.values,
                names=status_dist.index,
                hole=0.3
            )
            st.plotly_chart(fig1, width='stretch')

        with col2:
            # 任务优先级分布
            st.markdown("##### 🎯 任务优先级分布")
            priority_dist = df_tasks['priority'].value_counts()
            fig2 = px.bar(
                x=priority_dist.index,
                y=priority_dist.values
            )
            st.plotly_chart(fig2, width='stretch')

        # 月度任务趋势
        st.markdown("##### 📅 月度任务趋势")
        df_tasks['created_month'] = pd.to_datetime(df_tasks['created_at']).dt.strftime('%Y-%m')
        monthly_tasks = df_tasks.groupby(['created_month', 'status']).size().unstack(fill_value=0)

        fig3 = go.Figure()
        for status in monthly_tasks.columns:
            fig3.add_trace(go.Scatter(
                x=monthly_tasks.index,
                y=monthly_tasks[status],
                mode='lines+markers',
                name=status
            ))

        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')
    else:
        st.info("暂无任务数据")


# ========== 11. 业绩分析页面 ==========
def show_analytics():
    """显示业绩分析页面"""
    st.markdown("""
    <div class="main-header">
        <h1>📈 业绩分析</h1>
        <p>分析销售数据，洞察业务趋势</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["销售业绩", "客户分析", "团队表现"])

    with tab1:
        show_sales_analytics()
    with tab2:
        show_client_analytics()
    with tab3:
        show_team_analytics()


def show_sales_analytics():
    """显示销售业绩分析"""
    st.subheader("💰 销售业绩分析")

    # 日期范围选择
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("开始日期", value=datetime.now().replace(day=1))
    with col2:
        end_date = st.date_input("结束日期", value=datetime.now())

    if st.button("生成报告", type="primary"):
        # 获取销售机会数据
        query = """
                SELECT o.*, c.company_name, u.full_name as sales_name
                FROM opportunities o
                         LEFT JOIN clients c ON o.client_id = c.id
                         LEFT JOIN users u ON o.assigned_to = u.id
                WHERE o.expected_close BETWEEN ? AND ? \
                """

        if st.session_state.user['role'] != '管理员':
            query += " AND o.assigned_to = ?"
            params = (start_date, end_date, st.session_state.user['id'])
        else:
            params = (start_date, end_date)

        df_opps = pd.read_sql_query(query, conn, params=params)

        if not df_opps.empty:
            # 计算预计收入
            df_opps['expected_revenue'] = df_opps['estimated_value'] * df_opps['probability'] / 100

            col1, col2, col3 = st.columns(3)
            with col1:
                total_opps = len(df_opps)
                st.metric("机会数量", total_opps)
            with col2:
                total_value = df_opps['estimated_value'].sum()
                st.metric("预估金额", f"¥{total_value:,.0f}")
            with col3:
                expected_revenue = df_opps['expected_revenue'].sum()
                st.metric("预计收入", f"¥{expected_revenue:,.0f}")

            st.divider()

            # 阶段分布分析
            st.markdown("##### 📊 阶段分布")
            stage_analysis = df_opps.groupby('stage').agg({
                'estimated_value': 'sum',
                'expected_revenue': 'sum',
                'id': 'count'
            }).rename(columns={'id': 'count'})

            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.bar(
                    x=stage_analysis.index,
                    y=stage_analysis['estimated_value'],
                    labels={'x': '阶段', 'y': '预估金额'},
                    title="各阶段预估金额"
                )
                st.plotly_chart(fig1, width='stretch')

            with col2:
                fig2 = px.pie(
                    values=stage_analysis['count'],
                    names=stage_analysis.index,
                    title="机会数量分布"
                )
                st.plotly_chart(fig2, width='stretch')

            # 月度趋势
            st.markdown("##### 📅 月度趋势")
            df_opps['expected_month'] = pd.to_datetime(df_opps['expected_close']).dt.strftime('%Y-%m')
            monthly_trend = df_opps.groupby('expected_month').agg({
                'estimated_value': 'sum',
                'expected_revenue': 'sum'
            }).sort_index()

            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=monthly_trend.index,
                y=monthly_trend['estimated_value'],
                mode='lines+markers',
                name='预估金额'
            ))
            fig3.add_trace(go.Scatter(
                x=monthly_trend.index,
                y=monthly_trend['expected_revenue'],
                mode='lines+markers',
                name='预计收入'
            ))

            fig3.update_layout(height=400)
            st.plotly_chart(fig3, width='stretch')

            # 详细数据
            with st.expander("查看详细数据"):
                st.dataframe(df_opps[['opp_code', 'company_name', 'name', 'stage', 'estimated_value',
                                      'probability', 'expected_revenue', 'expected_close']],
                             width='stretch')
        else:
            st.info("该时间段内无销售机会数据")


def show_client_analytics():
    """显示客户分析"""
    st.subheader("👥 客户分析")

    # 获取客户数据
    query = """
            SELECT * \
            FROM clients
            WHERE assigned_to = ? \
               OR ? = '管理员' \
            """
    df_clients = pd.read_sql_query(query, conn, params=(st.session_state.user['id'], st.session_state.user['role']))

    if not df_clients.empty:
        col1, col2 = st.columns(2)

        with col1:
            # 客户来源分析
            st.markdown("##### 📍 客户来源分析")
            source_dist = df_clients['source'].value_counts()
            fig1 = px.pie(
                values=source_dist.values,
                names=source_dist.index,
                hole=0.3
            )
            st.plotly_chart(fig1, width='stretch')

        with col2:
            # 客户等级分布
            st.markdown("##### 🏆 客户等级分布")
            level_dist = df_clients['level'].value_counts()
            fig2 = px.bar(
                x=level_dist.index,
                y=level_dist.values,
                color=level_dist.index
            )
            st.plotly_chart(fig2, width='stretch')

        # 客户状态趋势
        st.markdown("##### 📈 客户状态趋势")
        df_clients['created_month'] = pd.to_datetime(df_clients['created_at']).dt.strftime('%Y-%m')
        status_trend = df_clients.pivot_table(
            index='created_month',
            columns='status',
            values='id',
            aggfunc='count',
            fill_value=0
        ).sort_index()

        fig3 = go.Figure()
        for status in status_trend.columns:
            fig3.add_trace(go.Scatter(
                x=status_trend.index,
                y=status_trend[status],
                mode='lines+markers',
                name=status
            ))

        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')

        # 客户地域分布
        st.markdown("##### 🗺️ 客户地域分布")
        province_dist = df_clients['province'].value_counts().head(10)
        fig4 = px.bar(
            x=province_dist.values,
            y=province_dist.index,
            orientation='h',
            title='客户地域分布TOP10'
        )
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, width='stretch')
    else:
        st.info("暂无客户数据")


def show_team_analytics():
    """显示团队表现分析"""
    if st.session_state.user['role'] != '管理员':
        st.warning("该功能仅限管理员使用")
        return

    st.subheader("👥 团队表现分析")

    # 获取销售团队数据
    df_sales = pd.read_sql_query("""
                                 SELECT u.id,
                                        u.full_name,
                                        u.department,
                                        COUNT(DISTINCT c.id)                                      as client_count,
                                        COUNT(DISTINCT o.id)                                      as opportunity_count,
                                        COALESCE(SUM(o.estimated_value), 0)                       as total_value,
                                        COALESCE(SUM(o.estimated_value * o.probability / 100), 0) as expected_revenue
                                 FROM users u
                                          LEFT JOIN clients c ON u.id = c.assigned_to
                                          LEFT JOIN opportunities o ON u.id = o.assigned_to
                                 WHERE u.role = '销售'
                                 GROUP BY u.id, u.full_name, u.department
                                 """, conn)

    if not df_sales.empty:
        # 团队总体表现
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("团队成员数", len(df_sales))
        with col2:
            st.metric("总客户数", df_sales['client_count'].sum())
        with col3:
            st.metric("总商机数", df_sales['opportunity_count'].sum())
        with col4:
            st.metric("预计总收入", f"¥{df_sales['expected_revenue'].sum():,.0f}")

        st.divider()

        # 个人业绩排行
        st.markdown("##### 🏅 个人业绩排行")

        tab1, tab2, tab3 = st.tabs(["客户数量", "预估金额", "预计收入"])

        with tab1:
            df_client_rank = df_sales.sort_values('client_count', ascending=False).head(10)
            fig1 = px.bar(
                df_client_rank,
                x='client_count',
                y='full_name',
                orientation='h',
                title='客户数量排行TOP10'
            )
            st.plotly_chart(fig1, width='stretch')

        with tab2:
            df_value_rank = df_sales.sort_values('total_value', ascending=False).head(10)
            fig2 = px.bar(
                df_value_rank,
                x='total_value',
                y='full_name',
                orientation='h',
                title='预估金额排行TOP10'
            )
            st.plotly_chart(fig2, width='stretch')

        with tab3:
            df_revenue_rank = df_sales.sort_values('expected_revenue', ascending=False).head(10)
            fig3 = px.bar(
                df_revenue_rank,
                x='expected_revenue',
                y='full_name',
                orientation='h',
                title='预计收入排行TOP10'
            )
            st.plotly_chart(fig3, width='stretch')

        # 部门表现对比
        st.markdown("##### 🏢 部门表现对比")
        dept_stats = df_sales.groupby('department').agg({
            'client_count': 'sum',
            'opportunity_count': 'sum',
            'total_value': 'sum',
            'expected_revenue': 'sum',
            'id': 'count'
        }).rename(columns={'id': 'member_count'})

        col1, col2 = st.columns(2)

        with col1:
            fig4 = px.pie(
                dept_stats,
                values='client_count',
                names=dept_stats.index,
                title='各部门客户数量分布'
            )
            st.plotly_chart(fig4, width='stretch')

        with col2:
            fig5 = px.pie(
                dept_stats,
                values='expected_revenue',
                names=dept_stats.index,
                title='各部门预计收入分布'
            )
            st.plotly_chart(fig5, width='stretch')

        # 详细数据
        with st.expander("查看详细数据"):
            st.dataframe(df_sales, width='stretch')
    else:
        st.info("暂无销售团队数据")


# ========== 12. 用户管理页面 ==========
def show_users():
    """显示用户管理页面"""
    if st.session_state.user['role'] != '管理员':
        st.warning("该功能仅限管理员使用")
        return

    st.markdown("""
    <div class="main-header">
        <h1>👤 用户管理</h1>
        <p>管理系统用户，分配权限</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["用户列表", "新增用户", "权限设置"])

    with tab1:
        show_user_list()
    with tab2:
        add_user()
    with tab3:
        show_permission_settings()


def show_user_list():
    """显示用户列表"""
    df_users = pd.read_sql_query("SELECT * FROM users ORDER BY role, username", conn)

    if not df_users.empty:
        # 用户统计
        admin_count = len(df_users[df_users['role'] == '管理员'])
        sales_count = len(df_users[df_users['role'] == '销售'])
        active_count = len(df_users[df_users['is_active'] == 1])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总用户数", len(df_users))
        with col2:
            st.metric("活跃用户", active_count)
        with col3:
            st.metric("销售人数", sales_count)

        st.divider()

        # 用户列表
        st.dataframe(
            df_users[['username', 'full_name', 'email', 'role', 'department', 'created_at', 'is_active']],
            column_config={
                "username": "用户名",
                "full_name": "姓名",
                "email": "邮箱",
                "role": "角色",
                "department": "部门",
                "created_at": "创建时间",
                "is_active": st.column_config.CheckboxColumn("状态", help="是否激活")
            },
            width='stretch'
        )

        # 用户操作
        st.markdown("### 🔧 用户操作")
        selected_id = st.selectbox("选择用户", df_users['id'].tolist(),
                                   format_func=lambda
                                       x: f"{df_users[df_users['id'] == x]['full_name'].iloc[0]} ({df_users[df_users['id'] == x]['username'].iloc[0]})")

        if selected_id:
            user = df_users[df_users['id'] == selected_id].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔒 重置密码", width='stretch'):
                    # 重置密码为默认密码
                    default_password = hashlib.sha256('123456'.encode()).hexdigest()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (default_password, selected_id))
                    conn.commit()
                    st.success(f"用户 '{user['username']}' 密码已重置为: 123456")

            with col2:
                new_status = not bool(user['is_active'])
                status_text = "激活" if new_status else "停用"
                if st.button(f"🔄 {status_text}用户", width='stretch'):
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (int(new_status), selected_id))
                    conn.commit()
                    st.success(f"用户 '{user['username']}' 已{status_text}")
                    st.rerun()
    else:
        st.info("暂无用户数据")


def add_user():
    """新增用户"""
    st.subheader("➕ 新增用户")

    with st.form("add_user_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            username = st.text_input("用户名*", placeholder="英文用户名，用于登录")
            full_name = st.text_input("姓名*", placeholder="用户真实姓名")
            email = st.text_input("邮箱*", placeholder="工作邮箱")
            phone = st.text_input("手机号", placeholder="11位手机号")

        with col2:
            role = st.selectbox("角色*", ["管理员", "销售", "客服", "技术支持"])
            department = st.selectbox("部门*", ["销售部", "市场部", "技术部", "客服部", "管理部"])
            password = st.text_input("初始密码*", type="password", value="123456")
            confirm_password = st.text_input("确认密码*", type="password", value="123456")

        is_active = st.checkbox("立即激活", value=True)

        submitted = st.form_submit_button("✅ 添加用户", type="primary")

        if submitted:
            if not all([username, full_name, email, role, department, password]):
                st.error("请填写所有带*的必填项")
            elif password != confirm_password:
                st.error("两次输入的密码不一致")
            else:
                try:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()

                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO users
                                      (username, password, full_name, email, phone, role, department, is_active)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (username, password_hash, full_name, email, phone or None,
                                    role, department, int(is_active)))
                    conn.commit()

                    st.success(f"✅ 用户 '{full_name}' 添加成功！")
                    st.balloons()
                except sqlite3.IntegrityError:
                    st.error("用户名已存在，请更换用户名")
                except Exception as e:
                    st.error(f"添加失败: {str(e)}")


def show_permission_settings():
    """显示权限设置"""
    st.subheader("⚙️ 权限设置")

    st.markdown("""
    ### 角色权限说明

    #### 👑 管理员
    - 管理所有用户
    - 查看所有数据
    - 系统设置
    - 数据导出

    #### 💼 销售
    - 管理自己的客户
    - 创建销售机会
    - 记录联系记录
    - 管理任务日程
    - 查看自己的业绩

    #### 📞 客服
    - 查看客户信息
    - 记录联系记录
    - 处理客户咨询
    - 创建服务任务

    #### 🔧 技术支持
    - 查看相关客户
    - 记录技术支持
    - 处理技术问题
    - 创建技术任务
    """)

    # 权限矩阵
    st.markdown("### 📊 权限矩阵")

    permission_matrix = pd.DataFrame({
        '功能': ['用户管理', '客户管理', '销售机会', '联系记录', '任务管理', '业绩分析', '数据导出'],
        '管理员': ['✅', '✅', '✅', '✅', '✅', '✅', '✅'],
        '销售': ['❌', '✅', '✅', '✅', '✅', '✅', '✅'],
        '客服': ['❌', '✅', '❌', '✅', '✅', '❌', '❌'],
        '技术支持': ['❌', '✅', '❌', '✅', '✅', '❌', '❌']
    })

    st.dataframe(permission_matrix.set_index('功能'), width='stretch')


def show_clients_page(subpage=""):
    """显示客户管理页面，支持子页面"""
    st.markdown("""
    <div class="main-header">
        <h1>👥 客户管理</h1>
        <p>管理客户信息，跟进客户状态</p>
    </div>
    """, unsafe_allow_html=True)

    # 如果从快速操作按钮进入，显示新增页面
    if subpage == "add":
        add_client()
        return

    # 子页面选择
    tab_labels = ["客户列表", "新增客户", "客户分析"]
    tab_selected = 0

    # 根据session state确定选中哪个tab
    if st.session_state.get('clients_subpage') == "list":
        tab_selected = 0
    elif st.session_state.get('clients_subpage') == "add":
        tab_selected = 1
    elif st.session_state.get('clients_subpage') == "analysis":
        tab_selected = 2

    # 使用tabs而不是radio，提供更好的用户体验
    tab1, tab2, tab3 = st.tabs(tab_labels)

    with tab1:
        st.session_state.clients_subpage = "list"
        show_client_list()

    with tab2:
        st.session_state.clients_subpage = "add"
        add_client()

    with tab3:
        st.session_state.clients_subpage = "analysis"
        show_client_analysis()


def show_opportunities_page(subpage=""):
    """显示销售机会页面，支持子页面"""
    st.markdown("""
    <div class="main-header">
        <h1>💼 销售机会管理</h1>
        <p>跟踪销售机会，预测销售业绩</p>
    </div>
    """, unsafe_allow_html=True)

    # 如果从快速操作按钮进入，显示新增页面
    if subpage == "add":
        add_opportunity()
        return

    # 子页面选择
    tab1, tab2, tab3 = st.tabs(["机会列表", "新增机会", "漏斗分析"])

    with tab1:
        st.session_state.opp_subpage = "list"
        show_opportunity_list()

    with tab2:
        st.session_state.opp_subpage = "add"
        add_opportunity()

    with tab3:
        st.session_state.opp_subpage = "funnel"
        show_funnel_analysis()


# 同样修改其他页面函数
def show_contacts_page(subpage=""):
    """显示联系记录页面，支持子页面"""
    st.markdown("""
    <div class="main-header">
        <h1>📞 联系记录</h1>
        <p>记录客户沟通，跟踪跟进进度</p>
    </div>
    """, unsafe_allow_html=True)

    if subpage == "add":
        add_contact()
        return

    tab1, tab2 = st.tabs(["记录列表", "新增记录"])

    with tab1:
        show_contact_list()

    with tab2:
        add_contact()


def show_tasks_page(subpage=""):
    """显示任务日程页面，支持子页面"""
    st.markdown("""
    <div class="main-header">
        <h1>📅 任务日程</h1>
        <p>管理待办任务，提高工作效率</p>
    </div>
    """, unsafe_allow_html=True)

    if subpage == "add":
        add_task()
        return

    tab1, tab2, tab3 = st.tabs(["我的任务", "新增任务", "任务统计"])

    with tab1:
        show_my_tasks()

    with tab2:
        add_task()

    with tab3:
        show_task_stats()

# ========== 13. 主程序入口 ==========
def main():
    """主程序入口"""
    # 检查用户认证
    if not check_auth():
        return

    # 调试信息
    st.sidebar.markdown(f"""
    <div style="background: #f0f2f6; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <small>调试信息</small><br>
        <small>当前页面: {st.session_state.get('page', 'dashboard')}</small><br>
        <small>子页面: {st.session_state.get('subpage', '')}</small>
    </div>
    """, unsafe_allow_html=True)

    # 初始化session state
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    if 'subpage' not in st.session_state:
        st.session_state.subpage = ""

    # 显示侧边栏并获取当前页面
    selected_page = show_sidebar()

    # 更新页面状态
    if selected_page and st.session_state.page != selected_page:
        st.session_state.page = selected_page
        st.session_state.subpage = ""

    # 根据选择显示对应页面
    current_page = st.session_state.page
    current_subpage = st.session_state.subpage

    # 页面路由映射
    page_map = {
        "dashboard": show_dashboard,
        "clients": lambda: show_clients_page(current_subpage),
        "opportunities": lambda: show_opportunities_page(current_subpage),
        "contacts": lambda: show_contacts_page(current_subpage),
        "tasks": lambda: show_tasks_page(current_subpage),
        "analytics": show_analytics,
        "users": show_users
    }

    if current_page in page_map:
        page_map[current_page]()
    else:
        show_dashboard()

    # # 根据选择显示对应页面
    # page_map = {
    #     "📊 仪表盘": show_dashboard,
    #     "👥 客户管理": show_clients,
    #     "💼 销售机会": show_opportunities,
    #     "📞 联系记录": show_contacts,
    #     "📅 任务日程": show_tasks,
    #     "📈 业绩分析": show_analytics,
    #     "👤 用户管理": show_users
    # }
    #
    # current_page = st.session_state.page
    #
    # if current_page in page_map:
    #     # 根据子页面显示不同内容
    #     if current_page == "clients" and st.session_state.subpage == "add":
    #         add_client()
    #     elif current_page == "opportunities" and st.session_state.subpage == "add":
    #         add_opportunity()
    #     else:
    #         page_map[current_page]()
    # else:
    #     show_dashboard()  # 默认显示仪表盘

    # 页脚
    st.divider()
    st.markdown(f"""
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
        <p>🤝 CRM客户关系管理系统 v1.0 | 当前用户: {st.session_state.user['full_name']} | 角色: {st.session_state.user['role']}</p>
        <p>📅 系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 如有问题请联系技术支持</p>
    </div>
    """, unsafe_allow_html=True)

    # 导出数据功能（管理员可用）
    if st.session_state.user['role'] == '管理员':
        with st.sidebar.expander("📤 数据导出"):
            export_type = st.selectbox("导出类型", ["客户数据", "销售机会", "联系记录", "任务数据"])
            if st.button("导出数据"):
                table_map = {
                    "客户数据": "clients",
                    "销售机会": "opportunities",
                    "联系记录": "contacts",
                    "任务数据": "tasks"
                }

                df = pd.read_sql_query(f"SELECT * FROM {table_map[export_type]}", conn)

                # 转换为CSV
                csv = df.to_csv(index=False).encode('utf-8-sig')

                # 提供下载链接
                st.download_button(
                    label=f"下载 {export_type} CSV",
                    data=csv,
                    file_name=f"{export_type}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )


# 运行主程序
if __name__ == "__main__":
    main()