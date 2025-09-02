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
- `detect_ingredient(ingredient)` → dict
- `detect_food_item(food_name)` → dict
- `analyze_recipe(name, ingredients)` → dict

### List Processing
- `check_ingredients_list(ingredients)` → dict
- `find_haram_ingredients(ingredients)` → list
- `find_questionable_ingredients(ingredients)` → list
- `get_safe_ingredients(ingredients)` → list
- `batch_detect(items, type)` → list

### Alternatives & Recommendations
- `get_halal_alternatives(haram_item)` → list

### Verification & Validation
- `verify_certification(brand, product)` → dict
- `check_restaurant_halal(name, location)` → dict
- `validate_halal_certificate(number, body)` → dict
- `get_halal_certified_brands(category)` → list

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
#   "concerns": ["Source unclear", "Processing method"]
# }
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
MIT License