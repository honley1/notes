from openai import OpenAI

client = OpenAI()

def get_answer(note_title: str, note_content: str):
    response = client.responses.create(
        model="gpt-5",
        input=f"""
        Помоги мне, это моя заметка то чего мне нужно сделать, распиши мне по шагово как ее решить: 
        Title: {note_title}\n\nContent: {note_content}
        """
    )

    return response.output_text