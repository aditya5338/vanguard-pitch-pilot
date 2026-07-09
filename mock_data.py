# Seed data for Vanguard Pitch-Pilot (FIFA World Cup 2026 Stadium Management App)

INITIAL_GATES = [
    {
        "id": "Gate A",
        "name": "Gate A (North Terminal)",
        "capacity": 25000,
        "current_flow": 18200,
        "status": "Normal",
        "recommended_reroute": "Gate B",
    },
    {
        "id": "Gate B",
        "name": "Gate B (East Stand Link)",
        "capacity": 20000,
        "current_flow": 12500,
        "status": "Normal",
        "recommended_reroute": "Gate C",
    },
    {
        "id": "Gate C",
        "name": "Gate C (South Transit Hub)",
        "capacity": 30000,
        "current_flow": 28500,
        "status": "Heavy",
        "recommended_reroute": "Gate D",
    },
    {
        "id": "Gate D",
        "name": "Gate D (VIP & West plaza)",
        "capacity": 15000,
        "current_flow": 14200,
        "status": "Critical",
        "recommended_reroute": "Gate B",
    },
]

INITIAL_PITCH_ZONES = [
    {
        "zone": "North Goalmouth",
        "moisture": 62,
        "turf_wear": 15,
        "watering_schedule": "22:00 (Post-Match)",
        "lighting_schedule": "00:00 - 06:00 (UV Grow Lights)",
        "status": "Excellent",
    },
    {
        "zone": "South Goalmouth",
        "moisture": 58,
        "turf_wear": 22,
        "watering_schedule": "22:00 (Post-Match)",
        "lighting_schedule": "00:00 - 06:00 (UV Grow Lights)",
        "status": "Good",
    },
    {
        "zone": "Center Circle",
        "moisture": 48,
        "turf_wear": 35,
        "watering_schedule": "22:30 (Post-Match)",
        "lighting_schedule": "23:00 - 05:00 (UV Grow Lights)",
        "status": "Fair",
    },
    {
        "zone": "East Touchline",
        "moisture": 65,
        "turf_wear": 10,
        "watering_schedule": "21:30 (Post-Match)",
        "lighting_schedule": "None",
        "status": "Excellent",
    },
    {
        "zone": "West Touchline",
        "moisture": 64,
        "turf_wear": 12,
        "watering_schedule": "21:30 (Post-Match)",
        "lighting_schedule": "None",
        "status": "Excellent",
    },
]

INITIAL_STAFF = [
    {
        "name": "Diego Alvarez",
        "role": "Security Steward",
        "assigned_zone": "Gate C",
        "status": "On Duty",
        "phone": "+1 (555) 019-2834",
    },
    {
        "name": "Sarah Jenkins",
        "role": "Medical Responder",
        "assigned_zone": "Stand East",
        "status": "On Duty",
        "phone": "+1 (555) 014-9921",
    },
    {
        "name": "Yuki Tanaka",
        "role": "Concessions Lead",
        "assigned_zone": "Concession Row",
        "status": "On Duty",
        "phone": "+1 (555) 018-3829",
    },
    {
        "name": "Marc Dubois",
        "role": "Pitch Groundsman",
        "assigned_zone": "Pitch-side",
        "status": "On Duty",
        "phone": "+1 (555) 012-7744",
    },
    {
        "name": "Amara Diallo",
        "role": "Access Coordinator",
        "assigned_zone": "Gate A",
        "status": "On Break",
        "phone": "+1 (555) 015-8833",
    },
    {
        "name": "Carlos Gomez",
        "role": "Security Steward",
        "assigned_zone": "Gate D",
        "status": "On Duty",
        "phone": "+1 (555) 019-3388",
    },
    {
        "name": "Emma Watson",
        "role": "Crowd Control Steward",
        "assigned_zone": "Gate C",
        "status": "Off Duty",
        "phone": "+1 (555) 011-2299",
    },
]

INITIAL_CONCESSIONS = [
    {
        "vendor": "Burgers & Brews (North)",
        "stock_level": 85,
        "queue_time": 8,
        "revenue": 14250.0,
        "status": "Optimal",
    },
    {
        "vendor": "World Cup Merch (East)",
        "stock_level": 35,
        "queue_time": 22,
        "revenue": 38900.0,
        "status": "High Queue",
    },
    {
        "vendor": "FIFA Bites (South)",
        "stock_level": 12,
        "queue_time": 5,
        "revenue": 11800.0,
        "status": "Low Stock",
    },
    {
        "vendor": "Zero Waste Drinks (West)",
        "stock_level": 90,
        "queue_time": 4,
        "revenue": 8700.0,
        "status": "Optimal",
    },
]

