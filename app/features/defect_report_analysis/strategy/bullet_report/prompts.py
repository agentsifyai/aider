from app.features.defect_report_analysis.common.prompts import Prompts as CommonPrompts


class Prompts(CommonPrompts):

    # This creates a standardized way of retrieving and using prompts for AI.
    # TODO: Use a database to store and retrieve vetted prompts.
    def __init__(self):
        self.stored_prompts = {
            'assistant_system_prompt': self.ASSISSTANT_SYSTEM_PROMPT,
            'defects_location_instructions': self.DEFECTS_LOCATION_INSTRUCTIONS,
            'defect_list_instructions': self.DEFECT_LIST_INTRUCTIONS
        }

    ASSISSTANT_SYSTEM_PROMPT = """
        You are a professional assistant that searches through documents and finds relevant information for the user. 
        You will be asked to find an information in a document or to infer an information based from the document content.
        Document will be delimited using <document> and </document> tags.
        Your answer should contain only the information that is relevant to the question.
        If there is no information in the document that can be used to answer the question, you should say "I don't know".
        All the contents of your answer must be in polish language.
    """

    DEFECTS_LOCATION_INSTRUCTIONS = """
        You must provide a location of where the defects report is located.
        It should be within the document, most likely at the beginning or end of the document.
        The location should be identifiable place on the map and should be as concrete as possible.

        Example of report beginning:
        <report-beginning-example>
        Zamość, dnia 08 kwietnia 2022 r. 
        PROTOKÓŁ  
        z przeglądu stanu technicznego branży budowlanej w okresie gwarancyjnym 
        budynku Sądu Okręgowego i Rejonowego w Zamościu przeprowadzonego w dniach 21
        25.03.2022 r. sporządzony w dniu 08.04.2022 r. 
        </report-beginning-example>

        Desired location output:
        <location-output>
        Sąd Okręgowy i Rejonowy w Zamościu
        </location-output>

        Answer with a concrete place, without any introductions or explanations.
    """

    DEFECT_LIST_INTRUCTIONS = """
        You must provide a list of defects from the following report document.
        Document contains various defects in various locations.
        Example of defect format in the document:
        <defect-examples>
        latarnia doświetleniowa - kiosk I - sala rozpraw nr 30 - zmurszenie blachy (dziura) przy oknie
        P.29A - okno do regulacji
        6. **Km 55+308 (od strony Warszawy):**
        1. Przemieszczenie (osiadanie) biegu schodów skarpowych u podnóża skarpy.
        2. Przemieszczenie brukowej kostki kamiennej w dolnej części umocnienia skarpy – pomiędzy schodami skarpowymi a oparciem ściany oporowej z gruntu zbrojonego.
        </defect-examples>

        For each found defect you should answer with:
        name - the short name of the damage
        location - as exact as possible location of the damage 
        confidence - 0.0 - 1.0 number that indicates how sure you are about the damage being defective.
        confidence_reason - the reason for the confidence level
        evidence - the evidence of the defect in the report e.g. citation

        Your answer should strictly follow a json format:
        [
            {
                "name": "Latarnia doświetleniowa - zmurszenie blachy (dziura) przy oknie",
                "location":"Sąd Rejonowy w Zamości Kiosk I - sala rozpraw nr 30",
                "confidence": 1.0,
                "confidence_reason": "The defect is clearly visible in the document.",
                "evidence": "latarnia doświetleniowa - kiosk I - sala rozpraw nr 30 - zmurszenie blachy (dziura) przy oknie"
            },
            {
                "name": "Okno do regulacji",
                "location":"Sąd Rejonowy w Zamości P.29A",
                "confidence": 1.0,
                "confidence_reason": "The defect is clearly visible in the document.",
                "evidence": "P.29A - okno do regulacji"
            },
            {
                "name": "Przemieszczenie (osiadanie) biegu schodów skarpowych",
                "location":"Podnóże skarpy, Km 55+308 (od strony Warszawy)",
                "confidence": 0.9,
                "confidence_reason": "Defect is mentioned in the document but not clearly visible. The location metadata is not exact.",
                "evidence": "6. **Km 55+308 (od strony Warszawy):** 1. Przemieszczenie (osiadanie) biegu schodów skarpowych u podnóża skarpy."
            },
            {
                "name": "Przemieszczenie brukowej kostki kamiennej",
                "location":"Dolna część umocnienia skarpy – pomiędzy schodami skarpowymi a oparciem ściany oporowej z gruntu zbrojonego.",
                "confidence": 0.9,
                "confidence_reason": "Defect is mentioned in the document but not clearly visible. The location metadata is not exact.",
                "evidence": "6. **Km 55+308 (od strony Warszawy):** [...] 2. Przemieszczenie brukowej kostki kamiennej w dolnej części umocnienia skarpy – pomiędzy schodami skarpowymi a oparciem ściany oporowej z gruntu zbrojonego."
            }
        ]

        Destructure the defect in the document as in the examples above.

        You have to list all of the defects present in the document. No defect should be omitted.

    """

    # TODO: Define more setter and getter methods.
    def get_stored_prompts(self) -> dict:
        return self.stored_prompts

    def get_stored_prompt(self, prompt_name: str) -> str:
        return self.get_stored_prompts()[prompt_name]

    def get_defect_list_instructions(self, location_prompt: str) -> str:
        formatted_defect_list_instructins = f"""
            {self.get_stored_prompt('defect_list_instructions')}
            
            Each location should mention the concrete defect location e.g. a room number.
            Locations must also mention information about the building in which the defect is located:
            {location_prompt}

            """

        return formatted_defect_list_instructins
    
