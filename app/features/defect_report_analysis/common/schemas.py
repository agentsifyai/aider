from typing import Dict, Any

def response_format_from_schema(json_schema: Dict[str, Any]) -> dict:
    """Convert a JSON schema to a response format for the LLM."""
    return {
        "type": "json_schema",
        "json_schema": json_schema
    }

POTENTIAL_DEFECT_LIST_SCHEMA = {
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
                  "description": "The name or description of the defect. This must be a single word or a short phrase describing the damage."
                },
                "location": {
                  "type": "string",
                  "description": "The location of the defect. Should be as specific as possible."
                },
                "confidence": {
                  "type": "number",
                  "description": "Confidence score indicating the reliability of the defect identification."
                },
                "confidence_reason": {
                  "type": "string",
                  "description": "Jutification and explanation of the confidence score."
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

COMMON_DETAILING_SCHEMA = {
      "name": "defect_report",
      "strict": True,
      "schema": {
        "type": "object",
        "properties": {
          "defects": {
            "type": "array",
            "description": "List of defects reported.",
            "items": {
              "type": "object",
              "properties": {
                "defect_id": {
                  "type": "string",
                  "description": "Unique identifier for the defect."
                },
                "verbose_description": {
                  "type": "string",
                  "description": "Detailed description of the defect."
                },
                "defect_cause": {
                  "type": "string",
                  "description": "The suspected cause of the defect."
                }
              },
              "required": [
                "defect_id",
                "verbose_description",
                "defect_cause"
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