
import re, json
def calculate_reward(svg_content: str, prompt: str) -> float:
    score = 0.0
    if '<svg' not in svg_content or '</svg>' not in svg_content:
        return 0.0
    score += 0.2
    open_tags = re.findall(r'<(\w+)[^>]*>', svg_content)
    close_tags = re.findall(r'</(\w+)>', svg_content)
    if len(open_tags) <= len(close_tags) + 5:
        score += 0.1
    viewbox_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_content)
    if viewbox_match:
        max_x, max_y = int(viewbox_match.group(1)), int(viewbox_match.group(2))
        coords = re.findall(r'[xy]="(\d+)"', svg_content)
        out = False
        for c in coords:
            if int(c) > max_x or int(c) > max_y:
                out = True
                break
        if not out:
            score += 0.1
    try:
        pd = json.loads(prompt)
        up = pd['messages'][0]['content']
        kws = [w for w in up.split() if len(w)>3][:5]
        if kws:
            matched = sum(1 for kw in kws if kw.lower() in svg_content.lower())
            score += 0.1 * (matched / len(kws))
    except:
        pass
    if len(svg_content) < 50:
        score = max(0, score - 0.2)
    else:
        score += 0.1
    return max(0.0, min(1.0, score))
