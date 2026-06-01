
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
# CONFIGURATION LUXE - OR & BLEU OUVERT
# ============================================

LUXURY_COLORS = {
    "primary": "#1a365d",      # Bleu foncé luxe
    "secondary": "#2c5282",    # Bleu ouvert
    "accent": "#d4af37",       # Or/Doré
    "accent_light": "#f0e68c", # Or clair
    "background": "#0f172a",   # Fond sombre élégant
    "card_bg": "#1e293b",      # Fond carte
    "text": "#f8fafc",         # Texte blanc
    "text_secondary": "#94a3b8", # Texte gris
    "success": "#10b981",      # Vert succès
    "warning": "#f59e0b",      # Orange warning
}

# ============================================
# TRADUCTIONS MULTILINGUES
# ============================================

TRANSLATIONS = {
    "en": {
        "title": "🏠 AI Real Estate Agent Team Pro",
        "subtitle": "Luxury Real Estate Solutions",
        "search_tab": "🔍 Search",
        "description_tab": "✍️ Descriptions",
        "comparison_tab": "⚖️ Compare",
        "analysis_tab": "📊 Analysis",
        "affiliation_tab": "🔗 Affiliates",
        "city": "City",
        "state": "State/Region",
        "min_price": "Min Price ($)",
        "max_price": "Max Price ($)",
        "bedrooms": "Bedrooms",
        "property_type": "Property Type",
        "search_button": "🚀 Launch Search",
        "searching": "Searching...",
        "properties_found": "properties found!",
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
        "price_per_sqft": "Price/sq ft",
        "market_stats": "📊 Market Statistics",
        "avg_price": "Average Price",
        "min_price_stat": "Min Price",
        "max_price_stat": "Max Price",
        "affiliate_programs": "🔗 Affiliate Programs",
        "commission": "Commission",
        "category": "Category",
        "copy_link": "📋 Copy",
        "footer": "© 2026 AI Real Estate Agent Team Pro | Luxury Edition",
        "welcome_message": "Welcome to your luxury real estate AI assistant",
        "select_property": "Select a property from Search tab to generate description",
        "add_compare": "Add at least 2 properties to compare",
        "search_first": "Launch a search first",
    },
    "fr": {
        "title": "🏠 AI Real Estate Agent Team Pro",
        "subtitle": "Solutions Immobilières de Luxe",
        "search_tab": "🔍 Recherche",
        "description_tab": "✍️ Descriptions",
        "comparison_tab": "⚖️ Comparer",
        "analysis_tab": "📊 Analyse",
        "affiliation_tab": "🔗 Affiliation",
        "city": "Ville",
        "state": "État/Région",
        "min_price": "Prix Min ($)",
        "max_price": "Prix Max ($)",
        "bedrooms": "Chambres",
        "property_type": "Type de Bien",
        "search_button": "🚀 Lancer la Recherche",
        "searching": "Recherche en cours...",
        "properties_found": "biens trouvés !",
        "describe_button": "✍️ Décrire",
        "compare_button": "⭐ Comparer",
        "generate_description": "📝 Générer la Description",
        "language": "Langue",
        "platform": "Plateforme",
        "tone": "Ton",
        "length": "Longueur",
        "professional": "Professionnel",
        "warm": "Chaleureux",
        "luxury": "Luxe",
        "family": "Familial",
        "short": "Courte (100 mots)",
        "medium": "Moyenne (200 mots)",
        "long": "Longue (300 mots)",
        "social_posts": "📱 Posts Réseaux Sociaux",
        "detailed_analysis": "🔍 Analyse Détaillée",
        "winner": "🏆 MEILLEUR RAPPORT QUALITÉ/PRIX",
        "price_per_sqft": "Prix/sq ft",
        "market_stats": "📊 Statistiques du Marché",
        "avg_price": "Prix Moyen",
        "min_price_stat": "Prix Min",
        "max_price_stat": "Prix Max",
        "affiliate_programs": "🔗 Programmes d'Affiliation",
        "commission": "Commission",
        "category": "Catégorie",
        "copy_link": "📋 Copier",
        "footer": "© 2026 AI Real Estate Agent Team Pro | Édition Luxe",
        "welcome_message": "Bienvenue dans votre assistant IA immobilier de luxe",
        "select_property": "Sélectionnez un bien dans l'onglet Recherche pour générer une description",
        "add_compare": "Ajoutez au moins 2 biens à comparer",
        "search_first": "Lancez d'abord une recherche",
    },
    "es": {
        "title": "🏠 AI Real Estate Agent Team Pro",
        "subtitle": "Soluciones Inmobiliarias de Lujo",
        "search_tab": "🔍 Búsqueda",
        "description_tab": "✍️ Descripciones",
        "comparison_tab": "⚖️ Comparar",
        "analysis_tab": "📊 Análisis",
        "affiliation_tab": "🔗 Afiliados",
        "city": "Ciudad",
        "state": "Estado/Región",
        "min_price": "Precio Mín ($)",
        "max_price": "Precio Máx ($)",
        "bedrooms": "Habitaciones",
        "property_type": "Tipo de Propiedad",
        "search_button": "🚀 Iniciar Búsqueda",
        "searching": "Buscando...",
        "properties_found": "propiedades encontradas!",
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
        "price_per_sqft": "Precio/sq ft",
        "market_stats": "📊 Estadísticas del Mercado",
        "avg_price": "Precio Promedio",
        "min_price_stat": "Precio Mín",
        "max_price_stat": "Precio Máx",
        "affiliate_programs": "🔗 Programas de Afiliación",
        "commission": "Comisión",
        "category": "Categoría",
        "copy_link": "📋 Copiar",
        "footer": "© 2026 AI Real Estate Agent Team Pro | Edición Lujo",
        "welcome_message": "Bienvenido a su asistente IA inmobiliario de lujo",
        "select_property": "Seleccione una propiedad de la pestaña Búsqueda para generar descripción",
        "add_compare": "Agregue al menos 2 propiedades para comparar",
        "search_first": "Inicie una búsqueda primero",
    },
    "ar": {
        "title": "🏠 فريق وكيل العقارات الذكي الاحترافي",
        "subtitle": "حلول عقارية فاخرة",
        "search_tab": "🔍 بحث",
        "description_tab": "✍️ وصف",
        "comparison_tab": "⚖️ مقارنة",
        "analysis_tab": "📊 تحليل",
        "affiliation_tab": "🔗 شراكات",
        "city": "المدينة",
        "state": "الولاية/المنطقة",
        "min_price": "السعر الأدنى ($)",
        "max_price": "السعر الأقصى ($)",
        "bedrooms": "غرف النوم",
        "property_type": "نوع العقار",
        "search_button": "🚀 بدء البحث",
        "searching": "جاري البحث...",
        "properties_found": "عقارات تم العثور عليها!",
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
        "price_per_sqft": "السعر/قدم مربع",
        "market_stats": "📊 إحصائيات السوق",
        "avg_price": "متوسط السعر",
        "min_price_stat": "السعر الأدنى",
        "max_price_stat": "السعر الأقصى",
        "affiliate_programs": "🔗 برامج الشراكة",
        "commission": "العمولة",
        "category": "الفئة",
        "copy_link": "📋 نسخ",
        "footer": "© 2026 فريق وكيل العقارات الذكي الاحترافي | النسخة الفاخرة",
        "welcome_message": "مرحباً بك في مساعدك العقاري الذكي الفاخر",
        "select_property": "اختر عقاراً من تبويب البحث لإنشاء وصف",
        "add_compare": "أضف عقارين على الأقل للمقارنة",
        "search_first": "ابدأ البحث أولاً",
    }
}

