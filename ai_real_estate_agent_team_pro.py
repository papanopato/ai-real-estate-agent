
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# TRANSLATIONS - COMPLETE FOR ALL LANGUAGES
# ============================================

T = {
    "en": {
        "title": "AI Real Estate Agent",
        "subtitle": "Luxury Property Solutions",
        "welcome": "Your luxury real estate AI assistant",
        "search": "🔍 Search",
        "descriptions": "✍️ Descriptions",
        "compare": "⚖️ Compare",
        "analysis": "📊 Analysis",
        "partners": "🔗 Partners",
        "city": "City",
        "state": "State",
        "min_price": "Min Price ($)",
        "max_price": "Max Price ($)",
        "bedrooms": "Bedrooms",
        "type": "Property Type",
        "search_btn": "🚀 Search Properties",
        "searching": "Searching...",
        "found": "luxury properties found",
        "describe": "✍️ Describe",
        "compare_btn": "⭐ Compare",
        "generate": "📝 Generate Description",
        "tone": "Tone",
        "platform": "Platform",
        "length": "Length",
        "luxury": "Luxury",
        "professional": "Professional",
        "warm": "Warm",
        "family": "Family",
        "short": "Short",
        "medium": "Medium",
        "long": "Long",
        "social": "📱 Social Media Posts",
        "analysis_btn": "🔍 Detailed Analysis",
        "best_value": "🏆 BEST VALUE",
        "price_sqft": "Price/sq ft",
        "market_stats": "Market Statistics",
        "avg": "Average",
        "min": "Min",
        "max": "Max",
        "partners_title": "Premium Partners",
        "commission": "Commission",
        "category": "Category",
        "access": "🔗 Access",
        "footer": "© 2026 AI Real Estate Agent | Luxury Edition",
        "select_property": "Select a property from Search tab",
        "add_compare": "Add at least 2 properties",
        "search_first": "Launch a search first",
        "all": "All",
        "villa": "Villa",
        "penthouse": "Penthouse",
        "estate": "Estate",
        "mansion": "Waterfront Mansion",
        "condo": "Luxury Condo",
    },
    "fr": {
        "title": "Agent Immobilier IA",
        "subtitle": "Solutions Immobilières de Luxe",
        "welcome": "Votre assistant immobilier de luxe",
        "search": "🔍 Recherche",
        "descriptions": "✍️ Descriptions",
        "compare": "⚖️ Comparer",
        "analysis": "📊 Analyse",
        "partners": "🔗 Partenaires",
        "city": "Ville",
        "state": "État",
        "min_price": "Prix Min ($)",
        "max_price": "Prix Max ($)",
        "bedrooms": "Chambres",
        "type": "Type de Bien",
        "search_btn": "🚀 Rechercher",
        "searching": "Recherche en cours...",
        "found": "biens de luxe trouvés",
        "describe": "✍️ Décrire",
        "compare_btn": "⭐ Comparer",
        "generate": "📝 Générer",
        "tone": "Ton",
        "platform": "Plateforme",
        "length": "Longueur",
        "luxury": "Luxe",
        "professional": "Professionnel",
        "warm": "Chaleureux",
        "family": "Familial",
        "short": "Courte",
        "medium": "Moyenne",
        "long": "Longue",
        "social": "📱 Réseaux Sociaux",
        "analysis_btn": "🔍 Analyse Détaillée",
        "best_value": "🏆 MEILLEUR RAPPORT",
        "price_sqft": "Prix/m²",
        "market_stats": "Statistiques du Marché",
        "avg": "Moyenne",
        "min": "Min",
        "max": "Max",
        "partners_title": "Partenaires Premium",
        "commission": "Commission",
        "category": "Catégorie",
        "access": "🔗 Accéder",
        "footer": "© 2026 Agent Immobilier IA | Édition Luxe",
        "select_property": "Sélectionnez un bien",
        "add_compare": "Ajoutez 2 biens minimum",
        "search_first": "Lancez une recherche",
        "all": "Tous",
        "villa": "Villa",
        "penthouse": "Penthouse",
        "estate": "Domaine",
        "mansion": "Manoir",
        "condo": "Condo Luxe",
    },
    "es": {
        "title": "Agente Inmobiliario IA",
        "subtitle": "Soluciones Inmobiliarias de Lujo",
        "welcome": "Tu asistente inmobiliario de lujo",
        "search": "🔍 Búsqueda",
        "descriptions": "✍️ Descripciones",
        "compare": "⚖️ Comparar",
        "analysis": "📊 Análisis",
        "partners": "🔗 Socios",
        "city": "Ciudad",
        "state": "Estado",
        "min_price": "Precio Mín ($)",
        "max_price": "Precio Máx ($)",
        "bedrooms": "Habitaciones",
        "type": "Tipo de Propiedad",
        "search_btn": "🚀 Buscar",
        "searching": "Buscando...",
        "found": "propiedades encontradas",
        "describe": "✍️ Describir",
        "compare_btn": "⭐ Comparar",
        "generate": "📝 Generar",
        "tone": "Tono",
        "platform": "Plataforma",
        "length": "Longitud",
        "luxury": "Lujo",
        "professional": "Profesional",
        "warm": "Cálido",
        "family": "Familiar",
        "short": "Corta",
        "medium": "Media",
        "long": "Larga",
        "social": "📱 Redes Sociales",
        "analysis_btn": "🔍 Análisis Detallado",
        "best_value": "🏆 MEJOR VALOR",
        "price_sqft": "Precio/sq ft",
        "market_stats": "Estadísticas del Mercado",
        "avg": "Promedio",
        "min": "Mín",
        "max": "Máx",
        "partners_title": "Socios Premium",
        "commission": "Comisión",
        "category": "Categoría",
        "access": "🔗 Acceder",
        "footer": "© 2026 Agente Inmobiliario IA | Edición Lujo",
        "select_property": "Selecciona una propiedad",
        "add_compare": "Agrega al menos 2 propiedades",
        "search_first": "Inicia una búsqueda",
        "all": "Todos",
        "villa": "Villa",
        "penthouse": "Penthouse",
        "estate": "Finca",
        "mansion": "Mansión",
        "condo": "Condo",
    },
    "ar": {
        "title": "وكيل عقارات ذكي",
        "subtitle": "حلول عقارية فاخرة",
        "welcome": "مساعدك العقاري الفاخر",
        "search": "🔍 بحث",
        "descriptions": "✍️ وصف",
        "compare": "⚖️ مقارنة",
        "analysis": "📊 تحليل",
        "partners": "🔗 شركاء",
        "city": "المدينة",
        "state": "المنطقة",
        "min_price": "الحد الأدنى ($)",
        "max_price": "الحد الأقصى ($)",
        "bedrooms": "غرف النوم",
        "type": "نوع العقار",
        "search_btn": "🚀 بحث",
        "searching": "جاري البحث...",
        "found": "عقارات تم العثور عليها",
        "describe": "✍️ وصف",
        "compare_btn": "⭐ مقارنة",
        "generate": "📝 إنشاء",
        "tone": "النبرة",
        "platform": "المنصة",
        "length": "الطول",
        "luxury": "فاخر",
        "professional": "احترافي",
        "warm": "دافئ",
        "family": "عائلي",
        "short": "قصير",
        "medium": "متوسط",
        "long": "طويل",
        "social": "📱 وسائل التواصل",
        "analysis_btn": "🔍 تحليل مفصل",
        "best_value": "🏆 أفضل قيمة",
        "price_sqft": "السعر/قدم",
        "market_stats": "إحصائيات السوق",
        "avg": "المتوسط",
        "min": "الأدنى",
        "max": "الأقصى",
        "partners_title": "شركاء مميزون",
        "commission": "العمولة",
        "category": "الفئة",
        "access": "🔗 دخول",
        "footer": "© 2026 وكيل عقارات ذكي | النسخة الفاخرة",
        "select_property": "اختر عقاراً",
        "add_compare": "أضف عقارين على الأقل",
        "search_first": "ابدأ البحث أولاً",
        "all": "الكل",
        "villa": "فيلا",
        "penthouse": "بنتهاوس",
        "estate": "عقار",
        "mansion": "قصر",
        "condo": "شقة فاخرة",
    }
}

