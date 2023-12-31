import jiggybase
import jiggybase.collection
import jiggybase.models
from jiggybase.models import PromptMessage
import jiggybase.org

#Create Jiggybase collection
jb = jiggybase.JiggyBase()                  # Initialize JiggyBase
ORGANIZATION_NAME = 'elm09'                 # Set your organization and collection name
COLLECTION_NAME = 'Climate disclosures'     # Get a specific collection
collection = jb.collection(COLLECTION_NAME) # Instantiate collection
org = jb.get_org(ORGANIZATION_NAME)

#Populate Jiggybase collection list
def collection_doc_names_id():
    doc_chunks, next_index = collection.get_doc_chunks()
    filename_id = [(doc_chunk[0].metadata.source_id, doc_chunk[0].metadata.document_id) for doc_chunk in doc_chunks]
    return filename_id

def upload_file(collection, file):
    try:
        upsert_rsp = collection.upsert_file(file)
    except Exception as e:
        print(f'Error on {file}: {e}')
        return
    doc_id = upsert_rsp.ids[0]
    dcl =  collection.get_doc(doc_id)
    text_len = len(" ".join([dc.text for dc in dcl]))
    title = dcl[0].metadata.title if dcl[0].metadata.title else "Unknown Title"

def submit_prompt(template,company,qnumber):
    # Split the template into separate prompts
    prompt = template.split('Prompt ')[qnumber]  # omit the first split result as it will be empty
    prompt_number, prompt_text = prompt.split(" :", 1)  # split only on the first " :", to separate the prompt number from the rest
    prompt_text = prompt_text.replace('X', company)  # replace 'X' with the company name
    prompt_message = PromptMessage(
        content=prompt_text,
        role="user",
        position=1,
        extras=None)
    task = org.create_prompt_task(
            name=company.replace(" ", "_"),  # Replace spaces with underscores in the prompt name
            version=1,
            prompts=[prompt_message],  # Wrap the prompt message in a list
            type=None,
            description=f"{company}_report"  # Use the company name in the description
            )

    response = collection._chat_completion(task.prompts,
                                        temperature=0,
                                        model="gpt-3.5-turbo"
                                        )
    return prompt_text, response.choices[0].message.content
    



