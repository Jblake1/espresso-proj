#coffee_advisor.py

import os 
import openai
import keyring 
import sys
import datetime
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain

#def set_api_key():
api_key = keyring.get_password("OPENAI_API_KEY", "openai_user")
os.environ["OPENAI_API_KEY"] = api_key



# account for deprecation of LLM model

current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
llm_model = "gpt-4" if current_date > target_date else "gpt-3.5-turbo-0301"
llm = ChatOpenAI(temperature=0.2, model=llm_model)

def get_coffee_advice(drink, coffee_beans, brewing_device, grinder, grind_range):
    coffee_setup = {
        "drink": drink,
        "coffee_beans": coffee_beans,
        "brewing_device": brewing_device,
        "grinder": grinder,
        "grind_range": grind_range
    }
    print("Coffee Setup:", coffee_setup)
    

    #Determine Coffee Profile
    first_prompt = ChatPromptTemplate.from_template("You are an expert barista answering questions for a customer making {drink} at home."
                                                    "The customer has purchased {coffee_beans} beans, but would like to understand the beans' " 
                                                    "characteristics. Provide a comprehensive description of {coffee_beans} beans including its "
                                                    "roast type (light, medium, dark) and density. The following is an example response to a customer "
                                                    "who purchased Red Bird Blue Jaguar Espresso beans: Red Bird Blue Jaguar Espresso beans are a "
                                                    "medium roast, designed to balance sweetness, acidity, and body. Being a medium roast, the beans "
                                                    "retain moderate density, which means they are neither as dense as light roasts nor as porous as dark roasts."
    )
    chain_one = LLMChain(llm=llm, prompt=first_prompt, output_key="bean_description")

    #Use Cofee Profile to determine grind segmentation
    second_prompt = ChatPromptTemplate.from_template("Based on the {bean_description} assign {coffee_beans} to one of three grind size segments: "
                                                     "1) Fine - Light roasts, single-origin coffees, or beans with high density, 2) Medium - Medium roasts, "
                                                     "balanced blends, or beans with medium density, 3) Coarse - Dark roasts or beans with lower density. Respond "
                                                     "to this prompt with only one of three grind sizes: Fine, Medium, Coarse"
    )
    chain_two = LLMChain(llm=llm, prompt=second_prompt, output_key="grind_segment")

    #Convert coffee segmentation to grind settting for specific grinder & grind scale
    third_prompt = ChatPromptTemplate.from_template("As an espresso expert advising a home barista, provide a numeric grind setting recommendation for grinding "
                                                    "{coffee_beans} using the {grinder} grinder. The {grinder} grinder has a numeric scale {grind_range} from finest to coarsest. Keep in "
                                                    "mind {coffee_beans} benefits from a {grind_segment} grind, so your response should be a number within {grind_range} "
                                                    "which corresponds to a {grind_segment} grind for espresso beans. "
    )
    chain_three = LLMChain(llm=llm, prompt=third_prompt, output_key="grind_setting")

    #Predict shot pull time
    fourth_prompt = ChatPromptTemplate.from_template("As an espresso expert advising a home barista, provide a recommended shot pull time for {coffee_beans} beans "
                                                    "given the home barista is using a {grinder} grinder set to a {grind_setting} grind which results in a {grind_segment} grind."
                                                    "The home bariasta is using a {brewing_device} to brew the {drink}. Respond to this prompt with a recommended shot pull time in seconds."
    )
    chain_four = LLMChain(llm=llm, prompt=fourth_prompt, output_key="brew_time")

    overall_chain = SequentialChain(
        chains=[chain_one, chain_two, chain_three, chain_four],
        input_variables=["grinder","drink","coffee_beans","brewing_device", "grind_range"],
        output_variables=["bean_description","grind_segment", "grind_setting","brew_time"],
        verbose=True
    )


    try:
        result = overall_chain(coffee_setup)
        print("Result:", result)
        return result
    except Exception as e:
        print("Error in get_coffee_advice:", str(e))
        raise





