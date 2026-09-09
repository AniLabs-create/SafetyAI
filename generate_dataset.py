import random
import csv

random.seed(42)

# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

equipment_by_category = {
    "Equipment": ["a hydraulic press", "a conveyor belt", "an air compressor", "a packaging machine", "a lifting hoist"],
    "Electrical": ["an electrical panel", "a distribution board", "a control cabinet", "a set of wiring cables", "a junction box"],
    "Chemical": ["a chemical storage tank", "a drum of solvent", "a chemical mixing vessel", "a container of cleaning acid", "a pipeline carrying reagent"],
    "Fire": ["a fire extinguisher", "a fire alarm panel", "a sprinkler valve", "a flammable storage cabinet", "a smoke detector"],
    "Workplace": ["a break room", "an office workstation", "a shared corridor", "a loading dock", "a warehouse aisle"],
    "PPE": ["a set of safety goggles", "a pair of insulated gloves", "a hard hat", "a respirator mask", "a high-visibility vest"],
    "Maintenance": ["a bearing on the main motor", "a hydraulic hose", "a gearbox", "a filtration unit", "a cooling fan"],
    "Environmental": ["a wastewater discharge line", "an air scrubber", "a runoff collection pit", "an exhaust vent", "a storm drain"],
    "Ergonomics": ["a manual lifting station", "an assembly workbench", "a packing table", "a repetitive-motion workstation", "a seating arrangement"],
    "Slips and Falls": ["a warehouse floor", "a stairwell", "a loading ramp", "a walkway near the loading bay", "a tiled entrance area"],
    "Process Safety": ["a pressure relief valve", "a distillation column", "a reactor vessel", "a steam boiler", "a process control loop"],
    "Emergency": ["an emergency exit", "a fire assembly point", "an emergency shutdown switch", "an evacuation route", "a first-aid station"],
    "Machinery": ["a CNC milling machine", "a stamping press", "a forklift", "a rotating drum mixer", "a band saw"],
    "Structural": ["a mezzanine platform", "a support beam", "a roof truss", "a loading dock canopy", "a storage rack"],
    "Housekeeping": ["a storage shelf", "a walkway", "a break area", "a tool cabinet", "a supply closet"],
}

locations = [
    "in the main production area", "near the loading dock", "on the second floor",
    "in the north warehouse", "close to the maintenance workshop", "in the packaging line",
    "along the east corridor", "in the outdoor storage yard", "near the boiler room",
    "in the quality control lab", "next to the employee break area", "in the shipping bay",
    "on the mezzanine level", "in the chemical storage room", "near the emergency exit",
]

times = [
    "during the morning shift", "during a routine inspection", "while performing a safety walk-through",
    "at the start of the night shift", "during a scheduled maintenance check",
    "while responding to a reported noise", "during a weekly audit", "after a shift change",
    "while reviewing equipment logs", "during a spot check",
]

actions = ["reported", "isolated", "repaired", "inspected", "ignored", "delayed", "escalated", "monitored", "shut down", "secured"]

# ---------------------------------------------------------------------------
# LOW risk sentence templates
# ---------------------------------------------------------------------------

low_templates = [
    "A minor scuff mark was noticed on {equip} {loc} {time}. No functional impact was observed and the item was noted for future reference.",
    "{Equip} showed slight cosmetic wear {loc}. The issue was documented but does not affect normal operation.",
    "A small amount of dust accumulation was found near {equip} {loc}. Housekeeping staff cleaned the area shortly after it was {action}.",
    "{Time2cap}, {equip} was found slightly out of alignment. The condition was corrected on the spot and no further action was needed.",
    "A label on {equip} {loc} had become faded and was replaced during routine upkeep.",
    "An employee noted that {equip} made a brief unusual sound {time}, but on inspection no defect was found.",
    "A minor spill of water, unrelated to any hazardous material, was quickly wiped up near {equip} {loc}.",
    "{Equip} was found to be slightly loose {loc}, and was tightened immediately with no disruption to work.",
    "A routine check {time} confirmed that {equip} is functioning within normal parameters, with only a small cosmetic flaw noted.",
    "Staff observed that a walkway sign {loc} had fallen over; it was picked up and reset without incident.",
    "A minor paint chip was noted on {equip} {loc}, considered a cosmetic issue with no safety implication.",
    "{Equip} was cleaned and returned to service after a light residue was noticed {time}.",
    "An extra box of supplies was temporarily stored {loc}; it was moved to proper storage the same day.",
    "A light bulb flickered briefly near {equip} {loc} and was replaced during the next maintenance round.",
    "{Equip} passed its scheduled inspection {time} with only a trivial note about surface wear.",
    "A small puddle of condensation was observed near {equip} {loc} and evaporated before any action was required.",
    "Employees {action} a slightly bent guard rail {loc}; it was already scheduled for cosmetic repair.",
    "A minor tripping hazard, a loose floor tile, was {action} and corrected the same afternoon {loc}.",
    "{Equip} required a routine cleaning {time} after light dust buildup was noted, with no operational concern.",
    "A short delay in restocking PPE supplies {loc} was noted and resolved before the next shift began.",
]