# ============================================
# AFFILIATE LINKS
# ============================================

AFFILIATE_LINKS = {
    "buildium": {
        "name": "Buildium",
        "url": "https://www.buildium.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Property Management Software", "fr": "Logiciel de gestion locative", "es": "Software de gestión de propiedades", "ar": "برنامج إدارة العقارات"},
        "commission": "25% recurring",
        "category": {"en": "Property Management", "fr": "Gestion locative", "es": "Gestión de propiedades", "ar": "إدارة العقارات"}
    },
    "dealcheck": {
        "name": "DealCheck",
        "url": "https://dealcheck.io?fp_ref=omar18",
        "description": {"en": "Real Estate Investment Analysis", "fr": "Analyse d'investissement immobilier", "es": "Análisis de inversión inmobiliaria", "ar": "تحليل الاستثمار العقاري"},
        "commission": "30% recurring",
        "category": {"en": "Deal Analysis", "fr": "Analyse de deals", "es": "Análisis de deals", "ar": "تحليل الصفقات"}
    },
    "foreclosure": {
        "name": "Foreclosure.com",
        "url": "https://www.foreclosure.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Foreclosed Properties", "fr": "Biens saisis", "es": "Propiedades embargadas", "ar": "عقارات مصادرة"},
        "commission": "25%",
        "category": {"en": "Foreclosures", "fr": "Biens saisis", "es": "Embargos", "ar": "مصادرة"}
    },
    "nolo": {
        "name": "NOLO",
        "url": "https://www.nolo.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Legal Documents", "fr": "Documents juridiques", "es": "Documentos legales", "ar": "المستندات القانونية"},
        "commission": "25-35%",
        "category": {"en": "Legal", "fr": "Juridique", "es": "Legal", "ar": "قانوني"}
    },
    "biggerpockets": {
        "name": "BiggerPockets Pro",
        "url": "https://www.biggerpockets.com/?ref=YOUR_AFFILIATE_ID",
        "description": {"en": "Investor Community", "fr": "Communauté investisseurs", "es": "Comunidad de inversores", "ar": "مجتمع المستثمرين"},
        "commission": "$75/signup",
        "category": {"en": "Education", "fr": "Éducation", "es": "Educación", "ar": "تعليم"}
    },
}

