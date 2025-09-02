import requests
import json
from typing import Dict, List, Optional, Union

class HalalDetector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://text.pollinations.ai/"
        
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