INITIAL_INFRASTRUCTURE = [
    {
        "id": "ES-1",
        "name": "Escalator 1 (North Stand)",
        "type": "Escalator",
        "status": "Operational",
        "alternative_route": "Ramp A (adjacent)",
    },
    {
        "id": "ES-2",
        "name": "Escalator 2 (East Stand)",
        "type": "Escalator",
        "status": "Operational",
        "alternative_route": "Stairs 3 & Lift B",
    },
    {
        "id": "LF-A",
        "name": "Elevator A (VIP Suites)",
        "type": "Elevator",
        "status": "Operational",
        "alternative_route": "Elevator B (50m South) or Ramp C",
    },
    {
        "id": "RP-B",
        "name": "Ramp B (South Stand Link)",
        "type": "Ramp",
        "status": "Operational",
        "alternative_route": "Stairs 5 (non-ADA) or Lift D",
    },
    {
        "id": "LF-D",
        "name": "Lift D (West Accessibility Hub)",
        "type": "Elevator",
        "status": "Operational",
        "alternative_route": "Ramp D (Northside)",
    },
]

INITIAL_INCIDENTS = [
    {
        "id": "INC-001",
        "timestamp": "2026-07-09 04:32:00",
        "zone": "Gate D",
        "category": "Crowd Control",
        "description": "Minor bottleneck at turnstiles due to scanner ticket failures.",
        "severity": "Medium",
        "status": "Active",
        "reported_by": "Carlos Gomez",
    },
    {
        "id": "INC-002",
        "timestamp": "2026-07-09 04:55:00",
        "zone": "Stand East",
        "category": "Medical",
        "description": "Spectator experiencing heat exhaustion in Row 14.",
        "severity": "High",
        "status": "Active",
        "reported_by": "Sarah Jenkins",
    },
    {
        "id": "INC-003",
        "timestamp": "2026-07-09 05:05:00",
        "zone": "Concession Row",
        "category": "Infrastructure",
        "description": "Minor water leak near POS registers at FIFA Bites.",
        "severity": "Low",
        "status": "Active",
        "reported_by": "Yuki Tanaka",
    },
]

ROLE_CHECKLISTS = {
    "Security Steward": [
        "Inspect bag check scanners at assigned gate.",
        "Clear queue pathways and remove physical obstructions.",
        "Report ticket-validation scanner errors immediately.",
        "Maintain visual scan of crowd density at turnstiles.",
        "Ensure emergency exits remain unlocked and unobstructed."
    ],
    "Medical Responder": [
        "Check trauma kit and automated external defibrillator (AED) batteries.",
        "Maintain direct radio contact with Command Dispatch.",
        "Confirm clear paths to first aid stations in the sector.",
        "Perform routine rounds through upper and lower seating tiers.",
        "Pre-stage hydration packs for high-temperature areas."
    ],
    "Crowd Control Steward": [
        "Monitor queue barriers at external stadium perimeter gates.",
        "Guide incoming spectators toward lower-density turnstile channels.",
        "Communicate gate-closure warnings or rerouting instructions.",
        "Verify ADA accessibility pathways are clear and signed.",
        "Coordinate crowd flow dynamics during peak pre-kickoff hour."
    ],
    "Pitch Groundsman": [
        "Measure surface moisture across goalmouths and center circle.",
        "Inspect hybrid turf integrity post warm-up drills.",
        "Check water sprinkler pressure levels.",
        "Prepare pitch watering schedule based on relative humidity.",
        "Ensure pitch lines are clearly marked and goals are anchored."
    ],
    "Access Coordinator / Concessions Lead": [
        "Verify operational status of lifts and escalators in the zone.",
        "Coordinate VIP / wheelchair arrivals with transport handlers.",
        "Check stock levels of key food/beverage and merch categories.",
        "Report queue delays exceeding 15 minutes to Command Center.",
        "Ensure zero-waste bins are correctly positioned and labeled."
    ]
}

# Simple translation/AI engine mappings for UI demo
MOCK_TRANSLATION_RULES = [
    {
        "keywords": ["évanouie", "évanouir", "medical", "malade", "blessure", "ambulance", "heat", "sick", "pain", "chest", "desmayada", "desmayó", "médico", "corazón"],
        "category": "Medical",
        "severity": "High",
        "english_translation": "Spectator collapsed / medical emergency reported.",
        "dispatch_unit": "First Aid Crew Unit 3"
    },
    {
        "keywords": ["bagarre", "fight", "bataille", "vol", "securite", "sécurité", "violence", "pelea", "robo", "seguridad", "intruso", "intruder"],
        "category": "Security",
        "severity": "Critical",
        "english_translation": "Physical altercation / security breach reported.",
        "dispatch_unit": "Rapid Response Security Team B"
    },
    {
        "keywords": ["escalier", "escalator", "panne", "ascenseur", "cassé", "broken", "leak", "water", "fuite", "lumière", "light", "inondation", "sensor", "scanner"],
        "category": "Infrastructure",
        "severity": "Medium",
        "english_translation": "Infrastructure malfunction (escalator/elevator/scanner offline or leak).",
        "dispatch_unit": "Technical Maintenance Squad"
    },
    {
        "keywords": ["bouteille", "foule", "bloqué", "bloque", "gate", "porte", "crowd", "surge", "bottleneck", "embouteillage", "bouchon"],
        "category": "Crowd Control",
        "severity": "High",
        "english_translation": "Crowd congestion / gate bottleneck detected.",
        "dispatch_unit": "Gate Staff Redeployment Unit"
    }
]
