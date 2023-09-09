# Generate Customer Contextualised Product Descriptions

This repository contains code to contextualise product descriptions given a customer profile description. A general product description should be transformed to a tailored product description to a customer profile. This example uses OpenAI's (an `OPENAI_API_KEY` will be required) chat model and langchain to perform the conversion.

## Areas for Improvement

This example is very crude and can be improved in several ways:

1. Prompt can be more detailed and clear to guide the model. This is controlled by the `prefix` variable in the script.
2. Include more few shot examples.
3. Reduce the dependency on a for loop to query LLM.
4. Integrate a more sophisticated representation of customer descriptions.

**Note**: I used `pip-tools` to handle dependencies so you can use `pip-sync` to load dependencies, preferably in a virtual environment.
