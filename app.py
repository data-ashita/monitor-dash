# -*- coding: utf-8 -*-
"""
Task Logs Dashboard - Streamlit Application (English Version)

Features:
- Simple task logs table
- Script execution statistics
- Error/failure alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client

# Set page config
st.set_page_config(
    page_title="Task Logs Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Supabase configuration
LOGGER_SUPABASE_URL = os.getenv("LOGGER_SUPABASE_URL")
LOGGER_SUPABASE_KEY = os.getenv("LOGGER_SUPABASE_KEY")

# Initialize Supabase client
@st.cache_resource
def get_supabase_client():
    """Get Supabase client"""
    if not LOGGER_SUPABASE_URL or not LOGGER_SUPABASE_KEY:
        st.error("❌ Error: Supabase credentials not configured. Please check .env file.")
        st.stop()
    return create_client(LOGGER_SUPABASE_URL, LOGGER_SUPABASE_KEY)

# Fetch data
@st.cache_data(ttl=60)
def fetch_task_logs(days=7):
    """Fetch task logs from Supabase"""
    try:
        supabase = get_supabase_client()
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query data
        response = supabase.table('task_logs') \
            .select('*') \
            .gte('created_at', start_date.isoformat()) \
            .lte('created_at', end_date.isoformat()) \
            .order('created_at', desc=True) \
            .execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Convert timestamp
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['timestamp'] = df['created_at']
            return df
        else:
            return pd.DataFrame()
    
    except Exception as e:
        st.error(f"❌ Failed to fetch data: {str(e)}")
        return pd.DataFrame()

# Page title
st.title("📊 Task Logs Dashboard")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Time range selection
    days = st.slider(
        "Select time range (days)",
        min_value=1,
        max_value=30,
        value=7,
        step=1
    )
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Fetch data
df = fetch_task_logs(days=days)

if df.empty:
    st.warning("⚠️ No data available. Please ensure scripts have been executed.")
else:
    # ==================== ALERTS ====================
    st.markdown("### 🚨 Alerts")
    
    # Check for errors/failures
    error_df = df[df['level'].isin(['ERROR', 'CRITICAL'])].copy()
    
    if not error_df.empty:
        error_count = len(error_df)
        failed_scripts = error_df['task_name'].unique().tolist()
        
        alert_message = f"⚠️ **{error_count} task(s) failed!** Failed scripts: {', '.join(failed_scripts)}"
        st.error(alert_message)
    else:
        st.success("✅ All tasks are running successfully!")
    
    st.markdown("---")
    
    # ==================== KEY METRICS ====================
    st.markdown("### 📈 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_runs = len(df)
        st.metric("Total Runs", total_runs)
    
    with col2:
        success_count = len(df[df['level'] == 'INFO'])
        st.metric("Success", success_count)
    
    with col3:
        error_count = len(df[df['level'].isin(['ERROR', 'CRITICAL'])])
        st.metric("Failed", error_count)
    
    with col4:
        success_rate = (success_count / total_runs * 100) if total_runs > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col5:
        unique_scripts = df['task_name'].nunique()
        st.metric("Total Scripts", unique_scripts)
    
    st.markdown("---")
    
    # ==================== TASK LOGS TABLE ====================
    st.markdown("### 📋 Task Logs")
    
    # Get latest run for each task
    latest_runs = df.sort_values('created_at', ascending=False).drop_duplicates('task_name')
    
    # Prepare table data
    table_data = []
    for idx, row in latest_runs.iterrows():
        # Get task status (based on level)
        status = "✅ Success" if row['level'] == 'INFO' else f"❌ {row['level']}"
        
        # Get message (only for errors)
        message = row['message'] if row['level'] in ['ERROR', 'CRITICAL'] else "-"
        
        # Format last run time
        last_run = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        table_data.append({
            'Task Name': row['task_name'],
            'Status': status,
            'Message': message,
            'Run Source': row['run_source'],
            'Last Run': last_run
        })
    
    # Create DataFrame for display
    display_df = pd.DataFrame(table_data)
    
    # Display table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.markdown("---")
    
    # ==================== SCRIPT STATISTICS ====================
    st.markdown("### 📊 Script Execution Statistics")
    
    # Calculate statistics for each script
    script_stats = []
    for script_name in sorted(df['task_name'].unique()):
        script_df = df[df['task_name'] == script_name]
        
        total = len(script_df)
        success = len(script_df[script_df['level'] == 'INFO'])
        error = len(script_df[script_df['level'].isin(['ERROR', 'CRITICAL'])])
        success_rate = (success / total * 100) if total > 0 else 0
        
        script_stats.append({
            'Script': script_name,
            'Total Runs': total,
            'Success': success,
            'Failed': error,
            'Success Rate': f"{success_rate:.1f}%"
        })
    
    stats_df = pd.DataFrame(script_stats)
    
    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.markdown("---")
    
    # ==================== EXECUTION TRENDS ====================
    st.markdown("### 📈 Execution Trends")
    
    col1, col2 = st.columns(2)
    
    # Daily execution trend
    with col1:
        daily_stats = df.groupby(df['created_at'].dt.date).size()
        fig_trend = px.line(
            x=daily_stats.index,
            y=daily_stats.values,
            labels={'x': 'Date', 'y': 'Executions'},
            title="Daily Execution Count",
            markers=True
        )
        fig_trend.update_layout(height=350)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Success/Failure distribution
    with col2:
        level_stats = df['level'].value_counts()
        colors = {'INFO': '#00CC96', 'ERROR': '#EF553B', 'CRITICAL': '#AB63FA'}
        fig_pie = px.pie(
            values=level_stats.values,
            names=level_stats.index,
            title="Execution Result Distribution",
            color_discrete_map=colors
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888;'><p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p></div>", unsafe_allow_html=True)