import json
from app.llm_client.exceptions import StructuredOutputError
class StructuredOutputParser:

    def parse(self, content: str, response_model):

        try:
            data = json.loads(content)

            return response_model.model_validate(data)

        except Exception as exc:
            raise StructuredOutputError(
                "Failed to parse structured output"
            ) from exc