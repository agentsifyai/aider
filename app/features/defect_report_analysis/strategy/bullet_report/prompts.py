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
        Your task is to provide a list of defects found in the document.
        The document is a report of defects related to construction.
        Document contains various defects in various locations.

        Defects in the report may be expressed in different ways, but they are usually in the form of a list.

        Here are examples of defects with the way of expressing them:

        <defect-examples>
        ## DACH S.O.
        latarnia doświetleniowa - kiosk I - sala rozpraw nr 30 - zmurszenie blachy (dziura) przy oknie
        P.29A - okno do regulacji

        6. **Km 55+308 (od strony Warszawy):**
        1. Przemieszczenie (osiadanie) biegu schodów skarpowych u podnóża skarpy.
        2. Przemieszczenie brukowej kostki kamiennej w dolnej części umocnienia skarpy – pomiędzy schodami skarpowymi a oparciem ściany oporowej z gruntu zbrojonego.
        </defect-examples>

        For each found defect you should answer with:
        name - the short name of the damage
        location - as exact as possible location of the damage. In most cases it should be provided at the beginning of the document. 
        confidence - 0.0 - 1.0 number that indicates how sure you are about the damage being defective.
        confidence_reason - the reason for the confidence level
        evidence - the evidence of the defect in the report e.g. citation

        Your answer should strictly follow a json format:
        [
            {
                "name": "Latarnia doświetleniowa - zmurszenie blachy (dziura) przy oknie",
                "location":"Kiosk I - sala rozpraw nr 30 DACH S.O.",
                "confidence": 1.0,
                "confidence_reason": "The defect is clearly visible in the document.",
                "evidence": "latarnia doświetleniowa - kiosk I - sala rozpraw nr 30 - zmurszenie blachy (dziura) przy oknie"
            },
            {
                "name": "Okno do regulacji",
                "location":"P.29A DACH S.O.",
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

    CHUNKING_INSTRUCTIONS = """
        Your task is to chunk the document into smaller parts.
        The document is a report of defects related to construction.

        Document should have sections where each section consists of a heading and a content.
        The heading is a concrete location present in the place the report was taken.
        The content is a list of defects related to the location.

        You should answer with a list of strings, where each string is a chunk of the document.

        Your answer should strictly follow a JSON format:

        [
        "Chunk 1", "Chunk 2", "Chunk 3"
        ]

        Example of an output:

        <example>
        [
        "5. **WD-26 w km 55+308 (od strony Gdańska):**
        - zarysowania na ściance oporowej nazięskowej niżsy łożyskowej – lewa strona drogi krajowej,
        - przemieszczenie osłonienia drenażu kontenera.",
        "3. **MA-33 w km 54+146 w ciągu prawej jezdni:**
        - przemieszczenie obrzęża i kostki kamiennej pod obiektem pod rurą odwodnienia zapryczółkowego – przy przyczółku od strony Gdańska,
        - przemieszczenie się wkładki uszczelniającej szczelinę pomiędzy ścianką boczną przyczółka i skrzydłem.",
        "7. **Km 57+670 (wiadukt w ciągu ul. Żuławskiej):**
        - ubytki spoinowania opornika betonowego stożka usytuowanego na końcu ściany oporowej z prawej strony drogi krajowej,
        - lokalne spękania prefabrykatów ściany oporowej – prawa strona drogi krajowej,
        - pojedyncze podłużne pęknięcie deski gzymsowej – prawa strona drogi krajowej,
        - odspojenie materiału plastycznego (sikaflexu) w spoinach dylatacyjnych z betonem oczełu ściany oporowej – prawa strona drogi krajowej.",
        "## Pokoje sędziowskie:
        - 3.49. P.54 -nie stwierdzono wad;
        - 3.50. P. 55 -zarysowania tynku ściany nad ościeżnicą ;
        - 3.51. P.56 -zarysowania tynku ściany przy drzwiach i opad nięte drzwi;
        - 3.52. P.57 -nie stwierdzono wad;
        - 3.53. P.58 -zarysowania tynku ściany;"
        ]
        </example>

        You must process all the document and not omit any part of it. 
        If a section does not correspond to the previous definition of a section, you should include it in the output as well.

        Provide only a JSON array without any introductions or explanations.
        Do not include any other text in the output.
        
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
    
