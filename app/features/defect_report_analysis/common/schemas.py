from typing import Dict, Any

def response_format_from_schema(json_schema: Dict[str, Any]) -> dict:
    """Convert a JSON schema to a response format for the LLM."""
    return {
        "type": "json_schema",
        "json_schema": json_schema
    }

POTENTIAL_DEFECT_SCHEMA = {
      "name": "my_schema",
      "strict": False,
      "schema": {
        "type": "object",
        "properties": {
          "defects": {
            "type": "array",
            "description": "A list of detected defects along with their details.",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "The name or description of the defect."
                },
                "location": {
                  "type": "string",
                  "description": "The specific location of the defect."
                },
                "confidence": {
                  "type": "number",
                  "description": "Confidence score indicating the reliability of the defect identification."
                },
                "confidence_reason": {
                  "type": "string",
                  "description": "Explanation of the confidence score."
                },
                "evidence": {
                  "type": "string",
                  "description": "Evidence from the document supporting the defect claim."
                }
              },
              "required": [
                "name",
                "location",
                "confidence",
                "confidence_reason",
                "evidence"
              ],
              "additionalProperties": False
            }
          }
        },
        "required": [
          "defects"
        ],
        "additionalProperties": False
      }
    }