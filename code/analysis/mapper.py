import os
import logging
import json
import re
from google import genai
from groq import Groq
from openai import OpenAI
from config import GEMINI_MODEL

logger = logging.getLogger(__name__)

# Easter Egg
# print("Mapper Loaded - Engineered by Adhir Singh")

def map_activity_to_competency(trainee_input, framework_data, provider=None):
    """
    Maps the trainee's input using the specified LLM provider (default: from config).
    """
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "gemini")
        
    logger.info(f"Using LLM Provider: {provider.upper()}")

    # 1. Parse Input (Targeted Competency Check)
    target_competency = None
    clean_input = trainee_input
    
    if "COMPETENCY:" in trainee_input and "EVIDENCE:" in trainee_input:
        try:
            parts = trainee_input.split("EVIDENCE:")
            comp_part = parts[0].split("COMPETENCY:")[1].strip()
            evidence_part = parts[1].strip()
            if comp_part and evidence_part:
                target_competency = comp_part
                clean_input = evidence_part
                logger.info(f"Explicit Competency Targeted: '{target_competency}'")
        except Exception:
            pass # Fallback to full string

    # 2. Prepare Context (Common)
    training_plan_raw = framework_data.get('training_plan', [])
    # Inject index for sorting later
    for idx, item in enumerate(training_plan_raw):
         item['_original_index'] = idx

    # Handle split providers
    if provider.lower() in ["github_mini", "github_4o"]:
        # Set transient env var or pass param? 
        # Easier to check provider string in _map_with_github
        if "mini" in provider.lower(): os.environ["GITHUB_MODEL"] = "gpt-4o-mini"
        if "4o" in provider.lower() and "mini" not in provider.lower(): os.environ["GITHUB_MODEL"] = "gpt-4o"
        provider = "github"

    try:
        if provider.lower() == "groq":
             mappings = _map_with_groq(clean_input, target_competency, framework_data)
        elif provider.lower() == "github":
             mappings = _map_with_github(clean_input, target_competency, framework_data)
        else:
             mappings = _map_with_gemini(clean_input, target_competency, framework_data)
             
        # 3. Common Post-Processing (Filtering & Sorting)
        return _post_process_mappings(mappings, training_plan_raw, target_competency, trainee_input)
        
    except Exception as e:
        logger.error(f"Error during AI mapping ({provider}): {e}")
        return get_mock_response(trainee_input, error_msg=str(e))

def _map_with_gemini(clean_input, target_competency, framework_data):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing.")
        
    client = genai.Client(api_key=api_key)

    # Full Context (No Truncation)
    def clean_floats(obj):
        if isinstance(obj, float) and obj != obj: return ""
        if isinstance(obj, dict): return {k: clean_floats(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_floats(i) for i in obj]
        return obj
        
    training_plan_clean = clean_floats(framework_data.get('training_plan', []))
    training_plan_json = json.dumps(training_plan_clean, indent=0)
    
    web_content = ""
    for url, text in framework_data.get('web_content', {}).items():
        web_content += f"Source: {url}\n{text}\n\n"

    context_text = ""
    for cat_name, cat_files in framework_data.get('additional_context', {}).items():
        context_text += f"=== Category: {cat_name} ===\n"
        for fname, ftext in cat_files.items():
            context_text += f"--- Document: {fname} ---\n{ftext}\n\n"

    prompt = _build_prompt(clean_input, target_competency, training_plan_json, context_text, web_content)
    
    logger.info(f"Sending request to Gemini ({GEMINI_MODEL})... Context: {len(prompt)} chars.")
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={'response_mime_type': 'application/json'}
    )
    return _parse_json_response(response.text)

def _map_with_groq(clean_input, target_competency, framework_data):
    key = os.getenv("GROQ_API_KEY")
    if not key or key == "deprecated":
         raise ValueError("GROQ_API_KEY is missing.")
        
    client = Groq(api_key=key)
    
    # Truncate Context for Groq Aggressively (TPM Limit is ~12k tokens)
    # 1. Minify Training Plan (Full plan is ~16k tokens -> Reduce to ~1k)
    training_plan = framework_data.get('training_plan', [])
    tp_mini = []
    for item in training_plan:
        tp_mini.append({
            "competency_code": item.get("competency_code", ""),
            "name": item.get("competency_name", ""), # Map competency_name to name for consistency with prompt
            "desc": (item.get("behavioral_indicators") or "")[:200]
        })
    tp_str = json.dumps(tp_mini, separators=(',', ':'))
 
    
    web_content = ""
    for k, v in framework_data.get('web_content', {}).items():
        web_content += f"{v[:500]}\n" # Cap web content to 500 chars

    # Drastically reduced from 50k to 15k to fit TPM limits
    MAX_CONTEXT_CHARS = 15000 
    context_text = ""
    current_chars = 0
    for cat_name, cat_files in framework_data.get('additional_context', {}).items():
        if current_chars >= MAX_CONTEXT_CHARS: break
        context_text += f"=== Category: {cat_name} ===\n"
        for fname, ftext in cat_files.items():
            if current_chars >= MAX_CONTEXT_CHARS: break
            # Take smaller snippets (3k chars) to get variety
            snippet = ftext[:3000]
            context_text += f"--- Document: {fname} ---\n{snippet}\n\n"
            current_chars += len(snippet)
    
    prompt = _build_prompt(clean_input, target_competency, tp_str, context_text, web_content)
    
    logger.info("Sending request to Groq (llama-3.3-70b-versatile)...")
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return _parse_json_response(chat_completion.choices[0].message.content)