# ---------------------------------------------------------------------------
# MEDIUM risk sentence templates
# ---------------------------------------------------------------------------

medium_templates = [
    "{Equip} was found operating at elevated temperature {loc} {time}. The unit was {action} pending further evaluation.",
    "An employee working {loc} was observed without a required piece of PPE. The worker was reminded and the incident was {action}.",
    "{Equip} showed visible wear that reduces efficiency but does not present immediate danger; the issue was {action} and a repair has been scheduled.",
    "A slippery patch was identified {loc}, likely caused by a minor leak from {equip}, and was marked with a warning sign.",
    "Maintenance on {equip} has been {action} twice this month, raising concern about its reliability.",
    "{Equip} displayed abnormal vibration {time}. The equipment remains in use but has been flagged for closer monitoring.",
    "A minor electrical concern was noted near {equip} {loc}, including a warm junction that was {action} for inspection.",
    "Repeated minor spills have occurred near {equip} {loc}, and the area has been {action} for a deeper review.",
    "{Equip} was found with a damaged but still functional guard {loc}. It remains operable while a replacement part is ordered.",
    "A worker reported mild discomfort after an extended shift working at {equip} {loc}, prompting a review of the workstation setup.",
    "{Equip} pressure readings were slightly above the normal range {time}, and the unit was {action} for a closer look.",
    "An incomplete set of PPE was found stored {loc}; missing items were flagged and additional inspection was requested.",
    "{Equip} required temporary bypass of a secondary safety feature {loc}, which was {action} and scheduled for prompt correction.",
    "A recurring minor hazard involving loose cabling near {equip} was {action} after being noticed for the third time this month.",
    "The ventilation system {loc} was found operating below expected capacity, and the issue was {action} for follow-up.",
    "{Equip} exhibited an unusual odor {time}; operations continued at reduced capacity while the cause was {action}.",
    "A supervisor noted that scheduled maintenance on {equip} {loc} has been {action} beyond the recommended window.",
    "Moisture buildup was observed inside {equip} {loc}, raising concern about corrosion if left unaddressed.",
    "A worker was seen bypassing a lockout procedure briefly on {equip}; the behavior was {action} and addressed with retraining.",
    "{Equip} showed a hairline crack in a non-critical component {loc}, and use has been restricted until it is {action}.",
]

# ---------------------------------------------------------------------------
# HIGH risk sentence templates
# ---------------------------------------------------------------------------

high_templates = [
    "A significant leak from {equip} {loc} released hazardous material before it could be fully {action}, posing a serious exposure risk.",
    "Live electrical components on {equip} were found exposed {loc}, creating an immediate electrocution hazard until the area was {action}.",
    "{Equip} suffered a severe mechanical failure {time}, sending debris across the surrounding area and requiring an emergency shutdown.",
    "A fire hazard was identified near {equip} {loc} after flammable material was found stored improperly close to an ignition source.",
    "The emergency exit {loc} was found completely blocked during a simulated evacuation, delaying evacuation by several minutes.",
    "Critical safety guards on {equip} were missing {time}, allowing direct access to moving parts during operation.",
    "Multiple prior warnings about {equip} were ignored, resulting in a serious failure that required the line to be {action} immediately.",
    "A structural crack was discovered in {equip} {loc}, raising concern of imminent collapse under normal load.",
    "Uncontrolled release of chemical vapor from {equip} forced an immediate evacuation of the surrounding work area.",
    "A worker narrowly avoided serious injury when {equip} activated unexpectedly {loc} due to a bypassed interlock.",
    "Critical maintenance on {equip} has been delayed repeatedly despite escalating warning signs, and it was finally {action} only after a near-miss.",
    "{Equip} showed a dangerous pressure spike {time}, and the system was {action} to prevent a potential rupture.",
    "Dangerous machinery {loc} was found operating without required guarding, exposing workers to a serious risk of amputation.",
    "A chemical container ruptured {loc}, spilling hazardous contents into a drainage area before containment teams {action} the site.",
    "An electrical fault caused visible sparking from {equip} {loc}, prompting an emergency shutdown of the entire section.",
    "An operator continued working despite a known brake failure on {equip}, an issue that had been {action} but not repaired.",
    "Toxic fumes were detected {loc} after {equip} malfunctioned, requiring respiratory protection and immediate evacuation.",
    "A load being lifted by {equip} shifted unexpectedly {loc}, nearly striking two workers before the operation was {action}.",
    "Severe corrosion was found on {equip} {loc}, compromising structural integrity and posing a risk of sudden failure.",
    "A gas leak from {equip} triggered the facility's alarm system {loc}, and emergency responders were called in as the area was {action}.",
]

# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------

def fill(template, category, allowed_actions=None):
    equip = random.choice(equipment_by_category[category])
    loc = random.choice(locations)
    time = random.choice(times)
    time2 = random.choice(times)
    action = random.choice(allowed_actions if allowed_actions else actions)
    text = template.format(
        equip=equip,
        Equip=equip[0].upper() + equip[1:],
        loc=loc,
        time=time,
        time2=time2,
        Time2cap=time2[0].upper() + time2[1:],
        action=action,
    )
    return text

