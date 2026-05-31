import os
import streamlit as st
import json
import time
from typing import List, Dict
import pandas as pd

# ============================================
# AFFILIATE LINKS CONFIGURATION
# ============================================

AFFILIATE_LINKS = {
    "buildium": {
        "name": "Buildium",
        "url": "https://www.buildium.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Logiciel de gestion locative #1 aux USA",
        "commission": "25% recurrent",
        "category": "Gestion locative"
    },
    "dealcheck": {
        "name": "DealCheck",
        "url": "https://dealcheck.io?fp_ref=omar18",
        "description": "Analyse d'investissement immobilier",
        "commission": "30% recurrent",
        "category": "Analyse de deals"
    },
    "foreclosure": {
        "name": "Foreclosure.com",
        "url": "https://www.foreclosure.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Biens saisis et ventes aux encheres",
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
        "commission": "30% recurrent",
        "category": "Leads"
    },
    "biggerpockets": {
        "name": "BiggerPockets Pro",
        "url": "https://www.biggerpockets.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Communaute investisseurs + outils",
        "commission": "$75/signup",
        "category": "Education"
    },
    "roofstock": {
        "name": "Roofstock",
        "url": "https://www.roofstock.com/?ref=YOUR_AFFILIATE_ID",
        "description": "Biens locatifs cle en main",
        "commission": "$15/referral",
        "category": "Investissement"
    },
    "rentredi": {
        "name": "RentRedi",
        "url": "https://rentredi.com/?ref=YOUR_AFFILIATE_ID",
        "description": "App de gestion pour proprietaires",
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
# PROPERTY DESCRIPTION GENERATOR
# ============================================

class PropertyDescriptionAgent:
    def generate_description(self, property_data: dict, language="fr") -> str:
        """Generate a compelling property description"""

        address = property_data.get('address', 'N/A')
        prop_type = property_data.get('property_type', 'N/A')
        price = property_data.get('price', 'N/A')
        bedrooms = property_data.get('bedrooms', 'N/A')
        bathrooms = property_data.get('bathrooms', 'N/A')
        sqft = property_data.get('square_feet', 'N/A')
        neighborhood = property_data.get('neighborhood', 'N/A')
        features = property_data.get('features', [])

        features_text = ", ".join(features) if features else "caracteristiques exceptionnelles"

        description = f"""
🏡 COUP DE COEUR ASSURE!

Située au coeur de {neighborhood}, cette magnifique {prop_type} de {sqft} sq ft 
vous seduira par son charme unique. Avec {bedrooms} chambres spacieuses, 
{bathrooms} salles de bain et {features_text}, elle est parfaite pour les familles.

✨ POINTS FORTS:
- Emplacement premium dans {neighborhood}
- {bedrooms} chambres + {bathrooms} salles de bain
- {features_text}
- Prix competitif: ${price:,}

📍 {address}

💰 Prix: ${price:,}

🔗 Analysez ce bien avec DealCheck: {AFFILIATE_LINKS['dealcheck']['url']}
📋 Documents juridiques avec NOLO: {AFFILIATE_LINKS['nolo']['url']}
👥 Rejoignez BiggerPockets: {AFFILIATE_LINKS['biggerpockets']['url']}
        """
        return description

    def generate_social_media_post(self, property_data: dict, platform="instagram") -> str:
        """Generate social media post for a property"""

        address = property_data.get('address', '')
        price = property_data.get('price', 'N/A')
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        prop_type = property_data.get('property_type', 'Bien')

        templates = {
            "instagram": f"""
🏠 {prop_type.upper()} A VENDRE

📍 {address}
💰 ${price:,}
🛏️ {bedrooms}ch | 🛁 {bathrooms}sdb

✨ Magnifique bien a ne pas manquer!

📞 Contactez-moi pour une visite!
🔗 Analysez ce bien: {AFFILIATE_LINKS['dealcheck']['url']}

#immobilier #vente #realestate #maison #investissement
            """,

            "facebook": f"""
🎉 NOUVEAUTE SUR LE MARCHE!

{prop_type} exceptionnel a vendre

📍 Localisation: {address}
💰 Prix: ${price:,}

Ce bien est parfait pour:
✅ Les familles
✅ Les investisseurs
✅ Premier achat

📊 Analysez le potentiel de ce bien avec DealCheck:
{AFFILIATE_LINKS['dealcheck']['url']}

📞 Contactez-moi pour organiser une visite!
            """,

            "linkedin": f"""
📊 OPPORTUNITE D'INVESTISSEMENT

{prop_type} | {address}

Points cles de l'investissement:
• Prix: ${price:,}
• Potentiel de rendement: A analyser
• Type: {prop_type}

Outils recommandes pour les investisseurs:
🔗 Analyse de deals: {AFFILIATE_LINKS['dealcheck']['url']}
🔗 Communaute investisseurs: {AFFILIATE_LINKS['biggerpockets']['url']}

#immobilier #investissement #opportunite
            """
        }

        return templates.get(platform, templates["instagram"])

# ============================================
# PROPERTY COMPARISON
# ============================================

class PropertyComparisonAgent:
    def compare_properties(self, properties: List[Dict]) -> Dict:
        """Compare multiple properties and return analysis"""

        if len(properties) < 2:
            return {"error": "Minimum 2 properties required for comparison"}

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
                "property_type": prop.get('property_type', 'N/A')
            }
            comparison_data.append(metrics)

        winner = min(comparison_data, key=lambda x: x['price_per_sqft'] if x['price_per_sqft'] > 0 else float('inf'))

        analysis = f"""
## Analyse Comparative

### Meilleur rapport qualite/prix:
**{winner['address']}** - ${winner['price']:,} (${winner['price_per_sqft']}/sq ft)

### Recommandations:
- **Pour les investisseurs**: Choisissez le bien avec le meilleur prix au sq ft
- **Pour les familles**: Privilegiez le nombre de chambres et le quartier
- **Pour la revente**: Analysez les tendances du marche avec DealCheck

### Outils recommandes:
- 🔗 {AFFILIATE_LINKS['dealcheck']['name']}: {AFFILIATE_LINKS['dealcheck']['url']}
- 🔗 {AFFILIATE_LINKS['foreclosure']['name']}: {AFFILIATE_LINKS['foreclosure']['url']}
- 🔗 {AFFILIATE_LINKS['nolo']['name']}: {AFFILIATE_LINKS['nolo']['url']}
        """

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
# STREAMLIT UI
# ============================================

def main():
    st.set_page_config(page_title="AI Real Estate Agent Team Pro", page_icon="🏠", layout="wide")

    st.title("🏠 AI Real Estate Agent Team Pro")
    st.caption("Pour Agents Immobiliers - Avec Generation de Descriptions & Comparaison")

    # Initialize session state
    if 'saved_properties' not in st.session_state:
        st.session_state.saved_properties = []
    if 'generated_descriptions' not in st.session_state:
        st.session_state.generated_descriptions = {}

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        with st.expander("🔗 Liens d'Affiliation"):
            st.write("Programmes integres:")
            for key, prog in AFFILIATE_LINKS.items():
                st.markdown(f"**{prog['name']}** - {prog['commission']}")
                st.caption(prog['description'])

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Recherche", "✍️ Descriptions", "⚖️ Comparaison", "📊 Analyse", "🔗 Affiliation"
    ])

    # TAB 1: SEARCH
    with tab1:
        st.subheader("🔍 Recherche de Biens")
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("Ville", placeholder="ex: Miami", value="Miami")
            min_price = st.number_input("Prix Min ($)", min_value=0, value=0, step=50000)
            min_bedrooms = st.selectbox("Min Chambres", [1, 2, 3, 4, 5])
        with col2:
            state = st.text_input("Etat/Region", placeholder="ex: FL", value="FL")
            max_price = st.number_input("Prix Max ($)", min_value=0, value=1000000, step=50000)
            property_type = st.selectbox("Type", ["Tous", "Maison", "Condo", "Appartement", "Terrain"])

        if st.button("🚀 Lancer la Recherche", type="primary"):
            progress = st.progress(0)
            status = st.empty()

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
                    "features": ["Renove", "Cuisine moderne"],
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
            status.success(f"✅ {len(demo_properties)} biens trouves!")

            # Display results
            for prop in demo_properties:
                with st.container():
                    cols = st.columns([3, 1, 1])
                    with cols[0]:
                        st.markdown(f"**{prop['address']}**")
                        st.write(f"💰 ${prop['price']:,} | 🛏️ {prop['bedrooms']}ch | 🛁 {prop['bathrooms']}sdb | 📐 {prop['square_feet']} sq ft")
                    with cols[1]:
                        if st.button("✍️ Decrire", key=f"desc_{prop['id']}"):
                            st.session_state.selected_for_description = prop
                    with cols[2]:
                        if st.button("⭐ Comparer", key=f"comp_{prop['id']}"):
                            if prop not in st.session_state.get('compare_list', []):
                                st.session_state.compare_list = st.session_state.get('compare_list', []) + [prop]
                    st.divider()

    # TAB 2: DESCRIPTIONS
    with tab2:
        st.subheader("✍️ Generateur de Descriptions")

        if 'selected_for_description' in st.session_state:
            prop = st.session_state.selected_for_description
            st.write(f"Bien selectionne: **{prop['address']}**")

            col1, col2 = st.columns(2)
            with col1:
                language = st.selectbox("Langue", ["Francais", "Anglais", "Espagnol"])
                platform = st.selectbox("Plateforme", ["Site web", "Instagram", "Facebook", "LinkedIn"])
            with col2:
                tone = st.selectbox("Ton", ["Professionnel", "Chaleureux", "Luxueux", "Familial"])
                length = st.selectbox("Longueur", ["Courte (100 mots)", "Moyenne (200 mots)", "Longue (300 mots)"])

            if st.button("📝 Generer la Description", type="primary"):
                desc_agent = PropertyDescriptionAgent()

                with st.spinner("Generation en cours..."):
                    description = desc_agent.generate_description(prop)
                    st.session_state.generated_descriptions[prop['id']] = description

                st.success("✅ Description generee!")
                st.text_area("Description", description, height=200)

                # Social media posts
                st.subheader("📱 Posts Reseaux Sociaux")
                for plat in ["instagram", "facebook", "linkedin"]:
                    post = desc_agent.generate_social_media_post(prop, plat)
                    with st.expander(f"{plat.title()}"):
                        st.text_area(f"Post {plat}", post, height=150)
                        st.button("📋 Copier", key=f"copy_{plat}")
        else:
            st.info("👆 Selectionnez un bien dans l'onglet 'Recherche' pour generer une description")

    # TAB 3: COMPARISON
    with tab3:
        st.subheader("⚖️ Comparaison de Biens")

        compare_list = st.session_state.get('compare_list', [])

        if len(compare_list) >= 2:
            st.write(f"**{len(compare_list)} biens a comparer**")

            comp_agent = PropertyComparisonAgent()
            df = comp_agent.generate_comparison_chart(compare_list)
            st.dataframe(df, use_container_width=True)

            if st.button("🔍 Analyse Detaillee", type="primary"):
                with st.spinner("Analyse en cours..."):
                    result = comp_agent.compare_properties(compare_list)

                st.subheader("📊 Resultat de l'Analyse")

                if result.get('winner'):
                    winner = result['winner']
                    st.success(f"🏆 MEILLEUR RAPPORT QUALITE/PRIX: {winner['address']} a ${winner['price']:,} (${winner['price_per_sqft']}/sq ft)")

                st.markdown(result['analysis'])

                st.subheader("🔗 Outils Recommandes")
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
                        st.markdown(f"[🔗 Acceder]({url})")
        else:
            st.info("👆 Ajoutez au moins 2 biens a comparer depuis l'onglet 'Recherche'")
            if len(compare_list) == 1:
                st.write(f"1 bien selectionne: {compare_list[0]['address']}")

    # TAB 4: ANALYSIS
    with tab4:
        st.subheader("📊 Analyse de Marche")

        if st.session_state.saved_properties:
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

            # Simple bar chart
            import plotly.express as px
            df_chart = pd.DataFrame(st.session_state.saved_properties)
            fig = px.bar(df_chart, x='address', y='price', title='Prix des Biens')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Lancez d'abord une recherche")

    # TAB 5: AFFILIATION
    with tab5:
        st.subheader("🔗 Programme d'Affiliation Integre")
        st.write("Ces outils sont recommandes a vos clients. Remplacez les liens par vos liens d'affiliation.")

        for key, prog in AFFILIATE_LINKS.items():
            with st.container():
                cols = st.columns([2, 2, 1, 1])
                with cols[0]:
                    st.markdown(f"**{prog['name']}**")
                    st.caption(prog['description'])
                with cols[1]:
                    st.write(f"Commission: {prog['commission']}")
                    st.caption(f"Categorie: {prog['category']}")
                with cols[2]:
                    st.markdown(f"[🔗 Lien]({prog['url']})")
                with cols[3]:
                    st.button("📋 Copier", key=f"aff_{key}")
                st.divider()

        st.info("💡 **Conseil**: Inscrivez-vous sur ces plateformes et remplacez 'YOUR_AFFILIATE_ID' par votre vrai ID pour commencer a gagner des commissions!")

if __name__ == "__main__":
    main()