def _map_with_github(clean_input, target_competency, framework_data):
    token = os.getenv("GITHUB_TOKEN")
    model_name = os.getenv("GITHUB_MODEL", "gpt-4o-mini")
    
    if not token:
        raise ValueError("GITHUB_TOKEN is missing.")

    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
    )
    
    # Use ultra-compact context preparation (Strict 8k Token Limit)
    # 1. Minify Training Plan (List of Lists instead of dicts to save key overhead)
    # Format: ["Code | Name | Desc"]
    training_plan = framework_data.get('training_plan', [])
    tp_mini = []
    for item in training_plan:
        code = item.get("competency_code", "")
        name = item.get("competency_name", "")
        desc = (item.get("behavioral_indicators") or "")[:100] # Cap description at 100 chars
        tp_mini.append(f"{code} | {name} | {desc}")
        
    tp_str = json.dumps(tp_mini)
    
    web_content = ""
    for k, v in framework_data.get('web_content', {}).items():
        web_content += f"{v[:500]}\n" # Cap web content

    # Context Truncation (Max 5000 chars ~1.2k tokens)
    MAX_CONTEXT_CHARS = 5000
    context_text = ""
    current_chars = 0
    for cat_name, cat_files in framework_data.get('additional_context', {}).items():
        if current_chars >= MAX_CONTEXT_CHARS: break
        context_text += f"=== Category: {cat_name} ===\n"
        for fname, ftext in cat_files.items():
            if current_chars >= MAX_CONTEXT_CHARS: break
            snippet = ftext[:2000]
            context_text += f"--- Document: {fname} ---\n{snippet}\n\n"
            current_chars += len(snippet)
    
    prompt = _build_prompt(clean_input, target_competency, tp_str, context_text, web_content)
    
    logger.info(f"Sending request to GitHub Models ({model_name})... Payload optimized for 8k limit.")
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
        response_format={"type": "json_object"}
    )
    
    return _parse_json_response(response.choices[0].message.content)

def _build_prompt(input_text, target, plan_json, context, web):
    return f"""
    **System Instruction / Prompt**
    **Role**: You are an expert audit documentation assistant for a PwC auditor. Your goal is to document professional competencies (accumens) for SAICA assessment.

    **Input**: You will receive a Summary of Activities for a specific month.
    **Input Data**:
    - Activity: "{input_text}"
    {f'- Targeted Competency: "{target}"' if target else ""}
    
    **Reference Data (Training Plan)**:
    {plan_json}
    
    **Reference Context**:
    {context}
    {web}

    **Goal**: Identify **ALL** relevant competencies from the Training Plan that this activity provides evidence for (with >75% confidence).
    
    **Output Requirement**: For **EACH** identified competency, generate a single, cohesive, professional paragraph narrative.

    **Structure of the Narrative**: For each mapping, weave the following four dimensions into a smooth flow:

    1. **Context (Task Understanding)**: Start by establishing When (month) and Where (Audit client/Location) the task took place, immediately linking it to the primary Action taken.
    2. **Action & Outcome (Task Understanding)**: Describe What steps were taken and How they were performed (painting the picture). Crucially, you must explicitly link these actions to the Competency being documented to explain Why it was done (the desired learning outcome).
       *Note: Mention Who else was involved if relevant for corroboration.*
    3. **Complexity (Task Completion)**: Towards the end of the paragraph, explicitly describe the Technical Complexity. Was it a predetermined step, or did it require integrating knowledge sources and skills?.
    4. **Autonomy (Guidance & Dependencies)**: Conclude by stating the level of Guidance received (e.g., limited guidance, under supervision) and the level of Responsibility taken (autonomy).

    **Negative Constraints (What NOT to do)**:
    - Never output the response as a list of answers to questions a–f.
    - Never use phrases like "The correct manner is..." or "What happened was..."
    - Do not separate the "Complexity" section into a new paragraph; keep it within the single block of text.
    - **CRITICAL**: Do NOT output text in brackets like "[Who]" or "[Client Name]". If a specific name is unknown, use general terms like "the client team" or "management" instead of leaving a placeholder.

    **Example of Desired Output Format** (Repeat this for each competency found): 
    "During the QYY manufacturing audit in August, I demonstrated my understanding of risk management by evaluating the client's internal controls over inventory. I physically toured the warehouse and reconciled stock counts to the general ledger, which ensured the accuracy of the financial statements. I engaged with the warehouse manager to clarify discrepancies in the count sheets. The technical context was complex as it involved assessing obsolete stock provisions under IFRS, and I completed this task with limited guidance, taking full responsibility for documenting the findings."

    **Instructions**:
    1. Scan the Training Plan for **ALL** potential matches.
    2. Filter: Only keep if >75% CONFIDENT.
       {f'- EXCEPTION: If TARGET "{target}" is requested, include it (mark confidence even if low).' if target else ""}
    3. Output a **LIST** of mappings in the specified JSON format.

    **JSON Format**:
    {{ "mappings": [ 
        {{ "competency_code": "...", "name": "...", "confidence": 0.95, "reasoning": "Narrative paragraph here..." }},
        {{ "competency_code": "...", "name": "...", "confidence": 0.85, "reasoning": "Narrative paragraph here..." }}
    ] }}
    """

