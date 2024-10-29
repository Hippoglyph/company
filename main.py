from dotenv import load_dotenv
load_dotenv(override=True)

from llm.llm_enum import LLMEnum

llm = LLMEnum.LLaMa3_8b.value

print(llm.query("", "What is the best thing you know?"))