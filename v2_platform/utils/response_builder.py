def parse_structured_response(raw_answer):
    sections = {
        "summary": "",
        "metrics": "",
        "insight": "",
        "sources": "",
        "limitations": ""
    }
    
    current = None
    lines = raw_answer.split("\n")
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        if line_lower.startswith("summary:"):
            current = "summary"
            remainder = line_stripped[8:].strip()
            if remainder:
                sections[current] += remainder + "\n"
        elif line_lower.startswith("key metrics:") or line_lower.startswith("metrics:"):
            current = "metrics"
        elif line_lower.startswith("insight:"):
            current = "insight"
            remainder = line_stripped[8:].strip()
            if remainder:
                sections[current] += remainder + "\n"
        elif line_lower.startswith("sources:"):
            current = "sources"
        elif line_lower.startswith("limitations:"):
            current = "limitations"
        elif current and line_stripped:
            sections[current] += line + "\n"
    
    if not any(sections.values()):
        sections["summary"] = raw_answer
    
    return sections


def format_sources_html(sources):
    if not sources:
        return ""
    
    html = "<div style='margin-top:20px;border-top:1px solid #1E293B;padding-top:16px;'>"
    html += "<div style='font-size:11px;color:#475569;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>Sources</div>"
    
    seen = set()
    for s in sources:
        key = s["display"]
        if key in seen:
            continue
        seen.add(key)
        
        html += f"""
        <div style='background:#0F172A;border:1px solid #334155;border-left:3px solid #2563EB;
                    border-radius:6px;padding:10px 14px;margin-bottom:6px;'>
            <div style='font-size:11px;font-weight:600;color:#2563EB;margin-bottom:2px;'>
                {s['company']} · {s['year']} · SEC 10-K Annual Report
            </div>
            <div style='font-size:12px;color:#475569;'>Retrieved via semantic search</div>
        </div>"""
    
    html += "</div>"
    return html