categories = list(equipment_by_category.keys())

# Some templates only make semantic sense with certain categories of equipment
# (e.g. "pressure spike" fits pressurized/mechanical equipment, not PPE).
TEMPLATE_CATEGORY_RESTRICTIONS = {
    "Uncontrolled release of chemical vapor from {equip} forced an immediate evacuation of the surrounding work area.":
        ["Chemical", "Process Safety", "Environmental"],
    "{Equip} showed a dangerous pressure spike {time}, and the system was {action} to prevent a potential rupture.":
        ["Process Safety", "Equipment", "Maintenance", "Machinery"],
    "An operator continued working despite a known brake failure on {equip}, an issue that had been {action} but not repaired.":
        ["Machinery", "Equipment", "Maintenance"],
    "A gas leak from {equip} triggered the facility's alarm system {loc}, and emergency responders were called in as the area was {action}.":
        ["Chemical", "Process Safety", "Environmental", "Fire"],
    "Toxic fumes were detected {loc} after {equip} malfunctioned, requiring respiratory protection and immediate evacuation.":
        ["Chemical", "Process Safety", "Environmental", "Fire"],
    "A load being lifted by {equip} shifted unexpectedly {loc}, nearly striking two workers before the operation was {action}.":
        ["Machinery", "Equipment", "Maintenance"],
    "Live electrical components on {equip} were found exposed {loc}, creating an immediate electrocution hazard until the area was {action}.":
        ["Electrical", "Equipment", "Machinery", "Maintenance"],
    "A structural crack was discovered in {equip} {loc}, raising concern of imminent collapse under normal load.":
        ["Structural", "Equipment", "Machinery", "Process Safety"],
    "Dangerous machinery {loc} was found operating without required guarding, exposing workers to a serious risk of amputation.":
        ["Machinery", "Equipment", "Maintenance"],
    "The emergency exit {loc} was found completely blocked during a simulated evacuation, delaying evacuation by several minutes.":
        ["Emergency", "Fire", "Workplace"],
    "A chemical container ruptured {loc}, spilling hazardous contents into a drainage area before containment teams {action} the site.":
        ["Chemical", "Environmental", "Process Safety"],
    "Staff observed that a walkway sign {loc} had fallen over; it was picked up and reset without incident.":
        ["Housekeeping", "Slips and Falls", "Workplace"],
    "An extra box of supplies was temporarily stored {loc}; it was moved to proper storage the same day.":
        ["Housekeeping", "Workplace"],
    "A minor tripping hazard, a loose floor tile, was {action} and corrected the same afternoon {loc}.":
        ["Slips and Falls", "Housekeeping"],
    "A short delay in restocking PPE supplies {loc} was noted and resolved before the next shift began.":
        ["PPE", "Housekeeping"],
    "An incomplete set of PPE was found stored {loc}; missing items were flagged and additional inspection was requested.":
        ["PPE", "Housekeeping"],
    "An electrical fault caused visible sparking from {equip} {loc}, prompting an emergency shutdown of the entire section.":
        ["Electrical", "Equipment", "Machinery", "Maintenance"],
}

TEMPLATE_ACTION_RESTRICTIONS = {
    "An employee working {loc} was observed without a required piece of PPE. The worker was reminded and the incident was {action}.":
        ["reported", "escalated", "monitored"],
    "Critical maintenance on {equip} has been delayed repeatedly despite escalating warning signs, and it was finally {action} only after a near-miss.":
        ["repaired", "inspected", "escalated", "secured", "shut down"],
}
# clean up: only keep actions that actually exist in the master action list
TEMPLATE_ACTION_RESTRICTIONS = {
    k: [a for a in v if a in actions] for k, v in TEMPLATE_ACTION_RESTRICTIONS.items()
}

def generate_set(templates, risk_label, target_count, global_seen):
    results = []
    seen_texts = set()
    attempts = 0
    while len(results) < target_count and attempts < target_count * 200:
        attempts += 1
        template = random.choice(templates)
        allowed = TEMPLATE_CATEGORY_RESTRICTIONS.get(template, categories)
        category = random.choice(allowed)
        text = fill(template, category, TEMPLATE_ACTION_RESTRICTIONS.get(template))
        if text not in seen_texts and text not in global_seen:
            seen_texts.add(text)
            global_seen.add(text)
            results.append((text, category, risk_label))
    return results

global_seen = set()
low_rows = generate_set(low_templates, "LOW", 100, global_seen)
medium_rows = generate_set(medium_templates, "MEDIUM", 100, global_seen)
high_rows = generate_set(high_templates, "HIGH", 100, global_seen)

all_rows = low_rows + medium_rows + high_rows

final_rows = all_rows
random.shuffle(final_rows)

print("Total rows:", len(final_rows))
from collections import Counter
print(Counter([r[2] for r in final_rows]))

with open("data/safety_reports.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["report_text", "category", "risk_label"])
    for row in final_rows:
        writer.writerow(row)