class StreamingResponse: 

    def process(self, provider_stream):

        for chunk in provider_stream:
            content = self.extract_content(chunk)
            if content:
                yield content
    