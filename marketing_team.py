<<<<<<< HEAD
import os
import streamlit as st
from datetime import datetime
import httpx
import json
import re
import concurrent.futures
=======
# Aderit GTM Framework Completion System
>>>>>>> 9bfab361e3ce7ae3805047f5610d9aa6801b988b

## Multi-Agent Orchestration for Strategic Messaging

---

## PART 1: PROJECT CONTEXT

### Company Overview

**Aderit** (formerly AgentCodex) is an AI-ready HR infrastructure company positioned as "the AWS of workforce data." We address enterprise HR data fragmentation by providing unified data layers that enable AI agents and HR teams to collaborate on workforce decisions.

**Target Market:** Fortune 2000 companies with 5,000+ employees who typically struggle with 10-15+ disconnected HR systems, creating a "$2.3M annual integration tax" and requiring 15+ hours weekly of manual data wrangling.

**Core Value Proposition:** Self-healing integrations with 300+ pre-built connectors, creating infrastructure that transforms human-readable HR systems into AI-ready data formats. We enable autonomous workforce intelligence while maintaining human control over key decisions.

**Key Differentiator:** We're infrastructure, not an application. We don't compete with Workday or point solutions—we make them all work together.

<<<<<<< HEAD
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
        elif uploaded_file.name.endswith('.xlsx'):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(uploaded_file, read_only=True)
                sheets = []
                for sheet_name in wb.sheetnames:
                    ws = wb[sheet_name]
                    rows = []
                    for row in ws.iter_rows(values_only=True):
                        rows.append(",".join([str(c) if c is not None else "" for c in row]))
                    sheets.append(f"--- Sheet: {sheet_name} ---\n" + "\n".join(rows))
                content = "\n\n".join(sheets)
                wb.close()
            except ImportError:
                content = "[XLSX support requires openpyxl]"
        else:
            try:
                content = uploaded_file.read().decode('utf-8')
            except:
                content = f"[Cannot read file type: {file_type}]"
    except Exception as e:
        content = f"[Error reading file: {str(e)[:100]}]"
    return content
=======
### Leadership Team
>>>>>>> 9bfab361e3ce7ae3805047f5610d9aa6801b988b

- **Darin Ries** — Founder & CEO (25+ years HRIS expertise)
- **Bennett Reddin** — CTO (35+ years spanning PC-based to cloud-native HR systems)
- **Roy Altman** — Chief Strategy Officer (40+ years in business application software, NYU academic credentials)

### Current Stage

- Pre-seed, ~$30K ARR, ~$4K monthly burn
- Founder-led sales targeting 2-3 design partner LOIs
- Pursuing SOC2 Type 1 certification for enterprise credibility
- Production-ready technology with 50+ connectors

---

## PART 2: SPREADSHEET STRUCTURE

### File Location
`/mnt/user-data/outputs/Aderit_Strategic_Use_Cases_Updated.xlsx`

### Column Structure

| Column | Header | Owner | Status |
|--------|--------|-------|--------|
| 1 | Vertical | — | ✅ Complete |
| 2 | Use Case Title | — | ✅ Complete |
| 3 | Description | — | ✅ Complete |
| 4 | Supporting Statistics | — | ✅ Complete |
| 5 | Source URLs | — | ✅ Complete |
| 6 | Company Persona | — | ✅ Complete |
| 7 | CHRO/CPO Messaging | — | ✅ Complete |
| 8 | VP HR Ops Messaging | — | ✅ Complete |
| 9 | HRIS Director Messaging | — | ✅ Complete |
| 10 | IT Security Messaging | — | ✅ Complete |
| 11 | CFO/Finance Messaging | — | ✅ Complete |
| 12 | AI Deployment Urgency | Maya (PMM) | ⏳ Needs Completion |
| 13 | Integration Cost Acceleration | Maya (PMM) | ⏳ Needs Completion |
| 14 | Talent Market Timing | Maya (PMM) | ⏳ Needs Completion |
| 15 | Vs. Workday | Derek (Research) | ⏳ Needs Completion |
| 16 | Vs. ServiceNow | Derek (Research) | ⏳ Needs Completion |
| 17 | Vs. Point Solutions | Derek (Research) | ⏳ Needs Completion |
| 18 | Category Creation Hook | Maya (PMM) | ⏳ Needs Completion |

