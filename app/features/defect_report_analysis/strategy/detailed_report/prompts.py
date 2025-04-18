from app.features.defect_report_analysis.common.prompts import Prompts as CommonPrompts


class Prompts(CommonPrompts):


    ASSISSTANT_SYSTEM_PROMPT = """
        You are a professional assistant that searches through documents and finds relevant information for the user. 
        You will be asked to find an information in a document or to infer an information based from the document content.
        Document will be delimited using <document> and </document> tags.
        Your answer should contain only the information that is relevant to the question.
        If there is no information in the document that can be used to answer the question, you should say "I don't know".
        All the contents of your answer must be in polish language.
    """

    DEFECT_LIST_INTRUCTIONS = """
        Your task is to provide a list of defects found in the document.
        The document is a report of defects related to construction.

        In the defect report there are details about the defects. You should search through the details to find unique defects.

        For each found defect you should answer with:
        name - the short name of the damage
        location - as exact as possible location of the damage. In most cases it should be provided at the beginning of the document. 
        confidence - 0.0 - 1.0 number that indicates how sure you are about the damage being defective.
        confidence_reason - the reason for the confidence level
        evidence - the evidence of the defect in the report e.g. citation

        <defect-examples>

        ## PROTOKÓŁ ZGŁOSZENIA WADY NIEISTOTNEJ

        ### PZW nr 04/11/2024 odc. 1 S5

        **KONTRAKT**: „Kontynuacja projektowania i budowy drogi ekspresowej S-5 na odcinku Nowe Marzy – Bydgoszcz – granica województwa kujawsko-pomorskiego i wielkopolskiego z podziałem na 2 części:

        **Część 1** - Kontynuacja projektowania i budowy drogi ekspresowej S-5 na odcinku od węzła „Nowe Marzy” (bez węzła) do węzła „Dworzysko” (z węzłem) o długości około 23,3 km.”

        **Umowa nr 2017.2020.I-A-D-3.2410.12.2019.51 (1) z dnia 27.04.2020 r.**

        1. **Data i godz. zgłoszenia**: 20.11.2024 r.

        2. **Osoba zgłaszająca wadę; stanowisko, tel. kontaktowy**: Fabian Wojczuk, Starszy Inspektor ds. utrzymania dróg, tel. 669 860 187

        3. **Odcinek; Obiekt; lokalizacja**: Węzeł Świecie Zachód

        4. Opis wady: awaria pojedynczych lamp o nr:
        - SOII 1/5, SOII 1/6, SOII 1/6.1, SOII 1/7 (SO2 S5 łącznice)
        - SOIII 1/1, SO III 1/1.1, SO III 1/1.3 (SO3 DK91)

        5. **Kwalifikacja wady** zgodnie z pkt 5 Gwarancji Jakości: nieistotna

        6. **Dokumentacja fotograficzna wady**:

        Obrazek 1. Przedstawiający lampy z numerami SOII 1/7 i SOII

        </defect-examples>

        Your answer should strictly follow a json format:
        [
            {
                "name": "SOII 1/5, SOII 1/6, SOII 1/6.1, SOII 1/7 (SO2 S5 łącznice)",
                "location":"Węzeł Świecie Zachód",
                "confidence": 1.0,
                "confidence_reason": "The defect is clearly visible in the document.",
                "evidence": "4. Opis wady: awaria pojedynczych lamp o nr:
                - SOII 1/5, SOII 1/6, SOII 1/6.1, SOII 1/7 (SO2 S5 łącznice)
                - SOIII 1/1, SO III 1/1.1, SO III 1/1.3 (SO3 DK91)"
            },
            {
                "name": "OSOIII 1/1, SO III 1/1.1, SO III 1/1.3 (SO3 DK91)",
                "location":"Węzeł Świecie Zachód",
                "confidence": 1.0,
                "confidence_reason": "The defect is mentioned in the document.",
                "evidence": "4. Opis wady: awaria pojedynczych lamp o nr:
                - SOII 1/5, SOII 1/6, SOII 1/6.1, SOII 1/7 (SO2 S5 łącznice)
                - SOIII 1/1, SO III 1/1.1, SO III 1/1.3 (SO3 DK91), Obrazek przedstawiający lampy z numerami SOII 1/7 i SOII"
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

    
