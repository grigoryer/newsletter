from openai import OpenAI
from sk import my_sk
from gmail_api import init_gmail_service, send_email
from datetime import date
import markdown

client = OpenAI(api_key=my_sk)
client_file = 'client_secret.json'
service = init_gmail_service(client_file)
list_filepath = "email_list2.txt"

def openai_gen():
    with open("prompt_cve.txt", "r", encoding="utf-8") as f:  
        instructions = f.read()

    response = client.chat.completions.create(
	model="gpt-4.1",
	messages=[
		{
		"role": "system",
		"content": instructions
		}
	],
	response_format={
		"type": "text"
	},
	temperature=1,
	max_completion_tokens=3000,
	top_p=1,
	frequency_penalty=0,
	presence_penalty=0,
	store=False
	)
    
    generated_message = response.choices[0].message.content
    generated_message = markdown.markdown(generated_message)
    return generated_message


def deliver_email(service, filepath, body):
    to_address = get_email_list(filepath)
    today = date.today().strftime("%B %d, %Y")
    email_subject = f"Cybersecurity Newsletter - {today}"
    email_body = body

    sending_email = send_email(
        service, 
        to_address,
        email_subject,
        email_body,
        body_type='html'
    )

    print(sending_email)


def get_email_list(file_path):
    try:
        with open(file_path, 'r') as file:
            email_list = [line.strip() for line in file if line.strip()]
        return email_list
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return [] 


def create_newsletter():
    generated_message = openai_gen()
    deliver_email(service, list_filepath, generated_message)

create_newsletter()