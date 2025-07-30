import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import re

# Set page config
st.set_page_config(
    page_title="LTE Network Monitoring Dashboard",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    :root {
        --primary: #1e3a8a;
        --secondary: #3b82f6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #1f2937;
        --light: #f9fafb;
    }
    
    body {
        background-color: #f0f2f6;
        color: var(--dark);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 4px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .metric-title {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6b7280;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    
    .metric-change {
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .kpi-card h3 {
        color: var(--primary);
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.75rem;
        margin-top: 0;
        font-weight: 600;
    }
    
    .last-updated {
        background: var(--dark);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stButton button {
        background: var(--primary) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    
    .stButton button:hover {
        background: var(--secondary) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4) !important;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-up {
        background-color: var(--success);
    }
    
    .status-warning {
        background-color: var(--warning);
    }
    
    .status-down {
        background-color: var(--danger);
    }
    
    .cell-health {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-radius: 8px;
        background-color: white;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .health-bar {
        height: 8px;
        border-radius: 5px;
        margin-top: 8px;
        background: linear-gradient(90deg, var(--success), var(--warning), var(--danger));
        position: relative;
        overflow: hidden;
    }
    
    .health-bar-fill {
        height: 100%;
        border-radius: 5px;
        background: var(--primary);
    }
    
    .health-metric {
        display: flex;
        justify-content: space-between;
        margin-top: 0.75rem;
        font-size: 0.85rem;
    }
    
    /* Table styling */
    .dataframe {
        width: 100% !important;
        font-size: 0.85rem;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background-color: var(--primary);
        color: white;
        padding: 0.75rem;
        text-align: left;
        font-weight: 600;
        position: sticky;
        top: 0;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .dataframe tr:hover {
        background-color: #f0f7ff;
    }
    
    /* Critical value highlighting */
    .highlight-critical {
        background-color: #ffebee !important;
        color: #c62828 !important;
        font-weight: bold !important;
    }
    
    /* KPI table container */
    .kpi-table-container {
        margin-bottom: 2rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Responsive table container */
    .table-container {
        width: 100%;
        overflow-x: auto;
        border-radius: 8px;
        background: white;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        height: 8px;
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Section headers */
    .section-header {
        color: var(--primary);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    .section-header-icon {
        margin-right: 0.75rem;
        font-size: 1.5rem;
    }
    
    /* Tooltip styling */
    .stTooltip {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to clean column names while preserving original for display
def clean_column_name(name):
    """Remove problematic characters but keep original for display"""
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_').replace('.', '_'))

# Function to process uploaded file with robust type handling
def process_uploaded_file(uploaded_file):
    try:
        # Read the CSV file with proper encoding and handle BOM
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        # Clean column names (remove BOM if present)
        df.columns = [col.strip('\ufeff') for col in df.columns]
        
        # Store original column names for display
        original_columns = df.columns.tolist()
        
        # Clean column names for internal processing
        clean_columns = [clean_column_name(col) for col in df.columns]
        df.columns = clean_columns
        
        # Create mapping from clean to original names
        col_mapping = dict(zip(clean_columns, original_columns))
        
        # Convert timestamp to datetime
        timestamp_col = None
        for col in df.columns:
            if 'Timestamp' in col:
                timestamp_col = col
                break
                
        if timestamp_col:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            # Extract time component for display
            df['Time'] = df[timestamp_col].dt.strftime('%H:%M')
        else:
            st.error("Timestamp column not found")
            return None, None
        
        # Define numeric and percentage columns
        numeric_cols = ['RRC_Attempt', 'ERAB_Attempt', 'QCI1_Attempt']
        percentage_cols = ['RRC_Setup_SR', 'ERAB_Setup_SR', 'Session_Drop_Rate', 
                          'QCI1_SR', 'QCI1_Drop_Rate', 'Availability']
        other_numeric_cols = ['Max_User', 'AVG_Users', 'Number_of_Drop', 'QCI1_abnormal_release',
                         'DL_Trafic_Volume_MB', 'UL_Trafic_Volume_MB', 'Avg_VoLTE_Users']
        
        # Function to convert to numeric, handling non-numeric and dashes
        def to_numeric(series):
            # If the series is string, replace commas and dashes
            if series.dtype == 'object':
                series = series.astype(str).str.replace(',', '')
                series = series.replace('-', np.nan)
                series = series.replace('', np.nan)
            return pd.to_numeric(series, errors='coerce')
        
        # Convert numeric columns
        for col in numeric_cols + other_numeric_cols:
            if col in df.columns:
                df[col] = to_numeric(df[col])
        
        # Convert percentage columns
        for col in percentage_cols:
            if col in df.columns:
                # If it's a string, remove percentage signs and dashes
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace('%', '')
                    df[col] = df[col].replace('-', np.nan)
                    df[col] = df[col].replace('', np.nan)
                df[col] = to_numeric(df[col])
        
        # Fill remaining NaN values with 0
        df.fillna(0, inplace=True)
        
        return df, col_mapping
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None, None

# Function to create gauge chart
def create_gauge(value, min_val, max_val, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#1e3a8a"},
            'steps': [
                {'range': [min_val, min_val + (max_val-min_val)/3], 'color': "#f0f9ff"},
                {'range': [min_val + (max_val-min_val)/3, min_val + 2*(max_val-min_val)/3], 'color': "#e1f0ff"},
                {'range': [min_val + 2*(max_val-min_val)/3, max_val], 'color': "#cfe5ff"}
            ],
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=50, b=10),
        font=dict(family="Inter")
    )
    return fig

# Function to calculate status indicator
def get_status_indicator(value, warning_threshold, danger_threshold, reverse=False):
    if reverse:
        if value > danger_threshold:
            return "status-down", "Critical"
        elif value > warning_threshold:
            return "status-warning", "Warning"
        else:
            return "status-up", "Normal"
    else:
        if value < danger_threshold:
            return "status-down", "Critical"
        elif value < warning_threshold:
            return "status-warning", "Warning"
        else:
            return "status-up", "Normal"

# Function to create cell health indicator
def create_cell_health(cell_name, availability, rrc_sr, drop_rate):
    # Calculate health score (simple average for demo)
    health_score = (availability + rrc_sr + (100 - drop_rate * 10)) / 3
    
    # Create health bar
    health_html = f"""
    <div class="cell-health">
        <div style="flex-grow: 1;">
            <strong>{cell_name}</strong>
            <div class="health-bar">
                <div class="health-bar-fill" style="width: {health_score}%"></div>
            </div>
            <div class="health-metric">
                <span>Avail: {availability:.1f}%</span>
                <span>RRC: {rrc_sr:.1f}%</span>
                <span>Drops: {drop_rate:.2f}%</span>
            </div>
        </div>
        <div style="margin-left: 1rem; font-weight: bold; font-size: 1.2rem; color: {'#10b981' if health_score > 85 else '#f59e0b' if health_score > 70 else '#ef4444'}">
            {health_score:.0f}
        </div>
    </div>
    """
    return health_html

# Function to apply highlighting to DataFrame (using Styler.map instead of deprecated applymap)
def highlight_critical_values(val, column_name):
    """
    Apply highlighting based on column name and value thresholds
    """
    if pd.isna(val):
        return ''
    
    # Success Rate highlighting (red background for < 99)
    if column_name in ['RRC_Setup_SR', 'ERAB_Setup_SR', 'QCI1_SR'] and val < 99:
        return 'background-color: #ffebee; color: #c62828; font-weight: bold;'
    
    # Drop Rate highlighting (red background for > 0.99)
    if column_name in ['Session_Drop_Rate', 'QCI1_Drop_Rate'] and val > 0.99:
        return 'background-color: #ffebee; color: #c62828; font-weight: bold;'
    
    # Traffic Volume highlighting (red background for < 1)
    if column_name == 'DL_Trafic_Volume_MB' and val < 1:
        return 'background-color: #ffebee; color: #c62828; font-weight: bold;'
    
    # Zero values highlighting (red background for 0)
    if column_name == 'AVG_Users' and val == 0:
        return 'background-color: #ffebee; color: #c62828; font-weight: bold;'
    
    return ''

# Main app
def main():
    # Header section
    st.markdown('<div class="header"><h1>📶 LTE Network Monitoring Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Create columns for header info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-top: -10px;">
            <span class="status-indicator status-up"></span>
            <span>All systems operational</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        refresh_btn = st.button("🔄 Refresh Data")
    
    # File upload
    with st.sidebar:
        st.subheader("Data Management")
        uploaded_file = st.file_uploader(
            "Upload LTE KPI Data", 
            type=["csv"],
            help="Upload the LTE KPI data file in CSV format"
        )
        
        st.markdown("---")
        st.subheader("Network Filters")
        
        col_mapping = None
        
        if uploaded_file is not None:
            df, col_mapping = process_uploaded_file(uploaded_file)
            
            if df is not None and col_mapping is not None:
                # Extract unique sectors
                df['sector'] = df['lte_cell_name'].str[:5]
                sectors = sorted(df['sector'].unique())
                
                # Sector selection
                selected_sector = st.selectbox(
                    "Select Sector", 
                    options=sectors,
                    index=0,
                    help="Select the sector to analyze"
                )
                
                # Filter cells based on selected sector
                sector_cells = sorted(df[df['sector'] == selected_sector]['lte_cell_name'].unique())
                
                # Cell selection
                selected_cells = st.multiselect(
                    "Select Cells", 
                    options=sector_cells,
                    default=sector_cells,
                    help="Select specific cells to analyze"
                )
                
                # Date range selector
                min_date = df['Timestamp_per_15_minutes'].min()
                max_date = df['Timestamp_per_15_minutes'].max()
                
                selected_dates = st.date_input(
                    "Select Date Range",
                    value=[min_date, max_date],
                    min_value=min_date,
                    max_value=max_date,
                    help="Select the date range for analysis"
                )
                
                # KPI selection - pre-select important KPIs
                default_kpis = [
                    'Availability',
                    'RRC_Setup_SR',
                    'ERAB_Setup_SR',
                    'DL_Trafic_Volume_MB',
                    'Session_Drop_Rate',
                    'QCI1_SR',
                    'QCI1_Drop_Rate',
                    'AVG_Users'
                ]
                
                # Get all available KPIs
                kpi_list = [
                    'Max_User', 'AVG_Users', 'Number_of_Drop', 'QCI1_abnormal_release',
                    'Availability', 'RRC_Attempt', 'RRC_Setup_SR', 'ERAB_Attempt',
                    'ERAB_Setup_SR', 'DL_Trafic_Volume_MB', 'UL_Trafic_Volume_MB',
                    'Session_Drop_Rate', 'QCI1_Attempt', 'QCI1_SR', 'Avg_VoLTE_Users',
                    'QCI1_Drop_Rate'
                ]
                
                # Get display names from mapping
                kpi_display_names = [col_mapping.get(kpi, kpi.replace('_', ' ')) for kpi in kpi_list]
                
                # Map default KPIs to display names
                default_display_names = [col_mapping.get(kpi, kpi.replace('_', ' ')) for kpi in default_kpis]
                
                selected_kpis = st.multiselect(
                    "Select KPIs to Display",
                    options=kpi_display_names,
                    default=default_display_names,
                    help="Select KPIs to display in the dashboard"
                )
                
                # Map back to internal names
                reverse_mapping = {v: k for k, v in col_mapping.items()}
                selected_kpi_codes = [reverse_mapping.get(kpi, clean_column_name(kpi)) for kpi in selected_kpis]
                
                # Threshold settings
                st.markdown("---")
                st.subheader("Alert Thresholds")
                availability_warning = st.slider("Availability Warning Threshold (%)", 90, 99, 95)
                rrc_sr_warning = st.slider("RRC Setup SR Warning Threshold (%)", 90, 99, 95)
                drop_rate_warning = st.slider("Drop Rate Warning Threshold (%)", 1, 10, 5)
                
                # Last updated info
                st.markdown("---")
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(f"<div class='last-updated'>Last Updated: {now}</div>", unsafe_allow_html=True)
    
    # Main content
    if uploaded_file is not None and df is not None and col_mapping is not None:
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)
            
            # Filter data based on selections
            filtered_df = df[
                (df['lte_cell_name'].isin(selected_cells)) &
                (df['Timestamp_per_15_minutes'] >= start_date) &
                (df['Timestamp_per_15_minutes'] <= end_date)
            ].copy()
            
            if not filtered_df.empty:
                # Create summary cards with requested metrics
                st.markdown('<div class="section-header"><span class="section-header-icon">📊</span> Network Performance Summary</div>', unsafe_allow_html=True)
                
                # Calculate summary metrics
                avg_availability = filtered_df['Availability'].mean()
                avg_rrc_sr = filtered_df['RRC_Setup_SR'].mean()
                avg_erab_sr = filtered_df['ERAB_Setup_SR'].mean()
                avg_dl_traffic = filtered_df['DL_Trafic_Volume_MB'].mean()
                avg_drop_rate = filtered_df['Session_Drop_Rate'].mean()
                avg_qci1_sr = filtered_df['QCI1_SR'].mean()
                
                # Create columns for summary metrics
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    avail_status, avail_text = get_status_indicator(avg_availability, availability_warning, 90)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Availability</div>
                        <div class="metric-value">{avg_availability:.2f}%</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{avail_status}"></span>
                            <span class="metric-change">{avail_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    rrc_status, rrc_text = get_status_indicator(avg_rrc_sr, rrc_sr_warning, 90)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">RRC SR</div>
                        <div class="metric-value">{avg_rrc_sr:.2f}%</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{rrc_status}"></span>
                            <span class="metric-change">{rrc_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    erab_status, erab_text = get_status_indicator(avg_erab_sr, rrc_sr_warning, 90)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">ERAB SR</div>
                        <div class="metric-value">{avg_erab_sr:.2f}%</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{erab_status}"></span>
                            <span class="metric-change">{erab_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    dl_status, dl_text = get_status_indicator(avg_dl_traffic, 5, 1, reverse=True)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">DL Traffic</div>
                        <div class="metric-value">{avg_dl_traffic:.2f} MB</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{dl_status}"></span>
                            <span class="metric-change">{dl_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    drop_status, drop_text = get_status_indicator(avg_drop_rate, drop_rate_warning, drop_rate_warning*2, reverse=True)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Drop Rate</div>
                        <div class="metric-value">{avg_drop_rate:.2f}%</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{drop_status}"></span>
                            <span class="metric-change">{drop_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col6:
                    qci1_status, qci1_text = get_status_indicator(avg_qci1_sr, rrc_sr_warning, 90)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">QCI1 SR</div>
                        <div class="metric-value">{avg_qci1_sr:.2f}%</div>
                        <div style="display: flex; align-items: center;">
                            <span class="{qci1_status}"></span>
                            <span class="metric-change">{qci1_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Create gauge charts
                st.markdown('<div class="section-header"><span class="section-header-icon">📈</span> Key Performance Indicators</div>', unsafe_allow_html=True)
                g1, g2, g3, g4 = st.columns(4)
                
                with g1:
                    fig = create_gauge(avg_availability, 0, 100, "Availability")
                    st.plotly_chart(fig, use_container_width=True)
                
                with g2:
                    fig = create_gauge(avg_rrc_sr, 0, 100, "RRC Success Rate")
                    st.plotly_chart(fig, use_container_width=True)
                
                with g3:
                    fig = create_gauge(avg_erab_sr, 0, 100, "ERAB Success Rate")
                    st.plotly_chart(fig, use_container_width=True)
                
                with g4:
                    fig = create_gauge(avg_drop_rate, 0, 20, "Drop Rate")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Cell health status
                st.markdown('<div class="section-header"><span class="section-header-icon">🏥</span> Cell Health Status</div>', unsafe_allow_html=True)
                health_cols = st.columns(3)
                
                # Get latest data for each cell
                latest_data = filtered_df.sort_values('Timestamp_per_15_minutes').groupby('lte_cell_name').last().reset_index()
                
                for idx, row in latest_data.iterrows():
                    with health_cols[idx % 3]:
                        health_html = create_cell_health(
                            row['lte_cell_name'],
                            row['Availability'],
                            row['RRC_Setup_SR'],
                            row['Session_Drop_Rate']
                        )
                        st.markdown(health_html, unsafe_allow_html=True)
                
                # Create grid of KPI charts - 2 per row
                st.markdown('<div class="section-header"><span class="section-header-icon">📊</span> Detailed KPI Analysis</div>', unsafe_allow_html=True)

                # Split selected KPIs into pairs for 2-column layout
                kpi_pairs = [selected_kpi_codes[i:i + 2] for i in range(0, len(selected_kpi_codes), 2)]

                for pair in kpi_pairs:
                    cols = st.columns(2)
                    for idx, kpi_code in enumerate(pair):
                        with cols[idx]:
                            # Get display name for the KPI
                            display_name = col_mapping.get(kpi_code, kpi_code.replace('_', ' '))
                            
                            # Create KPI card
                            st.markdown(f'<div class="kpi-card">', unsafe_allow_html=True)
                            st.markdown(f"<h3>{display_name}</h3>", unsafe_allow_html=True)
                            
                            # Time series plot
                            fig = px.line(
                                filtered_df,
                                x='Timestamp_per_15_minutes',
                                y=kpi_code,
                                color='lte_cell_name',
                                labels={
                                    'Timestamp_per_15_minutes': 'Time',
                                    kpi_code: display_name,
                                    'lte_cell_name': 'Cell Name'
                                },
                                height=300
                            )
                            fig.update_layout(
                                hovermode="x unified",
                                legend_title_text='Cell Name',
                                margin=dict(l=20, r=20, t=30, b=20),
                                showlegend=False,
                                font=dict(family="Inter")
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                # Now show all KPI tables in order after all graphs
                st.markdown('<div class="section-header"><span class="section-header-icon">📋</span> Detailed KPI Tables</div>', unsafe_allow_html=True)
                
                for kpi_code in selected_kpi_codes:
                    # Get display name for the KPI
                    display_name = col_mapping.get(kpi_code, kpi_code.replace('_', ' '))
                    
                    st.markdown(f"**{display_name}**")
                    
                    # Pivot table for the KPI with highlighting
                    pivot_df = filtered_df.pivot_table(
                        index='lte_cell_name',
                        columns='Time',
                        values=kpi_code,
                        aggfunc='first'
                    ).reset_index()

                    # Rename columns for display
                    pivot_df = pivot_df.rename(columns={'lte_cell_name': 'Cell Name'})

                    # Ensure all values (except first column) are numeric to avoid comparison errors
                    for col in pivot_df.columns[1:]:
                        pivot_df[col] = pd.to_numeric(pivot_df[col], errors='coerce')

                    # Create a style function that applies our highlighting
                    def style_kpi_table(s):
                        return s.map(lambda x: highlight_critical_values(x, kpi_code))
                    
                    # Apply the styling using Styler.map (replacing deprecated applymap)
                    styled_df = pivot_df.style.apply(style_kpi_table, subset=pivot_df.columns[1:])
                    
                    # Display the styled DataFrame in a container with proper scrolling
                    with st.container():
                        st.markdown(f'<div class="table-container">', unsafe_allow_html=True)
                        st.dataframe(
                            styled_df,
                            height=min(400, (len(pivot_df) + 1) * 35 + 3),
                            use_container_width=True
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")  # Add separator between tables
                
            else:
                st.warning("No data available for the selected filters.")
        else:
            st.warning("Please select a valid date range.")
    elif uploaded_file is None:
        # Show sample data and instructions
        st.info("Please upload a CSV file to begin analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            ### Expected File Format
            The CSV file should contain LTE KPI data with these columns:
            - Timestamp per 15 minutes
            - lte_cell_name
            - Max_User
            - AVG_Users
            - Number of Drop
            - QCI1 abnormal release
            - Availability
            - RRC_Attempt
            - RRC_Setup_SR
            - ERAB_Attempt
            - ERAB_Setup_SR
            - DL_Trafic_Volume MB
            - UL_Trafic_Volume MB
            - Session_Drop_Rate
            - QCI1 Attempt
            - QCI1 SR
            - Avg_VoLTE_Users
            - QCI1 Drop Rate
            """)
    
    # Handle refresh button
    if refresh_btn:
        st.rerun()

if __name__ == "__main__":
    main()
