def run_dispatcher_mode(user_input, participants, facilitator_llm, memory_context, session_id, status_container, documents, file_content=None):
    """Facilitator breaks work into chunks and dispatches to chosen personas"""
    
    facilitator_func = LLM_FUNCTIONS[facilitator_llm]
    
    # Build context about available personas with their expertise
    team_info = "AVAILABLE TEAM MEMBERS:\n"
    for p in participants:
        team_info += f"- {p['name']} (powered by {p['llm']}): {p['description'][:300]}\n\n"
    
    # Check if we have CSV/spreadsheet data
    is_spreadsheet = file_content and (',' in file_content[:500] or '\t' in file_content[:500])
    
    if is_spreadsheet:
        lines = file_content.strip().split('\n')
        header = lines[0] if lines else ""
        data_rows = lines[1:] if len(lines) > 1 else []
        
        dispatch_prompt = f"""{team_info}

USER REQUEST: {user_input}

SPREADSHEET DATA:
- Header: {header}
- Total rows: {len(data_rows)}
- Sample row: {data_rows[0] if data_rows else 'none'}

You are the dispatcher. Analyze this work and decide:
1. Should all rows get the same treatment, or do different rows need different expertise?
2. Which team member(s) should handle which portions based on their skills?

For example:
- If writing marketing copy, assign to the Copywriter
- If analyzing buyer pain points, assign to the Buyer Researcher
- If strategic positioning, assign to the Positioning Strategist
- You can split by row ranges OR by task type

Respond in JSON format:
{{"reasoning": "why you're assigning this way",
  "tasks": [
    {{"persona": "exact persona name", "start_row": 0, "end_row": 25, "instruction": "specific instruction for this persona"}},
    {{"persona": "exact persona name", "start_row": 26, "end_row": 50, "instruction": "specific instruction for this persona"}},
    ...
  ],
  "merge_instruction": "how to combine the results"}}

Available persona names: {', '.join([p['name'] for p in participants])}
"""
    else:
        dispatch_prompt = f"""{team_info}

USER REQUEST: {user_input}

CONTEXT:
{memory_context[:2000] if memory_context else 'No additional context'}

You are the dispatcher. Analyze this work and decide how to divide it among your team based on their expertise:

1. What distinct tasks or subtasks are needed?
2. Which team member is best suited for each based on their background?
3. Can any tasks run in parallel?

For example:
- Research tasks → Buyer Researcher
- Writing/copy tasks → Copywriter
- Strategic framing → Positioning Strategist
- Creative direction → Creative Director
- Executive perspective → CEO/CFO/CHRO advisors

Respond in JSON format:
{{"reasoning": "why you're assigning this way",
  "tasks": [
    {{"persona": "exact persona name", "task": "specific task description tailored to their expertise"}},
    {{"persona": "exact persona name", "task": "specific task description tailored to their expertise"}},
    ...
  ],
  "merge_instruction": "how to combine the results (single file or separate files)"}}

Available persona names: {', '.join([p['name'] for p in participants])}
"""
    
    status_container.write("**🎯 Dispatcher analyzing work and assigning to team...**")
    dispatch_response = facilitator_func(dispatch_prompt, "You are a skilled work dispatcher who assigns tasks based on team expertise.", None)
    add_message(session_id, "facilitator", dispatch_response, llm_name=facilitator_llm, persona_name="Dispatcher", persona_emoji="🎯")
    
    # Parse dispatch plan
    try:
        import re
        json_match = re.search(r'\{.*\}', dispatch_response, re.DOTALL)
        if json_match:
            dispatch_plan = json.loads(json_match.group())
        else:
            dispatch_plan = {"tasks": [{"persona": p['name'], "task": user_input} for p in participants]}
    except:
        dispatch_plan = {"tasks": [{"persona": p['name'], "task": user_input} for p in participants]}
    
    tasks = dispatch_plan.get("tasks", [])
    merge_instruction = dispatch_plan.get("merge_instruction", "Combine all results into a single coherent output.")
    reasoning = dispatch_plan.get("reasoning", "")
    
    if reasoning:
        status_container.write(f"**📋 Plan:** {reasoning[:200]}...")
    
    status_container.write(f"**📤 Dispatching {len(tasks)} tasks...**")
    
    results = []
    
    for i, task in enumerate(tasks):
        # Find participant by persona name
        target_persona = task.get("persona", "")
        target_participant = next((p for p in participants if p['name'].lower() == target_persona.lower()), None)
        
        # Fallback: try partial match
        if not target_participant:
            target_participant = next((p for p in participants if target_persona.lower() in p['name'].lower()), None)
        
        # Last fallback: use first participant
        if not target_participant:
            target_participant = participants[i % len(participants)]
            status_container.write(f"⚠️ Couldn't find '{target_persona}', using {target_participant['name']}")
        
        if is_spreadsheet and "start_row" in task:
            start = task.get("start_row", 0)
            end = task.get("end_row", len(data_rows))
            chunk_rows = data_rows[start:end]
            chunk_data = header + "\n" + "\n".join(chunk_rows)
            
            task_prompt = f"""You are the {target_participant['name']}.

TASK: {task.get('instruction', user_input)}

DATA (rows {start+1} to {end}):
{chunk_data}

Apply your expertise to process this data. Be thorough and leverage your specific background."""
        else:
            task_prompt = f"""You are the {target_participant['name']}.

TASK: {task.get('task', user_input)}

{memory_context if memory_context else ''}

Apply your specific expertise to complete this task thoroughly."""
        
        status_container.write(f"**{target_participant['emoji']} {target_participant['name']} working on: {task.get('task', task.get('instruction', ''))[:50]}...**")
        
        response = target_participant['func'](task_prompt, target_participant['description'], None)
        
        add_message(session_id, "participant", response, 
                   llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                   persona_emoji=target_participant['emoji'], round_num=i+1,
                   message_type="dispatch_result")
        
        results.append({
            "persona": target_participant['name'],
            "llm": target_participant['llm'],
            "task": task.get('task', task.get('instruction', '')),
            "result": response
        })
        
        # Quality check with retry
        quality_prompt = f"""The {target_participant['name']} was asked to: {task.get('task', task.get('instruction', ''))}

Their response:
{response[:1500]}

Evaluate:
1. Did they complete the task?
2. Did they apply their expertise appropriately?
3. Is the quality sufficient?

Respond with "APPROVED" or "RETRY: specific feedback"
"""
        
        quality_check = facilitator_func(quality_prompt, "You evaluate work quality.", None)
        
        if "RETRY" in quality_check:
            status_container.write(f"**🔄 Requesting revision from {target_participant['name']}...**")
            feedback = quality_check.replace("RETRY:", "").strip()
            
            retry_prompt = f"""Your previous response needs revision.

FEEDBACK: {feedback}

ORIGINAL TASK: {task.get('task', task.get('instruction', ''))}

Please revise your response addressing the feedback. Apply your full expertise as {target_participant['name']}."""
            
            response = target_participant['func'](retry_prompt, target_participant['description'], None)
            results[-1]["result"] = response
            add_message(session_id, "participant", f"[Revised] {response}", 
                       llm_name=target_participant['llm'], persona_name=target_participant['name'], 
                       persona_emoji=target_participant['emoji'], round_num=i+1)
    
    # Merge results
    status_container.write("**🎯 Dispatcher merging results...**")
    
    merge_prompt = f"""ORIGINAL REQUEST: {user_input}

MERGE INSTRUCTION: {merge_instruction}

RESULTS FROM TEAM:
"""
    for r in results:
        merge_prompt += f"\n--- {r['persona']} (Task: {r['task'][:50]}...) ---\n{r['result']}\n"
    
    merge_prompt += """

Combine these results according to the merge instruction. 
- If "single file" or "merge": Create one coherent output
- If "separate files": Clearly delineate each section
- Preserve the unique contributions of each team member's expertise"""
    
    merged_result = facilitator_func(merge_prompt, "You merge work results while preserving each contributor's expertise.", None)
    
    return results, merged_result
