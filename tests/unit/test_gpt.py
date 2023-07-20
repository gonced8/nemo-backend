from app.services.gpt import GPT


def test_gpt():
    """Test if GPT works"""

    response = GPT().chat_completion(
        [("user", 'say exactly "hello"')], temperature=0.0, top_p=1.0
    )
    assert response.lower() == "hello"
