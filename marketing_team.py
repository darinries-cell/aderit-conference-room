import os
import json
import streamlit as st
from datetime import datetime
import httpx

# ============================================
# CONFIGURATION
# ============================================

# Try to load from Streamlit secrets first, then environment
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

# Supabase config
SUPABASE_URL = "https://yntsgehumjnoxferoycy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InludHNnZWh1bWpub3gmZXJveWN5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3NDAwNDcsImV4cCI6MjA4NTMxNjA0N30.SVk7cRrHzTuPtVj3RxKOJ46x-LIa3iodytYMi63Ibz8"

# API Keys
ANTHROPIC_API_KEY = get_secret("ANTHROPIC_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")

# Set up clients
import anthropic
import openai
from google import genai

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# Check if Ollama is available (local only)
OLLAMA_AVAILABLE = False
try:
    import ollama
    ollama_client = ollama.Client()
    # Test connection
    ollama_client.list()
    OLLAMA_AVAILABLE = True
except:
    pass

def supabase_request(method, table, data=None, params=None):
    """Make a request to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    with httpx.Client() as client:
        if method == "GET":
            response = client.get(url, headers=headers, params=params)
        elif method == "POST":
            response = client.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = client.patch(url, headers=headers, json=data, params=params)
        elif method == "DELETE":
            response = client.delete(url, headers=headers, params=params)
        elif method == "UPSERT":
            headers["Prefer"] = "resolution=merge-duplicates,return=representation"
            response = client.post(url, headers=headers, json=data)
        
        if response.status_code >= 400:
            st.error(f"Supabase error: {response.status_code} - {response.text}")
            return None
        
        if response.text:
            return response.json()
        return []

# ============================================
# DEFAULT ROLES
# ============================================

DEFAULT_ROLES = {
    "positioning_strategist": {
        "name": "Positioning Strategist",
        "emoji": "🎯",
        "category": "Internal - Marketing",
        "description": """You are the Positioning Strategist on Aderit's marketing advisory team.

BACKGROUND: You've led positioning for enterprise SaaS companies including two successful category-creation plays. You studied under April Dunford and have deep expertise in competitive positioning, narrative strategy, and category design.

YOUR EXPERTISE: Defining "why us" and "why now", category creation, strategic narrative, positioning against competitors.

YOUR STYLE: Strategic, precise with language, obsessed with differentiation. You ask "what are we really selling?" and "why should anyone care?" """
    },
    "copywriter": {
        "name": "Copywriter",
        "emoji": "✍️",
        "category": "Internal - Marketing",
        "description": """You are the Copywriter on Aderit's marketing advisory team.

BACKGROUND: 15 years writing B2B enterprise copy. You've written for Salesforce, Workday, and multiple HR tech startups.

YOUR EXPERTISE: Headlines that stop scrollers, website copy that converts, sales deck language, one-pagers that get forwarded.

YOUR STYLE: Direct, punchy, allergic to jargon. You ask "would a real human say this?" and "can we cut this in half?" """
    },
    "creative_director": {
        "name": "Creative Director",
        "emoji": "🎨",
        "category": "Internal - Marketing",
        "description": """You are the Creative Director on Aderit's marketing advisory team.

BACKGROUND: Former creative lead at agencies working with enterprise tech brands. You've rebranded three B2B companies from "boring and technical" to "memorable and human."

YOUR EXPERTISE: Brand voice and personality, emotional resonance in B2B, visual and verbal differentiation.

YOUR STYLE: Creative, sometimes provocative, always pushing for distinctiveness. You hate safe and forgettable."""
    },
    "buyer_researcher": {
        "name": "Buyer Researcher",
        "emoji": "👥",
        "category": "Internal - Marketing",
        "description": """You are the Buyer Researcher on Aderit's marketing advisory team.

BACKGROUND: Former head of customer research at Gong. You've conducted hundreds of buyer interviews and analyzed thousands of sales calls.

YOUR EXPERTISE: How buyers describe their own pain, the language customers actually use, common objections, what triggers buying decisions.

YOUR STYLE: Grounded, evidence-based, always bringing it back to the customer. You ask "but what does the buyer actually say?" """
    },
    "ceo": {
        "name": "CEO Advisor",
        "emoji": "👔",
        "category": "Internal - Executive",
        "description": """You are the CEO advisor for Aderit.

