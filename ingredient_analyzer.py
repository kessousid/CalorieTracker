# Ingredient analyzer for health assessment
import json
from pathlib import Path

# ─── Unhealthy additives & ingredients to flag ──────────────────────────────
UNHEALTHY_ADDITIVES = {
    # Flavor enhancers (MSG, nucleotides)
    "INS 635": {"concern": "Flavor enhancer (sodium inosinate)", "severity": "medium"},
    "INS 631": {"concern": "Flavor enhancer (disodium inosinate)", "severity": "medium"},
    "INS 627": {"concern": "Flavor enhancer (guanosine 5'-disodium phosphate)", "severity": "medium"},
    "MSG": {"concern": "Monosodium glutamate - can cause headaches/sensitivity", "severity": "medium"},
    "monosodium glutamate": {"concern": "MSG - can cause headaches/sensitivity", "severity": "medium"},

    # High GI carbs & sugar
    "maltodextrin": {"concern": "High GI, rapid blood sugar spike", "severity": "medium"},
    "corn syrup": {"concern": "High fructose, linked to metabolic issues", "severity": "high"},
    "high fructose corn syrup": {"concern": "HFCS - metabolic stress", "severity": "high"},
    "added sugar": {"concern": "Empty calories, tooth decay, weight gain risk", "severity": "high"},
    "sugar": {"concern": "Added sugar - excess consumption harmful", "severity": "medium"},
    "refined sugar": {"concern": "Refined sugar - quick blood sugar spike", "severity": "high"},

    # Artificial sweeteners
    "aspartame": {"concern": "Artificial sweetener - controversial safety", "severity": "low"},
    "sucralose": {"concern": "Artificial sweetener - may affect gut bacteria", "severity": "low"},
    "saccharin": {"concern": "Artificial sweetener - older generation", "severity": "low"},
    "acesulfame-k": {"concern": "Artificial sweetener - limited studies", "severity": "low"},

    # Trans fats & problematic oils
    "trans fat": {"concern": "Trans fats - increase bad cholesterol", "severity": "high"},
    "partially hydrogenated": {"concern": "Source of trans fats", "severity": "high"},
    "vegetable shortening": {"concern": "Often contains trans fats", "severity": "high"},

    # Preservatives
    "BHA": {"concern": "Butylated hydroxyanisole - potential carcinogen", "severity": "high"},
    "BHT": {"concern": "Butylated hydroxytoluene - potential carcinogen", "severity": "high"},
    "sodium benzoate": {"concern": "Preservative - may cause hyperactivity in sensitive individuals", "severity": "low"},
    "potassium sorbate": {"concern": "Preservative - generally safe but worth monitoring", "severity": "low"},
    "sodium nitrite": {"concern": "Preservative - can form carcinogens when heated", "severity": "medium"},
    "sodium nitrate": {"concern": "Preservative - can form carcinogens when heated", "severity": "medium"},

    # Colors & dyes
    "tartrazine": {"concern": "Yellow dye (INS 102) - allergen for some, linked to hyperactivity", "severity": "medium"},
    "sunset yellow": {"concern": "Orange dye (INS 110) - potential allergen", "severity": "medium"},
    "allura red": {"concern": "Red dye (INS 129) - synthetic dye, potential hyperactivity link", "severity": "medium"},
    "FD&C": {"concern": "Synthetic food coloring", "severity": "low"},

    # Other concerning additives
    "caramel coloring": {"concern": "May contain carcinogenic compounds", "severity": "low"},
    "titanium dioxide": {"concern": "White pigment - nanoparticles raise concerns", "severity": "low"},
    "potassium bromate": {"concern": "Dough conditioner - potential toxin", "severity": "high"},

    # Hydrogenated oils
    "hydrogenated vegetable oil": {"concern": "Trans fat source", "severity": "high"},
    "hydrogenated palm oil": {"concern": "Trans fat source + environmental concern", "severity": "high"},

    # GMO & pesticides (if marked)
    "GMO": {"concern": "Genetically modified - controversial", "severity": "low"},
}

# Foods that naturally contain concerning items (not to flag)
NATURAL_EXCEPTIONS = {
    "sugar": ["fruits", "milk", "honey", "jaggery"],  # naturally occurring sugars
    "salt": ["all foods"],  # natural/added hard to distinguish
}