# ============================================
# AFFILIATE LINKS
# ============================================

AFFILIATES = {
    "dealcheck": {
        "name": "DealCheck",
        "url": "https://dealcheck.io?fp_ref=omar18",
        "desc": {"en": "Investment Analysis", "fr": "Analyse d'investissement", "es": "Análisis", "ar": "تحليل الاستثمار"},
        "commission": "30% recurring",
        "cat": {"en": "Analysis", "fr": "Analyse", "es": "Análisis", "ar": "تحليل"}
    },
    "buildium": {
        "name": "Buildium",
        "url": "https://www.buildium.com/?ref=YOUR_AFFILIATE_ID",
        "desc": {"en": "Property Management", "fr": "Gestion locative", "es": "Gestión", "ar": "إدارة العقارات"},
        "commission": "25% recurring",
        "cat": {"en": "Management", "fr": "Gestion", "es": "Gestión", "ar": "إدارة"}
    },
    "nolo": {
        "name": "NOLO",
        "url": "https://www.nolo.com/?ref=YOUR_AFFILIATE_ID",
        "desc": {"en": "Legal Documents", "fr": "Documents juridiques", "es": "Documentos", "ar": "مستندات قانونية"},
        "commission": "25-35%",
        "cat": {"en": "Legal", "fr": "Juridique", "es": "Legal", "ar": "قانوني"}
    },
    "biggerpockets": {
        "name": "BiggerPockets",
        "url": "https://www.biggerpockets.com/?ref=YOUR_AFFILIATE_ID",
        "desc": {"en": "Investor Community", "fr": "Communauté", "es": "Comunidad", "ar": "مجتمع المستثمرين"},
        "commission": "$75/signup",
        "cat": {"en": "Education", "fr": "Éducation", "es": "Educación", "ar": "تعليم"}
    },
}