def _parse_json_response(text):
    try:
        # Strip markdown code blocks if present
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
            
        data = json.loads(text)
        
        # Normalize Keys (Self-Healing)
        # Handle case where LLM outputs 'code' instead of 'competency_code'
        def normalize_item(item):
            if not isinstance(item, dict): return item
            if "code" in item and "competency_code" not in item:
                item["competency_code"] = item["code"]
            if "competency_name" in item and "name" not in item:
                item["name"] = item["competency_name"]
            return item

        raw_list = []
        if "mappings" in data: raw_list = data["mappings"]
        elif isinstance(data, list): raw_list = data
        elif "competency_code" in data or "code" in data: raw_list = [data]
        
        return [normalize_item(i) for i in raw_list]
    except Exception as e:
        logger.error(f"JSON Parsing failed: {e}. Raw text: {text[:100]}...")
        return []

def _post_process_mappings(mappings, training_plan, target_competency, original_input):
    # Create authoritative lookup for names AND descriptions: Code -> {Name, Desc}
    code_lookup = {}
    for item in training_plan:
        c = item.get('competency_code', '').replace(')', '').strip().lower()
        n = item.get('competency_name', '').strip()
        d = item.get('behavioral_indicators', '').strip()
        if c: code_lookup[c] = {"name": n, "desc": d}
        
    filtered = []
    if not mappings: return get_mock_response(original_input)

    # Strict Filtering Logic (Winner Takes All for Code)
    exact_code_matches = []
    fuzzy_matches = []

    for m in mappings:
        conf = m.get('confidence', 0)
        if conf <= 1.0: conf *= 100
        m['confidence'] = conf
        
        # Always normalize name/desc from lookup if possible
        code_key = m.get('competency_code', '').replace(')', '').strip().lower()
        if code_key in code_lookup:
             lookup_data = code_lookup[code_key]
             m['name'] = lookup_data['name']
             m['desc'] = lookup_data['desc']
        
        m_code = m.get('competency_code', '').strip().lower()
        m_name = m.get('name', '').strip().lower()

        if target_competency:
            t_clean = target_competency.strip().lower()
            
            # Robust Code Normalization (Remove all non-alphanumeric)
            def normalize_code(s): return re.sub(r'[^a-z0-9]', '', s)
            
            t_simple = normalize_code(t_clean)
            m_simple = normalize_code(m_code)

            # 1. Exact Code Match (Robust)
            if t_simple and t_simple == m_simple:
                exact_code_matches.append(m)
                continue
            
            # 2. Token Match
            is_targeted = True
            if not (len(t_clean) < 3 and any(c.isdigit() for c in t_clean)):
                 t_toks = [t for t in re.split(r'[^a-zA-Z0-9]+', t_clean) if len(t)>=3]
                 search_text = (m_name + " " + m_code).lower()
                 if not t_toks: is_targeted = False
                 for t in t_toks:
                    if t not in search_text:
                        is_targeted = False; break
            else:
                is_targeted = False
                
            if is_targeted:
                fuzzy_matches.append(m)
        else:
            if conf >= 75:
                filtered.append(m)
                
    if target_competency:
        # Priority Logic: If EXACT Code match found, ignore fuzzy
        if exact_code_matches:
            filtered = exact_code_matches
        else:
            filtered = fuzzy_matches
            # Mark weak if needed
            for m in filtered:
                 if m['confidence'] < 75: m['is_weak_target'] = True
            
    for m in filtered:
        # Fallback sorting
        name = m.get('name', '').strip().lower()
        code = m.get('competency_code', '').strip().lower()
        idx = float('inf')
        for item in training_plan:
            if item.get('competency_code','').lower() == code:
                idx = item.get('_original_index', 9999)
                break
        
        m['_sort_index'] = idx
        
    filtered.sort(key=lambda x: x['_sort_index'])
    for m in filtered: m.pop('_sort_index', None)
    
    return filtered

def get_mock_response(input_text, error_msg=None):
    reasoning = f"Mapping failed. Input: {input_text}"
    if error_msg:
        reasoning = f"Mapping failed. Error: {error_msg}. Input: {input_text}"
        
    return [{
        "competency_code": "ERR", "name": "Error", "confidence": 0,
        "reasoning": reasoning
    }]
