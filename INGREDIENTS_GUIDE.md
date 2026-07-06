# Ingredient Health Analysis System

This CalorieTracker now includes an automatic ingredient analyzer that flags unhealthy additives when you select a food.

## How It Works

1. **When you select a food** in the "Add Food Entry" section, the app automatically looks up its ingredients
2. **Ingredients are checked** against a database of unhealthy additives (MSG, maltodextrin, artificial sweeteners, trans fats, etc.)
3. **A health badge appears** showing:
   - 🟢 **Green (9/10)**: Clean ingredient profile
   - 🟡 **Yellow (6-7/10)**: Some additives flagged, moderation advised
   - 🔴 **Red (3-4/10)**: Multiple concerns or high-severity additives
   - 🔲 **Gray**: No ingredient data available

4. **Flagged ingredients are listed** with severity levels (high/medium/low)

## Example Results

| Food | Status | Score | Key Concerns |
|------|--------|-------|--------------|
| Idli | 🟢 Green | 9/10 | None - traditional recipe |
| Masala Dosa | 🟢 Green | 9/10 | None - fresh spices |
| Cola (Pepsi/Coke) | 🔴 Red | 3/10 | Added sugar, artificial sweetener, caramel coloring |
| Maggi Noodles | 🔴 Red | 2/10 | MSG, maltodextrin, artificial flavor, preservatives |
| Flavored Yogurt | 🟡 Yellow | 6/10 | Added sugar |
| Cornflakes | 🟡 Yellow | 5/10 | Added sugar, refined grains |

## Expanding the Ingredient Database

The ingredient data is stored in `ingredients_db.json`. You can add or update foods easily:

### Add a New Food

```json
{
  "Your Food Name": {
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
    "category": "Breakfast",
    "notes": "Optional description"
  }
}
```

### Example

```json
{
  "Horlicks with Milk": {
    "ingredients": ["milk", "horlicks malt powder", "sugar", "added sugar", "vitamins", "minerals"],
    "category": "Beverage",
    "notes": "Malted drink - contains added sugar"
  }
}
```

### Guidelines for Ingredients List

1. **Be specific**: Use ingredient names that appear on actual labels
2. **List actual ingredients**: Not just "flour" but "wheat flour" or "refined wheat flour"
3. **Include additives**: If the food contains artificial additives, list them
4. **Use lowercase**: Ingredient names should be lowercase for consistent matching
5. **Common format examples**:
   - Spices: "turmeric", "cumin", "cardamom", "ginger"
   - Flours: "wheat flour", "rice flour", "gram flour"
   - Additives: "MSG", "maltodextrin", "added sugar", "artificial flavor"
   - Oils: "palm oil", "refined vegetable oil", "ghee"

## Flagged Additives & Concerns

### High Severity (⚠️ Avoid)
- **Trans fats**: Linked to cardiovascular disease
- **MSG (INS codes 627, 631, 635)**: Flavor enhancers - can cause headaches
- **High fructose corn syrup**: Metabolic stress
- **BHA/BHT**: Potential carcinogens
- **Potassium bromate**: Dough conditioner toxin
- **Sodium nitrite/nitrate**: Can form carcinogens when heated

### Medium Severity (⚠️ Limit)
- **Maltodextrin**: High GI, rapid blood sugar spike
- **Added/refined sugar**: Empty calories, weight gain
- **Sodium benzoate**: May cause hyperactivity in sensitive people
- **Tartrazine/Sunset Yellow**: Dyes - potential allergens

### Low Severity (ℹ️ Note)
- **Artificial sweeteners**: Limited studies on long-term effects
- **Titanium dioxide**: Nanoparticles raise concerns
- **GMO**: Controversial but not definitively harmful
- **Caramel coloring**: May contain carcinogenic compounds

## Updating Foods with Missing Data

If a food shows "Unknown" (gray badge), you can add ingredients:

1. **Look up the product label** or packaging
2. **Find the food in `ingredients_db.json`**
3. **Add the ingredients list**
4. **Save the file** - changes take effect immediately

### Example: Adding Ingredients to an Existing Food

**Before:**
```json
"Bournvita with Milk": {
  "ingredients": [],
  "category": "Beverage"
}
```

**After:**
```json
"Bournvita with Milk": {
  "ingredients": ["milk", "bournvita powder", "sugar", "added sugar", "cocoa", "vitamins"],
  "category": "Beverage",
  "notes": "Chocolate drink - high sugar"
}
```

## Tips for Building Accurate Data

1. **For packaged foods**: Read the actual label
2. **For restaurant/home dishes**: List typical ingredients used
3. **For regional dishes**: List traditional ingredients (no additives for authentic recipes)
4. **For branded products**: Check the brand's official nutrition/ingredient list
5. **When in doubt**: Leave empty rather than guess

## Common Indian Food Ingredients

### Breakfast Items
- Urad dal, rice, salt, asafoetida, mustard seeds, curry leaves, turmeric, oil

### Dals & Curries
- Toor dal, moong dal, masoor dal, tomato, onion, ginger, garlic, turmeric, spices, salt, oil

### Breads
- Wheat flour, salt, water, oil/ghee, yeast (for leavened breads)

### Beverages
- Tea leaves, coffee powder, milk, sugar, spices

### Snacks (Traditional)
- Gram flour, vegetables, mustard seeds, curry leaves, salt, oil

### Modern/Packaged (Often High Additives)
- Check packaging for: MSG, maltodextrin, artificial flavor, preservatives, added sugar

## Tips for Healthier Choices

✅ **Prefer:**
- Traditional homemade recipes (no additives)
- Whole grains and millets
- Fresh vegetables and legumes
- Natural sweeteners (jaggery, honey - in moderation)
- Minimal oil cooking (steamed, boiled)

❌ **Limit:**
- Instant noodles (high MSG and additives)
- Processed snacks with multiple artificial ingredients
- Deep-fried foods with hydrogenated oils
- Foods with added sugars and artificial sweeteners
- Packaged foods with long ingredient lists

## Questions or Issues?

If you find:
1. **Incorrect ingredient data** - Update it in the JSON file
2. **A food missing ingredients** - Add them following the guidelines above
3. **An additive not flagged** - Check if it should be added to `UNHEALTHY_ADDITIVES` in `ingredient_analyzer.py`

Remember: This is a tool to help make informed choices, not medical advice. Consult a nutritionist for personalized dietary guidance.
