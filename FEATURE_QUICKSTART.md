# 🏥 Ingredient Health Analysis - Quick Start

## What You Get

When you log a food, you now see:

```
🟢 Healthy (9/10)  |  🟡 Moderate (6/10)  |  🔴 Concerning (3/10)  |  🔲 Unknown
✅ Clean ingredients  |  ⚠️ Some additives  |  🚫 Major concerns  |  ❓ No data
```

---

## Examples

### Good Choices (Green 🟢)
| Food | Score | Why |
|------|-------|-----|
| Idli | 9/10 | Traditional steamed cake - just rice, dal, salt |
| Dal Tadka | 9/10 | Whole lentils with basic spices |
| Roti | 9/10 | Wheat flour, salt, water, oil |
| Sambar | 9/10 | Lentil stew with natural ingredients |

### Moderate Choices (Yellow 🟡)
| Food | Score | Concern |
|------|-------|---------|
| Flavored Yogurt | 6/10 | Added sugar |
| Cornflakes | 5/10 | Added sugar + refined grains |
| Horlicks | 5/10 | Malted drink with added sugar |

### Avoid (Red 🔴)
| Food | Score | Concerns |
|------|-------|----------|
| Cola (Pepsi/Coke) | 3/10 | Added sugar, artificial sweetener, caramel coloring |
| Maggi Noodles | 3/10 | MSG, maltodextrin, artificial flavor, preservatives |
| Packaged Juice | 3/10 | High added sugar, preservatives |
| Cheese Slice | 4/10 | Emulsifiers, preservatives, artificial color |

---

## How to Use

### Step 1: Open App
```
streamlit run app.py
```

### Step 2: Add Food
- Click "Add Food Entry"
- Select meal period
- Choose food by category or search

### Step 3: See Health Analysis
- Health badge appears automatically ✨
- Read the recommendation
- Check flagged ingredients (if any)

### Step 4: Make Decision
- 🟢 Green → Safe, go ahead
- 🟡 Yellow → Okay in moderation
- 🔴 Red → Consider alternatives
- 🔲 Gray → No ingredient data (add it!)

---

## Adding Missing Ingredients

**Found a food with no data (🔲)? Add it!**

1. Open `ingredients_db.json`
2. Find your food (or add it)
3. Add ingredients list:

```json
{
  "Your Food": {
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
    "category": "Category",
    "notes": "Optional"
  }
}
```

**Example:**
```json
{
  "Yogabar High Protein Oats - Chocolate": {
    "ingredients": ["oats", "almonds", "cocoa", "natural flavors"],
    "category": "Breakfast",
    "notes": "Check for added sugar"
  }
}
```

4. Save file → Changes apply immediately ✅

---

## What's Flagged?

### ⚠️ High Severity (Avoid)
- Trans fats / Hydrogenated oils
- MSG & flavor enhancers (INS 627, 631, 635)
- BHA / BHT (preservatives)
- Potassium bromate
- High fructose corn syrup
- Sodium nitrite/nitrate

### 🟡 Medium Severity (Limit)
- Added sugar / Refined sugar
- Maltodextrin
- Artificial colors (Tartrazine, Sunset Yellow, etc.)
- Sodium benzoate
- Caramel coloring

### ℹ️ Low Severity (Monitor)
- Artificial sweeteners (Aspartame, Sucralose)
- Emulsifiers
- Titanium dioxide
- GMO ingredients

---

## Pro Tips

### Traditional Indian Foods (Usually Green ✅)
- Homemade curries
- Steamed/boiled items
- Breads (Roti, Naan, Paratha)
- Dals and legumes
- Regional specialties

### Packaged/Branded (Often Red 🔴)
- Instant noodles
- Soft drinks
- Packaged snacks
- Processed cereals
- Flavored drinks

### Better Alternatives

| Instead Of | Choose |
|-----------|--------|
| Cola | Water, fresh juice, herbal tea |
| Maggi Noodles | Homemade noodles, roti, rice |
| Packaged Juice | Fresh fruit, fresh juices |
| Cornflakes | Oats, ragi, traditional breakfast |
| Flavored Yogurt | Plain yogurt + fresh fruit |

---

## Test It Out

Try these to see the system in action:

### See a Red Status:
- Search: "Cola (Pepsi / Coke)"
- Or: "Maggi Noodles (1 pack cooked)"

### See a Green Status:
- Search: "Idli"
- Or: "Dal Tadka"
- Or: "Roti / Chapati"

---

## Questions?

📖 **Read more**: Check `INGREDIENTS_GUIDE.md` for detailed information

🔧 **Troubleshoot**: Make sure `ingredients_db.json` is valid (use an online JSON validator)

➕ **Add data**: Follow the format in `ingredients_db.json` - spaces and structure matter!

---

**Remember**: This is a tool to help you make informed choices. For personalized dietary advice, consult a qualified nutritionist or healthcare professional. 💚