BACKGROUND: Founded and sold an HR data integration company for $185M. You've been through the full journey from founding to exit.

YOUR EXPERTISE: Overall strategy, fundraising, M&A positioning, board management, competitive dynamics, exit timing.

YOUR STYLE: Strategic, sees the whole board. "What's the 3-year play?" "Who buys this and why?" """
    },
    "cro": {
        "name": "CRO Advisor",
        "emoji": "💼",
        "category": "Internal - Executive",
        "description": """You are the CRO (Chief Revenue Officer) advisor for Aderit.

BACKGROUND: Former VP Sales at Ceridian. Joined at $8M ARR, scaled to $80M+. Built enterprise sales orgs from scratch.

YOUR EXPERTISE: Enterprise sales cycles, hiring sales teams, pricing strategy, procurement navigation.

YOUR STYLE: Direct, numbers-driven. "What's the ARR?" "What's the sales cycle?" """
    },
    "cmo": {
        "name": "CMO Advisor",
        "emoji": "📣",
        "category": "Internal - Executive",
        "description": """You are the CMO (Chief Marketing Officer) advisor for Aderit.

BACKGROUND: Early marketing leader at Segment pre-acquisition. Built the "customer data infrastructure" category from nothing.

YOUR EXPERTISE: Category creation, brand positioning, narrative building, analyst relations, content strategy.

YOUR STYLE: Narrative-focused, creative, sometimes contrarian. "What's the story that makes analysts write about us?" """
    },
    "coo": {
        "name": "COO Advisor",
        "emoji": "🗂️",
        "category": "Internal - Executive",
        "description": """You are the COO (Chief Operating Officer) advisor for Aderit.

YOUR ROLE: Facilitate discussions, synthesize insights, keep operations running smoothly.

YOUR STYLE: Organized, direct, action-oriented. You ask "what's the next action?" and "who owns this?" """
    },
    "chro": {
        "name": "CHRO (Prospect)",
        "emoji": "👩‍💼",
        "category": "Client - Executive",
        "description": """You are a CHRO (Chief Human Resources Officer) at a Fortune 500 company with 15,000 employees.

YOUR SITUATION: You have 12+ HR systems that don't talk to each other. Your team spends 40% of their time on manual data reconciliation.

YOUR CONCERNS: Integration complexity, change management, proving ROI to the CFO, vendor stability.

YOUR STYLE: Strategic but practical. You've been burned by vendors before. You need real proof, not promises."""
    },
    "cfo_prospect": {
        "name": "CFO (Prospect)",
        "emoji": "💰",
        "category": "Client - Executive",
        "description": """You are a CFO at a mid-market company ($500M revenue) evaluating HR technology investments.

YOUR SITUATION: The CHRO wants budget for "HR transformation" but you've seen too many IT projects go over budget.

YOUR CONCERNS: TCO, implementation timeline, productivity gains, contract terms, time to value.

YOUR STYLE: Skeptical, numbers-focused. You ask "what's the payback period?" and "show me the ROI model." """
    },
    "talent_acquisition_director": {
        "name": "Director of Talent Acquisition",
        "emoji": "🎯",
        "category": "Client - HR Operations",
        "description": """You are a Director of Talent Acquisition at a fast-growing tech company.

YOUR SITUATION: Your ATS doesn't talk to your HRIS. Candidate data is everywhere. You're drowning in spreadsheets.

YOUR PAIN POINTS: Manual data entry, duplicate records, slow time-to-hire, poor reporting.

YOUR STYLE: Pragmatic, deadline-driven. You need solutions that work NOW."""
    },
    "hr_ops_manager": {
        "name": "HR Operations Manager",
        "emoji": "⚙️",
        "category": "Client - HR Operations",
        "description": """You are an HR Operations Manager at a company with 3,000 employees.

YOUR SITUATION: You're the person who actually has to make the HR systems work together. You spend your days fixing data errors.

YOUR PAIN POINTS: Data inconsistencies, manual reporting, compliance anxiety, audit prep nightmares.

YOUR STYLE: Detail-oriented, cautious about new tools. You ask "what happens to my existing data?" """
    },
    "it_director": {
        "name": "IT Director",
        "emoji": "💻",
        "category": "Client - IT",
        "description": """You are an IT Director responsible for enterprise applications.

YOUR SITUATION: HR keeps buying point solutions without consulting you. Now you have 15 HR systems to maintain and secure.

YOUR CONCERNS: Security, compliance, API reliability, SSO support, SLAs.

YOUR STYLE: Technical, risk-averse. You ask "what's the architecture?" and "how does this handle failures?" """
    },
    "facilitator": {
        "name": "Facilitator",
        "emoji": "🎤",
        "category": "Internal - Operations",
        "description": """You are a neutral facilitator for discussions.

YOUR ROLE: Keep discussion productive, summarize key points, identify agreement and disagreement, drive toward conclusions.

YOUR STYLE: Neutral, organized, focused on outcomes."""
    }
}

