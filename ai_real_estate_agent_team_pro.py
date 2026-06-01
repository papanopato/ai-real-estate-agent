import os
import streamlit as st
import json
import time
from typing import List, Dict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# CONFIGURATION LUXE - BLEU OUVERT & OR
# ============================================

LUXURY_COLORS = {
    "primary": "#4A90E2",      # Bleu ouvert (sky blue)
    "primary_dark": "#357ABD", # Bleu ouvert foncé
    "primary_light": "#7BB3F0", # Bleu ouvert clair
    "accent": "#D4AF37",       # Or/Doré
    "accent_light": "#F0E68C", # Or clair
    "background": "#F0F8FF",   # Fond bleu très clair (Alice Blue)
    "card_bg": "#FFFFFF",      # Fond carte blanc
    "text": "#1A365D",         # Texte bleu foncé
    "text_secondary": "#4A5568", # Texte gris-bleu
    "text_light": "#FFFFFF",   # Texte blanc
    "border": "#B8D4E8",       # Bordure bleu clair
    "success": "#48BB78",      # Vert
    "warning": "#ED8936",      # Orange
}

# ============================================
# TRADUCTIONS MULTILINGUES
# ============================================

TRANSLATIONS = {
    "en": {
        "title": "AI Real Estate Agent",
        "subtitle": "Luxury Property Solutions",
        "search_tab": "🔍 Search",
        "description_tab": "✍️ Descriptions",
        "comparison_tab": "⚖️ Compare",
        "analysis_tab": "📊 Analysis",
        "affiliation_tab": "🔗 Partners",
        "city": "City",
        "state": "State/Region",
        "min_price": "Min Price ($)",
        "max_price": "Max Price ($)",
        "bedrooms": "Bedrooms",
        "property_type": "Property Type",
        "search_button": "🚀 Search Properties",
        "searching": "Searching luxury properties...",
        "properties_found": "luxury properties found",
        "describe_button": "✍️ Describe",
        "compare_button": "⭐ Compare",
        "generate_description": "📝 Generate Description",
        "language": "Language",
        "platform": "Platform",
        "tone": "Tone",
        "length": "Length",
        "professional": "Professional",
        "warm": "Warm",
        "luxury": "Luxury",
        "family": "Family",
        "short": "Short (100 words)",
        "medium": "Medium (200 words)",
        "long": "Long (300 words)",
        "social_posts": "📱 Social Media Posts",
        "detailed_analysis": "🔍 Detailed Analysis",
        "winner": "🏆 BEST VALUE",
        "price_per_sqft": "Price per sq ft",
        "market_stats": "Market Statistics",
        "avg_price": "Average Price",
        "min_price_stat": "Min Price",
        "max_price_stat": "Max Price",
        "affiliate_programs": "Premium Partners",
        "commission": "Commission",
        "category": "Category",
        "copy_link": "Copy",
        "footer": "© 2026 AI Real Estate Agent | Luxury Edition",
        "welcome_message": "Your luxury real estate AI assistant",
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
        "search_tab": "🔍 Recherche",
        "description_tab": "✍️ Descriptions",
        "comparison_tab": "⚖️ Comparer",
        "analysis_tab": "📊 Analyse",
        "affiliation_tab": "🔗 Partenaires",
        "city": "Ville",
        "state": "État/Région",
        "min_price": "Prix Min ($)",
        "max_price": "Prix Max ($)",
        "bedrooms": "Chambres",
        "property_type": "Type de Bien",
        "search_button": "🚀 Rechercher",
        "searching": "Recherche de biens de luxe...",
        "properties_found": "biens de luxe trouvés",
        "describe_button": "✍️ Décrire",
        "compare_button": "⭐ Comparer",
        "generate_description": "📝 Générer",
        "language": "Langue",
        "platform": "Plateforme",
        "tone": "Ton",
        "length": "Longueur",
        "professional": "Professionnel",
        "warm": "Chaleureux",
        "luxury": "Luxe",
        "family": "Familial",
        "short": "Courte",
        "medium": "Moyenne",
        "long": "Longue",
        "social_posts": "📱 Réseaux Sociaux",
        "detailed_analysis": "🔍 Analyse Détaillée",
        "winner": "🏆 MEILLEUR RAPPORT",
        "price_per_sqft": "Prix/m²",
        "market_stats": "Statistiques du Marché",
        "avg_price": "Prix Moyen",
        "min_price_stat": "Prix Min",
        "max_price_stat": "Prix Max",
        "affiliate_programs": "Partenaires Premium",
        "commission": "Commission",
        "category": "Catégorie",
        "copy_link": "Copier",
        "footer": "© 2026 Agent Immobilier IA | Édition Luxe",
        "welcome_message": "Votre assistant immobilier de luxe",
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
        "search_tab": "🔍 Búsqueda",
        "description_tab": "✍️ Descripciones",
        "comparison_tab": "⚖️ Comparar",
        "analysis_tab": "📊 Análisis",
        "affiliation_tab": "🔗 Socios",
        "city": "Ciudad",
        "state": "Estado/Región",
        "min_price": "Precio Mín ($)",
        "max_price": "Precio Máx ($)",
        "bedrooms": "Habitaciones",
        "property_type": "Tipo de Propiedad",
        "search_button": "🚀 Buscar Propiedades",
        "searching": "Buscando propiedades de lujo...",
        "properties_found": "propiedades de lujo encontradas",
        "describe_button": "✍️ Describir",
        "compare_button": "⭐ Comparar",
        "generate_description": "📝 Generar Descripción",
        "language": "Idioma",
        "platform": "Plataforma",
        "tone": "Tono",
        "length": "Longitud",
        "professional": "Profesional",
        "warm": "Cálido",
        "luxury": "Lujo",
        "family": "Familiar",
        "short": "Corta (100 palabras)",
        "medium": "Media (200 palabras)",
        "long": "Larga (300 palabras)",
        "social_posts": "📱 Posts Redes Sociales",
        "detailed_analysis": "🔍 Análisis Detallado",
        "winner": "🏆 MEJOR RELACIÓN CALIDAD/PRECIO",
        "price_per_sqft": "Precio por sq ft",
        "market_stats": "Estadísticas del Mercado",
        "avg_price": "Precio Promedio",
        "min_price_stat": "Precio Mín",
        "max_price_stat": "Precio Máx",
        "affiliate_programs": "Socios Premium",
        "commission": "Comisión",
        "category": "Categoría",
        "copy_link": "Copiar",
        "footer": "© 2026 Agente Inmobiliario IA | Edición Lujo",
        "welcome_message": "Tu asistente inmobiliario de lujo",
        "select_property": "Selecciona una propiedad de la pestaña Búsqueda",
        "add_compare": "Agrega al menos 2 propiedades para comparar",
        "search_first": "Inicia una búsqueda primero",
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
        "search_tab": "🔍 بحث",
        "description_tab": "✍️ وصف",
        "comparison_tab": "⚖️ مقارنة",
        "analysis_tab": "📊 تحليل",
        "affiliation_tab": "🔗 شركاء",
        "city": "المدينة",
        "state": "المنطقة",
        "min_price": "الحد الأدنى ($)",
        "max_price": "الحد الأقصى ($)",
        "bedrooms": "غرف النوم",
        "property_type": "النوع",
        "search_button": "🚀 بحث",
        "searching": "جاري البحث...",
        "properties_found": "عقارات تم العثور عليها",
        "describe_button": "✍️ وصف",
        "compare_button": "⭐ مقارنة",
        "generate_description": "📝 إنشاء",
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

AFFILIATE_LINKS = {
    "buildium": {
        "name": "Buildium",
        "url": "https://www.buildium.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Property Management Software", "fr": "Logiciel de gestion locative", "es": "Software de gestión", "ar": "برنامج إدارة العقارات"},
        "commission": "25% recurring",
        "category": {"en": "Management", "fr": "Gestion", "es": "Gestión", "ar": "إدارة"}
    },
    "dealcheck": {
        "name": "DealCheck",
        "url": "https://dealcheck.io?fp_ref=omar18",
        "description": {"en": "Investment Analysis", "fr": "Analyse d'investissement", "es": "Análisis de inversión", "ar": "تحليل الاستثمار"},
        "commission": "30% recurring",
        "category": {"en": "Analysis", "fr": "Analyse", "es": "Análisis", "ar": "تحليل"}
    },
    "foreclosure": {
        "name": "Foreclosure.com",
        "url": "https://www.foreclosure.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Foreclosed Properties", "fr": "Biens saisis", "es": "Propiedades embargadas", "ar": "عقارات مصادرة"},
        "commission": "25%",
        "category": {"en": "Foreclosures", "fr": "Saisies", "es": "Embargos", "ar": "مصادرة"}
    },
    "nolo": {
        "name": "NOLO",
        "url": "https://www.nolo.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Legal Documents", "fr": "Documents juridiques", "es": "Documentos legales", "ar": "مستندات قانونية"},
        "commission": "25-35%",
        "category": {"en": "Legal", "fr": "Juridique", "es": "Legal", "ar": "قانوني"}
    },
    "biggerpockets": {
        "name": "BiggerPockets",
        "url": "https://www.biggerpockets.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Investor Community", "fr": "Communauté investisseurs", "es": "Comunidad inversores", "ar": "مجتمع المستثمرين"},
        "commission": "$75/signup",
        "category": {"en": "Education", "fr": "Éducation", "es": "Educación", "ar": "تعليم"}
    },
}