# ============================================
# DEMO PROPERTIES (Luxury Edition)
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
        "features": ["Infinity Pool", "Private Beach Access", "Smart Home", "Wine Cellar", "Home Theater"],
        "agent_name": "Alexandra Sterling",
        "agent_phone": "(305) 555-0199",
        "image": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"
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
        "features": ["Tennis Court", "Guest House", "Mediterranean Style", "Gated Community"],
        "agent_name": "Marcus Wellington",
        "agent_phone": "(305) 555-0288",
        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"
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
        "features": ["Private Dock", "Panoramic Views", "Elevator", "Spa", "Chef's Kitchen"],
        "agent_name": "Victoria Ashford",
        "agent_phone": "(305) 555-0377",
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"
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
        "features": ["360° Views", "Private Terrace", "Concierge", "Rooftop Pool", "Gym"],
        "agent_name": "James Carrington",
        "agent_phone": "(305) 555-0466",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800"
    }
]

# ============================================
# LUXURY CSS STYLING
# ============================================

def get_luxury_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f8fafc !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%) !important;
        color: #1a365d !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%) !important;
    }

    .stTabs [aria-selected="true"] {
        color: #1a365d !important;
        font-weight: 600 !important;
    }

    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }

    .stSelectbox > div > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }

    .stNumberInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }

    .stMetric {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    .stMetric > div {
        color: #d4af37 !important;
        font-family: 'Playfair Display', serif !important;
    }

    .stMetric > label {
        color: #94a3b8 !important;
    }

    div[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    .property-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }

    .property-card:hover {
        border-color: #d4af37;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15);
        transform: translateY(-4px);
    }

    .gold-text {
        color: #d4af37;
        font-family: 'Playfair Display', serif;
    }

    .luxury-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #d4af37 50%, transparent 100%);
        margin: 24px 0;
    }

    .footer {
        text-align: center;
        padding: 24px;
        color: #94a3b8;
        font-size: 14px;
        border-top: 1px solid #334155;
        margin-top: 48px;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0f172a;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #d4af37;
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
                "professional": f"""
🏠 PREMIUM {prop_type.upper()} FOR SALE - {neighborhood}

Address: {address}
Price: ${price:,}

Property Details:
• Type: {prop_type}
• Bedrooms: {bedrooms}
• Bathrooms: {bathrooms}
• Square Footage: {sqft:,} sq ft
• Year Built: {year}
• Features: {features_text}

This property is located in the desirable {neighborhood} neighborhood, offering convenient 
access to amenities and excellent investment potential.

🔗 DealCheck Analysis: {AFFILIATE_LINKS['dealcheck']['url']}
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
• Amplios espacios de vida diseñados para el entretenimiento

📍 UBICACIÓN PRESTIGIOSA:
Ubicado en el corazón de {neighborhood}, esta propiedad ofrece acceso privilegiado a restaurantes 
gourmet, boutiques de lujo y playas inmaculadas.

💎 DESTACADO DE INVERSIÓN:
Precio: ${price:,}, lo que representa un valor excepcional a ${price//sqft:,} $/sq ft 
en uno de los barrios más codiciados de Miami.

🔗 Analice esta inversión con DealCheck: {AFFILIATE_LINKS['dealcheck']['url']}
📋 Documentos legales con NOLO: {AFFILIATE_LINKS['nolo']['url']}
                """,
            },
            "ar": {
                "luxury": f"""
🏛️ {prop_type.upper()} فاخرة في {neighborhood}

مرحباً بك في مسكن استثنائي يعيد تعريف الفخامة. هذه {prop_type} الرائعة 
بمساحة {sqft:,} قدم مربع تقدم أسلوب حياة لا مثيل له في حي {neighborhood} المرموق.

✨ مميزات استثنائية:
• {bedrooms} أجنحة نوم فاخرة مع حمامات داخلية
• {bathrooms} حمامات مستوحاة من المنتجعات الصحية مع تشطيبات فاخرة
• {features_text}
• بنيت عام {year} باهتمام دقيق بالتفاصيل
• مساحات معيشة واسعة مصممة للاستقبال

📍 موقع مرموق:
تقع في قلب {neighborhood}، تقدم هذه العقار وصولاً مميزاً إلى المطاعم الراقية 
والبوتيكات الفاخرة والشواطئ النقية.

💎 نقطة قوة استثمارية:
السعر: ${price:,}، مما يمثل قيمة استثنائية بقيمة ${price//sqft:,} $/قدم مربع 
في أحد أكثر الأحياء المرغوبة في ميامي.

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

#luxuryrealestate #miami #{neighborhood.replace(' ', '')} #luxuryhome #investment #dreamhome #realestate
                """,
                "facebook": f"""
🏛️ EXCLUSIVE LISTING 🏛️

Presenting an exceptional {prop_type} in the prestigious {neighborhood} neighborhood.

📍 Location: {address}
💰 Price: ${price:,}
🛏️ Bedrooms: {bedrooms}
🛁 Bathrooms: {bathrooms}

This property represents a unique opportunity for discerning buyers seeking luxury and investment potential.

📊 Analyze the investment potential: {AFFILIATE_LINKS['dealcheck']['url']}
📞 Schedule your private tour today!

#luxuryrealestate #miami #investmentproperty
                """,
                "linkedin": f"""
📊 PREMIUM INVESTMENT OPPORTUNITY

{prop_type} | {neighborhood} | Miami

Investment Highlights:
• Asking Price: ${price:,}
• Location: Premier {neighborhood} address
• Type: Luxury {prop_type}
• Market: High-demand Miami corridor

This opportunity is ideal for:
✅ Luxury homebuyers
✅ Portfolio diversification
✅ Long-term appreciation

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

#immobilierdeluxe #miami #{neighborhood.replace(' ', '')} #maisondeluxe #investissement #maisondereve
                """,
                "facebook": f"""
🏛️ LISTING EXCLUSIF 🏛️

Présentation d'un(e) {prop_type} exceptionnel(le) dans le prestigieux quartier {neighborhood}.

📍 Adresse : {address}
💰 Prix : ${price:,}
🛏️ Chambres : {bedrooms}
🛁 Salles de bain : {bathrooms}

Cette propriété représente une opportunité unique pour les acheteurs exigeants.

📊 Analyse de l'investissement : {AFFILIATE_LINKS['dealcheck']['url']}
📞 Réservez votre visite privée !
                """,
                "linkedin": f"""
📊 OPPORTUNITÉ D'INVESTISSEMENT PREMIUM

{prop_type} | {neighborhood} | Miami

Points clés de l'investissement :
• Prix demandé : ${price:,}
• Emplacement : Adresse premium {neighborhood}
• Type : {prop_type} de luxe
• Marché : Corridor Miami très demandé

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
                "facebook": f"""
🏛️ LISTING EXCLUSIVO 🏛️

Presentación de un(a) {prop_type} excepcional en el prestigioso barrio {neighborhood}.

📍 Dirección: {address}
💰 Precio: ${price:,}
🛏️ Dormitorios: {bedrooms}
🛁 Baños: {bathrooms}

📊 Análisis de inversión: {AFFILIATE_LINKS['dealcheck']['url']}
                """,
                "linkedin": f"""
📊 OPORTUNIDAD DE INVERSIÓN PREMIUM

{prop_type} | {neighborhood} | Miami

Puntos clave de inversión:
• Precio: ${price:,}
• Ubicación: Dirección premium {neighborhood}

🔗 Análisis profesional: {AFFILIATE_LINKS['dealcheck']['url']}
                """
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
                "facebook": f"""
🏛️ إعلان حصري 🏛️

عرض {prop_type} استثنائي في الحي المرموق {neighborhood}.

📍 العنوان: {address}
💰 السعر: ${price:,}
🛏️ غرف النوم: {bedrooms}
🛁 الحمامات: {bathrooms}

📊 تحليل الاستثمار: {AFFILIATE_LINKS['dealcheck']['url']}
                """,
                "linkedin": f"""
📊 فرصة استثمارية مميزة

{prop_type} | {neighborhood} | ميامي

نقاط قوة الاستثمار:
• السعر: ${price:,}
• الموقع: عنوان مميز في {neighborhood}

🔗 تحليل احترافي: {AFFILIATE_LINKS['dealcheck']['url']}
                """
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
• {winner['features_count']} équipements premium inclus

**Outils Recommandés :**
🔗 {AFFILIATE_LINKS['dealcheck']['name']} : {AFFILIATE_LINKS['dealcheck']['url']}
            """,
            "es": f"""
### Análisis de Inversión

**Mejor Relación Calidad/Precio:** {winner['address']}
- Precio: ${winner['price']:,}
- Precio por sq ft: ${winner['price_per_sqft']}

**Puntos Clave:**
• La propiedad ganadora ofrece más espacio por dólar invertido
• {winner['neighborhood']} ofrece excelente potencial de apreciación

**Herramientas Recomendadas:**
🔗 {AFFILIATE_LINKS['dealcheck']['name']}: {AFFILIATE_LINKS['dealcheck']['url']}
            """,
            "ar": f"""
### تحليل الاستثمار

**أفضل قيمة:** {winner['address']}
- السعر: ${winner['price']:,}
- السعر/قدم مربع: ${winner['price_per_sqft']}

**نقاط رئيسية:**
• العقار الفائز يقدم أكبر مساحة لكل دولار مستثمر
• {winner['neighborhood']} تقدم إمكانية تقدير ممتازة

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
            "ar": {"address": "العنوان", "price": "السعر ($)", "ppsf": "السعر/قدم", "beds": "غرف النوم", "baths": "الحمامات", "sqft": "قدم مربع", "type": "النوع"},
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
        page_title="AI Real Estate Agent Team Pro - Luxury Edition",
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

    # Language selector in header
    col_lang1, col_lang2, col_lang3, col_lang4, col_space = st.columns([1, 1, 1, 1, 8])

    with col_lang1:
        if st.button("🇬🇧 EN", key="lang_en"):
            st.session_state.current_lang = "en"
    with col_lang2:
        if st.button("🇫🇷 FR", key="lang_fr"):
            st.session_state.current_lang = "fr"
    with col_lang3:
        if st.button("🇪🇸 ES", key="lang_es"):
            st.session_state.current_lang = "es"
    with col_lang4:
        if st.button("🇸🇦 AR", key="lang_ar"):
            st.session_state.current_lang = "ar"

    lang = st.session_state.current_lang
    t = TRANSLATIONS[lang]

    # Logo and Title
    col_logo, col_title = st.columns([1, 4])

    with col_logo:
        try:
            st.image("logo.png", width=120)
        except:
            st.markdown("<div style='font-size: 60px; text-align: center;'>🏛️</div>", unsafe_allow_html=True)

    with col_title:
        st.markdown(f"""
        <h1 style='font-family: Playfair Display, serif; color: #d4af37; margin-bottom: 0;'>
            {t['title']}
        </h1>
        <p style='color: #94a3b8; font-size: 18px; margin-top: 8px; font-style: italic;'>
            {t['subtitle']}
        </p>
        <div class="luxury-divider"></div>
        """, unsafe_allow_html=True)

    # Welcome message
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: rgba(30, 41, 59, 0.6); 
                border-radius: 16px; border: 1px solid #334155; margin-bottom: 24px;'>
        <p style='color: #d4af37; font-size: 20px; font-family: Playfair Display, serif;'>
            ✨ {t['welcome_message']} ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t['search_tab'], t['description_tab'], t['comparison_tab'], 
        t['analysis_tab'], t['affiliation_tab']
    ])

    # TAB 1: SEARCH
    with tab1:
        st.markdown(f"<h2 style='color: #d4af37; font-family: Playfair Display, serif;'>{t['search_tab']}</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input(t['city'], value="Miami", placeholder="Miami")
            min_price = st.number_input(t['min_price'], min_value=0, value=1000000, step=100000)
            bedrooms = st.selectbox(t['bedrooms'], [1, 2, 3, 4, 5, 6])
        with col2:
            state = st.text_input(t['state'], value="FL", placeholder="FL")
            max_price = st.number_input(t['max_price'], min_value=0, value=5000000, step=100000)
            property_type = st.selectbox(t['property_type'], 
                ["All", "Villa", "Penthouse", "Estate", "Waterfront Mansion", "Condo"] if lang == "en" else
                ["Tous", "Villa", "Penthouse", "Domaine", "Manoir Waterfront", "Condo"] if lang == "fr" else
                ["Todos", "Villa", "Penthouse", "Finca", "Mansión Waterfront", "Condo"] if lang == "es" else
                ["الكل", "فيلا", "بنتهاوس", "عقار", "قصر بحري", "شقة"]
            )

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
                                <h3 style="color: #d4af37; margin-bottom: 8px;">{prop['property_type']}</h3>
                                <p style="color: #f8fafc; font-size: 16px; margin-bottom: 8px;">📍 {prop['address']}</p>
                                <p style="color: #94a3b8; font-size: 14px;">
                                    💰 ${prop['price']:,} | 🛏️ {prop['bedrooms']} {t['bedrooms']} | 
                                    🛁 {prop['bathrooms']} Baths | 📐 {prop['square_feet']:,} sq ft
                                </p>
                                <p style="color: #d4af37; font-size: 13px; margin-top: 8px;">
                                    ✨ {', '.join(prop['features'][:3])}
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
        st.markdown(f"<h2 style='color: #d4af37; font-family: Playfair Display, serif;'>{t['description_tab']}</h2>", unsafe_allow_html=True)

        if st.session_state.selected_for_description:
            prop = st.session_state.selected_for_description
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin-bottom: 24px;">
                <p style="color: #d4af37; font-size: 18px;">🏛️ {prop['address']}</p>
                <p style="color: #94a3b8;">${prop['price']:,} | {prop['property_type']}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                tone = st.selectbox(t['tone'], 
                    [t['luxury'], t['professional'], t['warm'], t['family']])
                platform = st.selectbox(t['platform'], 
                    ["Instagram", "Facebook", "LinkedIn"])
            with col2:
                length = st.selectbox(t['length'], 
                    [t['short'], t['medium'], t['long']])

            tone_map = {t['luxury']: "luxury", t['professional']: "professional", 
                       t['warm']: "warm", t['family']: "family"}
            selected_tone = tone_map.get(tone, "luxury")

            if st.button(t['generate_description'], type="primary", use_container_width=True):
                desc_agent = PropertyDescriptionAgent()

                with st.spinner("✨ Generating..."):
                    description = desc_agent.generate_description(prop, lang, selected_tone)

                st.markdown("""
                <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #d4af37; 
                            border-radius: 16px; padding: 24px; margin-top: 16px;">
                """, unsafe_allow_html=True)
                st.markdown(description)
                st.markdown("</div>", unsafe_allow_html=True)

                # Social media posts
                st.markdown(f"<h3 style='color: #d4af37; margin-top: 32px;'>{t['social_posts']}</h3>", unsafe_allow_html=True)

                for plat in ["instagram", "facebook", "linkedin"]:
                    post = desc_agent.generate_social_media_post(prop, plat, lang)
                    with st.expander(plat.title()):
                        st.text_area(f"{plat}", post, height=150)
        else:
            st.info(t['select_property'])

    # TAB 3: COMPARISON
    with tab3:
        st.markdown(f"<h2 style='color: #d4af37; font-family: Playfair Display, serif;'>{t['comparison_tab']}</h2>", unsafe_allow_html=True)

        compare_list = st.session_state.compare_list

        if len(compare_list) >= 2:
            st.markdown(f"<p style='color: #94a3b8;'>{len(compare_list)} properties selected for comparison</p>", unsafe_allow_html=True)

            comp_agent = PropertyComparisonAgent()
            df = comp_agent.generate_comparison_chart(compare_list, lang)

            st.dataframe(df, use_container_width=True, hide_index=True)

            if st.button(t['detailed_analysis'], type="primary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    result = comp_agent.compare_properties(compare_list, lang)

                if result.get('winner'):
                    winner = result['winner']
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%); 
                                border: 2px solid #d4af37; border-radius: 16px; padding: 24px; margin: 24px 0;">
                        <h3 style="color: #d4af37; margin-bottom: 16px;">{t['winner']}</h3>
                        <p style="color: #f8fafc; font-size: 18px;">{winner['address']}</p>
                        <p style="color: #d4af37; font-size: 24px; font-weight: bold;">${winner['price']:,}</p>
                        <p style="color: #94a3b8;">{t['price_per_sqft']}: ${winner['price_per_sqft']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(result['analysis'])
        else:
            st.info(t['add_compare'])
            if len(compare_list) == 1:
                st.write(f"1 property selected: {compare_list[0]['address']}")

    # TAB 4: ANALYSIS
    with tab4:
        st.markdown(f"<h2 style='color: #d4af37; font-family: Playfair Display, serif;'>{t['analysis_tab']}</h2>", unsafe_allow_html=True)

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
                marker_color='#d4af37',
                text=df_chart['price'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
            ))
            fig.update_layout(
                title=dict(text=f"💰 {t['market_stats']}", font=dict(color='#d4af37', size=24, family='Playfair Display')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc'),
                xaxis=dict(gridcolor='#334155', tickfont=dict(color='#94a3b8')),
                yaxis=dict(gridcolor='#334155', tickfont=dict(color='#94a3b8')),
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
                font=dict(color='#f8fafc'),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info(t['search_first'])

    # TAB 5: AFFILIATION
    with tab5:
        st.markdown(f"<h2 style='color: #d4af37; font-family: Playfair Display, serif;'>{t['affiliation_tab']}</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid #d4af37; 
                    border-radius: 16px; padding: 24px; margin-bottom: 24px;">
            <p style="color: #d4af37; font-size: 18px; font-family: Playfair Display, serif;">
                💎 Premium Tools for Discerning Investors
            </p>
            <p style="color: #94a3b8;">
                Replace YOUR_AFFILIATE_ID with your real affiliate IDs to start earning commissions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        for key, prog in AFFILIATE_LINKS.items():
            with st.container():
                st.markdown(f"""
                <div class="property-card" style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h4 style="color: #d4af37; margin-bottom: 8px;">{prog['name']}</h4>
                            <p style="color: #94a3b8; font-size: 14px;">{prog['description'].get(lang, prog['description']['en'])}</p>
                            <p style="color: #d4af37; font-size: 13px;">
                                💰 {t['commission']}: {prog['commission']} | 📂 {t['category']}: {prog['category'].get(lang, prog['category']['en'])}
                            </p>
                        </div>
                        <div style="margin-left: 16px;">
                            <a href="{prog['url']}" target="_blank" 
                               style="background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%); 
                                      color: #1a365d; padding: 8px 16px; border-radius: 8px; 
                                      text-decoration: none; font-weight: 600; font-size: 14px;">
                                🔗 Access
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>{t['footer']}</p>
        <p style="color: #d4af37; font-family: Playfair Display, serif;">✨ Or-et-Pierre Luxury Real Estate ✨</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