# ============================================
# LUXURY PROPERTIES
# ============================================

PROPERTIES = [
    {"id": "p1", "address": "123 Ocean Drive, Miami Beach, FL", "price": 2500000, "bedrooms": 5, "bathrooms": 4.5, "sqft": 4200, "type": "Villa", "year": 2019, "area": "South Beach", "features": ["Infinity Pool", "Private Beach", "Smart Home", "Wine Cellar"]},
    {"id": "p2", "address": "456 Palm Avenue, Coral Gables, FL", "price": 1850000, "bedrooms": 4, "bathrooms": 3.5, "sqft": 3500, "type": "Estate", "year": 2017, "area": "Coral Gables", "features": ["Tennis Court", "Guest House", "Mediterranean"]},
    {"id": "p3", "address": "789 Star Island, Miami Beach, FL", "price": 4500000, "bedrooms": 6, "bathrooms": 5.5, "sqft": 5800, "type": "Waterfront Mansion", "year": 2021, "area": "Star Island", "features": ["Private Dock", "Panoramic Views", "Elevator", "Spa"]},
    {"id": "p4", "address": "321 Brickell Avenue, Miami, FL", "price": 3200000, "bedrooms": 3, "bathrooms": 3, "sqft": 2800, "type": "Penthouse", "year": 2022, "area": "Brickell", "features": ["360° Views", "Private Terrace", "Concierge", "Rooftop Pool"]},
]

# ============================================
# CSS STYLING
# ============================================

