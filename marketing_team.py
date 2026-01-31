import os
import streamlit as st
from datetime import datetime
import httpx
import json
import concurrent.futures

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
    with httpx.Client(timeout=60) as client:
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
# FILE / DOCUMENT HANDLING
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

def get_documents(session_id):
    result = supabase_request("GET", "documents", params={
        "select": "*",
        "session_id": f"eq.{session_id}",
        "order": "created_at.asc"
    })
    return result or []

def save_document(session_id, name, content, doc_type="output"):
    result = supabase_request("POST", "documents", data={
        "session_id": session_id,
        "name": name,
        "doc_type": doc_type,
        "content": content
    })
    return result[0] if result else None

def delete_document(doc_id):
    supabase_request("DELETE", "documents", params={"id": f"eq.{doc_id}"})

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

def create_session(name, project_id=None, mode="panel", facilitator_llm="Claude"):
    data = {"name": name[:100], "status": "active", "mode": mode, "facilitator_llm": facilitator_llm}
    if project_id:
        data["project_id"] = project_id
    result = supabase_request("POST", "sessions", data=data)
    if result and len(result) > 0:
        return result[0]["id"]
    return None

def update_session(session_id, updates):
    supabase_request("PATCH", "sessions", data=updates, params={"id": f"eq.{session_id}"})

def delete_session(session_id):
    supabase_request("DELETE", "documents", params={"session_id": f"eq.{session_id}"})
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

def ask_ollama(prompt, role_description="", memory_context=None):
    if not OLLAMA_AVAILABLE:
        return "[Ollama not available in cloud mode]"
    context = role_description + "\n" + COMPANY_CONTEXT if role_description else COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    try:
        response = ollama_client.chat(model='qwen2.5:7b', messages=[{'role': 'user', 'content': f"{context}\n\n{prompt}"}])
        return response['message']['content']
    except Exception as e:
        return f"[Ollama error: {str(e)[:100]}]"

