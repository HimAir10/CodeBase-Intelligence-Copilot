from pathlib import Path
import yaml

from app.llm_client.prompts_model import PromptTemplate


class PromptRegistry:

    def __init__(self, prompt_dir: str):
        self.prompt_dir = Path(prompt_dir)

    def get(
        self,
        prompt_id: str,
        version: str
    ) -> PromptTemplate:

        path = (
            self.prompt_dir
            / prompt_id
            / f"{version}.yaml"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt not found: {prompt_id}:{version}"
            )

        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return PromptTemplate.model_validate(data)