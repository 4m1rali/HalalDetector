from quran import HalalDetector 

detector = HalalDetector()

print("=== SIMPLE CHECKS ===")
print(f"Chicken is halal: {detector.is_halal('chicken')}")
print(f"Pork is haram: {detector.is_haram('pork')}")
print(f"Gelatin is questionable: {detector.is_questionable('gelatin')}")
print(f"Beef status: {detector.quick_check('beef')}")
print(f"Beef halal score: {detector.get_halal_score('beef')}")

print("\n=== RECIPE ANALYSIS ===")
ingredients = ["chicken", "rice", "vegetables", "spices", "oil"]
recipe = detector.analyze_recipe("Chicken Rice", ingredients)
print(f"Recipe: {recipe['recipe']}")
print(f"Status: {recipe['overall_status']}")
print(f"Halal %: {recipe['halal_percentage']}%")
print(f"Safe ingredients: {recipe['safe_ingredients']}")

print("\n=== INGREDIENT LISTS ===")
mixed_ingredients = ["beef", "pork", "chicken", "gelatin", "vegetables"]
print(f"All ingredients: {mixed_ingredients}")
print(f"Haram ingredients: {detector.find_haram_ingredients(mixed_ingredients)}")
print(f"Questionable: {detector.find_questionable_ingredients(mixed_ingredients)}")
print(f"Safe ingredients: {detector.get_safe_ingredients(mixed_ingredients)}")

print("\n=== MEAT TYPES ===")
print(f"Halal meats: {detector.get_halal_meat_types()}")
print(f"Haram meats: {detector.get_haram_meat_types()}")
print(f"Beef is halal meat: {detector.is_meat_halal('beef')}")
print(f"Pork is halal meat: {detector.is_meat_halal('pork')}")

print("\n=== RESTAURANT CHECK ===")
restaurant = detector.check_restaurant_halal("McDonald's", "New York")
print(f"McDonald's is halal: {restaurant['is_halal']}")
print(f"Certification body: {restaurant['certification_body']}")

print("\n=== BRAND CERTIFICATION ===")
brands = detector.get_halal_certified_brands("food")
print(f"Halal certified brands: {brands[:5]}")

print("\n=== ALTERNATIVES ===")
alternatives = detector.get_halal_alternatives("pork")
print(f"Halal alternatives to pork: {alternatives}")

print("\n=== CERTIFICATE VALIDATION ===")
cert = detector.validate_halal_certificate("HC123456", "HFS")
print(f"Certificate valid: {cert['is_valid']}")
print(f"Status: {cert['status']}")
print(f"Expiry: {cert['expiry_date']}")
