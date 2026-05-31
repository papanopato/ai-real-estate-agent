import os
import streamlit as st
import json
import time
import re
from agno.agent import Agent
from agno.models.ollama import Ollama
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import pandas as pd

# Load environment variables
load_dotenv()

# ============================================
# AFFILIATE LINKS CONFIGURATION
# ============================================
# Replace these placeholder links with your actual affiliate links
# after signing up for each program

AFFILIATE_LINKS = {
    "buildium": {
        "name": "Buildium",
        "url": "https://www.buildium.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Logiciel de gestion locative #1 aux USA",
        "commission": "25% récurrent",
        "category": "Gestion locative"
    },
    "dealcheck": {
        "name": "DealCheck",
        "url": "https://dealcheck.io/?ref=YOUR_AFFILIATE_ID",
        "description": "Analyse d'investissement immobilier",
        "commission": "30% récurrent",
        "category": "Analyse de deals"
    },
    "foreclosure": {
        "name": "Foreclosure.com",
        "url": "https://www.foreclosure.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Biens saisis et ventes aux enchères",
        "commission": "25%",
        "category": "Biens saisis"
    },
    "nolo": {
        "name": "NOLO",
        "url": "https://www.nolo.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Documents juridiques immobiliers",
        "commission": "25-35%",
        "category": "Juridique"
    },
    "carrot": {
        "name": "Carrot",
        "url": "https://www.carrot.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Sites web pour investisseurs immobiliers",
        "commission": "20-50%",
        "category": "Marketing"
    },
    "leadsbridge": {
        "name": "LeadsBridge",
        "url": "https://leadsbridge.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Automatisation des leads immobiliers",
        "commission": "30% récurrent",
        "category": "Leads"
    },
    "biggerpockets": {
        "name": "BiggerPockets Pro",
        "url": "https://www.biggerpockets.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Communauté investisseurs + outils",
        "commission": "$75/signup",
        "category": "Éducation"
    },
    "roofstock": {
        "name": "Roofstock",
        "url": "https://www.roofstock.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Biens locatifs clé en main",
        "commission": "$15/referral",
        "category": "Investissement"
    },
    "rentredi": {
        "name": "RentRedi",
        "url": "https://rentredi.com/?ref=YOUR_AFFILIATE_ID",
        "description": "App de gestion pour propriétaires",
        "commission": "40%",
        "category": "Gestion locative"
    },
    "vrbo": {
        "name": "VRBO",
        "url": "https://www.vrbo.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Locations de vacances",
        "commission": "4%",
        "category": "Location courte"
    }
}

# ============================================
# PYDANTIC SCHEMAS
# ============================================

class PropertyDetails(BaseModel):
    id: str = Field(description="Unique property ID")
    address: str = Field(description="Full property address")
    price: Optional[float] = Field(description="Property price")
    bedrooms: Optional[int] = Field(description="Number of bedrooms")
    bathrooms: Optional[float] = Field(description="Number of bathrooms")
    square_feet: Optional[int] = Field(description="Square footage")
    property_type: Optional[str] = Field(description="Type of property")
    year_built: Optional[int] = Field(description="Year built")
    description: Optional[str] = Field(description="Property description")
    listing_url: Optional[str] = Field(description="Original listing URL")
    features: Optional[List[str]] = Field(description="Property features")
    neighborhood: Optional[str] = Field(description="Neighborhood")
    images: Optional[List[str]] = Field(description="Property images")
    agent_name: Optional[str] = Field(description="Listing agent")
    agent_phone: Optional[str] = Field(description="Agent phone")

class PropertyComparison(BaseModel):
    properties: List[PropertyDetails] = Field(description="Properties to compare")
    comparison_table: Dict = Field(description="Comparison data")
    winner_id: Optional[str] = Field(description="Best property ID")
    analysis: str = Field(description="Comparison analysis")

# ============================================
# PROPERTY DESCRIPTION GENERATOR AGENT
# ============================================

