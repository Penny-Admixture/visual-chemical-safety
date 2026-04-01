"""
Visual Chemical Safety System
Based on: Kathy J. Malone, ManGuard Systems, Inc.
Core Principle: "It's What the Worker Understands That Matters"

Streamlit deployment for workplace chemical safety visualization
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Visual Chemical Safety",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    .chemical-name {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1f2937;
    }
    .chemical-formula {
        font-family: monospace;
        font-size: 1.2rem;
        color: #6b7280;
    }
    .warning-box {
        background-color: #fef3c7;
        border: 4px solid #f59e0b;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .critical-warning {
        background-color: #fee2e2;
        border: 4px solid #dc2626;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #dbeafe;
        border: 2px solid #3b82f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    .ppe-icon {
        font-size: 3rem;
        text-align: center;
        padding: 1rem;
        background-color: #f3f4f6;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .hazard-label {
        font-size: 0.875rem;
        font-weight: 600;
        text-align: center;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_speedometer(value, label):
    """
    Create hazard magnitude speedometer
    No numbers (avoids GHS 1=highest vs NFPA 4=highest confusion)
    Line thickness increases with severity (color-blind accessible)
    """
    # Map text levels to numeric values
    level_map = {'none': 0, 'low': 1, 'medium': 2, 'high': 3}
    numeric_value = level_map.get(value.lower(), 0)
    
    # Color and position mapping
    if numeric_value == 1:  # Low
        color = '#22c55e'
        angle = 60
    elif numeric_value == 2:  # Medium
        color = '#eab308'
        angle = 120
    elif numeric_value == 3:  # High
        color = '#ef4444'
        angle = 180
    else:  # None
        color = '#9ca3af'
        angle = 0
    
    fig = go.Figure()
    
    # Add gauge
    fig.add_trace(go.Indicator(
        mode="gauge",
        value=angle,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 180], 'visible': False},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': '#f3f4f6',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 60], 'color': '#dcfce7', 'line': {'width': numeric_value == 1 and 4 or 1}},
                {'range': [60, 120], 'color': '#fef9c3', 'line': {'width': numeric_value == 2 and 4 or 1}},
                {'range': [120, 180], 'color': '#fee2e2', 'line': {'width': numeric_value == 3 and 4 or 1}}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': angle
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'text': label, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#4b5563'}}
    )
    
    return fig

def create_clock_visual(minutes):
    """
    Create time-based instruction clock (15-minute rinse example)
    Both analog AND digital (accommodate different worker preferences)
    """
    import numpy as np
    
    # Calculate arc angle
    arc_angle = (minutes / 60) * 360
    
    # Create clock face
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    
    # Arc for highlighted time
    arc_theta = np.linspace(0, (arc_angle * np.pi / 180), 50)
    x_arc = np.append([0], np.cos(arc_theta - np.pi/2))
    y_arc = np.append([0], np.sin(arc_theta - np.pi/2))
    
    fig = go.Figure()
    
    # Clock circle
    fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        line=dict(color='#374151', width=3),
        fill='toself',
        fillcolor='white',
        showlegend=False
    ))
    
    # Highlighted arc
    fig.add_trace(go.Scatter(
        x=x_arc, y=y_arc,
        mode='lines',
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.3)',
        line=dict(color='rgba(59, 130, 246, 0.5)', width=1),
        showlegend=False
    ))
    
    # Hour hand (pointing up)
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[0, 0.7],
        mode='lines',
        line=dict(color='#374151', width=4),
        showlegend=False
    ))
    
    # Minute hand (pointing to target time)
    minute_x = 0.9 * np.sin(arc_angle * np.pi / 180)
    minute_y = 0.9 * np.cos(arc_angle * np.pi / 180)
    fig.add_trace(go.Scatter(
        x=[0, minute_x], y=[0, minute_y],
        mode='lines',
        line=dict(color='#ef4444', width=3),
        showlegend=False
    ))
    
    # Center dot
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(color='#374151', size=10),
        showlegend=False
    ))
    
    fig.update_layout(
        height=200,
        width=200,
        xaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'text': f"{minutes:02d}:00 minutes", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16, 'color': '#3b82f6', 'family': 'monospace'}}
    )
    
    return fig

# ============================================================================
# CHEMICAL DATABASE
# ============================================================================

CHEMICALS_DATABASE = {
    'bleach': {
        'name': 'Bleach',
        'formula': 'NaClO',
        'cas': '7681-52-9',
        'category': 'Corrosive',
        'template': 'hypochlorite',
        
        'properties': {
            'pH': 12.5,
            'flash_point': None,
            'specific_gravity': 1.2,
            'state': 'liquid',
            'appearance': 'Clear to pale yellow liquid',
            'odor': 'Chlorine odor'
        },
        
        'hazards': {
            'skin': {'level': 'medium', 'description': 'Causes skin irritation'},
            'eyes': {'level': 'high', 'description': 'Causes serious eye damage'},
            'inhalation': {'level': 'medium', 'description': 'May cause respiratory irritation'},
            'ingestion': {'level': 'high', 'description': 'Harmful if swallowed'}
        },
        
        'first_aid': {
            'skin': {'action': 'Rinse skin immediately', 'duration': 15, 'seek_help': False},
            'eyes': {'action': 'Rinse eyes continuously', 'duration': 15, 'seek_help': True},
            'inhalation': {'action': 'Move to fresh air immediately', 'seek_help': True},
            'ingestion': {'action': 'Call Poison Control immediately. Do NOT induce vomiting.', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Chemical splash goggles', 'required': True},
            {'icon': '🧤', 'label': 'Nitrile gloves', 'required': True},
            {'icon': '🦺', 'label': 'Chemical-resistant apron', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Ammonia', 'reaction': 'Toxic gas (chloramine)', 'severity': 'CRITICAL'},
            {'substance': 'Acids', 'reaction': 'Toxic chlorine gas', 'severity': 'CRITICAL'}
        ],
        
        'storage': 'Store in cool, dry, ventilated area away from incompatible materials',
        'disposal': 'Neutralize before disposal. Follow EPA guidelines.',
        'contraindications': ['Asthma or respiratory conditions', 'Skin sensitivity or dermatitis']
    },
    
    'acetone': {
        'name': 'Acetone',
        'formula': 'C₃H₆O',
        'cas': '67-64-1',
        'category': 'Flammable',
        'template': 'ketone_solvent',
        
        'properties': {
            'pH': 7.0,
            'flash_point': -4,
            'specific_gravity': 0.79,
            'state': 'liquid',
            'appearance': 'Clear, colorless liquid',
            'odor': 'Sweet, fruity odor'
        },
        
        'hazards': {
            'skin': {'level': 'low', 'description': 'May cause skin irritation with prolonged contact'},
            'eyes': {'level': 'medium', 'description': 'Causes serious eye irritation'},
            'inhalation': {'level': 'medium', 'description': 'May cause drowsiness or dizziness'},
            'ingestion': {'level': 'medium', 'description': 'Harmful if swallowed'}
        },
        
        'first_aid': {
            'skin': {'action': 'Wash with soap and water', 'duration': None, 'seek_help': False},
            'eyes': {'action': 'Rinse eyes continuously', 'duration': 15, 'seek_help': True},
            'inhalation': {'action': 'Move to fresh air. Monitor breathing.', 'seek_help': True},
            'ingestion': {'action': 'Call Poison Control. Do NOT induce vomiting.', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Safety glasses', 'required': True},
            {'icon': '🧤', 'label': 'Nitrile gloves', 'required': True},
            {'icon': '💨', 'label': 'Use in ventilated area', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Strong oxidizers', 'reaction': 'Fire/explosion risk', 'severity': 'HIGH'},
            {'substance': 'Strong acids/bases', 'reaction': 'Violent reaction', 'severity': 'MEDIUM'}
        ],
        
        'storage': 'Store in cool, well-ventilated area away from heat, sparks, open flames. Keep container tightly closed.',
        'disposal': 'Dispose as hazardous waste. Do not pour down drain.',
        'contraindications': ['Pregnancy (avoid prolonged exposure)', 'Liver or kidney conditions']
    },
    
    'ammonia': {
        'name': 'Ammonia',
        'formula': 'NH₃',
        'cas': '7664-41-7',
        'category': 'Toxic',
        'template': 'caustic_alkaline',
        
        'properties': {
            'pH': 11.6,
            'flash_point': None,
            'specific_gravity': 0.90,
            'state': 'liquid (aqueous solution)',
            'appearance': 'Clear, colorless liquid',
            'odor': 'Pungent, irritating odor'
        },
        
        'hazards': {
            'skin': {'level': 'high', 'description': 'Causes severe skin burns'},
            'eyes': {'level': 'high', 'description': 'Causes serious eye damage'},
            'inhalation': {'level': 'high', 'description': 'Toxic if inhaled'},
            'ingestion': {'level': 'high', 'description': 'Toxic if swallowed'}
        },
        
        'first_aid': {
            'skin': {'action': 'Remove contaminated clothing. Rinse skin immediately.', 'duration': 15, 'seek_help': True},
            'eyes': {'action': 'Rinse eyes continuously. Seek immediate medical attention.', 'duration': 15, 'seek_help': True},
            'inhalation': {'action': 'Move to fresh air immediately. Give artificial respiration if not breathing.', 'seek_help': True},
            'ingestion': {'action': 'CALL POISON CONTROL IMMEDIATELY. Do NOT induce vomiting.', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Chemical splash goggles + face shield', 'required': True},
            {'icon': '🧤', 'label': 'Neoprene or rubber gloves', 'required': True},
            {'icon': '🦺', 'label': 'Chemical-resistant apron', 'required': True},
            {'icon': '😷', 'label': 'Full-face respirator if poorly ventilated', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Bleach (hypochlorite)', 'reaction': 'Toxic chloramine gas', 'severity': 'CRITICAL'},
            {'substance': 'Acids', 'reaction': 'Violent reaction, heat generation', 'severity': 'CRITICAL'},
            {'substance': 'Heavy metals', 'reaction': 'Explosive compounds', 'severity': 'CRITICAL'}
        ],
        
        'storage': 'Store in cool, dry, ventilated area. Keep away from incompatible materials. Keep container tightly closed.',
        'disposal': 'Neutralize before disposal. Follow EPA and local regulations.',
        'contraindications': ['Asthma or respiratory disease', 'Skin conditions or sensitivities', 'Eye conditions']
    },
    
    'hcl': {
        'name': 'Hydrochloric Acid',
        'formula': 'HCl',
        'cas': '7647-01-0',
        'category': 'Corrosive',
        'template': 'mineral_acid',
        
        'properties': {
            'pH': 0.1,
            'flash_point': None,
            'specific_gravity': 1.18,
            'state': 'liquid',
            'appearance': 'Clear, colorless to pale yellow liquid',
            'odor': 'Pungent, irritating odor'
        },
        
        'hazards': {
            'skin': {'level': 'high', 'description': 'Causes severe skin burns'},
            'eyes': {'level': 'high', 'description': 'Causes serious eye damage'},
            'inhalation': {'level': 'high', 'description': 'Toxic if inhaled'},
            'ingestion': {'level': 'high', 'description': 'Toxic if swallowed. Causes severe internal burns.'}
        },
        
        'first_aid': {
            'skin': {'action': 'Remove contaminated clothing immediately. Flush skin with large amounts of water.', 'duration': 20, 'seek_help': True},
            'eyes': {'action': 'Rinse eyes continuously. Hold eyelids open. Seek immediate medical attention.', 'duration': 20, 'seek_help': True},
            'inhalation': {'action': 'Move to fresh air immediately. Give artificial respiration if not breathing.', 'seek_help': True},
            'ingestion': {'action': 'CALL 911 IMMEDIATELY. Do NOT induce vomiting. Do NOT give anything by mouth.', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Chemical splash goggles + face shield', 'required': True},
            {'icon': '🧤', 'label': 'Neoprene or PVC gloves', 'required': True},
            {'icon': '🦺', 'label': 'Acid-resistant apron', 'required': True},
            {'icon': '💨', 'label': 'Use in fume hood or well-ventilated area', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Bases (sodium hydroxide, ammonia)', 'reaction': 'Violent exothermic reaction', 'severity': 'CRITICAL'},
            {'substance': 'Metals', 'reaction': 'Hydrogen gas (explosive)', 'severity': 'CRITICAL'},
            {'substance': 'Bleach', 'reaction': 'Toxic chlorine gas', 'severity': 'CRITICAL'}
        ],
        
        'storage': 'Store in corrosion-resistant container in cool, dry, ventilated area. Keep away from bases and metals.',
        'disposal': 'Neutralize with base before disposal. Follow EPA guidelines.',
        'contraindications': ['Respiratory disease', 'Skin conditions', 'Eye conditions', 'Dental problems (vapors can erode tooth enamel)']
    },
    
    'ethanol': {
        'name': 'Ethanol',
        'formula': 'C₂H₅OH',
        'cas': '64-17-5',
        'category': 'Flammable',
        'template': 'alcohol_solvent',
        
        'properties': {
            'pH': 7.3,
            'flash_point': 55,
            'specific_gravity': 0.79,
            'state': 'liquid',
            'appearance': 'Clear, colorless liquid',
            'odor': 'Mild alcohol odor'
        },
        
        'hazards': {
            'skin': {'level': 'low', 'description': 'May cause skin dryness with prolonged contact'},
            'eyes': {'level': 'medium', 'description': 'Causes eye irritation'},
            'inhalation': {'level': 'low', 'description': 'May cause drowsiness with prolonged exposure'},
            'ingestion': {'level': 'medium', 'description': 'Harmful if swallowed in large amounts'}
        },
        
        'first_aid': {
            'skin': {'action': 'Wash with soap and water', 'duration': None, 'seek_help': False},
            'eyes': {'action': 'Rinse eyes', 'duration': 10, 'seek_help': False},
            'inhalation': {'action': 'Move to fresh air', 'seek_help': False},
            'ingestion': {'action': 'Call Poison Control if large amount swallowed', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Safety glasses', 'required': True},
            {'icon': '💨', 'label': 'Use in ventilated area', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Strong oxidizers', 'reaction': 'Fire risk', 'severity': 'HIGH'}
        ],
        
        'storage': 'Store in cool, well-ventilated area away from heat and ignition sources. Keep container tightly closed.',
        'disposal': 'Can be disposed in small quantities. Check local regulations.',
        'contraindications': ['Pregnancy (avoid prolonged exposure)', 'Recovering alcoholics (vapor exposure)']
    }
}

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Sidebar for chemical search
    with st.sidebar:
        st.markdown("### 🔍 Search Chemical")
        
        search_query = st.text_input(
            "Enter name, formula, or CAS number:",
            placeholder="bleach, C3H6O, 67-64-1...",
            help="Search by common name, chemical formula, or CAS registry number"
        )
        
        if st.button("🔎 Search", type="primary", use_container_width=True):
            # Search logic
            query = search_query.lower().strip()
            found = None
            
            for key, chem in CHEMICALS_DATABASE.items():
                if (query in chem['name'].lower() or 
                    query in chem['formula'].lower() or 
                    query in chem['cas'] or
                    query == key):
                    found = chem
                    st.session_state['selected_chemical'] = chem
                    break
            
            if not found:
                st.error("Chemical not found")
                st.info("Try: bleach, acetone, ammonia, hcl, or ethanol")
        
        st.markdown("---")
        st.markdown("### 📚 Available Chemicals")
        for key, chem in CHEMICALS_DATABASE.items():
            if st.button(f"{chem['name']}", key=f"btn_{key}", use_container_width=True):
                st.session_state['selected_chemical'] = chem
        
        st.markdown("---")
        st.markdown("""
        <div style='font-size: 0.75rem; color: #6b7280; text-align: center;'>
        Based on Kathy J. Malone<br>
        ManGuard Systems, Inc.<br>
        <em>"It's What the Worker Understands That Matters"</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if 'selected_chemical' not in st.session_state:
        # Welcome screen
        st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 3rem; font-weight: 300; color: #1f2937; margin: 0;'>
                Visual Chemical Safety
            </h1>
            <p style='font-size: 1.25rem; color: #6b7280; margin-top: 0.5rem;'>
                "It's What the Worker Understands That Matters..."
            </p>
            <p style='font-size: 0.875rem; color: #9ca3af;'>
                Independent of Language • Literacy • Cognitive Challenges
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Design Principles")
            st.markdown("""
            - **Visual First**: Pictures over words
            - **Speedometers**: Show hazard magnitude (color-blind friendly)
            - **Clocks**: Time-based instructions (15-min rinse)
            - **Body Systems**: Show what's affected
            """)
        
        with col2:
            st.markdown("### 📋 Templatization")
            st.markdown("""
            - **Group Similar Chemicals**: Reduce workload
            - **Saturn Example**: 10,000 SDSs → 70 templates
            - **Use-Type Specific**: Same chemical, different hazards
            - **"Mom & Apple Pie"**: Don't eat, drink, or expose
            """)
        
        with col3:
            st.markdown("### 👷 Worker Focus")
            st.markdown("""
            - **Strati-lingual Workforces**: Different languages
            - **Non-readers**: Visual comprehension
            - **Cognitive Challenges**: Simplified presentation
            - **Medical Screening**: Pre-existing conditions
            """)
        
        st.markdown("---")
        st.info("👈 Use the sidebar to search for a chemical or select from the available list")
        
    else:
        # Display selected chemical
        chem = st.session_state['selected_chemical']
        
        # Header
        st.markdown(f"""
        <div class='main-header'>
            <div class='chemical-name'>{chem['name']}</div>
            <div class='chemical-formula'>{chem['formula']}</div>
            <div style='font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;'>
                CAS: {chem['cas']} | Category: <span style='background: #dbeafe; padding: 0.25rem 0.5rem; border-radius: 0.25rem; color: #1e40af;'>{chem['category']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CRITICAL: Incompatibilities Warning
        if chem.get('incompatibilities'):
            st.markdown("### ⚠️ CRITICAL SAFETY WARNING")
            st.markdown("""
            <div class='critical-warning'>
                <h2 style='color: #991b1b; margin-top: 0;'>🚫 NEVER MIX WITH:</h2>
            """, unsafe_allow_html=True)
            
            for incomp in chem['incompatibilities']:
                st.markdown(f"""
                <div style='font-size: 1.125rem; margin: 0.75rem 0; padding: 0.5rem; background: white; border-radius: 0.25rem;'>
                    <strong style='color: #991b1b;'>{incomp['substance']}</strong> 
                    → {incomp['reaction']} 
                    <span style='background: #dc2626; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin-left: 0.5rem;'>{incomp['severity']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Hazard Overview
        st.markdown("## 📊 Hazard Overview")
        st.markdown("*Speedometer shows hazard magnitude - No numbers to avoid confusion between GHS and NFPA systems*")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fig = create_speedometer(chem['hazards']['skin']['level'], '👋 Skin Contact')
            st.plotly_chart(fig, use_container_width=True)
            st.caption(chem['hazards']['skin']['description'])
        
        with col2:
            fig = create_speedometer(chem['hazards']['eyes']['level'], '👁️ Eye Contact')
            st.plotly_chart(fig, use_container_width=True)
            st.caption(chem['hazards']['eyes']['description'])
        
        with col3:
            fig = create_speedometer(chem['hazards']['inhalation']['level'], '💨 Breathing')
            st.plotly_chart(fig, use_container_width=True)
            st.caption(chem['hazards']['inhalation']['description'])
        
        with col4:
            fig = create_speedometer(chem['hazards']['ingestion']['level'], '🍴 Ingestion')
            st.plotly_chart(fig, use_container_width=True)
            st.caption(chem['hazards']['ingestion']['description'])
        
        # First Aid
        st.markdown("## 🆘 First Aid Instructions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👋 Skin Contact")
            st.info(chem['first_aid']['skin']['action'])
            if chem['first_aid']['skin'].get('duration'):
                fig = create_clock_visual(chem['first_aid']['skin']['duration'])
                st.plotly_chart(fig, use_container_width=True)
            if chem['first_aid']['skin']['seek_help']:
                st.error("→ Seek medical attention")
            
            st.markdown("### 💨 Breathing/Inhalation")
            st.info(chem['first_aid']['inhalation']['action'])
            if chem['first_aid']['inhalation']['seek_help']:
                st.error("→ Seek medical attention")
        
        with col2:
            st.markdown("### 👁️ Eye Contact")
            st.info(chem['first_aid']['eyes']['action'])
            if chem['first_aid']['eyes'].get('duration'):
                fig = create_clock_visual(chem['first_aid']['eyes']['duration'])
                st.plotly_chart(fig, use_container_width=True)
            if chem['first_aid']['eyes']['seek_help']:
                st.error("→ Seek medical attention")
            
            st.markdown("### 🍴 Ingestion (Swallowed)")
            st.info(chem['first_aid']['ingestion']['action'])
            if chem['first_aid']['ingestion']['seek_help']:
                st.error("→ Call Poison Control: **1-800-222-1222**")
        
        # PPE Requirements
        st.markdown("## 🦺 Required Protective Equipment")
        
        ppe_cols = st.columns(len(chem['ppe']))
        for idx, ppe in enumerate(chem['ppe']):
            with ppe_cols[idx]:
                st.markdown(f"""
                <div class='ppe-icon'>{ppe['icon']}</div>
                <div class='hazard-label'>{ppe['label']}</div>
                """, unsafe_allow_html=True)
        
        # Physical/Chemical Properties
        st.markdown("## 🔬 Physical & Chemical Properties")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ph = chem['properties']['pH']
            is_corrosive = ph < 2 or ph > 12.5
            color = 'red' if is_corrosive else 'blue'
            st.metric("pH", f"{ph:.1f}" if ph else "N/A", 
                     delta="Corrosive" if is_corrosive else None,
                     delta_color="inverse")
        
        with col2:
            fp = chem['properties']['flash_point']
            if fp is not None:
                is_flammable = fp < 93
                st.metric("Flash Point", f"{fp}°F", 
                         delta="🔥 Flammable" if is_flammable else "Not flammable",
                         delta_color="inverse" if is_flammable else "off")
            else:
                st.metric("Flash Point", "None")
        
        with col3:
            sg = chem['properties']['specific_gravity']
            st.metric("Specific Gravity", f"{sg:.2f}",
                     delta="Floats on water" if sg < 1 else "Sinks in water",
                     delta_color="off")
        
        with st.expander("📋 Additional Properties"):
            st.markdown(f"**State:** {chem['properties']['state']}")
            st.markdown(f"**Appearance:** {chem['properties']['appearance']}")
            st.markdown(f"**Odor:** {chem['properties']['odor']}")
        
        # Storage & Disposal
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("## 📦 Storage")
            st.info(chem['storage'])
        
        with col2:
            st.markdown("## ♻️ Disposal")
            st.info(chem['disposal'])
        
        # Worker Contraindications
        if chem.get('contraindications'):
            st.markdown("## ⚕️ Worker Health Considerations")
            st.warning("Workers with the following conditions should avoid or limit exposure:")
            for condition in chem['contraindications']:
                st.markdown(f"- {condition}")
        
        # Link to Full SDS
        st.markdown("---")
        st.markdown("""
        <div class='info-box' style='text-align: center;'>
            <p style='margin-bottom: 0.5rem;'>For complete regulatory information and technical details:</p>
            <p style='margin: 0;'><strong>View Full Safety Data Sheet (SDS)</strong></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
