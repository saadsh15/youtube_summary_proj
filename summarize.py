import openai

# Replace with your OpenAI API Key
OPENAI_API_KEY="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"


def summarize_transcription(transcription, summary_length, points=False):
    """Summarizes the transcription based on the points flag."""
    print(summary_length)
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    if points:
        prompt = (
            "Summarize the following transcript into bullet points under separate topic headings. If the video is too long create headings for seperate topics, If the video is too long and the summary is supposed to be short then give a 1 medium sized bullet point for a the topic, if the video does not have a transcript get description and translate it to english if necessary and make a summary with that "
            "Identify key themes and structure the summary accordingly.\n\n"
            f"Transcript:\n{transcription}"
        )
    else:
        prompt = (
            "Summarize the following transcript into a single concise paragraph, capturing the key points.and gicve appropriate topics where it is necessary or the topic changes If the video is too long create headings for seperate topics, If the video is too long and the summary is supposed to be short then give a concise summary of the topic. if the video does not have a transcript get description and translate it to english if necessary and make a summary with that \n\n"
            f"Transcript:\n{transcription}"
        )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content


