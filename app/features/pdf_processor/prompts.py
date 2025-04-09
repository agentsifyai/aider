class Prompts:
    # This creates a standardized way of retrieving and using prompts for AI.
    # TODO: Use a database to store and retrieve vetted prompts.
    def __init__(self):
        self.assistant_system_prompt = """
        You are a helpful assistant that searches through documents and finds relevant info for the user. 
        You will be asked to find an information in a document or to infer an information based from the document content.
        Document will be delimited using <document> and </document> tags.
        Your answer should contain only the information that is relevant to the question.
        If there is no information in the document that can be used to answer the question, you should say "I don't know".
        Your answer should be in Polish language.
        """

        self.defects_location_instructions = """\n
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

        self.defect_list_instructions = """\n
        You must provide a list of defects from the following report document.
        Document contains various defects in various locations.
        Example of defect format in the document:
        <defect-examples>
        latarnia doświetleniowa - kiosk I - sala rozpraw nr 30 - zmurszenie blachy (dziura) przy oknie
        P.29A - okno do regulacji

        </defect-examples>

        Your answer should strictly follow a json format:
        [
            {
                "name": "Latarnia doświetleniowa - zmurszenie blachy (dziura) przy oknie",
                "location":"Sąd Rejonowy w Zamości Kiosk I - sala rozpraw nr 30"
            },
            {
                "name": "Okno do regulacji",
                "location":"Sąd Rejonowy w Zamości P.29A"
            }
        ]

        Destructure the defect in the document as in the example above.

        You have to list all of the defects present in the document. Go line by line and extract all the defects from the document. 
        """

        self.stored_prompts = {
            'assistant_system_prompt': self.assistant_system_prompt,
            'defects_location_instructions': self.defects_location_instructions,
            'defect_list_instructions': self.defect_list_instructions
        }

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
