# Telegram-AI-Codebase-Architect

> 🚧 _CURRENTLY IN DEVELOPMENT ..._

 Telegram bot that uses AI to generate full codebases from user prompts. It provides structured, ready-to-deploy software projects, differentiating from simple code generation by offering entire architectural solutions. Prompt the bot with a description of the (_low complexity_) software you want to build, and it will generate a full codebase for you and send the zipped code the Telegram chat.

 All codebase generation is done in a single API call to save on context token cost.

 > **Note:** Even though the Claude and OpenAI models are supported, Claude actually performs much better in this specific task. 

 ## Testing Prompts:

 `/generate basic software that allows the user to input two numbers from the command line. The output to the console should be "HELLO WORLD! Here is your number: <number>"`