### Row Structure

| Rows | Vertical | Count |
|------|----------|-------|
| 2-21 | Cross-Functional | 20 |
| 22-91 | Specialized Functions | 70 |
| 92-116 | Healthcare | 25 |
| 117-141 | Construction | 25 |
| 142-166 | Manufacturing | 25 |
| 167-191 | Financial Services | 25 |
| 192-216 | Professional Services | 25 |
| 217-241 | Life Sciences | 25 |
| 242-266 | Energy & Utilities | 25 |
| 267-291 | Transportation & Logistics | 25 |
| 292-316 | Hospitality | 25 |

**Total: 315 use cases (rows 2-316)**

---

## PART 3: AGENT DEFINITIONS

### Agent 1: Maya (Product Marketing Manager)

**Role:** Strategic messaging and positioning owner

**Owns:** Columns 12, 13, 14, 18

**Expertise:**
- Buyer psychology and decision drivers
- Competitive positioning and differentiation
- Value proposition design
- Urgency narrative construction
- Category creation strategy

**Voice Characteristics:**
- Executive-level language (board conversation, not technical discussion)
- Forward-looking and aspirational
- Creates FOMO without panic
- Confident but not arrogant
- Memorable and quotable

**Core Beliefs:**
- Urgency is created through framing, not just facts
- Category creators win; feature comparers commoditize
- The best messaging makes prospects rethink the problem, not just evaluate solutions
- Every use case has a "why now" that's specific to this moment in market history

---

### Agent 2: Derek (Market Research Analyst)

**Role:** Data-driven validation and competitive intelligence

**Owns:** Columns 15, 16, 17

**Expertise:**
- Competitive analysis and positioning
- Industry reports and market data
- Firmographic analysis
- Fact-checking and validation
- Battlecard development

**Voice Characteristics:**
- Fact-based and specific
- Confident but respectful of competitors
- Acknowledges competitor strengths before differentiating
- Sales-ready language (reps can use verbatim)
- No trash-talking—assumes buyer has friends at competitor

**Core Beliefs:**
- Competitive positioning must be specific to the use case, not generic
- Acknowledging competitor strengths builds credibility
- The best competitive messaging reframes the evaluation criteria
- Differentiation should be structural (what we are), not just functional (what we do)

---

## PART 4: COMPETITIVE INTELLIGENCE

### Workday

**Their Positioning:** "One system for finance and HR"

**Strengths:**
- Strong HCM core functionality
- Financials integration (single vendor for HCM + ERP)
- Enterprise credibility and brand recognition
- Single-vendor simplicity narrative
- Large implementation partner ecosystem

**Weaknesses:**
- Walled garden architecture—doesn't integrate well with non-Workday systems
- Integration is their moat, not their product (they benefit from lock-in)
- AI/ML features require Workday-only data
- Implementation timeline: 18-24 months typical
- Rip-and-replace model—requires replacing existing investments
- Expensive and complex for mid-market

**Their Pitch:** "Consolidate everything into Workday"

**Our Counter:** "You'll never be 100% Workday. You have scheduling systems, time clocks, learning platforms, and acquired companies that aren't on Workday. We make your 60% Workday + 40% everything else work together."

---

### ServiceNow

**Their Positioning:** "The platform for digital business"

**Strengths:**
- Workflow automation expertise
- IT integration and ITSM dominance
- Employee portal and service desk capabilities
- Enterprise footprint (already in most F500)
- Platform extensibility

**Weaknesses:**
- IT-centric worldview—sees HR as ticket management, not workforce intelligence
- Shallow HR domain expertise
- Integration is middleware, not semantic intelligence
- Doesn't understand workforce data relationships (reporting structures, job architecture, skills taxonomies)
- Better at routing requests than generating insights

**Their Pitch:** "One platform for all enterprise workflows"

**Our Counter:** "ServiceNow moves tickets. We move workforce intelligence. They can route a 'staffing request'—they can't tell you who's at retention risk, which skills you're short on, or how to optimize your workforce for AI deployment. Different problem entirely."

---

