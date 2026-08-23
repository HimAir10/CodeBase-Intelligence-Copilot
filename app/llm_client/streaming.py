class StreamingResponse:
    def process(self, provider_stream):
        for chunk in provider_stream:
            content = self.extract_content(chunk)
            if content:
                yield content

    @staticmethod
    def extract_content(chunk) -> str | None:
        if not chunk.choices:
            return None
        return chunk.choices[0].delta.content