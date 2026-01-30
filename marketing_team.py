import os
import json
import streamlit as st
from datetime import datetime
import httpx

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

SUPABASE_URL = "https://yntsgehumjnoxferoycy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InludHNnZWh1bWpub3hmZXJveWN5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTc0MDA0NywiZXhwIjoyMDg1MzE2MDQ3fQ.OCv9jKm_uDBDFDAgcJlljCAL0XJovK_ihrvA0zUr9qM"

ANTHROPIC_API_KEY = get_secret("ANTHROPIC_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")

import anthropic
import openai
from google import genai

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

OLLAMA_AVAILABLE = False
try:
    import ollama
    ollama_client = ollama.Client()
    ollama_client.list()
    OLLAMA_AVAILABLE = True
except:
    pass

def supabase_request(method, table, data=None, params=None):
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
        
        if response.status_code >= 400:
            st.error(f"Supabase error: {response.status_code} - {response.text}")
            return None
        
        if response.text:
            return response.json()
        return []

DEFAULT_ROLES = {
    "positioning_strategist": {
        "name": "Positioning Strategist",
        "emoji": "🎯",
        "category": "Internal - Marketing",
        "description": "You are the Positioning Strategist. Background: Led positioning for enterprise SaaS including category-creation plays. Studied under April Dunford. Expertise: Why us, why now, category creation, strategic narrative. Style: Strategic, precise, obsessed with differentiation."
    },
    "copywriter": {
        "name": "Copywriter",
        "emoji": "✍️",
        "category": "Internal - Marketing",
        "description": "You are the Copywriter. Background: 15 years B2B enterprise copy for Salesforce, Workday, HR tech startups. Expertise: Headlines, website copy, sales decks, one-pagers. Style: Direct, punchy, allergic to jargon."
    },
    "creative_director": {
        "name": "Creative Director",
        "emoji": "🎨",
        "category": "Internal - Marketing",
        "description": "You are the Creative Director. Background: Former agency creative lead for enterprise tech brands. Rebranded B2B companies from boring to memorable. Expertise: Brand voice, emotional resonance, differentiation. Style: Creative, provocative, hates forgettable."
    },
    "buyer_researcher": {
        "name": "Buyer Researcher",
        "emoji": "👥",
        "category": "Internal - Marketing",
        "description": "You are the Buyer Researcher. Background: Former head of customer research at Gong. Conducted hundreds of buyer interviews. Expertise: Buyer pain language, objections, purchase triggers. Style: Grounded, evidence-based, customer-focused."
    },
    "ceo": {
        "name": "CEO Advisor",
        "emoji": "👔",
        "category": "Internal - Executive",
        "description": "You are the CEO Advisor. Background: Founded and sold HR data integration company for $185M. Expertise: Strategy, fundraising, M&A, board management, exit timing. Style: Strategic, sees whole board."
    },
    "cro": {
        "name": "CRO Advisor",
        "emoji": "💼",
        "category": "Internal - Executive",
        "description": "You are the CRO Advisor. Background: Former VP Sales at Ceridian, $8M to $80M+ ARR. Expertise: Enterprise sales, hiring, pricing, procurement. Style: Direct, numbers-driven."
    },
    "chro": {
        "name": "CHRO (Prospect)",
        "emoji": "👩‍💼",
        "category": "Client - Executive",
        "description": "You are a CHRO at Fortune 500, 15K employees. Situation: 12+ disconnected HR systems, 40% time on data reconciliation. Concerns: Integration complexity, change management, ROI proof, vendor stability. Style: Strategic but practical, been burned before."
    },
    "cfo_prospect": {
        "name": "CFO (Prospect)",
        "emoji": "💰",
        "category": "Client - Executive",
        "description": "You are a CFO at $500M company evaluating HR tech. Situation: CHRO wants transformation budget but you've seen IT projects fail. Concerns: TCO, timeline, productivity gains, contract terms. Style: Skeptical, numbers-focused."
    },
    "talent_acquisition_director": {
        "name": "Director of Talent Acquisition",
        "emoji": "🎯",
        "category": "Client - HR Operations",
        "description": "You are Director of TA at fast-growing tech company. Situation: ATS and HRIS don't connect, drowning in spreadsheets. Pain: Manual entry, duplicates, slow hiring, poor reporting. Style: Pragmatic, needs solutions NOW."
    },
    "hr_ops_manager": {
        "name": "HR Operations Manager",
        "emoji": "⚙️",
        "category": "Client - HR Operations",
        "description": "You are HR Ops Manager at 3K employee company. Situation: You make HR systems work together, fixing data errors daily. Pain: Inconsistencies, manual reporting, compliance anxiety. Style: Detail-oriented, cautious."
    },
    "it_director": {
        "name": "IT Director",
        "emoji": "💻",
        "category": "Client - IT",
        "description": "You are IT Director for enterprise apps. Situation: HR bought 15 point solutions without consulting you. Concerns: Security, compliance, APIs, SSO, SLAs. Style: Technical, risk-averse."
    },
    "facilitator": {
        "name": "Facilitator",
        "emoji": "🎤",
        "category": "Internal - Operations",
        "description": "You are a neutral facilitator. Role: Keep discussion productive, summarize, identify agreement/disagreement, drive conclusions. Style: Neutral, organized, outcome-focused."
    }
}