class PropertyDescriptionAgent:
    def __init__(self, llm):
        self.agent = Agent(
            name="Property Description Generator",
            model=llm,
            instructions="""
            Tu es un rédacteur immobilier expert. Tu crées des descriptions 
            captivantes et professionnelles pour les biens immobiliers.

            RÈGLES:
            1. Ton chaleureux mais professionnel
            2. Met en valeur les points forts du bien
            3. Mentionne le quartier et les commodités
            4. Utilise un vocabulaire émotionnel ("coup de cœur", "rare", "unique")
            5. Structure: accroche → description → quartier → conclusion
            6. Longueur: 150-250 mots
            7. Inclus automatiquement les liens d'affiliation pertinents
            """
        )

    def generate_description(self, property_data: dict, language="fr") -> str:
        """Generate a compelling property description"""

        prompt = f"""
        Génère une description professionnelle pour ce bien immobilier:

        ADRESSE: {property_data.get('address', 'N/A')}
        TYPE: {property_data.get('property_type', 'N/A')}
        PRIX: ${property_data.get('price', 'N/A')}
        CHAMBRES: {property_data.get('bedrooms', 'N/A')}
        SALLES DE BAIN: {property_data.get('bathrooms', 'N/A')}
        SUPERFICIE: {property_data.get('square_feet', 'N/A')} sq ft
        ANNÉE: {property_data.get('year_built', 'N/A')}
        QUARTIER: {property_data.get('neighborhood', 'N/A')}
        CARACTÉRISTIQUES: {', '.join(property_data.get('features', []))}

        INCLURE ces liens d'affiliation pertinents dans la description:
        - DealCheck (analyse du bien): {AFFILIATE_LINKS['dealcheck']['url']}
        - NOLO (documents juridiques): {AFFILIATE_LINKS['nolo']['url']}
        - BiggerPockets (communauté investisseurs): {AFFILIATE_LINKS['biggerpockets']['url']}
        """

        result = self.agent.run(prompt)
        return result.content if hasattr(result, 'content') else str(result)

    def generate_social_media_post(self, property_data: dict, platform="instagram") -> str:
        """Generate social media post for a property"""

        templates = {
            "instagram": f"""
            🏠 {property_data.get('property_type', 'Bien').upper()} À VENDRE

            📍 {property_data.get('address', '')}
            💰 ${property_data.get('price', 'N/A'):,}
            🛏️ {property_data.get('bedrooms', 0)} ch | 🛁 {property_data.get('bathrooms', 0)} sdb
            📐 {property_data.get('square_feet', 'N/A')} sq ft

            ✨ {property_data.get('description', 'Magnifique bien')[:100]}...

            📞 Contactez-moi pour une visite!
            🔗 Analysez ce bien: {AFFILIATE_LINKS['dealcheck']['url']}

            #immobilier #vente #{property_data.get('city', 'realestate').lower()} #maison #investissement
            """,

            "facebook": f"""
            🎉 NOUVEAUTÉ SUR LE MARCHÉ!

            {property_data.get('property_type', 'Bien').title()} exceptionnel à vendre

            📍 Localisation: {property_data.get('address', '')}
            💰 Prix: ${property_data.get('price', 'N/A'):,}

            Ce bien est parfait pour:
            ✅ Les familles
            ✅ Les investisseurs
            ✅ Premier achat

            📊 Analysez le potentiel de ce bien avec DealCheck:
            {AFFILIATE_LINKS['dealcheck']['url']}

            📞 Appelez-moi au {property_data.get('agent_phone', '[VOTRE TÉLÉPHONE]')}
            pour organiser une visite!
            """,

            "linkedin": f"""
            📊 OPPORTUNITÉ D'INVESTISSEMENT

            {property_data.get('property_type', 'Bien').title()} | {property_data.get('address', '')}

            Points clés de l'investissement:
            • Prix: ${property_data.get('price', 'N/A'):,}
            • Potentiel de rendement: À analyser
            • Quartier: {property_data.get('neighborhood', 'N/A')}

            Outils recommandés pour les investisseurs:
            🔗 Analyse de deals: {AFFILIATE_LINKS['dealcheck']['url']}
            🔗 Communauté investisseurs: {AFFILIATE_LINKS['biggerpockets']['url']}
            🔗 Financement: {AFFILIATE_LINKS['new_silver']['url'] if 'new_silver' in AFFILIATE_LINKS else 'N/A'}

            #immobilier #investissement #opportunité
            """
        }

        return templates.get(platform, templates["instagram"])