def load_ingredients_db():
    """Load ingredient database from JSON file."""
    db_path = Path(__file__).parent / "ingredients_db.json"
    if db_path.exists():
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_ingredients(food_name: str) -> list:
    """Get ingredients for a food from the database."""
    db = load_ingredients_db()
    food_lower = food_name.lower()

    for key, data in db.items():
        if key.lower() == food_lower:
            return data.get("ingredients", [])
    return []

def analyze_health(food_name: str, ingredients: list = None) -> dict:
    """
    Analyze ingredients for unhealthy additives.

    Returns:
    {
        "health_status": "green" | "yellow" | "red",
        "concerns": [{"additive": "...", "concern": "...", "severity": "..."}],
        "recommendation": "...",
        "score": 0-10
    }
    """
    if ingredients is None:
        ingredients = get_ingredients(food_name)

    if not ingredients:
        return {
            "health_status": "gray",
            "concerns": [],
            "recommendation": "No ingredient data available",
            "score": None,
        }

    ingredients_lower = [ing.lower() for ing in ingredients]
    found_concerns = []
    severity_counts = {"high": 0, "medium": 0, "low": 0}

    # Check each ingredient against unhealthy list
    for additive, info in UNHEALTHY_ADDITIVES.items():
        additive_lower = additive.lower()

        for ing in ingredients_lower:
            if additive_lower in ing:
                # Check if it's a natural exception
                is_exception = False
                if additive in NATURAL_EXCEPTIONS:
                    # For now, we'll flag all—user can customize exceptions
                    pass

                if not is_exception:
                    found_concerns.append({
                        "additive": additive,
                        "concern": info["concern"],
                        "severity": info["severity"],
                    })
                    severity_counts[info["severity"]] += 1
                    break

    # Determine health status & score
    if severity_counts["high"] > 0:
        health_status = "red"
        score = 3
        recommendation = "⚠️ Contains additives of concern. Consider alternatives or consume in moderation."
    elif severity_counts["medium"] > 1:
        health_status = "red"
        score = 4
        recommendation = "⚠️ Multiple moderate concerns. Moderation advised."
    elif severity_counts["medium"] > 0:
        health_status = "yellow"
        score = 6
        recommendation = "⚠️ Some additives flagged. Check ingredient list for your comfort."
    elif severity_counts["low"] > 0:
        health_status = "yellow"
        score = 7
        recommendation = "ℹ️ Minor concerns noted. Generally acceptable."
    else:
        health_status = "green"
        score = 9
        recommendation = "✅ Clean ingredient profile. Good choice!"

    return {
        "health_status": health_status,
        "concerns": found_concerns,
        "recommendation": recommendation,
        "score": score,
    }

def get_health_badge_html(health_status: str, score: int = None) -> str:
    """Generate HTML badge for health status."""
    colors = {
        "green": "#10B981",
        "yellow": "#F59E0B",
        "red": "#EF4444",
        "gray": "#94A3B8",
    }
    icons = {
        "green": "✅",
        "yellow": "⚠️",
        "red": "🚫",
        "gray": "❓",
    }
    labels = {
        "green": "Healthy",
        "yellow": "Moderate",
        "red": "Concerning",
        "gray": "Unknown",
    }

    color = colors.get(health_status, colors["gray"])
    icon = icons.get(health_status, "?")
    label = labels.get(health_status, "Unknown")
    score_text = f" ({score}/10)" if score else ""

    return f"""
    <span style="
        background:{color}18;color:{color};font-size:0.7rem;
        font-weight:700;padding:0.2rem 0.6rem;border-radius:999px;
        border:1px solid {color}40;white-space:nowrap;display:inline-block;
    ">{icon} {label}{score_text}</span>
    """

def get_concerns_html(concerns: list) -> str:
    """Generate markdown for concern list."""
    if not concerns:
        return ""

    severity_emoji = {
        "high": "🚫",
        "medium": "🟡",
        "low": "ℹ️",
    }

    markdown = "\n**Concerns Found:**\n"
    for c in concerns:
        emoji = severity_emoji.get(c["severity"], "•")
        sev = c["severity"].upper()
        markdown += f"\n{emoji} **{c['additive']}** ({sev})\n"
        markdown += f"> {c['concern']}\n"

    return markdown