# ============================================
# DATABASE FUNCTIONS
# ============================================

@st.cache_data(ttl=5)
def load_roles_from_db():
    result = supabase_request("GET", "roles", params={"select": "*"})
    
    if not result:
        for key, role in DEFAULT_ROLES.items():
            supabase_request("POST", "roles", data={
                "key": key,
                "name": role["name"],
                "emoji": role["emoji"],
                "category": role["category"],
                "description": role["description"]
            })
        result = supabase_request("GET", "roles", params={"select": "*"})
    
    roles = {}
    for row in (result or []):
        roles[row["key"]] = {
            "name": row["name"],
            "emoji": row["emoji"],
            "category": row["category"],
            "description": row["description"]
        }
    return roles if roles else DEFAULT_ROLES

def save_role_to_db(key, name, emoji, category, description):
    supabase_request("UPSERT", "roles", data={
        "key": key,
        "name": name,
        "emoji": emoji,
        "category": category,
        "description": description
    })
    st.cache_data.clear()

def delete_role_from_db(key):
    supabase_request("DELETE", "roles", params={"key": f"eq.{key}"})
    st.cache_data.clear()

@st.cache_data(ttl=5)
def load_room_assignments():
    result = supabase_request("GET", "room_assignments", params={"select": "*"})
    assignments = {}
    for row in (result or []):
        assignments[row["llm_name"]] = row["role_key"]
    
    if not assignments:
        return {
            "Claude": "positioning_strategist",
            "ChatGPT": "copywriter",
            "Gemini": "creative_director",
            "Claude2": "buyer_researcher"
        }
    return assignments

def save_room_assignment(llm_name, role_key):
    supabase_request("UPSERT", "room_assignments", data={
        "llm_name": llm_name,
        "role_key": role_key,
        "updated_at": datetime.now().isoformat()
    })
    st.cache_data.clear()

@st.cache_data(ttl=10)
def load_discussions():
    result = supabase_request("GET", "discussions", params={
        "select": "*",
        "order": "created_at.desc",
        "limit": "50"
    })
    return result or []

def save_discussion(topic, synthesis, key_decisions, participants, keywords, full_log):
    supabase_request("POST", "discussions", data={
        "topic": topic,
        "synthesis": synthesis,
        "key_decisions": key_decisions,
        "participants": participants,
        "keywords": keywords,
        "full_log": full_log
    })
    st.cache_data.clear()

def find_relevant_context(question, max_results=3):
    discussions = load_discussions()
    if not discussions:
        return None
    
    question_keywords = set(extract_keywords(question))
    
    scored = []
    for d in discussions:
        d_keywords = set(d.get("keywords") or [])
        overlap = len(question_keywords & d_keywords)
        if overlap > 0:
            scored.append((overlap, d))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    top_results = scored[:max_results]
    
    if not top_results:
        return None
    
    context = "## RELEVANT PAST DISCUSSIONS:\n\n"
    for score, d in top_results:
        context += f"### {d['created_at'][:10]} - {d['topic'][:80]}\n"
        context += f"**Participants:** {', '.join(d.get('participants') or ['Unknown'])}\n"
        context += f"**Synthesis:** {(d.get('synthesis') or '')[:600]}\n\n"
    
    return context

def extract_keywords(text):
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'to', 'of',
                 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
                 'and', 'but', 'if', 'or', 'because', 'this', 'that', 'these', 'those',
                 'what', 'which', 'who', 'we', 'our', 'you', 'your', 'they', 'their',
                 'it', 'its', 'i', 'my', 'me', 'he', 'she', 'his', 'her', 'him'}
    words = text.lower().replace('\n', ' ').replace('.', ' ').replace(',', ' ').split()
    keywords = [w for w in words if len(w) > 3 and w not in stopwords]
    return list(set(keywords))[:30]

