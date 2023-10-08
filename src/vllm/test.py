from vllm import LLM

llm = LLM(model="../../models/llama-2-13b-chat.Q4_K_M.gguf")  # Name or path of your model
output = llm.generate("Hello, my name is")
print(output)