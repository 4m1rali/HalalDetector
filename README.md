# Quran - AI Halal/Haram Detection Library

Simple Python library for detecting halal and haram food items using AI technology.

## Quick Start

```bash
pip install -r requirements.txt
```

```python
from quran import HalalDetector

detector = HalalDetector()

print(detector.is_halal("chicken"))  # True
print(detector.is_haram("pork"))     # True
print(detector.quick_check("gelatin"))  # "Questionable"
```

## Simple Usage

### Basic Detection
```python
detector = HalalDetector()

# True/False checks
detector.is_halal("beef")        # True
detector.is_haram("pork")        # True
detector.is_questionable("gelatin")  # True

# Quick status
detector.quick_check("chicken")  # "Halal"
detector.get_halal_score("beef") # 100
```

### Recipe Analysis
```python
ingredients = ["chicken", "rice", "vegetables", "spices"]
result = detector.analyze_recipe("Chicken Biryani", ingredients)

print(result["overall_status"])      # "Halal"
print(result["halal_percentage"])    # 100.0
print(result["safe_ingredients"])    # ["chicken", "rice", "vegetables", "spices"]
```

### Ingredient Lists
```python
ingredients = ["beef", "pork", "chicken", "gelatin"]

# Find problematic ingredients
haram = detector.find_haram_ingredients(ingredients)        # ["pork"]
questionable = detector.find_questionable_ingredients(ingredients)  # ["gelatin"]
safe = detector.get_safe_ingredients(ingredients)           # ["beef", "chicken"]

# Check all at once
statuses = detector.check_ingredients_list(ingredients)
# {"beef": "Halal", "pork": "Haram", "chicken": "Halal", "gelatin": "Questionable"}
```

### Meat Types
```python
# Built-in meat lists
halal_meats = detector.get_halal_meat_types()  # ["beef", "lamb", "chicken", ...]
haram_meats = detector.get_haram_meat_types()  # ["pork", "bacon", "ham", ...]

# Quick meat check
detector.is_meat_halal("beef")   # True
detector.is_meat_halal("pork")   # False
```

### Restaurant & Brand Checks
```python
# Restaurant verification
restaurant = detector.check_restaurant_halal("McDonald's", "New York")
print(restaurant["is_halal"])  # True/False

# Brand certification
brands = detector.get_halal_certified_brands("food")
print(brands)  # ["Brand1", "Brand2", ...]

# Product certification
cert = detector.verify_certification("Nestle", "KitKat")
print(cert["has_certification"])  # True/False
```

### Certificate Validation
```python
cert = detector.validate_halal_certificate("HC123456", "HFS")
print(cert["is_valid"])      # True/False
print(cert["expiry_date"])   # "2024-12-31"
print(cert["status"])        # "active"
```

## All Methods

### Simple Detection
- `is_halal(item)` → bool
- `is_haram(item)` → bool  
- `is_questionable(item)` → bool
- `quick_check(item)` → str
- `get_halal_score(item)` → int (0-100)

### Detailed Analysis
- `detect_ingredient(ingredient, context)` → dict
- `detect_food_item(food_name, preparation_method, region)` → dict
- `analyze_recipe(name, ingredients)` → dict

### Advanced Analysis
- `advanced_ingredient_analysis(ingredient, source_country, processing_method)` → dict
- `detect_food_additives(additives)` → dict
- `check_halal_compliance_score(item, category)` → dict
- `detect_alcohol_content(item, alcohol_percentage)` → dict

### List Processing
- `check_ingredients_list(ingredients)` → dict
- `find_haram_ingredients(ingredients)` → list
- `find_questionable_ingredients(ingredients)` → list
- `get_safe_ingredients(ingredients)` → list
- `batch_detect(items, type)` → list

### Restaurant & Chain Analysis
- `check_restaurant_halal(name, location)` → dict
- `check_restaurant_chain_halal(chain_name, location, menu_items)` → dict

### Supply Chain & Certification
- `analyze_supply_chain(product_name, manufacturer, suppliers)` → dict
- `verify_certification(brand, product)` → dict
- `validate_halal_certificate(number, body)` → dict
- `get_halal_certified_brands(category)` → list
- `get_halal_certification_bodies(region)` → list

### Guidelines & Education
- `get_halal_guidelines(category)` → dict
- `get_halal_alternatives(haram_item)` → list

### Meat Classification
- `get_halal_meat_types()` → list
- `get_haram_meat_types()` → list
- `is_meat_halal(meat_type)` → bool

## Response Formats

### Simple Responses
```python
detector.is_halal("chicken")     # True
detector.quick_check("pork")     # "Haram"
detector.get_halal_score("beef") # 100
```

### Detailed Responses
```python
result = detector.detect_ingredient("gelatin")
# {
#   "ingredient": "gelatin",
#   "status": "Questionable", 
#   "explanation": "Source verification needed...",
#   "confidence": "Medium",
#   "concerns": ["Source unclear", "Processing method"],
#   "recommendations": ["Verify with halal certification"],
#   "certification_required": true,
#   "alternatives": ["Agar-agar", "Pectin"]
# }
```

### Advanced Analysis
```python
# Advanced ingredient analysis
result = detector.advanced_ingredient_analysis("gelatin", "USA", "enzymatic")
print(result["technical_details"])
print(result["supply_chain_risks"])

# Compliance scoring
score = detector.check_halal_compliance_score("chicken burger", "fast_food")
print(f"Overall score: {score['overall_score']}/100")
print(f"Ingredient score: {score['ingredient_score']}/100")

# Supply chain analysis
chain = detector.analyze_supply_chain("Chocolate Bar", "Nestle", ["Cocoa Supplier A", "Milk Supplier B"])
print(f"Compliance: {chain['overall_compliance']}")
print(f"Critical issues: {chain['critical_issues']}")

# Alcohol content analysis
alcohol = detector.detect_alcohol_content("Vanilla Extract", 35.0)
print(f"Status: {alcohol['status']}")
print(f"Islamic ruling: {alcohol['islamic_ruling']}")

# Halal guidelines
guidelines = detector.get_halal_guidelines("meat")
print(f"Halal principles: {guidelines['halal_principles']}")
print(f"Best practices: {guidelines['best_practices']}")
```

## Requirements
- Python 3.7+
- requests library

## Installation
```bash
git clone <repository>
cd quran
pip install -r requirements.txt
```

## License
MIT License with additional terms for halal/haram detection. See [LICENSE](LICENSE) file for complete terms.

## Disclaimer
This software provides AI-powered suggestions for halal/haram classification based on general Islamic dietary guidelines. Users are advised to:
- Consult with qualified Islamic scholars for religious guidance
- Verify information with trusted halal certification bodies
- Consider local Islamic community standards and practices
- Use this tool as a reference only, not as definitive religious authority

## Contributing
Contributions are welcome! Please ensure all new features maintain the library's focus on accuracy and Islamic compliance.