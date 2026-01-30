import os
import streamlit as st
from datetime import datetime
import httpx
import base64

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
    with httpx.Client(timeout=30) as client:
        if method == "GET":
            response = client.get(url, headers=headers, params=params)
        elif method == "POST":
            response = client.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = client.patch(url, headers=headers, json=data, params=params)
        elif method == "DELETE":
            response = client.delete(url, headers=headers, params=params)
        if response.status_code >= 400:
            st.error(f"DB error: {response.status_code} - {response.text}")
            return None
        if response.text:
            return response.json()
        return []

# ============================================
# FILE HANDLING
# ============================================

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type
    content = ""
    try:
        if file_type == "text/plain" or uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
        elif file_type == "text/markdown" or uploaded_file.name.endswith('.md'):
            content = uploaded_file.read().decode('utf-8')
        elif file_type == "text/csv" or uploaded_file.name.endswith('.csv'):
            content = uploaded_file.read().decode('utf-8')
        elif file_type == "application/pdf" or uploaded_file.name.endswith('.pdf'):
            try:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                content = "\n".join([page.extract_text() or "" for page in reader.pages])
            except ImportError:
                content = "[PDF support requires pypdf]"
        elif uploaded_file.name.endswith('.docx'):
            try:
                import docx
                doc = docx.Document(uploaded_file)
                content = "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                content = "[DOCX support requires python-docx]"
        else:
            try:
                content = uploaded_file.read().decode('utf-8')
            except:
                content = f"[Cannot read file type: {file_type}]"
    except Exception as e:
        content = f"[Error reading file: {str(e)[:100]}]"
    return content

# ============================================
# PROJECT MANAGEMENT
# ============================================

def get_projects():
    result = supabase_request("GET", "projects", params={"select": "*", "order": "name.asc"})
    return result or []

def create_project(name, emoji="📁", description=""):
    result = supabase_request("POST", "projects", data={"name": name, "emoji": emoji, "description": description})
    if result and len(result) > 0:
        return result[0]["id"]
    return None

def update_project(project_id, updates):
    supabase_request("PATCH", "projects", data=updates, params={"id": f"eq.{project_id}"})

def delete_project(project_id):
    # First unassign all sessions from this project
    supabase_request("PATCH", "sessions", data={"project_id": None}, params={"project_id": f"eq.{project_id}"})
    supabase_request("DELETE", "projects", params={"id": f"eq.{project_id}"})

# ============================================
# SESSION MANAGEMENT
# ============================================

def get_sessions(project_id=None):
    params = {"select": "*", "order": "updated_at.desc", "limit": "100"}
    if project_id:
        params["project_id"] = f"eq.{project_id}"
    result = supabase_request("GET", "sessions", params=params)
    return result or []

def get_unassigned_sessions():
    result = supabase_request("GET", "sessions", params={"select": "*", "order": "updated_at.desc", "project_id": "is.null", "limit": "100"})
    return result or []

def create_session(name, project_id=None):
    data = {"name": name[:100], "status": "active"}
    if project_id:
        data["project_id"] = project_id
    result = supabase_request("POST", "sessions", data=data)
    if result and len(result) > 0:
        return result[0]["id"]
    return None

def update_session(session_id, updates):
    supabase_request("PATCH", "sessions", data=updates, params={"id": f"eq.{session_id}"})

def delete_session(session_id):
    supabase_request("DELETE", "messages", params={"session_id": f"eq.{session_id}"})
    supabase_request("DELETE", "sessions", params={"id": f"eq.{session_id}"})

def get_messages(session_id):
    result = supabase_request("GET", "messages", params={
        "select": "*",
        "session_id": f"eq.{session_id}",
        "order": "created_at.asc"
    })
    return result or []

def add_message(session_id, role, content, llm_name=None, persona_name=None, persona_emoji=None, round_num=None, message_type="discussion"):
    supabase_request("POST", "messages", data={
        "session_id": session_id,
        "role": role,
        "llm_name": llm_name,
        "persona_name": persona_name,
        "persona_emoji": persona_emoji,
        "content": content,
        "round_num": round_num,
        "message_type": message_type
    })

# ============================================
# ROLES
# ============================================