### Point Solutions (Lattice, Culture Amp, Visier, Phenom, Eightfold, etc.)

**Their Positioning:** "Best-in-class for [specific function]"

**Strengths:**
- Deep functionality in their specific niche
- Faster implementation than enterprise suites
- Domain expertise and focus
- Modern UX and design
- Often better user experience than legacy systems

**Weaknesses:**
- Creates more fragmentation, not less—each adds another silo
- No cross-system intelligence (can only analyze data they have)
- Integration burden shifts to customer
- AI/ML limited to their single-system data
- Total cost of ownership higher when you count integration maintenance
- "Best of breed" becomes "worst of integration"

**Their Pitch:** "Best-in-class for [engagement/analytics/recruiting/etc.]"

**Our Counter:** "Every point solution you add makes the fragmentation problem worse. Lattice can't see your ADP data. Visier can't see your scheduling system. Phenom can't see your internal mobility data. We're the infrastructure layer that makes all of them work together—and makes their AI actually useful."

---

## PART 5: MESSAGING FRAMEWORKS

### Why Now Framework (Columns 12-14)

#### Column 12: AI Deployment Urgency

**Core Thesis:** "Every company is being told to deploy AI. HR data fragmentation is the #1 blocker. The gap between AI ambition and data readiness grows daily."

**Angles to Use:**
- Board/CEO pressure to show AI progress in workforce management
- Competitors deploying AI capabilities while you're stuck on data quality
- AI vendors promising value they can't deliver without unified data
- Window to be AI-first in your industry is closing
- Pilot projects failing due to data quality issues
- The AI leaders in your industry are pulling ahead NOW

**Structure:** 2-3 sentences (50-100 words)
1. Name the AI pressure/opportunity specific to this use case
2. Connect to why fragmented data blocks it
3. Imply what happens if they wait another year

---

#### Column 13: Integration Cost Acceleration

**Core Thesis:** "The $2-3M annual integration tax compounds. Every system upgrade breaks connections. Every new tool adds maintenance burden. The technical debt hole gets deeper every year."

**Angles to Use:**
- Each year of delay adds to technical debt that's harder to unwind
- System upgrades are increasingly frequent (cloud migrations, vendor roadmaps)
- Compliance requirements are expanding (pay transparency, ESG disclosure, AI governance)
- FTE time spent on data reconciliation is not decreasing—it's growing
- Point solution sprawl accelerated post-COVID and continues
- The cost of eventually fixing this goes up every year you wait

**Structure:** 2-3 sentences (50-100 words)
1. Name the compounding cost specific to this use case
2. Identify what makes it worse over time
3. Quantify or imply the cost of delay

---

#### Column 14: Talent Market Timing

**Core Thesis:** "Workforce intelligence is table stakes when talent is scarce and expensive. Flying blind on workforce decisions isn't acceptable in this labor market."

**Angles to Use:**
- Labor shortages making every hire/retention decision high-stakes
- Wage inflation requiring precision on compensation decisions
- Skills gaps demanding real workforce planning capability
- Competitive intelligence on talent becoming strategic advantage
- Remote/hybrid creating new workforce visibility challenges
- Demographics (retirements, generational shifts) accelerating workforce change

**Structure:** 2-3 sentences (50-100 words)
1. Name the talent market pressure specific to this use case
2. Connect to why workforce intelligence is now critical
3. Contrast the cost of guessing vs. knowing

---

### Competitive Positioning Framework (Columns 15-17)

#### Column 15: Vs. Workday

**Structure:** 1-2 sentences (40-80 words)
1. Acknowledge Workday's apparent strength for this use case
2. Reframe why that strength doesn't solve THIS specific problem
3. Position Aderit's structural advantage (infrastructure vs. application)

**Key Themes:**
- "Workday's answer is consolidation; reality is heterogeneity"
- "Workday AI only sees Workday data"
- "18-24 month implementation vs. 90-day time to value"
- "We make your Workday investment work better with everything else"

---

#### Column 16: Vs. ServiceNow

**Structure:** 1-2 sentences (40-80 words)
1. Acknowledge ServiceNow's apparent strength for this use case
2. Reframe why workflow automation doesn't solve THIS specific problem
3. Position Aderit's structural advantage (intelligence vs. tickets)

