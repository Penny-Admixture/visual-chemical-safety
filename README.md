# Visual Chemical Safety System

> "It's What the Worker Understands That Matters"

A production-grade chemical safety visualization system based on **Kathy J. Malone's** Visual Chemical Safety methodology from **ManGuard Systems, Inc.**

## 🎯 Purpose

Make chemical safety information accessible **independent of**:
- 🌍 Language
- 📖 Literacy level
- 🧠 Cognitive challenges

## 🚀 Live Demo

**[View Live Application →](https://visual-chemical-safety.streamlit.app/)**

## ✨ Features

### Core Visualizations
- ✅ **Speedometer Hazard Meters** - No numbers (avoids GHS vs NFPA confusion), line thickness increases with severity
- ✅ **15-Minute Rinse Clocks** - Both analog AND digital displays (worker preference)
- ✅ **Color-Blind Accessible** - Position and size convey magnitude, not just color
- ✅ **Critical Warnings** - Incompatibilities impossible to miss (e.g., bleach + ammonia)

### Safety Information
- ✅ **First Aid by Exposure Route** - Skin, eyes, inhalation, ingestion
- ✅ **PPE Requirements** - Visual icons with type-specific details
- ✅ **Physical/Chemical Properties** - pH, flash point, specific gravity with visual thresholds
- ✅ **Worker Screening** - Pre-existing condition contraindications

### Included Chemicals
- Bleach (NaClO)
- Acetone (C₃H₆O)
- Ammonia (NH₃)
- Hydrochloric Acid (HCl)
- Ethanol (C₂H₅OH)

## 📖 Design Principles

Based on Kathy Malone's Saturn methodology:

1. **Visual First** - Pictures over words
2. **Templatization** - Group similar chemicals (Saturn: 10,000 SDSs → 70 templates)
3. **Use-Type Specific** - Same chemical = different hazards based on application
4. **"Mom & Apple Pie" Baseline** - Don't eat, don't drink, don't unnecessarily expose

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run visual_chemical_safety_app.py

# Opens at http://localhost:8501
```

## 📦 Deploy to Streamlit Cloud

1. Fork/clone this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select this repository
6. Main file: `visual_chemical_safety_app.py`
7. Click "Deploy!"

## 📚 Documentation

See `/visual-chemical-safety-reference/` for:
- `DESIGN_PRINCIPLES.md` - Comprehensive design bible from Kathy Malone's work
- `TECHNICAL_REQUIREMENTS.md` - Implementation specifications

## 🏢 Credits

### Based on Work By:
**Kathy J. Malone, CHMM**  
ManGuard Systems, Inc.  
manguardEHS@gmail.com  
734-834-7733

### Source Materials:
- "What Might Visual Chemical Safety Look Like?" (ASSP Presentation, March 2022)
- ManGuard Systems blog (2022)
- Saturn Corporation HazComm implementation (1990s-2009)

### Key Innovations:
- **Director's Award Nominee**: SUI Templatization (10,000 SDSs → 70 templates)
- **Best Audit Score Ever**: OSHA Transfer Label solution
- **Gold Standard**: SOPs workers actually read and correct
- **Video Training**: "Everyone got it" vs paper SOP failures

## 📄 License

This implementation follows Kathy J. Malone's Visual Chemical Safety specifications.  
All design principles and methodologies are attributed to ManGuard Systems, Inc.

## 🤝 Contributing

This is a demonstration implementation of Malone's methodology. For production use:
1. Consult original source materials in `/visual-chemical-safety-reference/`
2. Follow Saturn's templatization approach (pH, Flash Point, DOT Hazard Class filters)
3. Implement use-type specificity (same chemical, different hazards per application)
4. Include worker medical screening (Phase III-IV features)

## 📞 Support

For methodology questions: Contact Kathy J. Malone (manguardEHS@gmail.com)  
For implementation questions: See documentation in `/visual-chemical-safety-reference/`

---

**Remember**: "It's What the Worker Understands That Matters"