def ask_claude(prompt, role_description="", memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT if role_description else COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_claude_haiku(prompt, role_description="", memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT if role_description else COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    message = claude_client.messages.create(model="claude-3-5-haiku-20241022", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return message.content[0].text

def ask_chatgpt(prompt, role_description="", memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT if role_description else COMPANY_CONTEXT
    if memory_context:
        context += "\n\n" + memory_context
    response = openai_client.chat.completions.create(model="gpt-4o", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
    return response.choices[0].message.content

def ask_gemini(prompt, role_description="", memory_context=None):
    context = role_description + "\n" + COMPANY_CONTEXT if role_description else COMPANY_CONTEXT
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
# FACILITATOR MODES
# ============================================

def run_panel_discussion(user_input, participants, num_rounds, memory_context, session_id, status_container):
    """Original panel discussion - all LLMs talk in rounds"""
    all_responses = {}
    previous_text = ""
    
    for round_num in range(1, num_rounds + 1):
        round_name, prompt_template = ROUND_PROMPTS[round_num]
        status_container.write(f"**Round {round_num}: {round_name}**")
        
        if round_num == 1:
            prompt = prompt_template.format(question=user_input)
        else:
            prompt = prompt_template.format(question=user_input, previous=previous_text)
        
        responses = {}
        for p in participants:
            status_container.write(f"{p['emoji']} {p['name']}...")
            response = p['func'](prompt, p['description'], memory_context)
            responses[p['llm']] = response
            add_message(session_id, "participant", response, 
                       llm_name=p['llm'], persona_name=p['name'], 
                       persona_emoji=p['emoji'], round_num=round_num)
        
        all_responses[round_num] = responses
        previous_text = "\n\n".join([f"{p['name']}: {responses[p['llm']]}" for p in participants])
    
    return all_responses, previous_text

def run_conversational_mode(user_input, participants, facilitator_llm, memory_context, session_id, status_container, documents):
    """Facilitator orchestrates, calling LLMs one at a time"""
    
    # Build context about available team members
    team_info = "AVAILABLE TEAM MEMBERS:\n"
    for p in participants:
        team_info += f"- {p['name']} ({p['llm']}): {p['description'][:200]}...\n"
    
    # Build document context
    doc_info = ""
    if documents:
        doc_info = "\nAVAILABLE DOCUMENTS:\n"
        for doc in documents:
            doc_info += f"- {doc['name']} ({doc['doc_type']}): {doc['content'][:200]}...\n"
    
    facilitator_func = LLM_FUNCTIONS[facilitator_llm]
    conversation_log = []
    max_turns = 10
    
    # Initial facilitator planning
    plan_prompt = f"""{team_info}{doc_info}

USER REQUEST: {user_input}

You are the facilitator. Analyze this request and plan your approach:
1. Who should you consult first and why?
2. What specific question will you ask them?

Respond in this JSON format:
{{"plan": "your overall plan", "first_call": {{"llm": "LLM name", "question": "specific question to ask"}}}}
"""
    
    status_container.write("**🎯 Facilitator planning...**")
    plan_response = facilitator_func(plan_prompt, "You are a skilled facilitator orchestrating a team discussion.", memory_context)
    add_message(session_id, "facilitator", plan_response, llm_name=facilitator_llm, persona_name="Facilitator", persona_emoji="🎯")
    conversation_log.append(f"Facilitator Plan: {plan_response}")
    
    # Try to parse the plan
    try:
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', plan_response, re.DOTALL)
        if json_match:
            plan_data = json.loads(json_match.group())
        else:
            plan_data = {"first_call": {"llm": participants[0]['llm'], "question": user_input}}
    except:
        plan_data = {"first_call": {"llm": participants[0]['llm'], "question": user_input}}
    
    turn = 0
    while turn < max_turns:
        turn += 1
        
        # Get the next call from facilitator's plan
        if turn == 1:
            next_call = plan_data.get("first_call", {})
            target_llm = next_call.get("llm", participants[0]['llm'])
            question = next_call.get("question", user_input)
        else:
            # Ask facilitator what to do next
            next_prompt = f"""CONVERSATION SO FAR:
{chr(10).join(conversation_log[-6:])}

Based on the responses so far, decide your next action:
1. Call another team member for input
2. Ask follow-up to same person
3. Conclude and synthesize

Respond in JSON:
{{"action": "call|followup|conclude", "llm": "LLM name if calling", "question": "question to ask", "reason": "why this action"}}
"""
            status_container.write("**🎯 Facilitator deciding next step...**")
            next_response = facilitator_func(next_prompt, "You are a skilled facilitator.", memory_context)
            
            try:
                json_match = re.search(r'\{.*\}', next_response, re.DOTALL)
                if json_match:
                    next_data = json.loads(json_match.group())
                else:
                    next_data = {"action": "conclude"}
            except:
                next_data = {"action": "conclude"}
            
            if next_data.get("action") == "conclude":
                status_container.write("**🎯 Facilitator concluding...**")
                break
            
            target_llm = next_data.get("llm", participants[0]['llm'])
            question = next_data.get("question", "Please provide your thoughts.")
            conversation_log.append(f"Facilitator: {next_data.get('reason', 'Continuing discussion')}")
        
        # Find the participant
        target_participant = next((p for p in participants if p['llm'] == target_llm), participants[0])
        
        status_container.write(f"**{target_participant['emoji']} Asking {target_participant['name']}...**")
        
        # Call the target LLM
        full_question = f"Context: {user_input}\n\nQuestion from facilitator: {question}"
        response = target_participant['func'](full_question, target_participant['description'], memory_context)
        
        add_message(session_id, "participant", response, 
                   llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                   persona_emoji=target_participant['emoji'], round_num=turn)
        
        conversation_log.append(f"{target_participant['name']}: {response}")
        
        # Quality check
        quality_prompt = f"""The {target_participant['name']} responded:
{response[:1000]}

Is this response:
1. HIGH QUALITY - useful, on-topic, actionable
2. NEEDS RETRY - unclear, off-topic, or insufficient

Respond with just "HIGH QUALITY" or "NEEDS RETRY: reason"
"""
        quality_check = facilitator_func(quality_prompt, "You evaluate response quality.", None)
        
        if "NEEDS RETRY" in quality_check and turn < max_turns - 1:
            status_container.write(f"**🔄 Facilitator requesting revision...**")
            retry_prompt = f"Your previous response needs improvement. {quality_check}\n\nOriginal question: {question}\n\nPlease try again with more detail and clarity."
            response = target_participant['func'](retry_prompt, target_participant['description'], memory_context)
            add_message(session_id, "participant", f"[Revised] {response}", 
                       llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                       persona_emoji=target_participant['emoji'], round_num=turn)
            conversation_log[-1] = f"{target_participant['name']} (revised): {response}"
    
    return conversation_log

def run_dispatcher_mode(user_input, participants, facilitator_llm, memory_context, session_id, status_container, documents, file_content=None):
    """Facilitator breaks work into chunks and dispatches in parallel"""
    
    facilitator_func = LLM_FUNCTIONS[facilitator_llm]
    
    # Build context about available team members
    team_info = "AVAILABLE WORKERS:\n"
    for p in participants:
        team_info += f"- {p['name']} ({p['llm']})\n"
    
    # Check if we have CSV/spreadsheet data
    is_spreadsheet = file_content and (',' in file_content[:500] or '\t' in file_content[:500])
    
    if is_spreadsheet:
        # Parse rows for distribution
        lines = file_content.strip().split('\n')
        header = lines[0] if lines else ""
        data_rows = lines[1:] if len(lines) > 1 else []
        
        dispatch_prompt = f"""{team_info}

USER REQUEST: {user_input}

SPREADSHEET DATA:
- Header: {header}
- Total rows: {len(data_rows)}

Divide this work among the available workers. Assign roughly equal chunks.

Respond in JSON format:
{{"tasks": [
    {{"llm": "LLM name", "start_row": 0, "end_row": 25, "instruction": "specific instruction"}},
    ...
]}}
"""
    else:
        dispatch_prompt = f"""{team_info}

USER REQUEST: {user_input}

CONTEXT:
{memory_context[:2000] if memory_context else 'No additional context'}

Break this work into parallel tasks for the available workers. Each worker should get a distinct piece of work.

Respond in JSON format:
{{"tasks": [
    {{"llm": "LLM name", "task": "specific task description"}},
    ...
], "merge_instruction": "how to combine results"}}
"""
    
    status_container.write("**🎯 Facilitator planning work distribution...**")
    dispatch_response = facilitator_func(dispatch_prompt, "You are a skilled work dispatcher.", None)
    add_message(session_id, "facilitator", dispatch_response, llm_name=facilitator_llm, persona_name="Dispatcher", persona_emoji="🎯")
    
    # Parse dispatch plan
    try:
        import re
        json_match = re.search(r'\{.*\}', dispatch_response, re.DOTALL)
        if json_match:
            dispatch_plan = json.loads(json_match.group())
        else:
            # Fallback: distribute evenly
            dispatch_plan = {"tasks": [{"llm": p['llm'], "task": user_input} for p in participants]}
    except:
        dispatch_plan = {"tasks": [{"llm": p['llm'], "task": user_input} for p in participants]}
    
    tasks = dispatch_plan.get("tasks", [])
    merge_instruction = dispatch_plan.get("merge_instruction", "Combine all results into a single coherent output.")
    
    status_container.write(f"**📤 Dispatching {len(tasks)} tasks in parallel...**")
    
    results = []
    
    # Execute tasks (could be parallel with ThreadPoolExecutor, but keeping simple for now)
    for i, task in enumerate(tasks):
        target_llm = task.get("llm", participants[0]['llm'])
        target_participant = next((p for p in participants if p['llm'] == target_llm), participants[0])
        
        if is_spreadsheet and "start_row" in task:
            # Spreadsheet task
            start = task.get("start_row", 0)
            end = task.get("end_row", len(data_rows))
            chunk_rows = data_rows[start:end]
            chunk_data = header + "\n" + "\n".join(chunk_rows)
            
            task_prompt = f"""TASK: {task.get('instruction', user_input)}

DATA (rows {start+1} to {end}):
{chunk_data}

Process this data according to the instruction. Output your results clearly."""
        else:
            task_prompt = f"""TASK: {task.get('task', user_input)}

{memory_context if memory_context else ''}

Complete this task thoroughly."""
        
        status_container.write(f"**{target_participant['emoji']} {target_participant['name']} working...**")
        
        response = target_participant['func'](task_prompt, target_participant['description'], None)
        
        add_message(session_id, "participant", response, 
                   llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                   persona_emoji=target_participant['emoji'], round_num=i+1,
                   message_type="dispatch_result")
        
        results.append({
            "llm": target_llm,
            "name": target_participant['name'],
            "result": response
        })
        
        # Quality check with retry
        quality_prompt = f"""Task result from {target_participant['name']}:
{response[:1000]}

Is this HIGH QUALITY or NEEDS RETRY?"""
        
        quality_check = facilitator_func(quality_prompt, "You evaluate work quality.", None)
        
        if "NEEDS RETRY" in quality_check:
            status_container.write(f"**🔄 Retrying {target_participant['name']}'s task...**")
            response = target_participant['func'](task_prompt + "\n\nPrevious attempt was insufficient. Please be more thorough.", target_participant['description'], None)
            results[-1]["result"] = response
            add_message(session_id, "participant", f"[Revised] {response}", 
                       llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                       persona_emoji=target_participant['emoji'], round_num=i+1)
    
    # Merge results
    status_container.write("**🎯 Facilitator merging results...**")
    
    merge_prompt = f"""ORIGINAL REQUEST: {user_input}

MERGE INSTRUCTION: {merge_instruction}

RESULTS FROM WORKERS:
"""
    for r in results:
        merge_prompt += f"\n--- {r['name']} ---\n{r['result']}\n"
    
    merge_prompt += "\n\nCombine these results into a single coherent output. If the user requested separate files, note that. Otherwise merge into one."
    
    merged_result = facilitator_func(merge_prompt, "You merge work results.", None)
    
    return results, merged_result

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
if "discussion_mode" not in st.session_state:
    st.session_state.discussion_mode = "panel"
if "facilitator_llm" not in st.session_state:
    st.session_state.facilitator_llm = "Claude"

roles = load_roles_from_db()
room_assignments = load_room_assignments()

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.title("🏢 Conference Room")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_session_id = None
        st.session_state.file_context = ""
        st.session_state.uploaded_filename = ""
        st.rerun()
    
    st.markdown("---")
    
    # Discussion Mode
    st.markdown("### 🎛️ Mode")
    st.session_state.discussion_mode = st.radio(
        "Discussion Mode",
        ["panel", "conversational", "dispatcher"],
        format_func=lambda x: {"panel": "👥 Panel Discussion", "conversational": "💬 Conversational", "dispatcher": "📤 Dispatcher"}[x],
        index=["panel", "conversational", "dispatcher"].index(st.session_state.discussion_mode),
        label_visibility="collapsed"
    )
    
    if st.session_state.discussion_mode != "panel":
        st.session_state.facilitator_llm = st.selectbox(
            "Facilitator",
            LLM_LIST,
            index=LLM_LIST.index(st.session_state.facilitator_llm) if st.session_state.facilitator_llm in LLM_LIST else 0
        )
    
    if st.session_state.discussion_mode == "panel":
        st.session_state.num_rounds = st.slider("Rounds", 1, 5, st.session_state.num_rounds)
    
    st.markdown("---")
    
    # File upload
    st.markdown("### 📎 Upload")
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
    
    # Projects
    st.markdown("### 📂 Projects")
    projects = get_projects()
    
    with st.expander("➕ New Project"):
        new_proj_name = st.text_input("Name", key="new_proj_name")
        new_proj_emoji = st.text_input("Emoji", value="📁", key="new_proj_emoji")
        if st.button("Create", key="create_proj"):
            if new_proj_name:
                create_project(new_proj_name, new_proj_emoji)
                st.rerun()
    
    for proj in projects:
        proj_sessions = get_sessions(proj["id"])
        is_current_proj = st.session_state.current_project_id == proj["id"]
        
        with st.expander(f"{proj.get('emoji', '📁')} {proj['name']} ({len(proj_sessions)})", expanded=is_current_proj):
            col1, col2 = st.columns(2)
            with col2:
                if st.button("🗑️", key=f"del_proj_{proj['id']}"):
                    delete_project(proj["id"])
                    st.rerun()
            
            for sess in proj_sessions:
                sess_name = sess["name"][:22] + "..." if len(sess["name"]) > 22 else sess["name"]
                is_current = st.session_state.current_session_id == sess["id"]
                
                if st.button(f"{'▶ ' if is_current else ''}{sess_name}", key=f"sess_{sess['id']}", use_container_width=True):
                    st.session_state.current_session_id = sess["id"]
                    st.session_state.current_project_id = proj["id"]
                    st.rerun()
    
    # Unassigned
    unassigned = get_unassigned_sessions()
    if unassigned:
        with st.expander(f"📋 Unassigned ({len(unassigned)})", expanded=True):
            for sess in unassigned[:15]:
                sess_name = sess["name"][:22] + "..." if len(sess["name"]) > 22 else sess["name"]
                is_current = st.session_state.current_session_id == sess["id"]
                
                if st.button(f"{'▶ ' if is_current else ''}{sess_name}", key=f"sess_{sess['id']}", use_container_width=True):
                    st.session_state.current_session_id = sess["id"]
                    st.session_state.current_project_id = None
                    st.rerun()
    
    st.markdown("---")
    
    # Participants tab
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
        for role_key, role in list(roles.items())[:8]:
            with st.expander(f"{role.get('emoji', '👤')} {role.get('name', role_key)[:15]}"):
                st.caption(role.get('description', '')[:100] + "...")
    
    with tab3:
        st.markdown("### Settings")
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

# Show mode and room
enabled_llms = st.session_state.enabled_llms
mode_display = {"panel": "👥 Panel", "conversational": "💬 Conversational", "dispatcher": "📤 Dispatcher"}[st.session_state.discussion_mode]

if enabled_llms:
    room_display = " | ".join([f"{roles.get(room_assignments.get(llm, ''), {}).get('emoji', '👤')} {roles.get(room_assignments.get(llm, ''), {}).get('name', '?')[:12]}" for llm in enabled_llms])
    st.caption(f"**Mode:** {mode_display} · **Room:** {room_display}")

if st.session_state.file_context:
    st.info(f"📎 {st.session_state.uploaded_filename}")

st.markdown("---")

# Document repository for current session
current_session_id = st.session_state.current_session_id

if current_session_id:
    documents = get_documents(current_session_id)
    
    if documents:
        with st.expander(f"📁 Documents ({len(documents)})", expanded=False):
            for doc in documents:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{'📥' if doc['doc_type'] == 'input' else '📤'} {doc['name']}")
                with col2:
                    st.download_button("⬇️", doc['content'], file_name=doc['name'], key=f"dl_{doc['id']}")
                with col3:
                    if st.button("🗑️", key=f"del_doc_{doc['id']}"):
                        delete_document(doc['id'])
                        st.rerun()
    
    # Display messages
    messages = get_messages(current_session_id)
    synthesis_content = ""
    
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 Darin:** {msg['content']}")
        elif msg["role"] == "facilitator":
            with st.expander(f"🎯 Facilitator ({msg.get('llm_name', '')})", expanded=False):
                st.markdown(msg["content"])
        elif msg["role"] == "participant":
            with st.expander(f"{msg.get('persona_emoji', '👤')} {msg.get('persona_name', 'Unknown')} ({msg.get('llm_name', '?')})", expanded=False):
                st.markdown(msg["content"])
        elif msg["role"] == "synthesis":
            st.markdown("### 📋 Synthesis")
            st.markdown(msg["content"])
            synthesis_content = msg["content"]
        elif msg["role"] == "decisions":
            st.markdown("### 🔑 Key Decisions")
            st.markdown(msg["content"])
        elif msg["role"] == "deliverable":
            st.markdown(f"### 📄 {msg.get('persona_name', 'Deliverable')}")
            st.markdown(msg["content"][:500] + "..." if len(msg["content"]) > 500 else msg["content"])
            st.download_button("⬇️ Download", msg["content"], file_name=f"{msg.get('persona_name', 'output')}.md", key=f"dl_msg_{msg['id']}")
    
    if messages:
        st.markdown("---")
        # Session management
        col1, col2, col3 = st.columns(3)
        with col1:
            new_name = st.text_input("Rename", value="", placeholder="New name...", key="rename_sess", label_visibility="collapsed")
            if new_name:
                update_session(current_session_id, {"name": new_name})
                st.rerun()
        with col2:
            move_options = ["(Select project)"] + [p["name"] for p in projects]
            move_to = st.selectbox("Move", move_options, key="move_sess", label_visibility="collapsed")
            if move_to != "(Select project)":
                target_proj = next((p for p in projects if p["name"] == move_to), None)
                if target_proj:
                    update_session(current_session_id, {"project_id": target_proj["id"]})
                    st.rerun()
else:
    documents = []
    st.markdown("### Start a new discussion")
    st.markdown(f"**Mode:** {mode_display}")
    if st.session_state.discussion_mode == "panel":
        st.caption("All participants discuss in rounds")
    elif st.session_state.discussion_mode == "conversational":
        st.caption(f"Facilitator ({st.session_state.facilitator_llm}) orchestrates the conversation")
    else:
        st.caption(f"Facilitator ({st.session_state.facilitator_llm}) dispatches work in parallel")

st.markdown("---")

# Input
user_input = st.chat_input("What would you like to discuss?")

if user_input:
    if not enabled_llms:
        st.error("Select at least one participant.")
    else:
        # Create session
        if not current_session_id:
            current_session_id = create_session(
                user_input[:100], 
                st.session_state.current_project_id,
                st.session_state.discussion_mode,
                st.session_state.facilitator_llm
            )
            st.session_state.current_session_id = current_session_id
        
        add_message(current_session_id, "user", user_input)
        
        # Save uploaded file as document
        file_context = st.session_state.file_context
        if file_context:
            save_document(current_session_id, st.session_state.uploaded_filename, file_context, "input")
        
        memory_context = ""
        if file_context:
            memory_context = f"## UPLOADED FILE ({st.session_state.uploaded_filename}):\n\n{file_context[:8000]}\n\n"
        
        # Build participants
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
        
        st.markdown(f"**🧑 Darin:** {user_input}")
        
        mode = st.session_state.discussion_mode
        
        with st.status(f"🎯 Running {mode} mode...", expanded=True) as status:
            
            if mode == "panel":
                all_responses, previous_text = run_panel_discussion(
                    user_input, participants, st.session_state.num_rounds, 
                    memory_context, current_session_id, st
                )
                final_responses = all_responses[st.session_state.num_rounds]
                
            elif mode == "conversational":
                conversation_log = run_conversational_mode(
                    user_input, participants, st.session_state.facilitator_llm,
                    memory_context, current_session_id, st, documents
                )
                previous_text = "\n\n".join(conversation_log)
                final_responses = {p['llm']: "" for p in participants}
                
            else:  # dispatcher
                results, merged_result = run_dispatcher_mode(
                    user_input, participants, st.session_state.facilitator_llm,
                    memory_context, current_session_id, st, documents, file_context
                )
                previous_text = merged_result
                final_responses = {r['llm']: r['result'] for r in results}
                
                # Save merged result as document
                save_document(current_session_id, "merged_output.md", merged_result, "output")
            
            # Synthesis
            st.write("**Synthesizing...**")
            synth_prompt = f'Topic: "{user_input}"\n\nDiscussion:\n{previous_text[:6000]}\n\nSynthesize in 3-4 paragraphs.'
            synthesis = ask_claude(synth_prompt, "You are a neutral facilitator.", memory_context)
            add_message(current_session_id, "synthesis", synthesis)
            
            decisions_prompt = f"List 3-5 key decisions as bullet points:\n\n{synthesis}"
            key_decisions = ask_claude(decisions_prompt, "Extract key decisions.", None)
            add_message(current_session_id, "decisions", key_decisions)
            
            # Check for file request
            if any(kw in user_input.lower() for kw in ["create a file", "create a markdown", "generate a file", "write a file", "create a prompt"]):
                st.write("**Generating deliverable...**")
                file_prompt = f"Based on this discussion:\n{synthesis}\n\nCreate the requested deliverable. Output ONLY the file content."
                deliverable = ask_claude(file_prompt, "Create professional deliverables.", memory_context)
                
                filename = "deliverable.md"
                if "lovable" in user_input.lower():
                    filename = "lovable_prompt.md"
                elif "website" in user_input.lower():
                    filename = "website_spec.md"
                
                add_message(current_session_id, "deliverable", deliverable, persona_name=filename)
                save_document(current_session_id, filename, deliverable, "output")
            
            update_session(current_session_id, {"status": "complete", "updated_at": datetime.now().isoformat()})
            status.update(label="✅ Complete!", state="complete")
        
        st.markdown("### 📋 Synthesis")
        st.markdown(synthesis)
        st.markdown("### 🔑 Key Decisions")
        st.markdown(key_decisions)
        
        st.rerun()