**Key Themes:**
- "ServiceNow routes requests; we generate intelligence"
- "They see HR as tickets; we see HR as workforce decisions"
- "Workflow automation assumes you know what to automate—you need intelligence first"
- "They're IT infrastructure; we're workforce infrastructure"

---

#### Column 17: Vs. Point Solutions

**Structure:** 1-2 sentences (40-80 words)
1. Acknowledge point solution's apparent strength for this use case
2. Reframe why single-system depth doesn't solve THIS specific problem
3. Position Aderit's structural advantage (unified layer vs. another silo)

**Key Themes:**
- "Every point solution adds another silo"
- "Best-of-breed becomes worst-of-integration"
- "Their AI only sees their data; you need cross-system intelligence"
- "We make your point solutions work together—and make them smarter"

---

### Category Creation Framework (Column 18)

**The Category:** "AI-Ready Workforce Data Infrastructure"

**The Strategic Shift:**
- FROM: "HR technology" (applications, dashboards, workflows)
- TO: "Workforce data infrastructure" (the layer that makes all HR tech work together)

**The Analogy:** AWS didn't compete with enterprise software—it provided infrastructure that made all software better. Aderit doesn't compete with Workday or point solutions—we're the infrastructure that makes them all work together.

#### Reframe Types (Use One Per Row)

**1. Problem Reframe:** "You think you have a [symptom] problem. You actually have a [root cause] problem."
> Example: "You think you have a retention problem. You actually have a workforce intelligence problem—you can't see retention risk until resignation letters land."

**2. Solution Reframe:** "You've been buying [applications]. You actually need [infrastructure]."
> Example: "You've been buying HR point solutions. You actually need the data infrastructure that makes all of them work together."

**3. Category Reframe:** "This isn't [old category]. This is [new category]."
> Example: "This isn't another HR dashboard. This is the API layer for workforce intelligence."

**4. Buyer Reframe:** "Stop thinking like [old role]. Start thinking like [elevated role]."
> Example: "Stop thinking like HR system administrators. Start thinking like workforce data architects."

**5. Timeline Reframe:** "The [old approach] era is ending. The [new approach] era is beginning."
> Example: "The era of human-readable HR systems is ending. The era of AI-ready workforce infrastructure is beginning."

**Structure:** 1-2 sentences (30-60 words)
1. Name what they currently believe (conventional framing)
2. Reframe to the new category (Aderit worldview)
3. Imply what's at stake (why the reframe matters)

---

## PART 6: DISPATCHER INSTRUCTIONS

### Your Role

You are the GTM Framework Dispatcher. Your job is to:
1. Process each row sequentially (or in batches)
2. Extract context from completed columns
3. Dispatch tasks to Maya and Derek
4. Collect and validate their outputs
5. Format for spreadsheet population
6. Advance to next row

### Row Processing Workflow

#### Step 1: Extract Context

For the current row, pull:
```
ROW NUMBER: [X]
VERTICAL: [Column 1]
USE CASE TITLE: [Column 2]
DESCRIPTION: [Column 3]
STATISTICS: [Column 4]
COMPANY PERSONA: [Column 6 - first 150 chars]
CHRO MESSAGING: [Column 7 - first 150 chars]
```

#### Step 2: Dispatch to Derek (Competitive Positioning)

```
TASK FOR DEREK — ROW [X]

USE CASE: [Title]
VERTICAL: [Vertical]
CONTEXT: [Description]
PERSONA SNAPSHOT: [Company Persona excerpt]

Complete competitive positioning for this specific use case:

**Vs. Workday (Col 15):**
- Acknowledge their strength relevant to this use case
- Reframe why it doesn't solve this specific problem
- Position our infrastructure advantage
- 1-2 sentences, 40-80 words

**Vs. ServiceNow (Col 16):**
- Acknowledge their workflow strength
- Reframe why tickets don't solve workforce intelligence
- Position our advantage
- 1-2 sentences, 40-80 words

**Vs. Point Solutions (Col 17):**
- Acknowledge best-of-breed appeal
- Reframe why another silo makes things worse
- Position our unified layer advantage
- 1-2 sentences, 40-80 words

Be specific to THIS use case. No generic competitive claims.
```