# ============================================
# LLM FUNCTIONS
# ============================================

COMPANY_CONTEXT = """
COMPANY CONTEXT:
Aderit is an AI-powered HR infrastructure platform seeking $5M Series A. 
Vision: "AWS of workforce data" - unifying disconnected enterprise HR systems.
Founder: Darin Ries
"""

def ask_ollama(prompt, role_description, memory_context=None):
    if not OLLAMA_AVAILABLE:
        return "[Ollama not available - running in cloud mode]"
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    try:
        response = ollama_client.chat(
            model='qwen2.5:7b',
            messages=[{'role': 'user', 'content': f"{context}\n\n{prompt}"}]
        )
        return response['message']['content']
    except Exception as e:
        return f"[Ollama error: {str(e)[:100]}]"

def ask_claude(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}]
    )
    return message.content[0].text

def ask_claude_haiku(prompt, role_description, memory_context=None):
    """Cheaper/faster Claude for the 4th seat when Ollama unavailable"""
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}]
    )
    return message.content[0].text

def ask_chatgpt(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}]
    )
    return response.choices[0].message.content

def ask_gemini(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{context}\n\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"[Gemini unavailable: {str(e)[:100]}]"

# Available LLMs depend on whether Ollama is running
if OLLAMA_AVAILABLE:
    LLM_FUNCTIONS = {
        'Claude': ask_claude,
        'ChatGPT': ask_chatgpt,
        'Gemini': ask_gemini,
        'Ollama': ask_ollama
    }
    LLM_LIST = ['Claude', 'ChatGPT', 'Gemini', 'Ollama']
else:
    LLM_FUNCTIONS = {
        'Claude': ask_claude,
        'ChatGPT': ask_chatgpt,
        'Gemini': ask_gemini,
        'Haiku': ask_claude_haiku
    }
    LLM_LIST = ['Claude', 'ChatGPT', 'Gemini', 'Haiku']

# ============================================
# STREAMLIT APP
# ============================================

st.set_page_config(
    page_title="Aderit Conference Room",
    page_icon="🏢",
    layout="wide"
)

# Refresh button
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

# Load data
roles = load_roles_from_db()
room_assignments = load_room_assignments()
discussions = load_discussions()

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.title("🏢 Conference Room")
    
    # Show mode
    if OLLAMA_AVAILABLE:
        st.success("🖥️ Local mode (Ollama available)")
    else:
        st.info("☁️ Cloud mode (using Haiku)")
    
    tab1, tab2, tab3 = st.tabs(["👥 Room", "📚 Roles", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### Who's in the room?")
        
        role_options = {k: f"{v['emoji']} {v['name']}" for k, v in roles.items()}
        role_keys = list(role_options.keys())
        
        for llm in LLM_LIST:
            current = room_assignments.get(llm, role_keys[0] if role_keys else None)
            current_idx = role_keys.index(current) if current in role_keys else 0
            
            selected = st.selectbox(
                f"**{llm}**",
                role_keys,
                index=current_idx,
                format_func=lambda x: role_options.get(x, x),
                key=f"assign_{llm}"
            )
            
            if selected != room_assignments.get(llm):
                save_room_assignment(llm, selected)
                room_assignments[llm] = selected
        
        st.markdown("---")
        st.markdown("### Current Room:")
        for llm in LLM_LIST:
            role_key = room_assignments.get(llm, "")
            role = roles.get(role_key, {})
            st.markdown(f"{role.get('emoji', '👤')} **{role.get('name', 'Unknown')}** ({llm})")
    
    with tab2:
        st.markdown("### Roles Library")
        
        categories = sorted(set(r.get('category', 'Uncategorized') for r in roles.values()))
        selected_category = st.selectbox("Filter:", ["All"] + categories)
        
        for role_key, role in roles.items():
            if selected_category != "All" and role.get('category') != selected_category:
                continue
            with st.expander(f"{role.get('emoji', '👤')} {role.get('name', role_key)}"):
                st.markdown(f"**Category:** {role.get('category', 'Uncategorized')}")
                st.markdown(f"**Description:**\n{role.get('description', '')[:500]}...")
                
                if st.button(f"🗑️ Delete", key=f"del_{role_key}"):
                    delete_role_from_db(role_key)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### ➕ Create New Role")
        
        with st.form("new_role_form"):
            new_name = st.text_input("Role Name:")
            new_emoji = st.text_input("Emoji:", value="👤")
            new_category = st.selectbox(
                "Category:",
                ["Internal - Executive", "Internal - Marketing", "Internal - Operations", 
                 "Client - Executive", "Client - HR Operations", "Client - IT", "Other"]
            )
            new_description = st.text_area("Description:", height=200)
            
            if st.form_submit_button("Create Role"):
                if new_name and new_description:
                    role_key = new_name.lower().replace(" ", "_")
                    save_role_to_db(role_key, new_name, new_emoji, new_category, new_description)
                    st.success(f"Created: {new_name}")
                    st.rerun()
                else:
                    st.error("Fill in name and description")
    
    with tab3:
        st.markdown("### Settings")
        st.markdown(f"📚 **Memory:** {len(discussions)} past discussions")
        
        if st.button("🔄 Force Refresh"):
            st.cache_data.clear()
            st.rerun()

# ============================================
# MAIN AREA
# ============================================

st.title("🏢 Aderit Conference Room")

room_display = " | ".join([
    f"{roles.get(room_assignments.get(llm, ''), {}).get('emoji', '👤')} {roles.get(room_assignments.get(llm, ''), {}).get('name', 'Unknown')}"
    for llm in LLM_LIST
])
st.markdown(f"**In the room:** {room_display}")
st.markdown("---")

# Past discussions
st.markdown("### 📜 Recent Discussions")
for d in discussions[:10]:
    with st.expander(f"{d['created_at'][:10]} - {(d.get('topic') or 'Untitled')[:60]}"):
        st.markdown(f"**Participants:** {', '.join(d.get('participants') or [])}")
        st.markdown(f"**Synthesis:** {d.get('synthesis', 'N/A')}")
        st.markdown(f"**Key Decisions:** {d.get('key_decisions', 'N/A')}")

st.markdown("---")

# Input
user_input = st.chat_input("What would you like to discuss?")

if user_input:
    st.markdown(f"**🧑 Darin:** {user_input}")
    
    memory_context = find_relevant_context(user_input)
    if memory_context:
        st.info("📚 Found relevant past discussions")
    
    participants = []
    for llm in LLM_LIST:
        role_key = room_assignments.get(llm, "")
        role = roles.get(role_key, {})
        participants.append({
            'llm': llm,
            'role_key': role_key,
            'name': role.get('name', 'Unknown'),
            'emoji': role.get('emoji', '👤'),
            'description': role.get('description', ''),
            'func': LLM_FUNCTIONS[llm]
        })
    
    with st.status("🎯 Discussion in progress...", expanded=True) as status:
        discussion_log = ""
        
        if memory_context:
            discussion_log += "## Referenced Past Discussions\n\n" + memory_context + "\n\n"
        
        # Round 1
        st.write("**Round 1: Initial Perspectives**")
        r1_prompt = f'Darin says: "{user_input}"\n\nGive your perspective in 2-3 paragraphs.'
        responses_r1 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} thinking...")
            responses_r1[p['llm']] = p['func'](r1_prompt, p['description'], memory_context)
        discussion_log += "## Round 1: Initial Perspectives\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']} ({p['llm']})\n{responses_r1[p['llm']]}\n\n"
        
        # Round 2
        st.write("**Round 2: React & Debate**")
        all_r1 = "\n\n".join([f"{p['name']}: {responses_r1[p['llm']]}" for p in participants])
        r2_prompt = f'Topic: "{user_input}"\n\nRound 1:\n{all_r1}\n\nReact: agreements, pushback, questions.'
        responses_r2 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} responding...")
            responses_r2[p['llm']] = p['func'](r2_prompt, p['description'], memory_context)
        discussion_log += "## Round 2: React & Debate\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']}\n{responses_r2[p['llm']]}\n\n"
        
        # Round 3
        st.write("**Round 3: Specific Proposals**")
        all_r2 = "\n\n".join([f"{p['name']}: {responses_r2[p['llm']]}" for p in participants])
        r3_prompt = f'Topic: "{user_input}"\n\nDiscussion:\n{all_r1}\n\n{all_r2}\n\nPropose 2-3 specific ideas.'
        responses_r3 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} proposing...")
            responses_r3[p['llm']] = p['func'](r3_prompt, p['description'], memory_context)
        discussion_log += "## Round 3: Specific Proposals\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']}\n{responses_r3[p['llm']]}\n\n"
        
        # Round 4
        st.write("**Round 4: Critique & Refine**")
        all_r3 = "\n\n".join([f"{p['name']}: {responses_r3[p['llm']]}" for p in participants])
        r4_prompt = f'Topic: "{user_input}"\n\nProposals:\n{all_r3}\n\nWhich ideas have merit? Start converging.'
        responses_r4 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} refining...")
            responses_r4[p['llm']] = p['func'](r4_prompt, p['description'], memory_context)
        discussion_log += "## Round 4: Critique & Refine\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']}\n{responses_r4[p['llm']]}\n\n"
        
        # Round 5
        st.write("**Round 5: Final Recommendations**")
        all_r4 = "\n\n".join([f"{p['name']}: {responses_r4[p['llm']]}" for p in participants])
        r5_prompt = f'Topic: "{user_input}"\n\nFull discussion:\n{all_r3}\n\n{all_r4}\n\nFinal recommendation.'
        responses_r5 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} finalizing...")
            responses_r5[p['llm']] = p['func'](r5_prompt, p['description'], memory_context)
        discussion_log += "## Round 5: Final Recommendations\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']}\n{responses_r5[p['llm']]}\n\n"
        
        # Synthesis
        st.write("**Synthesizing...**")
        synth_prompt = f'''Topic: "{user_input}"

Final recommendations:
{chr(10).join([f"{p['name']}: {responses_r5[p['llm']]}" for p in participants])}

Synthesize in 3-4 paragraphs: agreements, tensions, recommendations, next steps.'''
        synthesis = ask_claude(synth_prompt, "You are a neutral facilitator summarizing this discussion.", memory_context)
        
        decisions_prompt = f"List 3-5 key decisions as bullet points:\n\n{synthesis}"
        key_decisions = ask_claude(decisions_prompt, "Extract key decisions concisely.", None)
        
        discussion_log += "## 📋 Synthesis\n\n" + synthesis
        discussion_log += "\n\n## 🔑 Key Decisions\n\n" + key_decisions
        
        # Save
        participant_names = [p['name'] for p in participants]
        keywords = extract_keywords(user_input + " " + synthesis)
        save_discussion(user_input, synthesis, key_decisions, participant_names, keywords, discussion_log)
        
        status.update(label="✅ Discussion complete!", state="complete")
    
    st.markdown("### 📋 Synthesis")
    st.markdown(synthesis)
    
    st.markdown("### 🔑 Key Decisions")
    st.markdown(key_decisions)
    
    with st.expander("📖 View Full Discussion"):
        st.markdown(discussion_log)
```

Save and close.

---

## Step 5: Create .gitignore
```
notepad .gitignore
```

Paste:
```
.env
__pycache__/
*.pyc
memory/
migrate_to_supabase.py
```

Save and close.

---

## Step 6: Initialize Git and Push
```
git init
git add marketing_team.py requirements.txt .gitignore
git commit -m "Initial commit - Aderit Conference Room"
```

Now go to GitHub.com:
1. Click **+** → **New repository**
2. Name it `aderit-conference-room`
3. Leave it **Public** (required for free Streamlit hosting)
4. **Don't** check any boxes (no README, no .gitignore)
5. Click **Create repository**

GitHub will show you commands. Run these (replace YOUR_USERNAME):
```
git remote add origin https://github.com/YOUR_USERNAME/aderit-conference-room.git
git branch -M main
git push -u origin main
```

It will ask for your GitHub username and password (or personal access token).

---

## Step 7: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your repo: `aderit-conference-room`
5. Branch: `main`
6. Main file: `marketing_team.py`
7. Click **Advanced settings** → **Secrets**
8. Paste your API keys:
```
ANTHROPIC_API_KEY = "sk-ant-..."
OPENAI_API_KEY = "sk-..."
GOOGLE_API_KEY = "..."