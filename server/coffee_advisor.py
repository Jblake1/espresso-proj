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
    #return os.environ["OPENAI_API_KEY"]


# account for deprecation of LLM model

current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
llm_model = "gpt-3.5-turbo" if current_date > target_date else "gpt-3.5-turbo-0301"
llm = ChatOpenAI(temperature=0.3, model=llm_model)

def get_coffee_advice(drink, coffee_beans, brewing_device, grinder):
    coffee_setup = {
        "drink": drink,
        "coffee_beans": coffee_beans,
        "brewing_device": brewing_device,
        "grinder": grinder
    }

    #suggest grind size
    first_prompt = ChatPromptTemplate.from_template(
        "Respond to this prompt only with a numeric grind setting from 1 to 100 (1 being the finest setting)."
        "Optimizing for flavor suggest a numeric grind setting from 1 to 100"
        "given the grinder specified below is being used to brew the drink specified below"
        "with the coffee beans and brewing device specified below:"
        "\n\nGrinder: {grinder}\n\nDrink: {drink}\n\nCoffee Beans: {coffee_beans}\n\nBrewing Device: {brewing_device}"
    )
    chain_one = LLMChain(llm=llm, prompt=first_prompt, output_key="grind_setting")

    #predict brew time
    second_prompt = ChatPromptTemplate.from_template(
        "Optimizing for flavor, respond to this prompt only with a specific five second range suggesting"
        "a brew time given the grinder specified below"
        "is set the the grind settting specified below and being used to brew the drink specified below"
        "with the coffee beans and brewing device specified below:"
        "\n\nGrinder: {grinder}\n\nDrink: {drink}\n\nCoffee Beans: {coffee_beans}\n\n"
        "Brewing Device: {brewing_device}\n\nGrind Setting: {grind_setting}"
    )
    # chain 2: takes all inputs and provides brew time
    chain_two = LLMChain(llm=llm, prompt=second_prompt, output_key="brew_time")

    overall_chain = SequentialChain(
        chains=[chain_one, chain_two],
        input_variables=["grinder","drink","coffee_beans","brewing_device"],
        output_variables=["grind_setting", "brew_time"],
        verbose=True
    )


    result = overall_chain(coffee_setup)
    return result