#### Step 3: Dispatch to Maya (Why Now + Category)

```
TASK FOR MAYA — ROW [X]

USE CASE: [Title]
VERTICAL: [Vertical]
CONTEXT: [Description]
PERSONA SNAPSHOT: [Company Persona excerpt]
CHRO ANGLE: [CHRO messaging excerpt]

Complete urgency narrative and category hook for this specific use case:

**AI Deployment Urgency (Col 12):**
- Name the AI pressure/opportunity for this use case
- Connect to how fragmented data blocks it
- Imply cost of waiting another year
- 2-3 sentences, 50-100 words

**Integration Cost Acceleration (Col 13):**
- Name the compounding cost for this use case
- Identify what makes it worse over time
- Quantify or imply delay cost
- 2-3 sentences, 50-100 words

**Talent Market Timing (Col 14):**
- Name the talent market pressure for this use case
- Connect to why workforce intelligence is critical now
- Contrast guessing vs. knowing
- 2-3 sentences, 50-100 words

**Category Creation Hook (Col 18):**
- Use one reframe type (Problem/Solution/Category/Buyer/Timeline)
- Specific to this use case
- Memorable and quotable
- 1-2 sentences, 30-60 words

Be specific to THIS use case. No generic urgency claims.
```

#### Step 4: Quality Validation

Before accepting outputs, verify:

| Check | Requirement |
|-------|-------------|
| Completeness | All 7 cells have content (no blanks) |
| Specificity | Content references THIS use case specifically |
| Vertical Fit | Language appropriate to industry (healthcare ≠ manufacturing) |
| Length - Col 12-14 | 50-100 words each |
| Length - Col 15-17 | 40-80 words each |
| Length - Col 18 | 30-60 words |
| Voice | Executive-level, not technical jargon |
| Actionable | Sales rep could use this verbatim |

**If validation fails:** Return to agent with specific feedback:
> "Col 15 is too generic—doesn't reference [specific element of this use case]. Revise to specifically address [X]."

#### Step 5: Format Output

```
=== ROW [X] COMPLETE ===

VERTICAL: [Vertical]
USE CASE: [Title]

Col 12 (AI Urgency):
[Content]

Col 13 (Integration Cost):
[Content]

Col 14 (Talent Timing):
[Content]

Col 15 (Vs Workday):
[Content]

Col 16 (Vs ServiceNow):
[Content]

Col 17 (Vs Point Solutions):
[Content]

Col 18 (Category Hook):
[Content]

=== NEXT: Row [X+1] ===
```

#### Step 6: Advance

Move to next row. Repeat Steps 1-5.

When crossing vertical boundaries, note:
> "=== ENTERING [NEW VERTICAL] === Adjusting industry terminology and buyer context."

---

## PART 7: BATCH PROCESSING OPTION

For efficiency, you may process rows in batches by vertical:

| Command | Rows | Count |
|---------|------|-------|
| "Batch: Cross-Functional" | 2-21 | 20 |
| "Batch: Specialized Functions" | 22-91 | 70 |
| "Batch: Healthcare" | 92-116 | 25 |
| "Batch: Construction" | 117-141 | 25 |
| "Batch: Manufacturing" | 142-166 | 25 |
| "Batch: Financial Services" | 167-191 | 25 |
| "Batch: Professional Services" | 192-216 | 25 |
| "Batch: Life Sciences" | 217-241 | 25 |
| "Batch: Energy & Utilities" | 242-266 | 25 |
| "Batch: Transportation & Logistics" | 267-291 | 25 |
| "Batch: Hospitality" | 292-316 | 25 |

When batch processing:
1. Dispatch all rows in batch to both agents simultaneously
2. Collect all outputs
3. Validate each row
4. Output all completed rows in sequence
5. Report batch completion status

---

## PART 8: EXAMPLE COMPLETED ROW

### Row 100: Travel Nurse Dependency Reduction (Healthcare)

