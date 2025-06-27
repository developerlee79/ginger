import json

from app.image.detection.image_detector import ImageDetector
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

try:
    AI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
    AI_KEY = os.environ["AZURE_OPENAI_API_KEY"]
    deployment_name = "gpt-4.1-mini"
    api_version = '2024-12-01-preview'
except KeyError:
    print("Missing environment variable 'OPENAI_ENDPOINT' or 'OPENAI_KEY'")
    exit()

class AzureOpenAIVisionDetector(ImageDetector):

    def extract_info_from_image(self, image_url):
        client = AzureOpenAI(
            api_key=AI_KEY,
            api_version=api_version,
            base_url=f"{AI_ENDPOINT}/openai/deployments/{deployment_name}"
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI that identifies electronic devices from label photos.  You will be provided with an image of a label on an electronic device. Your tasks are:  Analyze the image to extract all visible serial numbers, model numbers, product codes, certification IDs, or any relevant alphanumeric identifiers. From the extracted codes, identify the serial number and model code only. Ignore any other codes. Based on the serial number, model code, and any visible context or layout of the label, infer the most likely manufacturer and model name of the electronic device. Format your response according to the strict JSON schema below. Response Format (Always respond in this exact JSON structure):  { \"serial_code\": \"extracted_serial_number\", \"model_code\": \"extracted_model_code\", \"manufacturer\": \"Example\",    \"model\": \"Example Model Name\",   \"description\": \"Explain how you identified the device. Mention the key codes used (especially serial_code and model_code), and how they helped in recognizing the manufacturer and model.\" } For manufacturer, provide only the brand name (e.g., use \"Apple\" instead of \"Apple Inc.\"). For model, use the manufacturer’s official model naming convention (e.g., \"MacBook Air (M1, 2020)\" for model code A2337). If no useful serial or model codes are found or the device cannot be identified confidently, set \"Unknown\" for serial_code, model_code, manufacturer, and model, and explain why in the description."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{image_url}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=3000
        )

        infer_result = response.choices[0].message.content
        return json.loads(infer_result)
