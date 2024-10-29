from dotenv import load_dotenv
load_dotenv(override=True)

from llm.groq_llm import GroqLLM

llm = GroqLLM()

print(llm.query("", ""))