@st.cache_data(ttl=5)
def load_roles_from_db():
    result = supabase_request("GET", "roles", params={"select": "*"})
    if not result:
        for key, role in DEFAULT_ROLES.items():
            supabase_request("POST", "roles", data={"key": key, "name": role["name"], "emoji": role["emoji"], "category": role["category"], "description": role["description"]})
        result = supabase_request("GET", "roles", params={"select": "*"})
    roles = {}
    for row in (result or []):
        roles[row["key"]] = {"name": row["name"], "emoji": row["emoji"], "category": row["category"], "description": row["description"]}
    return roles if roles else DEFAULT_ROLES

def save_role_to_db(key, name, emoji, category, description):
    supabase_request("DELETE", "roles", params={"key": f"eq.{key}"})
    supabase_request("POST", "roles", data={"key": key, "name": name, "emoji": emoji, "category": category, "description": description})
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
        return {"Claude": "positioning_strategist", "ChatGPT": "copywriter", "Gemini": "creative_director", "Haiku": "buyer_researcher"}
    return assignments

def save_room_assignment(llm_name, role_key):
    supabase_request("DELETE", "room_assignments", params={"llm_name": f"eq.{llm_name}"})
    supabase_request("POST", "room_assignments", data={"llm_name": llm_name, "role_key": role_key, "updated_at": datetime.now().isoformat()})
    st.cache_data.clear()

@st.cache_data(ttl=10)
def load_discussions():
    result = supabase_request("GET", "discussions", params={"select": "*", "order": "created_at.desc", "limit": "50"})
    return result or []

def save_discussion(topic, synthesis, key_decisions, participants, keywords, full_log):
    supabase_request("POST", "discussions", data={"topic": topic, "synthesis": synthesis, "key_decisions": key_decisions, "participants": participants, "keywords": keywords, "full_log": full_log})
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
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'and', 'but', 'if', 'or', 'because', 'this', 'that', 'these', 'those', 'what', 'which', 'who', 'we', 'our', 'you', 'your', 'they', 'their', 'it', 'its', 'i', 'my', 'me', 'he', 'she', 'his', 'her', 'him'}
    words = text.lower().replace('\n', ' ').replace('.', ' ').replace(',', ' ').split()
    keywords = [w for w in words if len(w) > 3 and w not in stopwords]
    return list(set(keywords))[:30]

COMPANY_CONTEXT = """
COMPANY CONTEXT:
Aderit is an AI-powered HR infrastructure platform seeking $5M Series A. 
Vision: "AWS of workforce data" - unifying disconnected enterprise HR systems.
Founder: Darin Ries
"""

def ask_ollama(prompt, role_description, memory_context=None):
    if not OLLAMA_AVAILABLE:
        return "[Ollama not available in cloud mode]"
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    try:
        response = ollama_client.chat(model='qwen2.5:7b', messages=[{'role': 'user', 'content': f"{context}\n\n{prompt}"}])
        return response['message']['content']
    except Exception as e:
        return f"[Ollama error: {str(e)[:100]}]"

