from quran import HalalDetector
import json

detector = HalalDetector()

ingredient_result = detector.detect_ingredient("gelatin")
print("Ingredient Analysis:")
print(f"Status: {ingredient_result['status']}")
print(f"Explanation: {ingredient_result['explanation']}")
print(f"Confidence: {ingredient_result['confidence']}")
print(f"Concerns: {ingredient_result['concerns']}")
print()

food_result = detector.detect_food_item("chicken burger")
print("Food Item Analysis:")
print(f"Status: {food_result['status']}")
print(f"Explanation: {food_result['explanation']}")
print(f"Confidence: {food_result['confidence']}")
print(f"Concerns: {food_result['concerns']}")
print()

alternatives = detector.get_halal_alternatives("pork")
print("Halal Alternatives for pork:")
for alt in alternatives:
    print(f"- {alt}")
print()

certification = detector.verify_certification("McDonald's", "Big Mac")
print("Certification Check:")
print(f"Has Certification: {certification['has_certification']}")
print(f"Certifying Body: {certification['certifying_body']}")
print(f"Reliability: {certification['reliability']}")
print(f"Details: {certification['details']}")
print()

batch_items = ["beef", "pork", "chicken", "fish"]
batch_results = detector.batch_detect(batch_items, "ingredient")
print("Batch Analysis:")
for result in batch_results:
    print(f"{result['ingredient']}: {result['status']} ({result['confidence']}) - {result['concerns']}")

print("\nJSON Output Example:")
print(json.dumps(ingredient_result, indent=2))