DEFAULT_ROLES = {
    "positioning_strategist": {"name": "Positioning Strategist", "emoji": "🎯", "category": "Internal - Marketing", "description": "You are the Positioning Strategist. Background: Led positioning for enterprise SaaS including category-creation plays. Studied under April Dunford. Expertise: Why us, why now, category creation, strategic narrative. Style: Strategic, precise, obsessed with differentiation."},
    "copywriter": {"name": "Copywriter", "emoji": "✍️", "category": "Internal - Marketing", "description": "You are the Copywriter. Background: 15 years B2B enterprise copy for Salesforce, Workday, HR tech startups. Expertise: Headlines, website copy, sales decks, one-pagers. Style: Direct, punchy, allergic to jargon."},
    "creative_director": {"name": "Creative Director", "emoji": "🎨", "category": "Internal - Marketing", "description": "You are the Creative Director. Background: Former agency creative lead for enterprise tech brands. Rebranded B2B companies from boring to memorable. Expertise: Brand voice, emotional resonance, differentiation. Style: Creative, provocative, hates forgettable."},
    "buyer_researcher": {"name": "Buyer Researcher", "emoji": "👥", "category": "Internal - Marketing", "description": "You are the Buyer Researcher. Background: Former head of customer research at Gong. Conducted hundreds of buyer interviews. Expertise: Buyer pain language, objections, purchase triggers. Style: Grounded, evidence-based, customer-focused."},
    "ceo": {"name": "CEO Advisor", "emoji": "👔", "category": "Internal - Executive", "description": "You are the CEO Advisor. Background: Founded and sold HR data integration company for $185M. Expertise: Strategy, fundraising, M&A, board management, exit timing. Style: Strategic, sees whole board."},
    "cro": {"name": "CRO Advisor", "emoji": "💼", "category": "Internal - Executive", "description": "You are the CRO Advisor. Background: Former VP Sales at Ceridian, $8M to $80M+ ARR. Expertise: Enterprise sales, hiring, pricing, procurement. Style: Direct, numbers-driven."},
    "chro": {"name": "CHRO (Prospect)", "emoji": "👩‍💼", "category": "Client - Executive", "description": "You are a CHRO at Fortune 500, 15K employees. Situation: 12+ disconnected HR systems, 40% time on data reconciliation. Concerns: Integration complexity, change management, ROI proof, vendor stability. Style: Strategic but practical, been burned before."},
    "cfo_prospect": {"name": "CFO (Prospect)", "emoji": "💰", "category": "Client - Executive", "description": "You are a CFO at $500M company evaluating HR tech. Situation: CHRO wants transformation budget but you've seen IT projects fail. Concerns: TCO, timeline, productivity gains, contract terms. Style: Skeptical, numbers-focused."},
    "talent_acquisition_director": {"name": "Director of Talent Acquisition", "emoji": "🎯", "category": "Client - HR Operations", "description": "You are Director of TA at fast-growing tech company. Situation: ATS and HRIS don't connect, drowning in spreadsheets. Pain: Manual entry, duplicates, slow hiring, poor reporting. Style: Pragmatic, needs solutions NOW."},
    "hr_ops_manager": {"name": "HR Operations Manager", "emoji": "⚙️", "category": "Client - HR Operations", "description": "You are HR Ops Manager at 3K employee company. Situation: You make HR systems work together, fixing data errors daily. Pain: Inconsistencies, manual reporting, compliance anxiety. Style: Detail-oriented, cautious."},
    "it_director": {"name": "IT Director", "emoji": "💻", "category": "Client - IT", "description": "You are IT Director for enterprise apps. Situation: HR bought 15 point solutions without consulting you. Concerns: Security, compliance, APIs, SSO, SLAs. Style: Technical, risk-averse."},
    "facilitator": {"name": "Facilitator", "emoji": "🎤", "category": "Internal - Operations", "description": "You are a neutral facilitator. Role: Keep discussion productive, summarize, identify agreement/disagreement, drive conclusions. Style: Neutral, organized, outcome-focused."}
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
    message = claude_client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_claude_haiku(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(model="claude-3-5-haiku-20241022", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_chatgpt(prompt, role_description, memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    response = openai_client.chat.completions.create(model="gpt-4o", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
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

ROUND_PROMPTS = {
    1: ("Initial Perspectives", 'Darin says: "{question}"\n\nGive your perspective in 2-3 paragraphs.'),
    2: ("React & Debate", 'Topic: "{question}"\n\nPrevious discussion:\n{previous}\n\nReact: agreements, pushback, questions.'),
    3: ("Specific Proposals", 'Topic: "{question}"\n\nDiscussion so far:\n{previous}\n\nPropose 2-3 specific ideas.'),
    4: ("Critique & Refine", 'Topic: "{question}"\n\nProposals:\n{previous}\n\nWhich ideas have merit? Start converging.'),
    5: ("Final Recommendations", 'Topic: "{question}"\n\nFull discussion:\n{previous}\n\nFinal recommendation.'),
}

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(page_title="Aderit Conference Room", page_icon="🏢", layout="wide")

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "current_project_id" not in st.session_state:
    st.session_state.current_project_id = None
if "enabled_llms" not in st.session_state:
    st.session_state.enabled_llms = LLM_LIST.copy()
if "num_rounds" not in st.session_state:
    st.session_state.num_rounds = 5
if "file_context" not in st.session_state:
    st.session_state.file_context = ""
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = ""

roles = load_roles_from_db()
room_assignments = load_room_assignments()

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.title("🏢 Conference Room")
    
    # New Chat button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_session_id = None
        st.session_state.file_context = ""
        st.session_state.uploaded_filename = ""
        st.rerun()
    
    st.markdown("---")
    
    # File upload
    st.markdown("### 📎 Upload Context")
    uploaded_file = st.file_uploader("Add file", type=['txt', 'md', 'csv', 'pdf', 'docx'], key="file_uploader", label_visibility="collapsed")
    
    if uploaded_file:
        if uploaded_file.name != st.session_state.uploaded_filename:
            with st.spinner("Reading..."):
                content = extract_text_from_file(uploaded_file)
                st.session_state.file_context = content
                st.session_state.uploaded_filename = uploaded_file.name
            st.success(f"✓ {uploaded_file.name[:20]}")
    
    if st.session_state.file_context:
        st.caption(f"📄 {st.session_state.uploaded_filename[:20]}")
        if st.button("✕ Clear", key="clear_file"):
            st.session_state.file_context = ""
            st.session_state.uploaded_filename = ""
            st.rerun()
    
    st.markdown("---")
    
    # Projects and Chats
    st.markdown("### 📂 Projects")
    
    projects = get_projects()
    
    # Add project button
    with st.expander("➕ New Project"):
        new_proj_name = st.text_input("Name", key="new_proj_name")
        new_proj_emoji = st.text_input("Emoji", value="📁", key="new_proj_emoji")
        if st.button("Create Project", key="create_proj"):
            if new_proj_name:
                create_project(new_proj_name, new_proj_emoji)
                st.rerun()
    
    # Show projects with their chats
    for proj in projects:
        proj_sessions = get_sessions(proj["id"])
        is_current_proj = st.session_state.current_project_id == proj["id"]
        
        with st.expander(f"{proj.get('emoji', '📁')} {proj['name']} ({len(proj_sessions)})", expanded=is_current_proj):
            # Project actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝", key=f"edit_proj_{proj['id']}", help="Rename"):
                    st.session_state[f"editing_proj_{proj['id']}"] = True
            with col2:
                if st.button("🗑️", key=f"del_proj_{proj['id']}", help="Delete"):
                    delete_project(proj["id"])
                    st.rerun()
            
            # Edit project name
            if st.session_state.get(f"editing_proj_{proj['id']}"):
                new_name = st.text_input("New name", value=proj["name"], key=f"rename_proj_{proj['id']}")
                if st.button("Save", key=f"save_proj_{proj['id']}"):
                    update_project(proj["id"], {"name": new_name})
                    st.session_state[f"editing_proj_{proj['id']}"] = False
                    st.rerun()
            
            # Sessions in this project
            for sess in proj_sessions:
                sess_name = sess["name"][:25] + "..." if len(sess["name"]) > 25 else sess["name"]
                is_current = st.session_state.current_session_id == sess["id"]
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"{'▶ ' if is_current else ''}{sess_name}", key=f"sess_{sess['id']}", use_container_width=True):
                        st.session_state.current_session_id = sess["id"]
                        st.session_state.current_project_id = proj["id"]
                        st.rerun()
                with col2:
                    if st.button("⚙️", key=f"cfg_{sess['id']}"):
                        st.session_state[f"editing_sess_{sess['id']}"] = True
                
                # Edit session
                if st.session_state.get(f"editing_sess_{sess['id']}"):
                    new_sess_name = st.text_input("Rename", value=sess["name"], key=f"rename_{sess['id']}")
                    move_to = st.selectbox("Move to", ["(Unassigned)"] + [p["name"] for p in projects], key=f"move_{sess['id']}")
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("💾", key=f"save_sess_{sess['id']}"):
                            updates = {"name": new_sess_name}
                            if move_to == "(Unassigned)":
                                updates["project_id"] = None
                            else:
                                target_proj = next((p for p in projects if p["name"] == move_to), None)
                                if target_proj:
                                    updates["project_id"] = target_proj["id"]
                            update_session(sess["id"], updates)
                            st.session_state[f"editing_sess_{sess['id']}"] = False
                            st.rerun()
                    with c2:
                        if st.button("❌", key=f"cancel_{sess['id']}"):
                            st.session_state[f"editing_sess_{sess['id']}"] = False
                            st.rerun()
                    with c3:
                        if st.button("🗑️", key=f"del_sess_{sess['id']}"):
                            delete_session(sess["id"])
                            if st.session_state.current_session_id == sess["id"]:
                                st.session_state.current_session_id = None
                            st.rerun()
    
    # Unassigned chats
    unassigned = get_unassigned_sessions()
    if unassigned:
        with st.expander(f"📋 Unassigned ({len(unassigned)})", expanded=True):
            for sess in unassigned[:20]:
                sess_name = sess["name"][:25] + "..." if len(sess["name"]) > 25 else sess["name"]
                is_current = st.session_state.current_session_id == sess["id"]
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"{'▶ ' if is_current else ''}{sess_name}", key=f"sess_{sess['id']}", use_container_width=True):
                        st.session_state.current_session_id = sess["id"]
                        st.session_state.current_project_id = None
                        st.rerun()
                with col2:
                    if st.button("⚙️", key=f"cfg_{sess['id']}"):
                        st.session_state[f"editing_sess_{sess['id']}"] = True
                
                if st.session_state.get(f"editing_sess_{sess['id']}"):
                    new_sess_name = st.text_input("Rename", value=sess["name"], key=f"rename_{sess['id']}")
                    move_to = st.selectbox("Move to", ["(Unassigned)"] + [p["name"] for p in projects], key=f"move_{sess['id']}")
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("💾", key=f"save_sess_{sess['id']}"):
                            updates = {"name": new_sess_name}
                            if move_to != "(Unassigned)":
                                target_proj = next((p for p in projects if p["name"] == move_to), None)
                                if target_proj:
                                    updates["project_id"] = target_proj["id"]
                            update_session(sess["id"], updates)
                            st.session_state[f"editing_sess_{sess['id']}"] = False
                            st.rerun()
                    with c2:
                        if st.button("❌", key=f"cancel_{sess['id']}"):
                            st.session_state[f"editing_sess_{sess['id']}"] = False
                            st.rerun()
                    with c3:
                        if st.button("🗑️", key=f"del_sess_{sess['id']}"):
                            delete_session(sess["id"])
                            if st.session_state.current_session_id == sess["id"]:
                                st.session_state.current_session_id = None
                            st.rerun()
    
    st.markdown("---")
    
    # Tabs for config
    tab1, tab2, tab3 = st.tabs(["👥", "📚", "⚙️"])
    
    with tab1:
        st.markdown("### Participants")
        role_options = {k: f"{v['emoji']} {v['name']}" for k, v in roles.items()}
        role_keys = list(role_options.keys())
        
        enabled_llms = []
        for llm in LLM_LIST:
            col_check, col_select = st.columns([1, 3])
            with col_check:
                enabled = st.checkbox("", value=llm in st.session_state.enabled_llms, key=f"enable_{llm}", label_visibility="collapsed")
            with col_select:
                current = room_assignments.get(llm, role_keys[0] if role_keys else None)
                current_idx = role_keys.index(current) if current in role_keys else 0
                selected = st.selectbox(llm, role_keys, index=current_idx, format_func=lambda x: role_options.get(x, x), key=f"assign_{llm}", disabled=not enabled, label_visibility="collapsed")
                if selected != room_assignments.get(llm):
                    save_room_assignment(llm, selected)
                    room_assignments[llm] = selected
            if enabled:
                enabled_llms.append(llm)
        
        st.session_state.enabled_llms = enabled_llms
    
    with tab2:
        st.markdown("### Roles")
        categories = sorted(set(r.get('category', 'Uncategorized') for r in roles.values()))
        selected_category = st.selectbox("Filter:", ["All"] + categories, key="role_filter")
        for role_key, role in roles.items():
            if selected_category != "All" and role.get('category') != selected_category:
                continue
            with st.expander(f"{role.get('emoji', '👤')} {role.get('name', role_key)}"):
                st.caption(role.get('description', '')[:150] + "...")
                if st.button("🗑️", key=f"del_{role_key}"):
                    delete_role_from_db(role_key)
                    st.rerun()
        
        with st.expander("➕ New Role"):
            new_name = st.text_input("Name:", key="new_role_name")
            new_emoji = st.text_input("Emoji:", value="👤", key="new_role_emoji")
            new_cat = st.selectbox("Category:", ["Internal - Marketing", "Internal - Executive", "Client - Executive", "Client - HR Operations", "Client - IT", "Other"], key="new_role_cat")
            new_desc = st.text_area("Description:", key="new_role_desc", height=80)
            if st.button("Create", key="create_role"):
                if new_name and new_desc:
                    save_role_to_db(new_name.lower().replace(" ", "_"), new_name, new_emoji, new_cat, new_desc)
                    st.rerun()
    
    with tab3:
        st.markdown("### Settings")
        st.session_state.num_rounds = st.slider("Rounds", 1, 5, st.session_state.num_rounds)
        
        if OLLAMA_AVAILABLE:
            st.success("🖥️ Local")
        else:
            st.info("☁️ Cloud")
        
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()

# ============================================
# MAIN AREA
# ============================================

col1, col2 = st.columns([5, 1])
with col1:
    st.title("🏢 Aderit Conference Room")
with col2:
    if st.button("🔄 Sync"):
        st.rerun()

enabled_llms = st.session_state.enabled_llms
if enabled_llms:
    room_display = " | ".join([f"{roles.get(room_assignments.get(llm, ''), {}).get('emoji', '👤')} {roles.get(room_assignments.get(llm, ''), {}).get('name', '?')}" for llm in enabled_llms])
    st.caption(f"**Room:** {room_display} · {st.session_state.num_rounds} rounds")

if st.session_state.file_context:
    st.info(f"📎 Context: {st.session_state.uploaded_filename}")

st.markdown("---")

# Display current session
current_session_id = st.session_state.current_session_id
synthesis_content = ""
full_discussion = ""

if current_session_id:
    messages = get_messages(current_session_id)
    
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 Darin:** {msg['content']}")
            full_discussion += f"## User Question\n\n{msg['content']}\n\n"
        elif msg["role"] == "context":
            st.info(f"📎 File context: {msg.get('persona_name', 'file')}")
            full_discussion += f"## File Context\n\n{msg['content'][:500]}...\n\n"
        elif msg["role"] == "participant":
            with st.expander(f"{msg.get('persona_emoji', '👤')} {msg.get('persona_name', 'Unknown')} ({msg.get('llm_name', '?')}) — Round {msg.get('round_num', '?')}", expanded=False):
                st.markdown(msg["content"])
            full_discussion += f"### {msg.get('persona_name', 'Unknown')} (Round {msg.get('round_num', '?')})\n\n{msg['content']}\n\n"
        elif msg["role"] == "synthesis":
            st.markdown("### 📋 Synthesis")
            st.markdown(msg["content"])
            synthesis_content = msg["content"]
            full_discussion += f"## Synthesis\n\n{msg['content']}\n\n"
        elif msg["role"] == "decisions":
            st.markdown("### 🔑 Key Decisions")
            st.markdown(msg["content"])
            full_discussion += f"## Key Decisions\n\n{msg['content']}\n\n"
        elif msg["role"] == "deliverable":
            st.markdown("### 📄 Generated Deliverable")
            st.markdown(msg["content"])
            st.download_button("⬇️ Download", msg["content"], file_name=f"{msg.get('persona_name', 'output')}.md", mime="text/markdown")
    
    if full_discussion:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Export Discussion", full_discussion, file_name="discussion.md", mime="text/markdown")
        with col2:
            if synthesis_content:
                st.download_button("⬇️ Export Synthesis", synthesis_content, file_name="synthesis.md", mime="text/markdown")
else:
    st.markdown("### Start a new discussion")
    st.markdown("Type your topic below, or upload a file first for context.")

st.markdown("---")

def is_file_request(text):
    keywords = ["create a file", "create a markdown", "generate a file", "write a file", 
                "create a prompt", "generate a prompt", "make a file", "write a markdown",
                "create a document", "generate a document", "create the prompt", "write the prompt"]
    return any(kw in text.lower() for kw in keywords)

user_input = st.chat_input("What would you like to discuss?")

if user_input:
    if not enabled_llms:
        st.error("Select at least one participant.")
    else:
        if not current_session_id:
            current_session_id = create_session(user_input[:100], st.session_state.current_project_id)
            st.session_state.current_session_id = current_session_id
        
        add_message(current_session_id, "user", user_input)
        
        file_context = st.session_state.file_context
        if file_context:
            add_message(current_session_id, "context", file_context[:10000], persona_name=st.session_state.uploaded_filename)
        
        memory_context = ""
        if file_context:
            memory_context = f"## UPLOADED FILE CONTEXT ({st.session_state.uploaded_filename}):\n\n{file_context[:8000]}\n\n"
        
        participants = []
        for llm in enabled_llms:
            role_key = room_assignments.get(llm, "")
            role = roles.get(role_key, {})
            participants.append({
                'llm': llm,
                'name': role.get('name', 'Unknown'),
                'emoji': role.get('emoji', '👤'),
                'description': role.get('description', ''),
                'func': LLM_FUNCTIONS[llm]
            })
        
        num_rounds = st.session_state.num_rounds
        wants_file = is_file_request(user_input)
        
        st.markdown(f"**🧑 Darin:** {user_input}")
        if file_context:
            st.info(f"📎 Using: {st.session_state.uploaded_filename}")
        
        with st.status(f"🎯 {len(participants)} participants, {num_rounds} rounds...", expanded=True) as status:
            all_responses = {}
            previous_text = ""
            
            for round_num in range(1, num_rounds + 1):
                round_name, prompt_template = ROUND_PROMPTS[round_num]
                st.write(f"**Round {round_num}: {round_name}**")
                
                if round_num == 1:
                    prompt = prompt_template.format(question=user_input)
                else:
                    prompt = prompt_template.format(question=user_input, previous=previous_text)
                
                responses = {}
                for p in participants:
                    st.write(f"{p['emoji']} {p['name']}...")
                    response = p['func'](prompt, p['description'], memory_context)
                    responses[p['llm']] = response
                    add_message(current_session_id, "participant", response, 
                               llm_name=p['llm'], persona_name=p['name'], 
                               persona_emoji=p['emoji'], round_num=round_num)
                
                all_responses[round_num] = responses
                previous_text = "\n\n".join([f"{p['name']}: {responses[p['llm']]}" for p in participants])
            
            st.write("**Synthesizing...**")
            final_responses = all_responses[num_rounds]
            synth_prompt = f'Topic: "{user_input}"\n\nFinal perspectives:\n' + "\n".join([f"{p['name']}: {final_responses[p['llm']]}" for p in participants]) + "\n\nSynthesize in 3-4 paragraphs: agreements, tensions, recommendations, next steps."
            synthesis = ask_claude(synth_prompt, "You are a neutral facilitator summarizing this discussion.", memory_context)
            add_message(current_session_id, "synthesis", synthesis)
            
            decisions_prompt = f"List 3-5 key decisions as bullet points:\n\n{synthesis}"
            key_decisions = ask_claude(decisions_prompt, "Extract key decisions concisely.", None)
            add_message(current_session_id, "decisions", key_decisions)
            
            if wants_file:
                st.write("**Generating deliverable...**")
                file_gen_prompt = f"""Based on this discussion, create the requested deliverable.

ORIGINAL REQUEST: {user_input}

DISCUSSION SYNTHESIS:
{synthesis}

KEY DECISIONS:
{key_decisions}

FULL DISCUSSION:
{previous_text[:4000]}

Create the actual deliverable. Output ONLY the file content - no explanations."""
                
                deliverable = ask_claude(file_gen_prompt, "You create professional deliverables. Output only file content.", memory_context)
                
                filename = "deliverable"
                if "lovable" in user_input.lower():
                    filename = "lovable_prompt"
                elif "website" in user_input.lower():
                    filename = "website_spec"
                elif "prompt" in user_input.lower():
                    filename = "prompt"
                
                add_message(current_session_id, "deliverable", deliverable, persona_name=filename)
            
            update_session(current_session_id, {"status": "complete", "updated_at": datetime.now().isoformat()})
            status.update(label="✅ Complete!", state="complete")
        
        st.markdown("### 📋 Synthesis")
        st.markdown(synthesis)
        st.markdown("### 🔑 Key Decisions")
        st.markdown(key_decisions)
        
        if wants_file:
            st.markdown("### 📄 Deliverable")
            st.markdown(deliverable)
            st.download_button("⬇️ Download", deliverable, file_name=f"{filename}.md", mime="text/markdown")
        
        st.rerun()