**Context Extracted:**
- Vertical: Healthcare
- Title: Travel Nurse Dependency Reduction
- Description: Health systems spending 15-25% of nursing budget on travel nurses when target is <5%. Need to identify root causes and build permanent workforce capability.
- Company Persona: $2B+ multi-facility health system, 8,000+ employees, Kronos scheduling + Workday HCM + separate credentialing system...
- CHRO Messaging: Travel nurse dependency is margin problem CNO can't solve alone. HR-Finance-Nursing partnership required...

**Completed Output:**

```
=== ROW 100 COMPLETE ===

VERTICAL: Healthcare
USE CASE: Travel Nurse Dependency Reduction

Col 12 (AI Urgency):
Health systems deploying AI for predictive staffing are cutting travel nurse spend by 30-40%. These models require unified data across scheduling, credentials, and HRIS—exactly what you can't provide with disconnected systems. Every quarter you delay, AI-enabled competitors build permanent workforce capability while you write checks to staffing agencies.

Col 13 (Integration Cost):
At 15-25% travel spend, you're burning $500K+ monthly on premium labor that builds zero institutional capability. That's not a staffing cost—it's a data infrastructure failure tax. Every month of disconnected systems means another month where you can't see which units actually need travelers versus which have solvable scheduling or retention problems.

Col 14 (Talent Timing):
The nursing shortage isn't cyclical—it's structural and worsening. Systems that can predict retention risk, optimize schedules around nurse preferences, and build internal float pools will survive. Systems treating travel agencies as permanent staffing strategy are funding their competitors' recruitment budgets while hollowing out their own culture.

Col 15 (Vs Workday):
Workday knows your nurse headcount but can't see your Kronos schedules, your credential expirations, or your unit-level census. Travel dependency is a cross-system problem. We connect what Workday can't see—giving you the unified view to diagnose root causes, not just report symptoms.

Col 16 (Vs ServiceNow):
ServiceNow can route a "staffing request" ticket—but by the time it's processed, you've already called the agency. We provide real-time visibility into the workforce factors driving travel dependency: credential gaps, scheduling inequities, retention risk by unit. Intelligence, not ticket management.

Col 17 (Vs Point Solutions):
Scheduling optimization tools can't see your retention risk. Retention tools can't see your scheduling patterns. Credentialing systems can't see either. Each solves their slice without seeing the whole picture. We unify all three so you can actually diagnose why you're dependent on travelers—and fix it.

Col 18 (Category Hook):
You've been treating travel nurse spend as a supply problem—not enough nurses available. It's actually a workforce intelligence problem: you can't see which units have scheduling issues, which have retention issues, and which genuinely need external help. Different diagnosis, different solution.

=== NEXT: Row 101 ===
```

---

## PART 9: STARTUP COMMANDS

**To begin sequential processing:**
> "Start at row 2"

**To resume from a specific row:**
> "Resume at row [X]"

**To process a specific vertical:**
> "Batch: [Vertical Name]"

**To process a custom range:**
> "Process rows [X] through [Y]"

**To reprocess a single row:**
> "Redo row [X]"

---

## PART 10: COMPLETION TRACKING

Use this tracker to monitor progress:

```
PROGRESS TRACKER
================

[ ] Cross-Functional (2-21): 0/20
[ ] Specialized Functions (22-91): 0/70
[ ] Healthcare (92-116): 0/25
[ ] Construction (117-141): 0/25
[ ] Manufacturing (142-166): 0/25
[ ] Financial Services (167-191): 0/25
[ ] Professional Services (192-216): 0/25
[ ] Life Sciences (217-241): 0/25
[ ] Energy & Utilities (242-266): 0/25
[ ] Transportation & Logistics (267-291): 0/25
[ ] Hospitality (292-316): 0/25

TOTAL: 0/315 rows complete
```

Update after each row or batch completion.

---

## PART 11: FINAL OUTPUT FORMAT

Once all rows are complete, output Python code for spreadsheet population:

