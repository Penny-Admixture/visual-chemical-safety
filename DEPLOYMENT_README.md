# Visual Chemical Safety - Streamlit Deployment Guide

## Quick Start (Local Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run visual_chemical_safety_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Deploy to Streamlit Cloud (Free)

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Steps:

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Visual Chemical Safety Streamlit app"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign in" and use your GitHub account

3. **Create New App**
   - Click "New app"
   - Select your GitHub repository
   - **Main file path**: `visual_chemical_safety_app.py`
   - **Python version**: 3.11
   - Click "Deploy"

4. **Wait for deployment** (usually 2-5 minutes)
   - Streamlit will automatically install dependencies from `requirements.txt`
   - Your app will be live at: `https://your-app-name.streamlit.app`

---

## Deploy to Other Platforms

### Heroku

```bash
# Create Procfile
echo "web: streamlit run visual_chemical_safety_app.py --server.port=\$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY visual_chemical_safety_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "visual_chemical_safety_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t visual-chemical-safety .
docker run -p 8501:8501 visual-chemical-safety
```

---

## Configuration Options

Create `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f3f4f6"
textColor = "#1f2937"
font = "sans serif"

[server]
headless = true
port = 8501
```

---

## File Structure

```
your-repo/
├── visual_chemical_safety_app.py   # Main Streamlit app
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration (optional)
└── visual-chemical-safety-reference/
    ├── DESIGN_PRINCIPLES.md       # Kathy Malone's design bible
    └── TECHNICAL_REQUIREMENTS.md  # Implementation specifications
```

---

## Features

### Core Functionality
✅ Chemical search by name, formula, or CAS number  
✅ Hazard magnitude speedometers (color-blind accessible)  
✅ 15-minute rinse clocks (analog + digital)  
✅ Critical incompatibility warnings  
✅ First aid instructions by exposure route  
✅ PPE requirements with visual icons  
✅ Physical/chemical properties display  
✅ Worker contraindication screening  

### Based On
- **Kathy J. Malone's Visual Chemical Safety System**
- **ManGuard Systems, Inc.**
- **Core Principle**: "It's What the Worker Understands That Matters"

### Design Principles
- Visual-first (pictures over words)
- Language-independent
- Literacy-independent
- Color-blind accessible
- Templatization strategy (Saturn's 10,000 SDSs → 70 templates)

---

## Customization

### Adding New Chemicals

Edit `CHEMICALS_DATABASE` in `visual_chemical_safety_app.py`:

```python
CHEMICALS_DATABASE = {
    'new_chemical': {
        'name': 'Chemical Name',
        'formula': 'H₂O',
        'cas': '0000-00-0',
        'category': 'Category',
        'template': 'template_name',
        
        'properties': {
            'pH': 7.0,
            'flash_point': None,  # or temperature in °F
            'specific_gravity': 1.0,
            'state': 'liquid',
            'appearance': 'Description',
            'odor': 'Description'
        },
        
        'hazards': {
            'skin': {'level': 'low|medium|high', 'description': 'Text'},
            'eyes': {'level': 'low|medium|high', 'description': 'Text'},
            'inhalation': {'level': 'low|medium|high', 'description': 'Text'},
            'ingestion': {'level': 'low|medium|high', 'description': 'Text'}
        },
        
        'first_aid': {
            'skin': {'action': 'Instructions', 'duration': 15, 'seek_help': True},
            'eyes': {'action': 'Instructions', 'duration': 15, 'seek_help': True},
            'inhalation': {'action': 'Instructions', 'seek_help': True},
            'ingestion': {'action': 'Instructions', 'seek_help': True}
        },
        
        'ppe': [
            {'icon': '🥽', 'label': 'Description', 'required': True},
            {'icon': '🧤', 'label': 'Description', 'required': True}
        ],
        
        'incompatibilities': [
            {'substance': 'Substance', 'reaction': 'What happens', 'severity': 'CRITICAL|HIGH|MEDIUM'}
        ],
        
        'storage': 'Storage instructions',
        'disposal': 'Disposal instructions',
        'contraindications': ['Condition 1', 'Condition 2']
    }
}
```

### Connecting to a Database

Replace `CHEMICALS_DATABASE` dict with database queries:

```python
import sqlite3

def get_chemical(search_query):
    conn = sqlite3.connect('chemicals.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chemicals 
        WHERE name LIKE ? OR formula LIKE ? OR cas LIKE ?
    """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    result = cursor.fetchone()
    conn.close()
    return result
```

---

## Troubleshooting

### Common Issues

**App won't start locally**
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Deployment fails on Streamlit Cloud**
- Check that `requirements.txt` is in the root directory
- Verify main file path is correct
- Check logs in Streamlit Cloud dashboard

**Visualizations not showing**
```bash
# Update plotly
pip install plotly --upgrade
```

---

## Support & Contact

**Based on work by:**  
Kathy J. Malone  
ManGuard Systems, Inc.  
manguardEHS@gmail.com  
734-834-7733

**For implementation questions:**  
See `/visual-chemical-safety-reference/DESIGN_PRINCIPLES.md` for authoritative guidance

---

## License

This implementation follows Kathy J. Malone's Visual Chemical Safety specifications.  
All design principles and methodologies are attributed to ManGuard Systems, Inc.
