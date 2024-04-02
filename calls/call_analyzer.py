from openai import OpenAI
import json
import asyncio
from utils import download_and_convert_audio, transcribe, delete_file
import logging


### Give a text, Generate the Summary:
system_message = """
# Background
You are an expert executive assistant to a lawyer. You are helping in summarizing client calls. 
You will be provided with the call transcript.
Here are the key things you should do:
1) Topic: Generate A topic of the call with Caller Name & source.
3) Executive Summary:SUMMARY STRICTLY NOT EXCEEDING 30 WORDS. 
4) STAR analysis: Situation, Task, Action, Result. Do not exceed 15 words for each.
5) Positive Energy: What was the positive outcome of the call, from the client's perspective.
6) Negative Energy: What could have been better.
7) Estimated NPS: On a scale of 1-10, how likely is the client to recommend the service to others.
8) CSR Rating: On a scale of 1-10, how well did the CSR handle the call

Note: You can ignore if the transcription is not clear or is not understandable. Just return text: 
"Transcription not clear."


# Formatting
Your response will be a json object detailing the conversation. RESPOND ONLY WITH THE JSON. See example below.
Every key item pair should be delimited by a comma.

Example:
text:"OWS2, this is Summer speaking, how may I help you? Hi there, my name is Bhavish, I'm a real estate agent with EXP. This number is differed by my friend and a client, 
Pranay Shivastav. And I just want to know, do you guys you guys do like a real estate closing? Yes, 
yes. Yes. So my client just bought a property in Hamilton, new construction, 2024 builds,
and it is bought from the developer itself. So you do that as well, right? Yes, yes, we do. 
Yeah, so I just would recommend that you email the solicitor. I can give you his email with the 
information and then Yeah, oh you have it? Do you want my client? No, do you want my client to Do 
you want my client to talk to you first or do you want the client's email address so that 
they can send you all the information or do you want me to send the information? You can send the 
information to the solicitor via email. That's the best way to get him and then I will let him 
know if you want to give me the client name and number, 
I'll let Shawar, the solicitor, know to contact them. And also, 
if you could, yeah, send the agreement through email, that would be great. 
Yeah, got it. I'll do that. And how much fees do you charge? 
It's really dependent on the situation. Shawar won't go over that. The solicitor. Yeah? 
Got it. Got it. So, yes, I will, should you want me, can you shoot your email or how should I do it? 
Like, can you take my email address? Yeah, you can, I can give you our emails. 
And then and then yeah if you want to send the email, the information to me and Shawar 
that would be great. Got it. Okay, email address. Okay, my email is A-S-S-I-S-T-A-N-T. 
Can you go slow? A-S-S-I-S-T-A-N-T, assistant. T-A-N-T, okay. At owslaw.ca. O-W-S-Law.ca. Yep. 
And Shawar, his email is S-H-A-H-W-A-R. A-S-T-A-N-T. Yep, and Shawar, his email is shahwarSlaw.ca.
Got it. So I got it. Assistant at OWSlaw.ca. Yep. And shower, uh, S-H-A-H, W-A-R, uh, at OWSlaw.ca. 
Yes, perfect Okay, I'll send you The information and the contact number and then agreements as well. 
Yes What's the maximum fee like I just need to know the approximate amount like it's just a Bias and I did I wouldn't know honestly. 
That's something I can I can give Shawar your number and he can go over that with you, 
but I wouldn't personally know how much maximum fees would be. Can I have this yours number? 
Yeah, so I will take your number down and we will give you a call back. Got it. 
Okay, and this number is okay to give you a call back on? Yes, please. 
Yep, and can I get your full name please? Yeah, it's B-H-A-V-E-F-H. 
Yep, and your last name? G-U-L-S-H Yep, and your last name? G-U-L-V-I Okay, 
and you said you're a real estate agent, right? Yes, please. Okay, perfect. Okay, 
and this number 647-608-3904 is okay? Right. Okay, perfect. Okay, 
we'll give you a call back and I'll let Chihuahua know that you are emailing him okay 
thank you so much thank you thank you bye bye"


Answer: 

{
  "Topic": "Real Estate Closing Services Inquiry by Bhavish from EXP Realty",
  "Executive Summary": "Bhavish discusses closing services for a Hamilton property purchase.",
  "STAR analysis": {
    "Situation": "Bhavish, an agent, has a client with a new property in Hamilton, needing closing services.",
    "Task": "Inquire about closing services and process for a new construction purchase from a developer.",
    "Action": "Instructed to email solicitor with client details and agreement for further processing.",
    "Result": "Committed to emailing solicitor; discussed fees, but specifics deferred to solicitor."
  },
  "Positive Energy": "Received instructions on how to proceed with closing services.",
  "Negative Energy": "Uncertainty about fees could create hesitation or confusion.",
  "Estimated NPS": 6,
  "CSR Rating": 7,
}

"""


def analysis(text: str, token: str) -> dict:
    user_message = f"""Please assist in summarizing the following voice mail transcription:
    {text}
    """

    client = OpenAI(api_key=token)

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    output = response.choices[0].message.content

    # convert to json
    output = json.loads(output)

    return output


def main(url: str, key: str) -> dict:
    # download and convert the audio file
    logging.info("Process started")
    audio_path = download_and_convert_audio(url)
    print(audio_path)
    # apply transcription
    print("Transcribing audio")
    text = transcribe(audio_path)
    print("Audio file transcribed")
    # # do the analysis
    print("Analyzing the transcription")
    result = analysis(text, key)
    print("Analysis completed")
    # delete the audio file
    delete_file(audio_path)

    return result


# res = main(
#     "https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-Alaw-AFsp.wav"
# )

# print(res)
