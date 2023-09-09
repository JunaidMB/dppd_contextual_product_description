## Few Shot Prompt Example
from langchain import FewShotPromptTemplate, PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import numpy as np
from pathlib import Path
from pprint import pprint
import json

load_dotenv()

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0.5)

# Load Product Description Examples
with open('product_descriptions.json', 'r') as openfile:
    product_descriptions = json.load(openfile)

# Create examples of how we want the LLM to generate product descriptions
few_shot_examples = [
    {
        "customer_description": "A working single mother with young children.",
        "original_product_description": "Smart Home Thermostat: The Smart Home Thermostat allows you to effortlessly control your home's temperature and energy consumption. With intuitive smartphone integration, you can adjust settings from anywhere." ,
        "contextual_product_description": "Smart Home Thermostat: Perfect for a cosy night in with the kids! Control your home's temperature and energy consumption with ease. Our Smart Home Thermostat allows you to adjust settings from anywhere to make sure your loved ones never get too hot or too cold while you're on the go."

    },
    {
        "customer_description": "A working single mother with young children.",
        "original_product_description": "Women's Athletic Shoes: Elevate your workout performance and style with our Women's Athletic Shoes. Designed for maximum comfort and support, these shoes feature advanced cushioning and a sleek, modern look." ,
        "contextual_product_description": "Women's Athletic Shoes: Sleak and stylist athletic shoes. Designed to help you chase after rowdy little ones and keep you comfortable on your feet all day."

    },
    {
        "customer_description": "A 26 year old single video game enthusiast",
        "original_product_description": "The Gaming Console offers immersive gaming experiences with stunning graphics and lightning-fast performance. Enjoy a vast library of games and seamless online multiplayer. Get ready to embark on epic adventures." ,
        "contextual_product_description": "Gaming Console: Perfect for the avid gamer! Control your home's temperature and energy consumption with ease. Our Smart Home Thermostat allows you to adjust settings from anywhere to create optimal gaming conditions."

    },
]

example_template = """
customer_description: {customer_description}
original_product_description: {original_product_description}
contextual_product_description: {contextual_product_description}
"""

example_prompt = PromptTemplate(
    input_variables=["customer_description", "original_product_description", "contextual_product_description"],
    template=example_template,
)


prefix = '''
You are a service that rewrites product descriptions to appeal to a customer description. 
You will take a {customer_description} and a {original_product_description} and rewrite the product description in a style that matches a customer's attitude and profile - this is called {contextual_product_description}. 
Your aim is to write a {contextual_product_description} that will appeal to the {customer_description}.
Here are some examples:
'''

suffix = """
customer_description: {customer_description}
original_product_description: {original_product_description}
contextual_product_description: """

few_shot_prompt_template = FewShotPromptTemplate(
    examples=few_shot_examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["customer_description", "original_product_description"],
    example_separator="\n\n"
)

# Create the LLMChain for the few-shot prompt template
chain = LLMChain(
    llm=llm, 
    prompt=few_shot_prompt_template
)

# Define the user query
customer_description = "A female university graduate, living alone for the first time. Enjoys going to the gym. Her hobbies include running, climbing and swimming."

# Generate contextualised product descriptions for all products
recommendations_list = []
for idx, product in enumerate(product_descriptions):
    original_product_description = product['product_description']

    # Run the LLMChain for the user query
    response = chain.run(
        {
            "customer_description": customer_description,
            "original_product_description": original_product_description
        }
        )
    
    # Parse Output
    contextualised_product_description = {
        "customer_description": customer_description,
        "original_product_description": original_product_description,
        "contextual_product_description": response.split(": ")[-1]
        }
    
    recommendations_list.append(contextualised_product_description)

# Augment the product descriptions 
recommendations_product_list = product_descriptions.copy()

for idx, prod_dict in enumerate(recommendations_product_list):
    prod_dict['customer_description'] = customer_description
    prod_dict['contextual_product_description'] = recommendations_list[idx]['contextual_product_description']

# Save the recommendations
Path("./generated_recommendations").mkdir(parents=True, exist_ok=True)

with open("./generated_recommendations/female_graduate_recommended_products.json", 'w') as file:
    json.dump(recommendations_product_list, file)