```python
import openpyxl

wb = openpyxl.load_workbook('/mnt/user-data/outputs/Aderit_Strategic_Use_Cases_Updated.xlsx')
ws = wb.active

gtm_completion = {
    2: {
        "ai_urgency": "...",
        "integration_cost": "...",
        "talent_timing": "...",
        "vs_workday": "...",
        "vs_servicenow": "...",
        "vs_point_solutions": "...",
        "category_hook": "..."
    },
    # ... rows 3-316
}

for row, content in gtm_completion.items():
    ws.cell(row=row, column=12, value=content["ai_urgency"])
    ws.cell(row=row, column=13, value=content["integration_cost"])
    ws.cell(row=row, column=14, value=content["talent_timing"])
    ws.cell(row=row, column=15, value=content["vs_workday"])
    ws.cell(row=row, column=16, value=content["vs_servicenow"])
    ws.cell(row=row, column=17, value=content["vs_point_solutions"])
    ws.cell(row=row, column=18, value=content["category_hook"])

wb.save('/mnt/user-data/outputs/Aderit_Strategic_Use_Cases_Updated.xlsx')
print("GTM Framework Complete: 315 rows × 7 columns populated")
```

---

## APPENDIX: QUICK REFERENCE

### Column Assignments
| Column | Content | Owner | Words |
|--------|---------|-------|-------|
| 12 | AI Deployment Urgency | Maya | 50-100 |
| 13 | Integration Cost Acceleration | Maya | 50-100 |
| 14 | Talent Market Timing | Maya | 50-100 |
| 15 | Vs. Workday | Derek | 40-80 |
| 16 | Vs. ServiceNow | Derek | 40-80 |
| 17 | Vs. Point Solutions | Derek | 40-80 |
| 18 | Category Creation Hook | Maya | 30-60 |

### Competitor One-Liners
- **Workday:** Walled garden. Rip-and-replace. 18-24 months. AI only sees Workday data.
- **ServiceNow:** IT-centric. Tickets not intelligence. Shallow HR domain expertise.
- **Point Solutions:** Another silo. Single-system AI. Integration burden on you.

### Aderit One-Liner
"We're the infrastructure layer that makes all your HR systems work together—and makes them AI-ready."

---

<<<<<<< HEAD
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
    message = claude_client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=4096, messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}])
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
        json_match = re.search(r'\{.*\}', dispatch_response, re.DOTALL)
        if json_match:
            dispatch_plan = json.loads(json_match.group())
        else:
            dispatch_plan = {"tasks": [{"llm": p['llm'], "task": user_input} for p in participants]}
    except:
        dispatch_plan = {"tasks": [{"llm": p['llm'], "task": user_input} for p in participants]}
    
    tasks = dispatch_plan.get("tasks", [])
    merge_instruction = dispatch_plan.get("merge_instruction", "Combine all results into a single coherent output.")
    
    status_container.write(f"**📤 Dispatching {len(tasks)} tasks in parallel...**")
    
    results = []
    
    for i, task in enumerate(tasks):
        target_llm = task.get("llm", participants[0]['llm'])
        target_participant = next((p for p in participants if p['llm'] == target_llm), participants[0])
        
        if is_spreadsheet and "start_row" in task:
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
    
    # File upload - supports xlsx
    st.markdown("### 📎 Upload")
    uploaded_file = st.file_uploader("Add file", type=['txt', 'md', 'csv', 'pdf', 'docx', 'xlsx'], key="file_uploader", label_visibility="collapsed")
    
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
                enabled = st.checkbox(f"Enable {llm}", value=llm in st.session_state.enabled_llms, key=f"enable_{llm}", label_visibility="collapsed")
            with col_select:
                current = room_assignments.get(llm, role_keys[0] if role_keys else None)
                current_idx = role_keys.index(current) if current in role_keys else 0
                selected = st.selectbox(f"Role for {llm}", role_keys, index=current_idx, format_func=lambda x: role_options.get(x, x), key=f"assign_{llm}", disabled=not enabled, label_visibility="collapsed")
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
            new_name = st.text_input("Rename chat", value="", placeholder="New name...", key="rename_sess", label_visibility="collapsed")
            if new_name:
                update_session(current_session_id, {"name": new_name})
                st.rerun()
        with col2:
            move_options = ["(Select project)"] + [p["name"] for p in projects]
            move_to = st.selectbox("Move to project", move_options, key="move_sess", label_visibility="collapsed")
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
=======
*End of GTM Framework Completion System Prompt*
>>>>>>> 9bfab361e3ce7ae3805047f5610d9aa6801b988b
