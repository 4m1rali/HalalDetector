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
    
    def _generate_ai_response(self, prompt: str, context: str = "") -> Dict:
        try:
            system_prompt = """You are a highly knowledgeable Islamic scholar and food safety expert specializing in halal and haram food classification. You have deep understanding of:

1. Islamic dietary laws (Shariah) and their application to modern food production
2. Food processing methods and their impact on halal status
3. Ingredient sourcing and supply chain considerations
4. Regional variations in halal standards and certification bodies
5. Modern food additives, preservatives, and processing aids
6. Cross-contamination risks and prevention measures

CRITICAL INSTRUCTIONS:
- Always respond with valid JSON format only
- Base decisions on authentic Islamic sources and established halal standards
- Consider both traditional and modern food processing methods
- Account for regional differences in halal certification
- Provide detailed explanations for questionable items
- Include specific concerns and recommendations
- Use confidence levels based on available information quality

REQUIRED JSON FORMAT:
{
  "status": "Halal/Haram/Questionable",
  "explanation": "Detailed explanation with Islamic reasoning",
  "confidence": "High/Medium/Low",
  "concerns": ["specific concern 1", "specific concern 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "certification_required": true/false,
  "alternatives": ["halal alternative 1", "halal alternative 2"]
}"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context}\n\n{prompt}" if context else prompt}
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
                        "concerns": ["Invalid JSON response"],
                        "recommendations": ["Verify with Islamic scholar"],
                        "certification_required": True,
                        "alternatives": []
                    }
            else:
                return {
                    "status": "Error",
                    "explanation": f"HTTP {response.status_code}",
                    "confidence": "Low",
                    "concerns": ["API Error"],
                    "recommendations": ["Check internet connection", "Try again later"],
                    "certification_required": True,
                    "alternatives": []
                }
                
        except Exception as e:
            return {
                "status": "Error",
                "explanation": str(e),
                "confidence": "Low",
                "concerns": ["Network Error"],
                "recommendations": ["Check internet connection", "Verify API availability"],
                "certification_required": True,
                "alternatives": []
            }
    
    def detect_ingredient(self, ingredient: str, context: str = "") -> Dict[str, Union[str, bool, List]]:
        context_info = f"Context: {context}" if context else ""
        prompt = f"Analyze this ingredient for halal/haram status: '{ingredient}'. {context_info}\n\nConsider:\n1. Source and origin of the ingredient\n2. Processing methods used\n3. Potential cross-contamination risks\n4. Regional halal standards\n5. Modern food production practices\n\nProvide comprehensive analysis with Islamic reasoning."
        
        ai_response = self._generate_ai_response(prompt, context)
        
        return {
            "ingredient": ingredient,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "certification_required": ai_response.get("certification_required", False),
            "alternatives": ai_response.get("alternatives", [])
        }
    
    def detect_food_item(self, food_name: str, preparation_method: str = "", region: str = "") -> Dict[str, Union[str, bool, List]]:
        context_parts = []
        if preparation_method:
            context_parts.append(f"Preparation method: {preparation_method}")
        if region:
            context_parts.append(f"Region: {region}")
        context = "; ".join(context_parts)
        
        prompt = f"Analyze this food item for halal/haram status: '{food_name}'.\n\nConsider:\n1. All potential ingredients and additives\n2. Food preparation and cooking methods\n3. Cross-contamination risks\n4. Regional halal standards and practices\n5. Modern food processing techniques\n6. Storage and handling procedures\n\nProvide detailed analysis with specific Islamic reasoning."
        
        ai_response = self._generate_ai_response(prompt, context)
        
        return {
            "food_item": food_name,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "certification_required": ai_response.get("certification_required", False),
            "alternatives": ai_response.get("alternatives", [])
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
    
    def advanced_ingredient_analysis(self, ingredient: str, source_country: str = "", processing_method: str = "") -> Dict:
        context = f"Source country: {source_country}; Processing method: {processing_method}" if source_country or processing_method else ""
        prompt = f"Perform advanced halal analysis for ingredient: '{ingredient}'.\n\nAnalyze:\n1. Ingredient composition and molecular structure\n2. Manufacturing processes and chemical treatments\n3. Potential haram derivatives or by-products\n4. Cross-contamination risks in production\n5. Storage and transportation considerations\n6. Regional halal certification standards\n7. Alternative halal sources and suppliers\n\nProvide comprehensive technical analysis."
        
        ai_response = self._generate_ai_response(prompt, context)
        
        return {
            "ingredient": ingredient,
            "source_country": source_country,
            "processing_method": processing_method,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "certification_required": ai_response.get("certification_required", False),
            "alternatives": ai_response.get("alternatives", []),
            "technical_details": ai_response.get("technical_details", ""),
            "supply_chain_risks": ai_response.get("supply_chain_risks", [])
        }
    
    def detect_food_additives(self, additives: List[str]) -> Dict:
        prompt = f"Analyze these food additives for halal status: {', '.join(additives)}.\n\nConsider:\n1. Chemical composition and origin\n2. Manufacturing processes\n3. Potential animal-derived components\n4. Alcohol content or derivatives\n5. Cross-contamination risks\n6. Regional halal standards for additives\n\nProvide detailed analysis for each additive."
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "additives": additives,
            "overall_status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "certification_required": ai_response.get("certification_required", False),
            "alternatives": ai_response.get("alternatives", []),
            "individual_analysis": ai_response.get("individual_analysis", {})
        }
    
    def check_restaurant_chain_halal(self, chain_name: str, location: str = "", menu_items: List[str] = []) -> Dict:
        menu_context = f"Menu items to check: {', '.join(menu_items)}" if menu_items else ""
        prompt = f"Analyze halal status for restaurant chain: '{chain_name}' in {location}.\n\nEvaluate:\n1. Overall halal certification status\n2. Kitchen practices and cross-contamination prevention\n3. Ingredient sourcing and supplier verification\n4. Staff training on halal requirements\n5. Menu item analysis for potential haram ingredients\n6. Regional halal standards compliance\n7. Certification body and validity\n\nProvide comprehensive restaurant analysis."
        
        ai_response = self._generate_ai_response(prompt, menu_context)
        
        return {
            "chain_name": chain_name,
            "location": location,
            "menu_items": menu_items,
            "is_halal": ai_response.get("is_halal", False),
            "certification_body": ai_response.get("certification_body", "Unknown"),
            "last_verified": ai_response.get("last_verified", "Unknown"),
            "notes": ai_response.get("notes", ai_response.get("explanation", "No additional information")),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "menu_analysis": ai_response.get("menu_analysis", {}),
            "kitchen_practices": ai_response.get("kitchen_practices", [])
        }
    
    def analyze_supply_chain(self, product_name: str, manufacturer: str = "", suppliers: List[str] = []) -> Dict:
        supplier_context = f"Manufacturer: {manufacturer}; Suppliers: {', '.join(suppliers)}" if manufacturer or suppliers else ""
        prompt = f"Analyze halal compliance of supply chain for product: '{product_name}'.\n\nEvaluate:\n1. Manufacturer halal certification and practices\n2. Supplier verification and certification status\n3. Raw material sourcing and origin verification\n4. Production facility halal compliance\n5. Cross-contamination prevention measures\n6. Quality control and testing procedures\n7. Transportation and storage halal requirements\n8. Documentation and traceability systems\n\nProvide comprehensive supply chain analysis."
        
        ai_response = self._generate_ai_response(prompt, supplier_context)
        
        return {
            "product_name": product_name,
            "manufacturer": manufacturer,
            "suppliers": suppliers,
            "overall_compliance": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "certification_required": ai_response.get("certification_required", False),
            "supply_chain_risks": ai_response.get("supply_chain_risks", []),
            "compliance_score": ai_response.get("compliance_score", 0),
            "critical_issues": ai_response.get("critical_issues", [])
        }
    
    def get_halal_certification_bodies(self, region: str = "global") -> List[Dict]:
        prompt = f"List major halal certification bodies for {region} region.\n\nInclude:\n1. Official certification body names\n2. Their recognition status\n3. Geographic coverage\n4. Specialization areas\n5. Contact information if available\n\nRespond with JSON format containing certification bodies list."
        
        ai_response = self._generate_ai_response(prompt)
        
        if isinstance(ai_response, dict) and "certification_bodies" in ai_response:
            return ai_response["certification_bodies"]
        
        return []
    
    def check_halal_compliance_score(self, item: str, category: str = "food") -> Dict:
        prompt = f"Calculate halal compliance score for '{item}' in {category} category.\n\nEvaluate:\n1. Ingredient halal status (40% weight)\n2. Processing method compliance (30% weight)\n3. Certification status (20% weight)\n4. Cross-contamination risks (10% weight)\n\nProvide numerical score (0-100) with detailed breakdown."
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "item": item,
            "category": category,
            "overall_score": ai_response.get("overall_score", 0),
            "ingredient_score": ai_response.get("ingredient_score", 0),
            "processing_score": ai_response.get("processing_score", 0),
            "certification_score": ai_response.get("certification_score", 0),
            "contamination_score": ai_response.get("contamination_score", 0),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "recommendations": ai_response.get("recommendations", []),
            "improvement_areas": ai_response.get("improvement_areas", [])
        }
    
    def detect_alcohol_content(self, item: str, alcohol_percentage: float = 0.0) -> Dict:
        context = f"Alcohol content: {alcohol_percentage}%" if alcohol_percentage > 0 else ""
        prompt = f"Analyze alcohol content and halal status for '{item}'.\n\nConsider:\n1. Alcohol content percentage and type\n2. Source of alcohol (natural fermentation vs added)\n3. Islamic rulings on alcohol consumption\n4. Cooking and processing effects on alcohol\n5. Regional variations in alcohol tolerance\n6. Alternative non-alcoholic options\n\nProvide detailed alcohol analysis with Islamic perspective."
        
        ai_response = self._generate_ai_response(prompt, context)
        
        return {
            "item": item,
            "alcohol_percentage": alcohol_percentage,
            "status": ai_response.get("status", "Unknown"),
            "explanation": ai_response.get("explanation", "No explanation provided"),
            "confidence": ai_response.get("confidence", "Low"),
            "concerns": ai_response.get("concerns", []),
            "recommendations": ai_response.get("recommendations", []),
            "alternatives": ai_response.get("alternatives", []),
            "cooking_effects": ai_response.get("cooking_effects", ""),
            "islamic_ruling": ai_response.get("islamic_ruling", "")
        }
    
    def get_halal_guidelines(self, category: str = "general") -> Dict:
        prompt = f"Provide comprehensive halal guidelines for {category} category.\n\nInclude:\n1. Basic halal principles\n2. Common haram items to avoid\n3. Questionable items requiring verification\n4. Best practices for halal compliance\n5. Regional variations and considerations\n6. Certification requirements\n7. Common mistakes and misconceptions\n\nProvide detailed guidelines with practical examples."
        
        ai_response = self._generate_ai_response(prompt)
        
        return {
            "category": category,
            "guidelines": ai_response.get("guidelines", []),
            "halal_principles": ai_response.get("halal_principles", []),
            "haram_items": ai_response.get("haram_items", []),
            "questionable_items": ai_response.get("questionable_items", []),
            "best_practices": ai_response.get("best_practices", []),
            "regional_variations": ai_response.get("regional_variations", []),
            "certification_requirements": ai_response.get("certification_requirements", []),
            "common_mistakes": ai_response.get("common_mistakes", []),
            "practical_examples": ai_response.get("practical_examples", [])
        }