# ============================================
# PROPERTY COMPARISON AGENT
# ============================================

class PropertyComparisonAgent:
    def __init__(self, llm):
        self.agent = Agent(
            name="Property Comparison Agent",
            model=llm,
            instructions="""
            Tu es un expert en comparaison de biens immobiliers.
            Tu analyses et compares plusieurs propriétés objectivement.

            RÈGLES:
            1. Compare prix, superficie, chambres, sdb, emplacement
            2. Calcule le prix au sq ft
            3. Identifie le meilleur rapport qualité/prix
            4. Donne un score sur 100 pour chaque bien
            5. Recommande le meilleur bien avec justification
            6. Inclus les liens d'affiliation pertinents
            """
        )

    def compare_properties(self, properties: List[Dict]) -> Dict:
        """Compare multiple properties and return analysis"""

        if len(properties) < 2:
            return {"error": "Minimum 2 properties required for comparison"}

        # Calculate metrics
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
                "year_built": prop.get('year_built', 'N/A'),
                "neighborhood": prop.get('neighborhood', 'N/A'),
                "property_type": prop.get('property_type', 'N/A')
            }
            comparison_data.append(metrics)

        # AI Analysis
        prompt = f"""
        Compare ces {len(properties)} biens immobiliers et donne une analyse détaillée:

        {json.dumps(comparison_data, indent=2, ensure_ascii=False)}

        Fournis:
        1. Tableau comparatif
        2. Score sur 100 pour chaque bien
        3. Meilleur rapport qualité/prix
        4. Recommandation finale
        5. Liens d'affiliation utiles:
           - DealCheck (analyse): {AFFILIATE_LINKS['dealcheck']['url']}
           - Foreclosure (biens saisis): {AFFILIATE_LINKS['foreclosure']['url']}
           - NOLO (contrats): {AFFILIATE_LINKS['nolo']['url']}
        """

        result = self.agent.run(prompt)
        analysis = result.content if hasattr(result, 'content') else str(result)

        # Determine winner based on price per sqft
        winner = min(comparison_data, key=lambda x: x['price_per_sqft'] if x['price_per_sqft'] > 0 else float('inf'))

        return {
            "comparison_table": comparison_data,
            "winner": winner,
            "analysis": analysis
        }

    def generate_comparison_chart(self, properties: List[Dict]) -> pd.DataFrame:
        """Generate a pandas DataFrame for comparison"""
        data = []
        for prop in properties:
            price = prop.get('price', 0) or 0
            sqft = prop.get('square_feet', 1) or 1
            data.append({
                "Adresse": prop.get('address', 'N/A')[:30] + "...",
                "Prix ($)": f"${price:,}",
                "Prix/sq ft": f"${round(price/sqft, 2)}",
                "Chambres": prop.get('bedrooms', 0),
                "SDB": prop.get('bathrooms', 0),
                "Superficie": f"{prop.get('square_feet', 0):,} sq ft",
                "Type": prop.get('property_type', 'N/A')
            })
        return pd.DataFrame(data)

# ============================================
# FIRECRAWL AGENT
# ============================================

class DirectFirecrawlAgent:
    def __init__(self, firecrawl_api_key, model_id="gpt-oss:20b"):
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        self.model_id = model_id

    def find_properties_direct(self, city, state, user_criteria, selected_websites):
        all_properties = []
        for website in selected_websites:
            try:
                search_url = self._construct_search_url(website, city, state, user_criteria)
                scrape_result = self.firecrawl.scrape_url(
                    url=search_url,
                    params={"formats": ["markdown", "html"], "only_main_content": True}
                )
                properties = self._extract_properties(scrape_result, website)
                all_properties.extend(properties)
            except Exception as e:
                st.warning(f"Error searching {website}: {str(e)}")
                continue
        return {"properties": all_properties, "total_count": len(all_properties), "source_websites": selected_websites}

    def _construct_search_url(self, website, city, state, criteria):
        city_encoded = city.replace(" ", "-").lower()
        state_encoded = state.lower()
        if "zillow" in website.lower():
            return f"https://www.zillow.com/{city_encoded}-{state_encoded}/"
        elif "realtor" in website.lower():
            return f"https://www.realtor.com/realestateandhomes-search/{city_encoded}_{state_encoded}"
        elif "redfin" in website.lower():
            return f"https://www.redfin.com/city/{city_encoded}-{state_encoded}"
        else:
            return f"https://www.zillow.com/{city_encoded}-{state_encoded}/"

    def _extract_properties(self, scrape_result, website):
        properties = []
        if hasattr(scrape_result, 'markdown'):
            content = scrape_result.markdown
        else:
            content = str(scrape_result)
        return properties

