from .openai_client import client


def run_openai_smoke_test():

    response = client.responses.create(
        model="gpt-5.6-luna",
        input="What is a landscape design-build company?"
    )

    return response.output_text