# ============================================
# LUXURY PROPERTIES
# ============================================

LUXURY_PROPERTIES = [
    {
        "id": "prop_001",
        "address": "123 Ocean Drive, Miami Beach, FL",
        "price": 2500000,
        "bedrooms": 5,
        "bathrooms": 4.5,
        "square_feet": 4200,
        "property_type": "Villa",
        "year_built": 2019,
        "neighborhood": "South Beach",
        "features": ["Infinity Pool", "Private Beach", "Smart Home", "Wine Cellar"],
        "agent_name": "Alexandra Sterling",
        "agent_phone": "(305) 555-0199",
    },
    {
        "id": "prop_002",
        "address": "456 Palm Avenue, Coral Gables, FL",
        "price": 1850000,
        "bedrooms": 4,
        "bathrooms": 3.5,
        "square_feet": 3500,
        "property_type": "Estate",
        "year_built": 2017,
        "neighborhood": "Coral Gables",
        "features": ["Tennis Court", "Guest House", "Mediterranean Style"],
        "agent_name": "Marcus Wellington",
        "agent_phone": "(305) 555-0288",
    },
    {
        "id": "prop_003",
        "address": "789 Star Island, Miami Beach, FL",
        "price": 4500000,
        "bedrooms": 6,
        "bathrooms": 5.5,
        "square_feet": 5800,
        "property_type": "Waterfront Mansion",
        "year_built": 2021,
        "neighborhood": "Star Island",
        "features": ["Private Dock", "Panoramic Views", "Elevator", "Spa"],
        "agent_name": "Victoria Ashford",
        "agent_phone": "(305) 555-0377",
    },
    {
        "id": "prop_004",
        "address": "321 Brickell Avenue, Miami, FL",
        "price": 3200000,
        "bedrooms": 3,
        "bathrooms": 3,
        "square_feet": 2800,
        "property_type": "Penthouse",
        "year_built": 2022,
        "neighborhood": "Brickell",
        "features": ["360° Views", "Private Terrace", "Concierge", "Rooftop Pool"],
        "agent_name": "James Carrington",
        "agent_phone": "(305) 555-0466",
    }
]