def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    .main {
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 25%, #7DD3FC 50%, #38BDF8 75%, #0EA5E9 100%);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }

    .lang-btn {
        background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 50%, #38BDF8 100%) !important;
        color: white !important;
        border: 2px solid #7DD3FC !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
    }

    .lang-btn:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.5) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 50%, #D4AF37 100%) !important;
        color: #0C4A6E !important;
        border: 2px solid #B45309 !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 16px 32px !important;
        font-size: 17px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(212, 175, 55, 0.6) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #0284C7 0%, #0EA5E9 50%, #38BDF8 100%) !important;
        border-radius: 20px !important;
        padding: 14px !important;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 100%) !important;
        border-radius: 12px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #0C4A6E !important;
        font-weight: 700 !important;
    }

    .property-card {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #7DD3FC;
        border-radius: 24px;
        padding: 32px;
        margin: 20px 0;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.15);
    }

    .property-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 12px 40px rgba(212, 175, 55, 0.25);
        transform: translateY(-6px);
    }

    .welcome-banner {
        background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 50%, #38BDF8 100%);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 12px 40px rgba(2, 132, 199, 0.3);
    }

    .header-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 32px;
        box-shadow: 0 8px 30px rgba(2, 132, 199, 0.2);
        border: 2px solid #BAE6FD;
    }

    .footer {
        text-align: center;
        padding: 40px;
        color: #0369A1;
        font-size: 16px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        margin-top: 60px;
        border: 2px solid #BAE6FD;
    }

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #E0F2FE;
    }

    ::-webkit-scrollbar-thumb {
        background: #7DD3FC;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0284C7;
    }
    </style>
    """

# ============================================
# MAIN APP
# ============================================

def main():
    st.set_page_config(page_title="AI Real Estate - Luxury", page_icon="🏛️", layout="wide")
    st.markdown(get_css(), unsafe_allow_html=True)

    # Session state
    if 'lang' not in st.session_state:
        st.session_state.lang = "en"
    if 'saved' not in st.session_state:
        st.session_state.saved = []
    if 'selected' not in st.session_state:
        st.session_state.selected = None
    if 'compare' not in st.session_state:
        st.session_state.compare = []

    # Language selector
    c1, c2, c3, c4, sp = st.columns([1, 1, 1, 1, 8])
    with c1:
        if st.button("🇬🇧 EN", key="en"):
            st.session_state.lang = "en"
    with c2:
        if st.button("🇫🇷 FR", key="fr"):
            st.session_state.lang = "fr"
    with c3:
        if st.button("🇪🇸 ES", key="es"):
            st.session_state.lang = "es"
    with c4:
        if st.button("🇸🇦 AR", key="ar"):
            st.session_state.lang = "ar"

    L = st.session_state.lang
    t = T[L]

    # Header
    st.markdown("<div class='header-section'>", unsafe_allow_html=True)
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        try:
            st.image("logo.png", width=180)
        except:
            st.markdown("<div style='font-size: 100px; text-align: center;'>🏛️</div>", unsafe_allow_html=True)
    with col_title:
        st.markdown(f"<h1 style='color: #0C4A6E; font-size: 48px; margin-bottom: 8px;'>{t['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #0284C7; font-size: 22px; font-style: italic;'>✨ {t['subtitle']} ✨</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Welcome
    st.markdown(f"""
    <div class="welcome-banner">
        <h2 style="color: white; font-size: 32px;">🌟 {t['welcome']} 🌟</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 20px; margin-top: 16px;">
            Premium Real Estate Solutions Worldwide
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([t['search'], t['descriptions'], t['compare'], t['analysis'], t['partners']])

    # TAB 1: SEARCH
    with tab1:
        st.markdown(f"<h2 style='color: #0C4A6E; font-size: 36px;'>{t['search']}</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            city = st.text_input(t['city'], "Miami")
            min_p = st.number_input(t['min_price'], 0, 10000000, 1000000, 100000)
            beds = st.selectbox(t['bedrooms'], [1, 2, 3, 4, 5, 6])
        with c2:
            state = st.text_input(t['state'], "FL")
            max_p = st.number_input(t['max_price'], 0, 10000000, 5000000, 100000)
            types = [t['all'], t['villa'], t['penthouse'], t['estate'], t['mansion'], t['condo']]
            ptype = st.selectbox(t['type'], types)

        if st.button(t['search_btn'], type="primary", use_container_width=True):
            st.session_state.saved = PROPERTIES
            st.success(f"✨ {len(PROPERTIES)} {t['found']}")

            for p in PROPERTIES:
                st.markdown(f"""
                <div class="property-card">
                    <h3 style="color: #D4AF37; font-size: 28px;">🏛️ {p['type']}</h3>
                    <p style="color: #0C4A6E; font-size: 20px; font-weight: 600;">📍 {p['address']}</p>
                    <p style="color: #0369A1; font-size: 18px;">
                        💰 <span style="color: #D4AF37; font-weight: 700; font-size: 24px;">${p['price']:,}</span> | 
                        🛏️ {p['bedrooms']} | 🛁 {p['bathrooms']} | 📐 {p['sqft']:,} sq ft
                    </p>
                    <p style="color: #0284C7; font-size: 15px;">✨ {', '.join(p['features'])}</p>
                </div>
                """, unsafe_allow_html=True)

                b1, b2, _ = st.columns([1, 1, 4])
                with b1:
                    if st.button(t['describe'], key=f"d_{p['id']}"):
                        st.session_state.selected = p
                with b2:
                    if st.button(t['compare_btn'], key=f"c_{p['id']}"):
                        if p not in st.session_state.compare:
                            st.session_state.compare.append(p)

    # TAB 2: DESCRIPTIONS
    with tab2:
        st.markdown(f"<h2 style='color: #0C4A6E; font-size: 36px;'>{t['descriptions']}</h2>", unsafe_allow_html=True)
        if st.session_state.selected:
            p = st.session_state.selected
            st.markdown(f"""
            <div style="background: white; border: 3px solid #D4AF37; border-radius: 24px; padding: 28px; margin-bottom: 32px;">
                <h3 style="color: #D4AF37; font-size: 26px;">🏛️ {p['address']}</h3>
                <p style="color: #0C4A6E; font-size: 22px; font-weight: 700;">${p['price']:,}</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                tone = st.selectbox(t['tone'], [t['luxury'], t['professional'], t['warm'], t['family']])
                plat = st.selectbox(t['platform'], ["Instagram", "Facebook", "LinkedIn"])
            with c2:
                length = st.selectbox(t['length'], [t['short'], t['medium'], t['long']])

            if st.button(t['generate'], type="primary", use_container_width=True):
                st.markdown("""
                <div style="background: white; border: 3px solid #D4AF37; border-radius: 24px; padding: 32px;">
                    <h3 style="color: #D4AF37;">🏛️ LUXURY PROPERTY DESCRIPTION</h3>
                """, unsafe_allow_html=True)
                st.write(f"**{p['type']}** in {p['area']}")
                st.write(f"Price: ${p['price']:,}")
                st.write(f"Features: {', '.join(p['features'])}")
                st.markdown(f"🔗 [DealCheck]({AFFILIATES['dealcheck']['url']})")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"<h3 style='color: #0C4A6E; margin-top: 40px;'>{t['social']}</h3>", unsafe_allow_html=True)
                for pl in ["instagram", "facebook", "linkedin"]:
                    with st.expander(pl.title()):
                        st.text_area(pl, f"✨ {p['type']} | {p['area']}\n📍 {p['address']}\n💰 ${p['price']:,}\n🔗 {AFFILIATES['dealcheck']['url']}", height=120)
        else:
            st.info(t['select_property'])

    # TAB 3: COMPARE
    with tab3:
        st.markdown(f"<h2 style='color: #0C4A6E; font-size: 36px;'>{t['compare']}</h2>", unsafe_allow_html=True)
        cl = st.session_state.compare
        if len(cl) >= 2:
            st.write(f"{len(cl)} properties selected")
            data = []
            for p in cl:
                data.append({
                    "Address": p['address'][:40],
                    "Price": f"${p['price']:,}",
                    "Price/sqft": f"${round(p['price']/p['sqft'], 2)}",
                    "Beds": p['bedrooms'],
                    "Baths": p['bathrooms'],
                    "Sqft": f"{p['sqft']:,}",
                    "Type": p['type']
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

            if st.button(t['analysis_btn'], type="primary", use_container_width=True):
                winner = min(cl, key=lambda x: x['price']/x['sqft'])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(212,175,55,0.2) 0%, rgba(212,175,55,0.05) 100%); 
                            border: 3px solid #D4AF37; border-radius: 24px; padding: 32px;">
                    <h2 style="color: #D4AF37; font-size: 28px;">{t['best_value']}</h2>
                    <p style="color: #0C4A6E; font-size: 22px; font-weight: 600;">{winner['address']}</p>
                    <p style="color: #D4AF37; font-size: 36px; font-weight: 700;">${winner['price']:,}</p>
                    <p style="color: #0284C7; font-size: 20px;">{t['price_sqft']}: ${round(winner['price']/winner['sqft'], 2)}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t['add_compare'])

    # TAB 4: ANALYSIS
    with tab4:
        st.markdown(f"<h2 style='color: #0C4A6E; font-size: 36px;'>{t['analysis']}</h2>", unsafe_allow_html=True)
        if st.session_state.saved:
            prices = [p['price'] for p in st.session_state.saved]
            sqfts = [p['sqft'] for p in st.session_state.saved]

            c1, c2, c3, c4 = st.columns(4)
            c1.metric(t['avg'], f"${sum(prices)//len(prices):,}")
            c2.metric(t['min'], f"${min(prices):,}")
            c3.metric(t['max'], f"${max(prices):,}")
            c4.metric(t['price_sqft'], f"${sum(prices)//sum(sqfts)}")

            df = pd.DataFrame(st.session_state.saved)
            fig = go.Figure(go.Bar(x=df['address'], y=df['price'], marker_color='#0284C7',
                                   text=df['price'].apply(lambda x: f'${x:,.0f}'), textposition='auto'))
            fig.update_layout(title=t['market_stats'], plot_bgcolor='rgba(0,0,0,0)', 
                            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#0C4A6E'), height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['search_first'])

    # TAB 5: PARTNERS
    with tab5:
        st.markdown(f"<h2 style='color: #0C4A6E; font-size: 36px;'>{t['partners']}</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: white; border: 3px solid #D4AF37; border-radius: 24px; padding: 32px; margin-bottom: 32px;">
            <h3 style="color: #D4AF37; font-size: 24px;">💎 Premium Tools for Investors</h3>
            <p style="color: #0369A1;">Replace YOUR_AFFILIATE_ID with your real IDs</p>
        </div>
        """, unsafe_allow_html=True)

        for key, prog in AFFILIATES.items():
            st.markdown(f"""
            <div class="property-card" style="border-left: 5px solid #D4AF37;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #D4AF37; font-size: 24px;">{prog['name']}</h4>
                        <p style="color: #0369A1;">{prog['desc'].get(L, prog['desc']['en'])}</p>
                        <p style="color: #0284C7;">💰 {t['commission']}: {prog['commission']} | 📂 {t['category']}: {prog['cat'].get(L, prog['cat']['en'])}</p>
                    </div>
                    <a href="{prog['url']}" target="_blank" style="background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 100%); 
                       color: #0C4A6E; padding: 14px 28px; border-radius: 14px; text-decoration: none; font-weight: 700;">
                        {t['access']}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer">
        <p style="color: #0369A1; font-size: 18px;">{t['footer']}</p>
        <p style="color: #D4AF37; font-family: Playfair Display, serif; font-size: 24px; margin-top: 16px;">
            ✨ Luxury Real Estate Solutions ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