# ============================================
# CREATE SPECIALIZED AGENTS
# ============================================

def create_sequential_agents(llm, user_criteria):
    property_search_agent = Agent(
        name="Property Search Agent",
        model=llm,
        instructions="""
        You are a property search expert. Find and extract property listings.
        WORKFLOW:
        1. SEARCH FOR PROPERTIES using Firecrawl data
        2. EXTRACT: Address, price, bedrooms, bathrooms, sq ft, type, features
        """
    )
    market_analysis_agent = Agent(
        name="Market Analysis Agent",
        model=llm,
        instructions="""
        Market analysis expert. Provide CONCISE insights.
        COVER: Market condition, key neighborhoods, investment outlook.
        FORMAT: Bullet points, under 100 words per section.
        """
    )
    property_valuation_agent = Agent(
        name="Property Valuation Agent",
        model=llm,
        instructions="""
        Property valuation expert. CONCISE assessments.
        FOR EACH PROPERTY: Value assessment, investment potential, key recommendation.
        FORMAT: Under 50 words per property, bullet points.
        """
    )
    return property_search_agent, market_analysis_agent, property_valuation_agent

# ============================================
# STREAMLIT UI
# ============================================

def main():
    st.set_page_config(page_title="AI Real Estate Agent Team Pro", page_icon="🏠", layout="wide")

    st.title("🏠 AI Real Estate Agent Team Pro")
    st.caption("Pour Agents Immobiliers - Avec Génération de Descriptions & Comparaison")

    # Initialize session state
    if 'saved_properties' not in st.session_state:
        st.session_state.saved_properties = []
    if 'generated_descriptions' not in st.session_state:
        st.session_state.generated_descriptions = {}

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        with st.expander("🔑 API Keys", expanded=True):
            firecrawl_key = st.text_input("Firecrawl API Key", type="password")
            st.info("🤖 Ollama: gpt-oss:20b (local)")

        with st.expander("🔗 Liens d'Affiliation"):
            st.write("Programmes intégrés:")
            for key, prog in AFFILIATE_LINKS.items():
                st.markdown(f"**{prog['name']}** - {prog['commission']}")
                st.caption(prog['description'])

        with st.expander("🌐 Recherche"):
            selected_websites = st.multiselect(
                "Sites immobiliers",
                ["Zillow", "Realtor.com", "Redfin"],
                default=["Zillow"]
            )

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Recherche", "✍️ Descriptions", "⚖️ Comparaison", "📊 Analyse", "🔗 Affiliation"
    ])

    # TAB 1: SEARCH
    with tab1:
        st.subheader("🔍 Recherche de Biens")
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("Ville", placeholder="ex: Miami")
            min_price = st.number_input("Prix Min ($)", min_value=0, value=0, step=50000)
            min_bedrooms = st.selectbox("Min Chambres", [1, 2, 3, 4, 5])
        with col2:
            state = st.text_input("État/Région", placeholder="ex: FL")
            max_price = st.number_input("Prix Max ($)", min_value=0, value=1000000, step=50000)
            property_type = st.selectbox("Type", ["Tous", "Maison", "Condo", "Appartement", "Terrain"])

        if st.button("🚀 Lancer la Recherche", type="primary"):
            if not firecrawl_key:
                st.error("⚠️ Clé API Firecrawl requise")
                return

            progress = st.progress(0)
            status = st.empty()

            # Simulate search (in real app, this calls Firecrawl)
            status.info("🔍 Recherche en cours...")
            progress.progress(0.3)
            time.sleep(1)

            # Demo properties
            demo_properties = [
                {
                    "id": "prop_001",
                    "address": f"123 Main St, {city}, {state}",
                    "price": 450000,
                    "bedrooms": 3,
                    "bathrooms": 2.5,
                    "square_feet": 2100,
                    "property_type": "Maison",
                    "year_built": 2015,
                    "neighborhood": "Downtown",
                    "features": ["Piscine", "Garage", "Jardin"],
                    "agent_name": "John Doe",
                    "agent_phone": "(555) 123-4567"
                },
                {
                    "id": "prop_002",
                    "address": f"456 Oak Ave, {city}, {state}",
                    "price": 380000,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "square_feet": 1800,
                    "property_type": "Maison",
                    "year_built": 2010,
                    "neighborhood": "Midtown",
                    "features": ["Rénové", "Cuisine moderne"],
                    "agent_name": "Jane Smith",
                    "agent_phone": "(555) 987-6543"
                },
                {
                    "id": "prop_003",
                    "address": f"789 Pine Rd, {city}, {state}",
                    "price": 520000,
                    "bedrooms": 4,
                    "bathrooms": 3,
                    "square_feet": 2400,
                    "property_type": "Maison",
                    "year_built": 2018,
                    "neighborhood": "Uptown",
                    "features": ["Suite parentale", "Bureau", "Terrasse"],
                    "agent_name": "Mike Johnson",
                    "agent_phone": "(555) 456-7890"
                }
            ]

            st.session_state.saved_properties = demo_properties
            progress.progress(1.0)
            status.success(f"✅ {len(demo_properties)} biens trouvés!")

            # Display results
            for prop in demo_properties:
                with st.container():
                    cols = st.columns([3, 1, 1])
                    with cols[0]:
                        st.markdown(f"**{prop['address']}**")
                        st.write(f"💰 ${prop['price']:,} | 🛏️ {prop['bedrooms']}ch | 🛁 {prop['bathrooms']}sdb | 📐 {prop['square_feet']} sq ft")
                    with cols[1]:
                        if st.button("✍️ Décrire", key=f"desc_{prop['id']}"):
                            st.session_state.selected_for_description = prop
                    with cols[2]:
                        if st.button("⭐ Comparer", key=f"comp_{prop['id']}"):
                            if prop not in st.session_state.get('compare_list', []):
                                st.session_state.compare_list = st.session_state.get('compare_list', []) + [prop]
                    st.divider()

    # TAB 2: DESCRIPTIONS
    with tab2:
        st.subheader("✍️ Générateur de Descriptions")

        if 'selected_for_description' in st.session_state:
            prop = st.session_state.selected_for_description
            st.write(f"Bien sélectionné: **{prop['address']}**")

            col1, col2 = st.columns(2)
            with col1:
                language = st.selectbox("Langue", ["Français", "Anglais", "Espagnol"])
                platform = st.selectbox("Plateforme", ["Site web", "Instagram", "Facebook", "LinkedIn"])
            with col2:
                tone = st.selectbox("Ton", ["Professionnel", "Chaleureux", "Luxueux", "Familial"])
                length = st.selectbox("Longueur", ["Courte (100 mots)", "Moyenne (200 mots)", "Longue (300 mots)"])

            if st.button("📝 Générer la Description", type="primary"):
                llm = Ollama(id="gpt-oss:20b")
                desc_agent = PropertyDescriptionAgent(llm)

                with st.spinner("Génération en cours..."):
                    description = desc_agent.generate_description(prop)
                    st.session_state.generated_descriptions[prop['id']] = description

                st.success("✅ Description générée!")
                st.text_area("Description", description, height=200)

                # Social media posts
                st.subheader("📱 Posts Réseaux Sociaux")
                for plat in ["instagram", "facebook", "linkedin"]:
                    post = desc_agent.generate_social_media_post(prop, plat)
                    with st.expander(f"{plat.title()}"):
                        st.text_area(f"Post {plat}", post, height=150)
                        st.button("📋 Copier", key=f"copy_{plat}")
        else:
            st.info("👆 Sélectionnez un bien dans l'onglet 'Recherche' pour générer une description")

    # TAB 3: COMPARISON
    with tab3:
        st.subheader("⚖️ Comparaison de Biens")

        compare_list = st.session_state.get('compare_list', [])

        if len(compare_list) >= 2:
            st.write(f"**{len(compare_list)} biens à comparer**")

            # Display comparison table
            llm = Ollama(id="gpt-oss:20b")
            comp_agent = PropertyComparisonAgent(llm)
            df = comp_agent.generate_comparison_chart(compare_list)
            st.dataframe(df, use_container_width=True)

            # Detailed comparison
            if st.button("🔍 Analyse Détaillée", type="primary"):
                with st.spinner("Analyse en cours..."):
                    result = comp_agent.compare_properties(compare_list)

                st.subheader("📊 Résultat de l'Analyse")

                # Winner highlight
                if result.get('winner'):
                    winner = result['winner']
                    st.success(f"🏆 MEILLEUR RAPPORT QUALITÉ/PRIX: {winner['address']} à ${winner['price']:,} (${winner['price_per_sqft']}/sq ft)")

                # Analysis text
                st.markdown(result['analysis'])

                # Affiliate recommendations
                st.subheader("🔗 Outils Recommandés")
                cols = st.columns(3)
                tools = [
                    ("DealCheck", AFFILIATE_LINKS['dealcheck']['url'], "Analysez ce deal"),
                    ("Foreclosure", AFFILIATE_LINKS['foreclosure']['url'], "Biens saisis similaires"),
                    ("NOLO", AFFILIATE_LINKS['nolo']['url'], "Documents juridiques")
                ]
                for i, (name, url, desc) in enumerate(tools):
                    with cols[i]:
                        st.markdown(f"**{name}**")
                        st.caption(desc)
                        st.markdown(f"[🔗 Accéder]({url})")
        else:
            st.info("👆 Ajoutez au moins 2 biens à comparer depuis l'onglet 'Recherche'")
            if len(compare_list) == 1:
                st.write(f"1 bien sélectionné: {compare_list[0]['address']}")

    # TAB 4: ANALYSIS
    with tab4:
        st.subheader("📊 Analyse de Marché")

        if st.session_state.saved_properties:
            # Market stats
            prices = [p['price'] for p in st.session_state.saved_properties]
            sqfts = [p['square_feet'] for p in st.session_state.saved_properties]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Prix Moyen", f"${sum(prices)/len(prices):,.0f}")
            with col2:
                st.metric("Prix Min", f"${min(prices):,}")
            with col3:
                st.metric("Prix Max", f"${max(prices):,}")
            with col4:
                st.metric("Prix/sq ft Moy.", f"${sum(prices)/sum(sqfts):.0f}")

            # Charts
            import plotly.express as px
            df_chart = pd.DataFrame(st.session_state.saved_properties)
            fig = px.bar(df_chart, x='address', y='price', title='Prix des Biens')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Lancez d'abord une recherche")

    # TAB 5: AFFILIATION
    with tab5:
        st.subheader("🔗 Programme d'Affiliation Intégré")
        st.write("Ces outils sont recommandés à vos clients. Remplacez les liens par vos liens d'affiliation.")

        for key, prog in AFFILIATE_LINKS.items():
            with st.container():
                cols = st.columns([2, 2, 1, 1])
                with cols[0]:
                    st.markdown(f"**{prog['name']}**")
                    st.caption(prog['description'])
                with cols[1]:
                    st.write(f"Commission: {prog['commission']}")
                    st.caption(f"Catégorie: {prog['category']}")
                with cols[2]:
                    st.markdown(f"[🔗 Lien]({prog['url']})")
                with cols[3]:
                    st.button("📋 Copier", key=f"aff_{key}")
                st.divider()

        st.info("💡 **Conseil**: Inscrivez-vous sur ces plateformes et remplacez 'YOUR_AFFILIATE_ID' par votre vrai ID pour commencer à gagner des commissions!")

if __name__ == "__main__":
    main()
