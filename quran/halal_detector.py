import requests
import json
from typing import Dict, List, Optional, Union

class HalalDetector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://text.pollinations.ai/"
        self.halal_keywords = ["halal", "permissible", "allowed", "clean", "pure"]
        self.haram_keywords = ["haram", "forbidden", "prohibited", "unclean", "impure"]
        
    def _clean_response(self, text: str) -> str:
        return text.replace("Powered by Pollinations.AI", "").replace("Support our mission", "").replace("https://pollinations.ai", "").replace("pollinations.ai", "").replace("pollinations", "").strip()
    
    def _generate_ai_response(self, prompt: str) -> Dict:
        try:
            messages = [
                {"role": "system", "content": "You are an Islamic scholar expert in halal and haram food classification. Always respond with valid JSON format containing: status (Halal/Haram/Questionable), explanation (string), confidence (High/Medium/Low), and concerns (array of strings)."},
                {"role": "user", "content": prompt}
            ]
            
            response = requests.post(
                self.base_url,
                headers={"Content-Type": "application/json"},
                json={
                    "messages": messages,
                    "model": "openai",
                    "private": True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                cleaned_text = self._clean_response(response.text)
                try:
                    return json.loads(cleaned_text)
                except json.JSONDecodeError:
                    return {
                        "status": "Unknown",
                        "explanation": cleaned_text,
                        "confidence": "Low",
                        "concerns": ["Invalid JSON response"]
                    }
            else:
                return {
                    "status": "Error",
                    "explanation": f"HTTP {response.status_code}",
                    "confidence": "Low",
                    "concerns": ["API Error"]
                }
                
        except Exception as e:
            return {
                "status": "Error",
                "explanation": str(e),
                "confidence": "Low",
                "concerns": ["Network Error"]
            }
    
    def detect_ingredient(self, ingredient: str) -> Dict[str, Union[str, bool, List]]:
        prompt = f"Analyze this ingredient for halal/haram status: '{ingredient}'. Respond with JSON: {{'status': 'Halal/Haram/Questionable', 'explanation': 'detailed explanation', 'confidence': 'High/Medium/Low', 'concerns': ['list of concerns']}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "ingredient": ingredient,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", [])
        }
    
    def detect_food_item(self, food_name: str) -> Dict[str, Union[str, bool, List]]:
        prompt = f"Analyze this food item for halal/haram status: '{food_name}'. Consider all ingredients and preparation methods. Respond with JSON: {{'status': 'Halal/Haram/Questionable', 'explanation': 'detailed explanation', 'confidence': 'High/Medium/Low', 'concerns': ['list of concerns']}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "food_item": food_name,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", [])
        }
    
    def batch_detect(self, items: List[str], item_type: str = "ingredient") -> List[Dict[str, Union[str, bool, List]]]:
        results = []
        for item in items:
            if item_type == "ingredient":
                result = self.detect_ingredient(item)
            else:
                result = self.detect_food_item(item)
            results.append(result)
        return results
    
    def get_halal_alternatives(self, haram_item: str) -> List[str]:
        prompt = f"Provide 3-5 halal alternatives for this haram/questionable item: '{haram_item}'. Respond with JSON: {{'alternatives': ['alternative1', 'alternative2', 'alternative3', 'alternative4', 'alternative5']}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        if isinstance(ai_response, dict) and "alternatives" in ai_response:
            return ai_response["alternatives"][:5]
        
        alternatives = []
        if isinstance(ai_response, dict) and "explanation" in ai_response:
            lines = ai_response["explanation"].split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Error'):
                    alternatives.append(line)
        
        return alternatives[:5]
    
    def verify_certification(self, brand: str, product: str) -> Dict[str, Union[str, bool, List]]:
        prompt = f"Check if '{brand}' brand's '{product}' has halal certification. Respond with JSON: {{'has_certification': true/false, 'certifying_body': 'body name', 'reliability': 'High/Medium/Low', 'details': 'detailed information'}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "brand": brand,
            "product": product,
            "has_certification": ai_response.get("has_certification", False),
            "certifying_body": ai_response.get("certifying_body", "Unknown"),
            "reliability": ai_response.get("reliability", "Low"),
            "details": ai_response.get("details", ai_response.get("explanation", "No details available"))
        }
    
    def is_halal(self, item: str) -> bool:
        result = self.detect_ingredient(item)
        return result["status"].lower() == "halal"
    
    def is_haram(self, item: str) -> bool:
        result = self.detect_ingredient(item)
        return result["status"].lower() == "haram"
    
    def is_questionable(self, item: str) -> bool:
        result = self.detect_ingredient(item)
        return result["status"].lower() == "questionable"
    
    def quick_check(self, item: str) -> str:
        result = self.detect_ingredient(item)
        return result["status"]
    
    def get_halal_score(self, item: str) -> int:
        result = self.detect_ingredient(item)
        if result["status"].lower() == "halal":
            return 100
        elif result["status"].lower() == "questionable":
            return 50
        elif result["status"].lower() == "haram":
            return 0
        else:
            return -1
    
    def check_ingredients_list(self, ingredients: List[str]) -> Dict[str, str]:
        results = {}
        for ingredient in ingredients:
            result = self.detect_ingredient(ingredient)
            results[ingredient] = result["status"]
        return results
    
    def find_haram_ingredients(self, ingredients: List[str]) -> List[str]:
        haram_list = []
        for ingredient in ingredients:
            if self.is_haram(ingredient):
                haram_list.append(ingredient)
        return haram_list
    
    def find_questionable_ingredients(self, ingredients: List[str]) -> List[str]:
        questionable_list = []
        for ingredient in ingredients:
            if self.is_questionable(ingredient):
                questionable_list.append(ingredient)
        return questionable_list
    
    def get_safe_ingredients(self, ingredients: List[str]) -> List[str]:
        safe_list = []
        for ingredient in ingredients:
            if self.is_halal(ingredient):
                safe_list.append(ingredient)
        return safe_list
    
    def analyze_recipe(self, recipe_name: str, ingredients: List[str]) -> Dict:
        haram_ingredients = self.find_haram_ingredients(ingredients)
        questionable_ingredients = self.find_questionable_ingredients(ingredients)
        safe_ingredients = self.get_safe_ingredients(ingredients)
        
        overall_status = "Halal"
        if haram_ingredients:
            overall_status = "Haram"
        elif questionable_ingredients:
            overall_status = "Questionable"
        
        return {
            "recipe": recipe_name,
            "overall_status": overall_status,
            "safe_ingredients": safe_ingredients,
            "questionable_ingredients": questionable_ingredients,
            "haram_ingredients": haram_ingredients,
            "total_ingredients": len(ingredients),
            "halal_percentage": (len(safe_ingredients) / len(ingredients)) * 100 if ingredients else 0
        }
    
    def get_halal_certified_brands(self, category: str = "food") -> List[str]:
        prompt = f"List 10 halal certified brands in {category} category. Respond with JSON: {{'brands': ['brand1', 'brand2', 'brand3', 'brand4', 'brand5', 'brand6', 'brand7', 'brand8', 'brand9', 'brand10']}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        if isinstance(ai_response, dict) and "brands" in ai_response:
            return ai_response["brands"]
        
        return []
    
    def check_restaurant_halal(self, restaurant_name: str, location: str = "") -> Dict:
        prompt = f"Check if '{restaurant_name}' restaurant{f' in {location}' if location else ''} is halal certified. Respond with JSON: {{'is_halal': true/false, 'certification_body': 'body name', 'last_verified': 'date', 'notes': 'additional info'}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "restaurant": restaurant_name,
            "location": location,
            "is_halal": ai_response.get("is_halal", False),
            "certification_body": ai_response.get("certification_body", "Unknown"),
            "last_verified": ai_response.get("last_verified", "Unknown"),
            "notes": ai_response.get("notes", ai_response.get("explanation", "No additional information"))
        }
    
    def get_halal_meat_types(self) -> List[str]:
        return ["beef", "lamb", "goat", "chicken", "turkey", "duck", "fish", "seafood"]
    
    def get_haram_meat_types(self) -> List[str]:
        return ["pork", "bacon", "ham", "sausage", "pepperoni", "salami"]
    
    def is_meat_halal(self, meat_type: str) -> bool:
        halal_meats = self.get_halal_meat_types()
        haram_meats = self.get_haram_meat_types()
        
        if meat_type.lower() in haram_meats:
            return False
        elif meat_type.lower() in halal_meats:
            return True
        else:
            return self.is_halal(meat_type)
    
    def validate_halal_certificate(self, certificate_number: str, certifying_body: str) -> Dict:
        prompt = f"Validate halal certificate number '{certificate_number}' from '{certifying_body}'. Respond with JSON: {{'is_valid': true/false, 'expiry_date': 'date', 'status': 'active/expired/invalid', 'details': 'validation info'}}"
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "certificate_number": certificate_number,
            "certifying_body": certifying_body,
            "is_valid": ai_response.get("is_valid", False),
            "expiry_date": ai_response.get("expiry_date", "Unknown"),
            "status": ai_response.get("status", "Unknown"),
            "details": ai_response.get("details", ai_response.get("explanation", "No validation details"))
        }