def ask_claude(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1024, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_claude_haiku(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(model="claude-3-5-haiku-20241022", max_tokens=1024, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_chatgpt(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    response = openai_client.chat.completions.create(model="gpt-4o", max_tokens=1024, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return response.choices[0].message.content

def ask_gemini(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    try:
        response = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=f"{context}\n\n{prompt}")
        return response.text
    except Exception as e:
        return f"[Gemini unavailable: {str(e)[:100]}]"

if OLLAMA_AVAILABLE:
    LLM_FUNCTIONS = {'Claude': ask_claude, 'ChatGPT': ask_chatgpt, 'Gemini': ask_gemini, 'Ollama': ask_ollama}
    LLM_LIST = ['Claude', 'ChatGPT', 'Gemini', 'Ollama']
else:
    LLM_FUNCTIONS = {'Claude': ask_claude, 'ChatGPT': ask_chatgpt, 'Gemini': ask_gemini, 'Haiku': ask_claude_haiku}
    LLM_LIST = ['Claude', 'ChatGPT', 'Gemini', 'Haiku']

st.set_page_config(page_title="Aderit Conference Room", page_icon="🏢", layout="wide")

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

roles = load_roles_from_db()
room_assignments = load_room_assignments()
discussions = load_discussions()

with st.sidebar:
    st.title("🏢 Conference Room")
    if OLLAMA_AVAILABLE:
        st.success("🖥️ Local mode")
    else:
        st.info("☁️ Cloud mode")
    
    tab1, tab2, tab3 = st.tabs(["👥 Room", "📚 Roles", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### Who's in the room?")
        role_options = {k: f"{v['emoji']} {v['name']}" for k, v in roles.items()}
        role_keys = list(role_options.keys())
        for llm in LLM_LIST:
            current = room_assignments.get(llm, role_keys[0] if role_keys else None)
            current_idx = role_keys.index(current) if current in role_keys else 0
            selected = st.selectbox(f"**{llm}**", role_keys, index=current_idx, format_func=lambda x: role_options.get(x, x), key=f"assign_{llm}")
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
            new_category = st.selectbox("Category:", ["Internal - Executive", "Internal - Marketing", "Internal - Operations", "Client - Executive", "Client - HR Operations", "Client - IT", "Other"])
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

st.title("🏢 Aderit Conference Room")
room_display = " | ".join([f"{roles.get(room_assignments.get(llm, ''), {}).get('emoji', '👤')} {roles.get(room_assignments.get(llm, ''), {}).get('name', 'Unknown')}" for llm in LLM_LIST])
st.markdown(f"**In the room:** {room_display}")
st.markdown("---")

st.markdown("### 📜 Recent Discussions")
for d in discussions[:10]:
    with st.expander(f"{d['created_at'][:10]} - {(d.get('topic') or 'Untitled')[:60]}"):
        st.markdown(f"**Participants:** {', '.join(d.get('participants') or [])}")
        st.markdown(f"**Synthesis:** {d.get('synthesis', 'N/A')}")
        st.markdown(f"**Key Decisions:** {d.get('key_decisions', 'N/A')}")

st.markdown("---")

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
        participants.append({'llm': llm, 'role_key': role_key, 'name': role.get('name', 'Unknown'), 'emoji': role.get('emoji', '👤'), 'description': role.get('description', ''), 'func': LLM_FUNCTIONS[llm]})
    
    with st.status("🎯 Discussion in progress...", expanded=True) as status:
        discussion_log = ""
        if memory_context:
            discussion_log += "## Referenced Past Discussions\n\n" + memory_context + "\n\n"
        
        st.write("**Round 1: Initial Perspectives**")
        r1_prompt = f'Darin says: "{user_input}"\n\nGive your perspective in 2-3 paragraphs.'
        responses_r1 = {}
        for p in participants:
            st.write(f"{p['emoji']} {p['name']} thinking...")
            responses_r1[p['llm']] = p['func'](r1_prompt, p['description'], memory_context)
        discussion_log += "## Round 1: Initial Perspectives\n\n"
        for p in participants:
            discussion_log += f"### {p['emoji']} {p['name']} ({p['llm']})\n{responses_r1[p['llm']]}\n\n"
        
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
        
        st.write("**Synthesizing...**")
        synth_prompt = f'Topic: "{user_input}"\n\nFinal recommendations:\n' + "\n".join([f"{p['name']}: {responses_r5[p['llm']]}" for p in participants]) + "\n\nSynthesize in 3-4 paragraphs: agreements, tensions, recommendations, next steps."
        synthesis = ask_claude(synth_prompt, "You are a neutral facilitator summarizing this discussion.", memory_context)
        
        decisions_prompt = f"List 3-5 key decisions as bullet points:\n\n{synthesis}"
        key_decisions = ask_claude(decisions_prompt, "Extract key decisions concisely.", None)
        
        discussion_log += "## Synthesis\n\n" + synthesis
        discussion_log += "\n\n## Key Decisions\n\n" + key_decisions
        
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