# ============================================
# CSS STYLING - BLEU OUVERT & OR
# ============================================

def get_luxury_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    .main {
        background: linear-gradient(180deg, #F0F8FF 0%, #E6F2FF 50%, #F0F8FF 100%);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1A365D !important;
    }

    /* Language buttons */
    .lang-btn {
        background: linear-gradient(135deg, #4A90E2 0%, #7BB3F0 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3) !important;
    }

    .lang-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4) !important;
    }

    /* Primary buttons */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 100%) !important;
        color: #1A365D !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        border-radius: 16px !important;
        padding: 12px !important;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 100%) !important;
        border-radius: 10px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #1A365D !important;
        font-weight: 700 !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #B8D4E8 !important;
        color: #1A365D !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 15px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important;
    }

    .stSelectbox > div > div > div {
        background: white !important;
        border: 2px solid #B8D4E8 !important;
        color: #1A365D !important;
        border-radius: 10px !important;
    }

    .stNumberInput > div > div > input {
        background: white !important;
        border: 2px solid #B8D4E8 !important;
        color: #1A365D !important;
        border-radius: 10px !important;
    }

    /* Metrics */
    .stMetric {
        background: white !important;
        border: 2px solid #B8D4E8 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.1) !important;
    }

    .stMetric > div {
        color: #D4AF37 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    .stMetric > label {
        color: #4A5568 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* Property cards */
    .property-card {
        background: white;
        border: 2px solid #B8D4E8;
        border-radius: 20px;
        padding: 28px;
        margin: 16px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.1);
    }

    .property-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.2);
        transform: translateY(-4px);
    }

    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 8px 30px rgba(74, 144, 226, 0.3);
    }

    .welcome-banner h2 {
        color: white !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 28px !important;
        margin-bottom: 8px !important;
    }

    .welcome-banner p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 16px !important;
    }

    /* Header section */
    .header-section {
        background: white;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.15);
        border: 2px solid #B8D4E8;
    }

    /* Gold accent */
    .gold-accent {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
    }

    /* Divider */
    .luxury-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #D4AF37 30%, #4A90E2 70%, transparent 100%);
        margin: 24px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 32px;
        color: #4A5568;
        font-size: 14px;
        background: white;
        border-radius: 20px;
        margin-top: 48px;
        border: 2px solid #B8D4E8;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F0F8FF;
    }

    ::-webkit-scrollbar-thumb {
        background: #B8D4E8;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #4A90E2;
    }

    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #48BB78 0%, #38A169 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    /* Info message */
    .stInfo {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    </style>
    """

# ============================================
# PROPERTY DESCRIPTION GENERATOR
# ============================================

class PropertyDescriptionAgent:
    def generate_description(self, property_data: dict, lang: str = "en", tone: str = "luxury") -> str:
        address = property_data.get('address', 'N/A')
        prop_type = property_data.get('property_type', 'N/A')
        price = property_data.get('price', 0)
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        sqft = property_data.get('square_feet', 0)
        neighborhood = property_data.get('neighborhood', 'N/A')
        features = property_data.get('features', [])
        year = property_data.get('year_built', 'N/A')

        features_text = ", ".join(features) if features else "exceptional features"

        descriptions = {
            "en": {
                "luxury": f"""
🏛️ AN EXQUISITE {prop_type.upper()} IN {neighborhood.upper()}

Welcome to an extraordinary residence that defines luxury living. This magnificent {prop_type.lower()} 
spanning {sqft:,} square feet offers an unparalleled lifestyle in the prestigious {neighborhood} enclave.

✨ EXCEPTIONAL FEATURES:
• {bedrooms} sumptuous bedroom suites with en-suite baths
• {bathrooms} spa-inspired bathrooms with premium finishes
• {features_text}
• Built in {year} with meticulous attention to detail
• Expansive living spaces designed for entertaining

📍 PREMIUM LOCATION:
Situated in the heart of {neighborhood}, this property offers proximity to world-class dining, 
boutique shopping, and pristine beaches.

💎 INVESTMENT HIGHLIGHT:
Priced at ${price:,}, this represents exceptional value at ${price//sqft:,} per square foot 
in one of Miami's most coveted neighborhoods.

🔗 Analyze this investment with DealCheck: {AFFILIATE_LINKS['dealcheck']['url']}
📋 Legal documents with NOLO: {AFFILIATE_LINKS['nolo']['url']}
                """,
            },
            "fr": {
                "luxury": f"""
🏛️ UNE {prop_type.upper()} D'EXCEPTION À {neighborhood.upper()}

Bienvenue dans une résidence extraordinaire qui redéfinit le luxe. Cette magnifique {prop_type.lower()} 
de {sqft:,} pieds carrés offre un style de vie incomparable dans le prestigieux quartier {neighborhood}.

✨ CARACTÉRISTIQUES EXCEPTIONNELLES :
• {bedrooms} suites chambres somptueuses avec salles de bain privatives
• {bathrooms} salles de bain inspirées des spas avec finitions premium
• {features_text}
• Construit en {year} avec une attention méticuleuse aux détails
• Espaces de vie spacieux conçus pour recevoir

📍 EMPLACEMENT PRESTIGIEUX :
Situé au cœur de {neighborhood}, cette propriété offre un accès privilégié aux restaurants 
gastronomiques, boutiques de luxe et plages immaculées.

💎 POINT FORT INVESTISSEMENT :
Prix : ${price:,}, ce qui représente une valeur exceptionnelle à ${price//sqft:,} $/sq ft 
dans l'un des quartiers les plus prisés de Miami.

🔗 Analysez cet investissement avec DealCheck : {AFFILIATE_LINKS['dealcheck']['url']}
📋 Documents juridiques avec NOLO : {AFFILIATE_LINKS['nolo']['url']}
                """,
            },
            "es": {
                "luxury": f"""
🏛️ UNA {prop_type.upper()} DE EXCEPCIÓN EN {neighborhood.upper()}

Bienvenido a una residencia extraordinaria que redefine el lujo. Esta magnífica {prop_type.lower()} 
de {sqft:,} pies cuadrados ofrece un estilo de vida incomparable en el prestigioso {neighborhood}.

✨ CARACTERÍSTICAS EXCEPCIONALES:
• {bedrooms} suites de dormitorio suntuosas con baños en suite
• {bathrooms} baños inspirados en spas con acabados premium
• {features_text}
• Construido en {year} con meticulosa atención al detalle

🔗 Analice esta inversión con DealCheck: {AFFILIATE_LINKS['dealcheck']['url']}
📋 Documentos legales con NOLO: {AFFILIATE_LINKS['nolo']['url']}
                """,
            },
            "ar": {
                "luxury": f"""
🏛️ {prop_type.upper()} فاخرة في {neighborhood}

مرحباً بك في مسكن استثنائي يعيد تعريف الفخامة. هذه {prop_type} الرائعة 
بمساحة {sqft:,} قدم مربع تقدم أسلوب حياة لا مثيل له.

✨ مميزات استثنائية:
• {bedrooms} أجنحة نوم فاخرة مع حمامات داخلية
• {bathrooms} حمامات مستوحاة من المنتجعات الصحية
• {features_text}
• بنيت عام {year} باهتمام دقيق بالتفاصيل

🔗 حلل هذا الاستثمار مع DealCheck: {AFFILIATE_LINKS['dealcheck']['url']}
📋 المستندات القانونية مع NOLO: {AFFILIATE_LINKS['nolo']['url']}
                """,
            }
        }

        return descriptions.get(lang, descriptions["en"]).get(tone, descriptions["en"]["luxury"])

    def generate_social_media_post(self, property_data: dict, platform: str = "instagram", lang: str = "en") -> str:
        address = property_data.get('address', '')
        price = property_data.get('price', 0)
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        prop_type = property_data.get('property_type', 'Property')
        neighborhood = property_data.get('neighborhood', '')

        posts = {
            "en": {
                "instagram": f"""
✨ LUXURY LIVING AT ITS FINEST ✨

{prop_type} | {neighborhood}
📍 {address}
💰 ${price:,}
🛏️ {bedrooms} Suites | 🛁 {bathrooms} Baths

Your dream home awaits. Contact us for a private viewing.

🔗 Investment Analysis: {AFFILIATE_LINKS['dealcheck']['url']}

#luxuryrealestate #miami #{neighborhood.replace(' ', '')} #luxuryhome
                """,
                "facebook": f"""
🏛️ EXCLUSIVE LISTING 🏛️

Presenting an exceptional {prop_type} in the prestigious {neighborhood} neighborhood.

📍 Location: {address}
💰 Price: ${price:,}
🛏️ Bedrooms: {bedrooms}
🛁 Bathrooms: {bathrooms}

📊 Analyze the investment potential: {AFFILIATE_LINKS['dealcheck']['url']}
📞 Schedule your private tour today!
                """,
                "linkedin": f"""
📊 PREMIUM INVESTMENT OPPORTUNITY

{prop_type} | {neighborhood} | Miami

Investment Highlights:
• Asking Price: ${price:,}
• Location: Premier {neighborhood} address
• Type: Luxury {prop_type}

🔗 Professional Analysis: {AFFILIATE_LINKS['dealcheck']['url']}
🔗 Investor Community: {AFFILIATE_LINKS['biggerpockets']['url']}

#realestateinvestment #luxuryproperty #miamirealestate
                """
            },
            "fr": {
                "instagram": f"""
✨ L'ART DE VIVRE À L'ÉTAT PUR ✨

{prop_type} | {neighborhood}
📍 {address}
💰 ${price:,}
🛏️ {bedrooms} Suites | 🛁 {bathrooms} SDB

Votre maison de rêve vous attend. Contactez-nous pour une visite privée.

🔗 Analyse d'investissement : {AFFILIATE_LINKS['dealcheck']['url']}

#immobilierdeluxe #miami #{neighborhood.replace(' ', '')} #maisondeluxe
                """,
                "facebook": f"""
🏛️ LISTING EXCLUSIF 🏛️

Présentation d'un(e) {prop_type} exceptionnel(le) dans le prestigieux quartier {neighborhood}.

📍 Adresse : {address}
💰 Prix : ${price:,}
🛏️ Chambres : {bedrooms}
🛁 Salles de bain : {bathrooms}

📊 Analyse de l'investissement : {AFFILIATE_LINKS['dealcheck']['url']}
📞 Réservez votre visite privée !
                """,
                "linkedin": f"""
📊 OPPORTUNITÉ D'INVESTISSEMENT PREMIUM

{prop_type} | {neighborhood} | Miami

Points clés de l'investissement :
• Prix demandé : ${price:,}
• Emplacement : Adresse premium {neighborhood}

🔗 Analyse professionnelle : {AFFILIATE_LINKS['dealcheck']['url']}
🔗 Communauté investisseurs : {AFFILIATE_LINKS['biggerpockets']['url']}
                """
            },
            "es": {
                "instagram": f"""
✨ EL ARTE DE VIVIR EN ESTADO PURO ✨

{prop_type} | {neighborhood}
📍 {address}
💰 ${price:,}
🛏️ {bedrooms} Suites | 🛁 {bathrooms} Baños

Tu hogar de ensueño te espera. Contáctanos para una visita privada.

🔗 Análisis de inversión: {AFFILIATE_LINKS['dealcheck']['url']}
                """,
            },
            "ar": {
                "instagram": f"""
✨ فن العيش بأبهى صوره ✨

{prop_type} | {neighborhood}
📍 {address}
💰 ${price:,}
🛏️ {bedrooms} أجنحة | 🛁 {bathrooms} حمامات

منزل أحلامك في انتظارك. تواصل معنا لجولة خاصة.

🔗 تحليل الاستثمار: {AFFILIATE_LINKS['dealcheck']['url']}
                """,
            }
        }

        return posts.get(lang, posts["en"]).get(platform, posts["en"]["instagram"])

# ============================================
# PROPERTY COMPARISON
# ============================================

class PropertyComparisonAgent:
    def compare_properties(self, properties: List[Dict], lang: str = "en") -> Dict:
        if len(properties) < 2:
            return {"error": "Minimum 2 properties required"}

        comparison_data = []
        for prop in properties:
            price = prop.get('price', 0) or 0
            sqft = prop.get('square_feet', 0) or 1

            metrics = {
                "id": prop.get('id', 'N/A'),
                "address": prop.get('address', 'N/A'),
                "price": price,
                "price_per_sqft": round(price / sqft, 2) if sqft > 0 else 0,
                "bedrooms": prop.get('bedrooms', 0),
                "bathrooms": prop.get('bathrooms', 0),
                "square_feet": sqft,
                "property_type": prop.get('property_type', 'N/A'),
                "neighborhood": prop.get('neighborhood', 'N/A'),
                "year_built": prop.get('year_built', 'N/A'),
                "features_count": len(prop.get('features', []))
            }
            comparison_data.append(metrics)

        winner = min(comparison_data, key=lambda x: x['price_per_sqft'] if x['price_per_sqft'] > 0 else float('inf'))

        analyses = {
            "en": f"""
### Investment Analysis

**Best Value Property:** {winner['address']}
- Price: ${winner['price']:,}
- Price per sq ft: ${winner['price_per_sqft']}

**Key Insights:**
• The winner offers the most space per dollar invested
• {winner['neighborhood']} provides excellent appreciation potential
• {winner['features_count']} premium features included

**Recommended Tools:**
🔗 {AFFILIATE_LINKS['dealcheck']['name']}: {AFFILIATE_LINKS['dealcheck']['url']}
🔗 {AFFILIATE_LINKS['foreclosure']['name']}: {AFFILIATE_LINKS['foreclosure']['url']}
            """,
            "fr": f"""
### Analyse d'Investissement

**Meilleur Rapport Qualité/Prix :** {winner['address']}
- Prix : ${winner['price']:,}
- Prix au sq ft : ${winner['price_per_sqft']}

**Points Clés :**
• Le bien gagnant offre le plus d'espace par dollar investi
• {winner['neighborhood']} offre un excellent potentiel d'appréciation

**Outils Recommandés :**
🔗 {AFFILIATE_LINKS['dealcheck']['name']} : {AFFILIATE_LINKS['dealcheck']['url']}
            """,
            "es": f"""
### Análisis de Inversión

**Mejor Relación Calidad/Precio:** {winner['address']}
- Precio: ${winner['price']:,}
- Precio por sq ft: ${winner['price_per_sqft']}

**Herramientas Recomendadas:**
🔗 {AFFILIATE_LINKS['dealcheck']['name']}: {AFFILIATE_LINKS['dealcheck']['url']}
            """,
            "ar": f"""
### تحليل الاستثمار

**أفضل قيمة:** {winner['address']}
- السعر: ${winner['price']:,}
- السعر/قدم مربع: ${winner['price_per_sqft']}

**أدوات موصى بها:**
🔗 {AFFILIATE_LINKS['dealcheck']['name']}: {AFFILIATE_LINKS['dealcheck']['url']}
            """
        }

        return {
            "comparison_table": comparison_data,
            "winner": winner,
            "analysis": analyses.get(lang, analyses["en"])
        }

    def generate_comparison_chart(self, properties: List[Dict], lang: str = "en") -> pd.DataFrame:
        labels = {
            "en": {"address": "Address", "price": "Price ($)", "ppsf": "Price/sq ft", "beds": "Bedrooms", "baths": "Bathrooms", "sqft": "Sq Ft", "type": "Type"},
            "fr": {"address": "Adresse", "price": "Prix ($)", "ppsf": "Prix/sq ft", "beds": "Chambres", "baths": "SDB", "sqft": "Sq Ft", "type": "Type"},
            "es": {"address": "Dirección", "price": "Precio ($)", "ppsf": "Precio/sq ft", "beds": "Dormitorios", "baths": "Baños", "sqft": "Sq Ft", "type": "Tipo"},
            "ar": {
        "title": "وكيل عقارات ذكي",
        "subtitle": "حلول عقارية فاخرة",
        "search_tab": "🔍 بحث",
        "description_tab": "✍️ وصف",
        "comparison_tab": "⚖️ مقارنة",
        "analysis_tab": "📊 تحليل",
        "affiliation_tab": "🔗 شركاء",
        "city": "المدينة",
        "state": "المنطقة",
        "min_price": "الحد الأدنى ($)",
        "max_price": "الحد الأقصى ($)",
        "bedrooms": "غرف النوم",
        "property_type": "نوع العقار",
        "search_button": "🚀 بحث عن عقارات",
        "searching": "جاري البحث عن عقارات فاخرة...",
        "properties_found": "عقارات فاخرة تم العثور عليها",
        "describe_button": "✍️ وصف",
        "compare_button": "⭐ مقارنة",
        "generate_description": "📝 إنشاء وصف",
        "language": "اللغة",
        "platform": "المنصة",
        "tone": "النبرة",
        "length": "الطول",
        "professional": "احترافي",
        "warm": "دافئ",
        "luxury": "فاخر",
        "family": "عائلي",
        "short": "قصير (100 كلمة)",
        "medium": "متوسط (200 كلمة)",
        "long": "طويل (300 كلمة)",
        "social_posts": "📱 منشورات التواصل الاجتماعي",
        "detailed_analysis": "🔍 تحليل مفصل",
        "winner": "🏆 أفضل قيمة",
        "price_per_sqft": "السعر لكل قدم مربع",
        "market_stats": "إحصائيات السوق",
        "avg_price": "متوسط السعر",
        "min_price_stat": "الحد الأدنى",
        "max_price_stat": "الحد الأقصى",
        "affiliate_programs": "شركاء مميزون",
        "commission": "العمولة",
        "category": "الفئة",
        "copy_link": "نسخ",
        "footer": "© 2026 وكيل عقارات ذكي | النسخة الفاخرة",
        "welcome_message": "مساعدك العقاري الفاخر",
        "select_property": "اختر عقاراً من تبويب البحث",
        "add_compare": "أضف عقارين على الأقل للمقارنة",
        "search_first": "ابدأ البحث أولاً",
        "all": "الكل",
        "villa": "فيلا",
        "penthouse": "بنتهاوس",
        "estate": "عقار",
        "mansion": "قصر",
        "condo": "شقة فاخرة",
    },
        }

        l = labels.get(lang, labels["en"])
        data = []
        for prop in properties:
            price = prop.get('price', 0) or 0
            sqft = prop.get('square_feet', 1) or 1
            data.append({
                l["address"]: prop.get('address', 'N/A')[:35] + "...",
                l["price"]: f"${price:,}",
                l["ppsf"]: f"${round(price/sqft, 2)}",
                l["beds"]: prop.get('bedrooms', 0),
                l["baths"]: prop.get('bathrooms', 0),
                l["sqft"]: f"{prop.get('square_feet', 0):,}",
                l["type"]: prop.get('property_type', 'N/A')
            })
        return pd.DataFrame(data)

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Real Estate Agent - Luxury Edition",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply luxury CSS
    st.markdown(get_luxury_css(), unsafe_allow_html=True)

    # Initialize session state
    if 'saved_properties' not in st.session_state:
        st.session_state.saved_properties = []
    if 'selected_for_description' not in st.session_state:
        st.session_state.selected_for_description = None
    if 'compare_list' not in st.session_state:
        st.session_state.compare_list = []
    if 'current_lang' not in st.session_state:
        st.session_state.current_lang = "en"

    # ============================================
    # HEADER SECTION WITH LANGUAGE SELECTOR
    # ============================================

    # Language selector - top right
    lang_col1, lang_col2, lang_col3, lang_col4, lang_spacer = st.columns([1, 1, 1, 1, 8])

    with lang_col1:
        if st.button("🇬🇧 EN", key="lang_en", help="English"):
            st.session_state.current_lang = "en"
    with lang_col2:
        if st.button("🇫🇷 FR", key="lang_fr", help="Français"):
            st.session_state.current_lang = "fr"
    with lang_col3:
        if st.button("🇪🇸 ES", key="lang_es", help="Español"):
            st.session_state.current_lang = "es"
    with lang_col4:
        if st.button("🇸🇦 AR", key="lang_ar", help="العربية"):
            st.session_state.current_lang = "ar"

    lang = st.session_state.current_lang
    t = TRANSLATIONS[lang]

    # ============================================
    # LOGO AND TITLE SECTION
    # ============================================

    st.markdown("""
    <div class="header-section">
        <div style="display: flex; align-items: center; gap: 24px;">
            <div style="flex-shrink: 0;">
    """, unsafe_allow_html=True)

    # Logo
    col_logo, col_title = st.columns([1, 4])

    with col_logo:
        try:
            st.image("logo.png", width=150)
        except:
            st.markdown("<div style='font-size: 80px; text-align: center;'>🏛️</div>", unsafe_allow_html=True)

    with col_title:
        st.markdown(f"""
        <h1 style='font-family: Playfair Display, serif; color: #1A365D; font-size: 42px; margin-bottom: 8px;'>
            {t['title']}
        </h1>
        <p style='color: #4A90E2; font-size: 20px; font-style: italic; margin: 0;'>
            ✨ {t['subtitle']} ✨
        </p>
        <div class="luxury-divider"></div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ============================================
    # WELCOME BANNER
    # ============================================

    st.markdown(f"""
    <div class="welcome-banner">
        <h2>🌟 {t['welcome_message']} 🌟</h2>
        <p style="font-size: 18px; margin-top: 12px;">
            Premium Real Estate Solutions for Discerning Clients Worldwide
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # MAIN TABS
    # ============================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t['search_tab'], t['description_tab'], t['comparison_tab'], 
        t['analysis_tab'], t['affiliation_tab']
    ])

    # TAB 1: SEARCH
    with tab1:
        st.markdown(f"<h2 style='color: #1A365D; font-family: Playfair Display, serif; font-size: 32px;'>{t['search_tab']}</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input(t['city'], value="Miami", placeholder="Miami")
            min_price = st.number_input(t['min_price'], min_value=0, value=1000000, step=100000)
            bedrooms = st.selectbox(t['bedrooms'], [1, 2, 3, 4, 5, 6])
        with col2:
            state = st.text_input(t['state'], value="FL", placeholder="FL")
            max_price = st.number_input(t['max_price'], min_value=0, value=5000000, step=100000)

            prop_types = {
                "en": ["All", "Villa", "Penthouse", "Estate", "Waterfront Mansion", "Luxury Condo"],
                "fr": ["Tous", "Villa", "Penthouse", "Domaine", "Manoir", "Condo Luxe"],
                "es": ["Todos", "Villa", "Penthouse", "Finca", "Mansión", "Condo"],
                "ar": ["الكل", "فيلا", "بنتهاوس", "عقار", "قصر", "شقة فاخرة"],
            }
            property_type = st.selectbox(t['property_type'], prop_types.get(lang, prop_types["en"]))

        if st.button(t['search_button'], type="primary", use_container_width=True):
            with st.spinner(t['searching']):
                time.sleep(1.5)
                st.session_state.saved_properties = LUXURY_PROPERTIES

            st.success(f"✨ {len(LUXURY_PROPERTIES)} {t['properties_found']}")

            for prop in LUXURY_PROPERTIES:
                with st.container():
                    st.markdown(f"""
                    <div class="property-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h3 style="color: #D4AF37; font-family: Playfair Display, serif; font-size: 24px; margin-bottom: 12px;">
                                    🏛️ {prop['property_type']}
                                </h3>
                                <p style="color: #1A365D; font-size: 18px; margin-bottom: 8px; font-weight: 600;">
                                    📍 {prop['address']}
                                </p>
                                <p style="color: #4A5568; font-size: 16px; line-height: 1.6;">
                                    💰 <span style="color: #D4AF37; font-weight: 700; font-size: 20px;">${prop['price']:,}</span> | 
                                    🛏️ {prop['bedrooms']} {t['bedrooms']} | 
                                    🛁 {prop['bathrooms']} Baths | 
                                    📐 {prop['square_feet']:,} sq ft
                                </p>
                                <p style="color: #4A90E2; font-size: 14px; margin-top: 12px; font-weight: 500;">
                                    ✨ {', '.join(prop['features'])}
                                </p>
                                <p style="color: #4A5568; font-size: 13px; margin-top: 8px;">
                                    👤 {prop['agent_name']} | 📞 {prop['agent_phone']}
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_btn1, col_btn2, col_space = st.columns([1, 1, 4])
                    with col_btn1:
                        if st.button(t['describe_button'], key=f"desc_{prop['id']}"):
                            st.session_state.selected_for_description = prop
                    with col_btn2:
                        if st.button(t['compare_button'], key=f"comp_{prop['id']}"):
                            if prop not in st.session_state.compare_list:
                                st.session_state.compare_list.append(prop)

    # TAB 2: DESCRIPTIONS
    with tab2:
        st.markdown(f"<h2 style='color: #1A365D; font-family: Playfair Display, serif; font-size: 32px;'>{t['description_tab']}</h2>", unsafe_allow_html=True)

        if st.session_state.selected_for_description:
            prop = st.session_state.selected_for_description
            st.markdown(f"""
            <div style="background: white; border: 2px solid #B8D4E8; border-radius: 20px; padding: 24px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(74, 144, 226, 0.15);">
                <h3 style="color: #D4AF37; font-family: Playfair Display, serif; margin-bottom: 12px;">🏛️ {prop['address']}</h3>
                <p style="color: #4A5568; font-size: 18px;">
                    <span style="color: #D4AF37; font-weight: 700; font-size: 24px;">${prop['price']:,}</span> | {prop['property_type']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                tone_options = {
                    "en": [t['luxury'], t['professional'], t['warm'], t['family']],
                    "fr": [t['luxury'], t['professional'], t['warm'], t['family']],
                    "es": ["Lujo", "Profesional", "Cálido", "Familiar"],
                    "ar": ["فاخر", "احترافي", "دافئ", "عائلي"],
                }
                tone = st.selectbox(t['tone'], tone_options.get(lang, tone_options["en"]))
                platform = st.selectbox(t['platform'], ["Instagram", "Facebook", "LinkedIn"])
            with col2:
                length_options = {
                    "en": [t['short'], t['medium'], t['long']],
                    "fr": [t['short'], t['medium'], t['long']],
                    "es": ["Corta", "Media", "Larga"],
                    "ar": ["قصير", "متوسط", "طويل"],
                }
                length = st.selectbox(t['length'], length_options.get(lang, length_options["en"]))

            tone_map = {"Luxe": "luxury", "Luxury": "luxury", "فاخر": "luxury",
                       "Professionnel": "professional", "Professional": "professional", "احترافي": "professional",
                       "Chaleureux": "warm", "Warm": "warm", "Cálido": "warm", "دافئ": "warm",
                       "Familial": "family", "Family": "family", "Familiar": "family", "عائلي": "family"}
            selected_tone = tone_map.get(tone, "luxury")

            if st.button(t['generate_description'], type="primary", use_container_width=True):
                desc_agent = PropertyDescriptionAgent()

                with st.spinner("✨ Generating luxury description..."):
                    description = desc_agent.generate_description(prop, lang, selected_tone)

                st.markdown("""
                <div style="background: white; border: 3px solid #D4AF37; 
                            border-radius: 24px; padding: 32px; margin-top: 24px;
                            box-shadow: 0 8px 30px rgba(212, 175, 55, 0.2);">
                """, unsafe_allow_html=True)
                st.markdown(description)
                st.markdown("</div>", unsafe_allow_html=True)

                # Social media posts
                st.markdown(f"<h3 style='color: #1A365D; font-family: Playfair Display, serif; margin-top: 40px; font-size: 28px;'>{t['social_posts']}</h3>", unsafe_allow_html=True)

                for plat in ["instagram", "facebook", "linkedin"]:
                    post = desc_agent.generate_social_media_post(prop, plat, lang)
                    with st.expander(f"📱 {plat.title()}"):
                        st.text_area(f"{plat}", post, height=150)
                        st.button("📋 Copy", key=f"copy_{plat}_{prop['id']}")
        else:
            st.info(t['select_property'])

    # TAB 3: COMPARISON
    with tab3:
        st.markdown(f"<h2 style='color: #1A365D; font-family: Playfair Display, serif; font-size: 32px;'>{t['comparison_tab']}</h2>", unsafe_allow_html=True)

        compare_list = st.session_state.compare_list

        if len(compare_list) >= 2:
            st.markdown(f"<p style='color: #4A5568; font-size: 18px; margin-bottom: 24px;'>{len(compare_list)} properties selected</p>", unsafe_allow_html=True)

            comp_agent = PropertyComparisonAgent()
            df = comp_agent.generate_comparison_chart(compare_list, lang)

            st.dataframe(df, use_container_width=True, hide_index=True)

            if st.button(t['detailed_analysis'], type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing..."):
                    result = comp_agent.compare_properties(compare_list, lang)

                if result.get('winner'):
                    winner = result['winner']
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(212, 175, 55, 0.05) 100%); 
                                border: 3px solid #D4AF37; border-radius: 24px; padding: 32px; margin: 32px 0;
                                box-shadow: 0 8px 30px rgba(212, 175, 55, 0.2);">
                        <h2 style="color: #D4AF37; font-family: Playfair Display, serif; margin-bottom: 20px; font-size: 28px;">
                            {t['winner']}
                        </h2>
                        <p style="color: #1A365D; font-size: 20px; font-weight: 600;">{winner['address']}</p>
                        <p style="color: #D4AF37; font-size: 32px; font-weight: 700; margin: 16px 0;">${winner['price']:,}</p>
                        <p style="color: #4A5568; font-size: 18px;">{t['price_per_sqft']}: <span style="color: #4A90E2; font-weight: 700;">${winner['price_per_sqft']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(result['analysis'])
        else:
            st.info(t['add_compare'])
            if len(compare_list) == 1:
                st.write(f"1 property: {compare_list[0]['address']}")

    # TAB 4: ANALYSIS
    with tab4:
        st.markdown(f"<h2 style='color: #1A365D; font-family: Playfair Display, serif; font-size: 32px;'>{t['analysis_tab']}</h2>", unsafe_allow_html=True)

        if st.session_state.saved_properties:
            prices = [p['price'] for p in st.session_state.saved_properties]
            sqfts = [p['square_feet'] for p in st.session_state.saved_properties]

            col1, col2, col3, col4 = st.columns(4)
            metrics = [
                (t['avg_price'], f"${sum(prices)/len(prices):,.0f}"),
                (t['min_price_stat'], f"${min(prices):,}"),
                (t['max_price_stat'], f"${max(prices):,}"),
                (t['price_per_sqft'], f"${sum(prices)/sum(sqfts):.0f}")
            ]

            for col, (label, value) in zip([col1, col2, col3, col4], metrics):
                with col:
                    st.metric(label, value)

            # Charts
            df_chart = pd.DataFrame(st.session_state.saved_properties)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_chart['address'],
                y=df_chart['price'],
                marker_color='#4A90E2',
                text=df_chart['price'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            ))
            fig.update_layout(
                title=dict(text=f"💰 {t['market_stats']}", font=dict(color='#1A365D', size=28, family='Playfair Display')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1A365D', family='Inter'),
                xaxis=dict(gridcolor='#B8D4E8', tickfont=dict(color='#4A5568')),
                yaxis=dict(gridcolor='#B8D4E8', tickfont=dict(color='#4A5568')),
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Price per sq ft comparison
            df_chart['price_per_sqft'] = df_chart['price'] / df_chart['square_feet']
            fig2 = px.scatter(df_chart, x='square_feet', y='price', 
                             size='bedrooms', color='neighborhood',
                             hover_data=['address', 'price_per_sqft'],
                             title=f"📊 {t['price_per_sqft']} Analysis")
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1A365D', family='Inter'),
                title_font=dict(family='Playfair Display', size=24),
                height=500,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info(t['search_first'])

    # TAB 5: AFFILIATION
    with tab5:
        st.markdown(f"<h2 style='color: #1A365D; font-family: Playfair Display, serif; font-size: 32px;'>{t['affiliation_tab']}</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: white; border: 2px solid #D4AF37; 
                    border-radius: 24px; padding: 32px; margin-bottom: 32px;
                    box-shadow: 0 8px 30px rgba(212, 175, 55, 0.15);">
            <h3 style="color: #D4AF37; font-family: Playfair Display, serif; font-size: 24px; margin-bottom: 12px;">
                💎 Premium Tools for Discerning Investors
            </h3>
            <p style="color: #4A5568; font-size: 16px;">
                Replace YOUR_AFFILIATE_ID with your real affiliate IDs to start earning commissions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        for key, prog in AFFILIATE_LINKS.items():
            with st.container():
                st.markdown(f"""
                <div class="property-card" style="margin: 16px 0; border-left: 4px solid #D4AF37;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="color: #D4AF37; font-family: Playfair Display, serif; font-size: 22px; margin-bottom: 8px;">
                                {prog['name']}
                            </h4>
                            <p style="color: #4A5568; font-size: 15px; line-height: 1.5;">
                                {prog['description'].get(lang, prog['description']['en'])}
                            </p>
                            <p style="color: #4A90E2; font-size: 14px; margin-top: 8px; font-weight: 600;">
                                💰 {t['commission']}: {prog['commission']} | 📂 {t['category']}: {prog['category'].get(lang, prog['category']['en'])}
                            </p>
                        </div>
                        <div style="margin-left: 24px; margin-top: 12px;">
                            <a href="{prog['url']}" target="_blank" 
                               style="background: linear-gradient(135deg, #D4AF37 0%, #F0E68C 100%); 
                                      color: #1A365D; padding: 12px 24px; border-radius: 12px; 
                                      text-decoration: none; font-weight: 700; font-size: 15px;
                                      display: inline-block; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);">
                                🔗 Access
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ============================================
    # FOOTER
    # ============================================

    st.markdown(f"""
    <div class="footer">
        <p style="color: #4A5568; font-size: 16px;">{t['footer']}</p>
        <p style="color: #D4AF37; font-family: Playfair Display, serif; font-size: 20px; margin-top: 12px;">
            ✨ Luxury Real Estate Solutions ✨
        </p>
        <p style="color: #4A90E2; font-size: 14px; margin-top: 8px;">
            🌍 Global Markets | 🏛️ Premium Properties | 💎 Exclusive Service
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
