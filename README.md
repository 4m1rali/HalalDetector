# Quran - AI-Powered Halal/Haram Detection Library

A Python library for detecting halal and haram food items using AI technology.

## Installation

```bash
pip install -r requirements.txt
```

Or install the package:

```bash
pip install .
```

## Usage

```python
from quran import HalalDetector
import json

detector = HalalDetector()

result = detector.detect_ingredient("gelatin")
print(result['status'])
print(result['explanation'])
print(result['concerns'])

food_result = detector.detect_food_item("chicken burger")
print(food_result['status'])
print(food_result['confidence'])

alternatives = detector.get_halal_alternatives("pork")
print(alternatives)

certification = detector.verify_certification("McDonald's", "Big Mac")
print(certification['has_certification'])
print(certification['certifying_body'])

print(json.dumps(result, indent=2))
```

## Features

- Detect halal/haram status of ingredients
- Analyze complete food items
- Get halal alternatives for haram items
- Verify halal certifications
- Batch processing for multiple items
- AI-powered analysis with confidence levels
- JSON-based AI responses for structured data
- Detailed concerns and explanations

## Methods

- `detect_ingredient(ingredient)`: Analyze single ingredient
- `detect_food_item(food_name)`: Analyze complete food item
- `get_halal_alternatives(haram_item)`: Get halal alternatives
- `verify_certification(brand, product)`: Check certification status
- `batch_detect(items, item_type)`: Process multiple items

## Requirements

- Python 3.7+
- requests library
