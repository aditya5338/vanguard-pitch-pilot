import json
import re

SYSTEM_INSTRUCTIONS = """
You are the Vanguard Pitch-Pilot AI Dispatch Agent for the FIFA World Cup 2026.
Your task is to parse unstructured, multilingual volunteer incident reports from the stadium grounds and output a structured JSON object.

Strictly adhere to the following rules:
1. Translate any non-English text into clear, professional English operations reports.
2. Identify the language of the input report.
3. Categorize the incident into one of these types: Medical, Security, Crowd Control, Infrastructure, Pitch/Field, or General.
4. Assign a severity level: Low, Medium, High, or Critical.
5. Determine if immediate crew dispatch is required (True/False).
6. Recommend the appropriate dispatch unit based on the incident type:
   - Medical -> "Stadium First Aid Unit 2" or "First Aid Crew Unit 3"
   - Security -> "Rapid Response Security Team B"
   - Crowd Control -> "Steward Patrol Unit A" or "Gate Staff Redeployment Unit"
   - Infrastructure -> "Technical Maintenance Squad"
   - Pitch/Field -> "Pitch Groundsman"
   - General/Other -> "Standard Duty Crew"

Return format must be valid JSON matching this schema:
{
    "detected_language": "string",
    "category": "string",
    "severity": "string",
    "english_translation": "string",
    "needs_immediate_dispatch": boolean,
    "recommended_crew": "string"
}
"""

# Multilingual keywords and mapping dictionary for rule-based parsing engine
RULES = [
    {
        "keywords": [r"évanouie", r"évanouir", r"desmayada", r"desmayó", r"sick", r"medical", r"médico", r"blessure", r"injury", r"pain", r"heart", r"corazón", r"ambulance", r"sang", r"blood", r"herido", r"heat", r"chaleur", r"calor"],
        "category": "Medical",
        "severity": "High",
        "french_translation": "Spectator collapsed / medical emergency reported.",
        "spanish_translation": "Spectator collapsed / medical emergency reported.",
        "english_translation": "Medical incident reported on stadium grounds.",
        "needs_dispatch": True,
        "recommended_crew": "First Aid Crew Unit 3"
    },
    {
        "keywords": [r"bagarre", "fight", r"bataille", r"pelea", r"securite", r"sécurité", "security", r"seguridad", r"violence", r"vol", r"robo", r"intruso", r"intruder", r"arma", r"weapon", r"arme"],
        "category": "Security",
        "severity": "Critical",
        "french_translation": "Physical altercation / security breach reported.",
        "spanish_translation": "Physical altercation / security breach reported.",
        "english_translation": "Security disturbance or physical altercation reported.",
        "needs_dispatch": True,
        "recommended_crew": "Rapid Response Security Team B"
    },
    {
        "keywords": [r"bloqué", r"bloque", r"crowd", r"surge", r"foule", r"bottleneck", r"embouteillage", r"bouchon", r"gate", r"porte", r"turnstile", r"tourniquet", r"molinete", r"congestion"],
        "category": "Crowd Control",
        "severity": "High",
        "french_translation": "Crowd congestion / gate bottleneck detected.",
        "spanish_translation": "Crowd congestion / gate bottleneck detected.",
        "english_translation": "Crowd flow issue or gate bottleneck reported.",
        "needs_dispatch": True,
        "recommended_crew": "Gate Staff Redeployment Unit"
    },
    {
        "keywords": [r"panne", r"cassé", r"broken", r"leak", r"fuite", r"inondation", r"water", r"eau", r"agua", r"escalator", r"ascenseur", r"elevator", r"lights", r"lumières", r"luces", r"sensor", r"scanner"],
        "category": "Infrastructure",
        "severity": "Medium",
        "french_translation": "Infrastructure malfunction (elevator/escalator/sensor offline or leak).",
        "spanish_translation": "Infrastructure malfunction (elevator/escalator/sensor offline or leak).",
        "english_translation": "Infrastructure issue or equipment malfunction reported.",
        "needs_dispatch": True,
        "recommended_crew": "Technical Maintenance Squad"
    },
    {
        "keywords": [r"pelouse", r"grass", r"pitch", r"field", r"moisture", r"turf", r"gazon", r"césped", r"sprinkler", r"arroseur", r"riego"],
        "category": "Pitch/Field",
        "severity": "Medium",
        "french_translation": "Pitch surface or turf integrity issue.",
        "spanish_translation": "Pitch surface or turf integrity issue.",
        "english_translation": "Field turf or irrigation issue reported.",
        "needs_dispatch": False,
        "recommended_crew": "Pitch Groundsman"
    }
]

def detect_language(text: str) -> str:
    text_lower = text.lower()
    # Simple heuristics for language detection
    french_words = ["évanouie", "évanouir", "panne", "ascenseur", "cassé", "bagarre", "porte", "foule", "eau", "pelouse", "gazon", "arroseur", "blessure"]
    spanish_words = ["desmayada", "desmayó", "pelea", "seguridad", "intruso", "médico", "agua", "césped", "riego", "herido", "luces", "molinete"]
    
    if any(word in text_lower for word in french_words):
        return "French 🇫🇷"
    elif any(word in text_lower for word in spanish_words):
        return "Spanish 🇪🇸"
    return "English 🇺🇸"

def parse_incident_report(report_text: str) -> str:
    """
    Parses unstructured multilingual volunteer incident reports into a structured JSON string.
    Implements Vanguard Pitch-Pilot system instructions using local parsing engine.
    """
    if not report_text or not report_text.strip():
        # Return empty structured schema
        empty_schema = {
            "detected_language": "Unknown",
            "category": "General",
            "severity": "Low",
            "english_translation": "",
            "needs_immediate_dispatch": False,
            "recommended_crew": "Standard Duty Crew"
        }
        return json.dumps(empty_schema, indent=4)

    text_lower = report_text.lower()
    lang = detect_language(report_text)
    
    parsed_category = "General"
    parsed_severity = "Low"
    parsed_translation = report_text
    needs_dispatch = False
    recommended_crew = "Standard Duty Crew"

    # Match rules
    for rule in RULES:
        match = False
        for kw in rule["keywords"]:
            if re.search(kw, text_lower):
                match = True
                break
        
        if match:
            parsed_category = rule["category"]
            parsed_severity = rule["severity"]
            needs_dispatch = rule["needs_dispatch"]
            recommended_crew = rule["recommended_crew"]
            
            if lang == "French 🇫🇷":
                parsed_translation = rule["french_translation"]
            elif lang == "Spanish 🇪🇸":
                parsed_translation = rule["spanish_translation"]
            else:
                parsed_translation = rule["english_translation"]
            break

    # If no rule matches, create a generic translation
    if parsed_category == "General":
        parsed_translation = f"[Translation Check Required] {report_text}"
        if len(report_text) > 30:
            parsed_severity = "Medium"
            needs_dispatch = True

    result = {
        "detected_language": lang,
        "category": parsed_category,
        "severity": parsed_severity,
        "english_translation": parsed_translation,
        "needs_immediate_dispatch": needs_dispatch,
        "recommended_crew": recommended_crew
    }
    
    return json.dumps(result, indent=4)
