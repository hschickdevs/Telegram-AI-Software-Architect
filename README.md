<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python3-yellow?style=for-the-badge" alt="Made with Python3" />
  <a href="https://github.com/hschickdevs/Telegram-AI-Codebase-Architect/stargazers"><img src="https://img.shields.io/github/stars/hschickdevs/Telegram-AI-Codebase-Architect.svg?style=for-the-badge&color=219ED9" alt="Stargazers" /></a>
  <a href="https://github.com/hschickdevs/Telegram-AI-Codebase-Architect/blob/main/LICENSE"><img src="https://img.shields.io/github/license/hschickdevs/Telegram-AI-Codebase-Architect.svg?style=for-the-badge&color=green" alt="GPLv3 License" /></a>
</p>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="./docs/logo_circle.png" alt="Logo" width="150" height="150">

  <h3 align="center">Telegram-AI-Codebase-Architect</h3>

  <p align="center">
    A powerful Telegram bot that uses large language models (LLMs) to architect fully structured, ready-to-deploy software projects from user prompts in a matter of seconds.
    <br />
    <h4>Notable Features:</h4>
    <p>
        <i>Single model call for codebase generation to reduce token cost</i>
    </p>
    <p>
        <i>Supports <a href="https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo">OpenAI</a> and <a href="https://www.anthropic.com/claude">Claude</a> language models</i>
    </p>
    <p>
        <i>Output includes requirement and readme files for setup & usage</i>
    </p>
    <a href="#about-the-project"><strong>Learn More »</strong></a>
    <br />
    <br />
    <a href="https://t.me/AITelegramTranslate_bot">Try Demo</a>
    ·
    <a href="#deployment">Deployment</a>
    ·
    <a href="#bot-commands">Commands</a>
    ·
    <a href="#contributing">Contribute</a>
  </p>
</div>

<!-- # Telegram-AI-Codebase-Architect

> 🚧 _CURRENTLY IN DEVELOPMENT ..._

 Telegram bot that uses AI to generate full codebases from user prompts. It provides structured, ready-to-deploy software projects, differentiating from simple code generation by offering entire architectural solutions. Prompt the bot with a detailed description of the software you want to build, and it will generate a full codebase for you and send the zipped code the Telegram chat.

 **Notable Features**:

 * Codebase generation is done in a single API call to save on context token cost.

 * Supports [OpenAI](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) and [Claude](https://www.anthropic.com/claude) language models (_Claude performs significantly better_)

 > **Note:** Even though the Claude and OpenAI models are supported, Claude actually performs much better in this specific task. 

 ## Testing Prompts:

 `/generate basic software that allows the user to input two numbers from the command line. The output to the console should be "HELLO WORLD! Here is your number: <number>"` -->

<!-- ABOUT THE PROJECT -->
## About the Project

![PRODUCT DEMO/GIF](docs/demo.gif)

This Telegram bot leverages the power of OpenAI's GPT language models to provide advanced text translations. Unlike traditional translation services like Google Translate, this bot offers several unique advantages:

1. **Contextual and Punctual Accuracy**: Through prompt engineering, the bot is capable of understanding the context and nuances of the text, providing translations that are both contextually and punctually accurate.

2. **Specific Language Context**: The bot can be configured to understand and translate specific dialects or regional language variations, such as Spanish (Mexico Dialect).

3. **Typo Detection**: The advanced AI model automatically detects typos and corrects them, ensuring the translation is as accurate as possible.

> 💡 **Tip:** This bot can be used in group chats as well as private chats for live translations!


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get your own local instance of the Telegram AI translation bot up and running, follow these simple steps:

### Prerequisites

Before you continue, you will need to do the following:

1. Get an **OpenAI API key**. If you don't know how to do so, use [**this guide**](https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt) for reference.

    > Before sure to review the [pricing](https://openai.com/pricing/) for OpenAI's API in deciding which model to use. The default model is `gpt-3.5-turbo`, which is the cheaper and faster option.

2. Create a new **Telegram bot** and get the **bot token** using [**BotFather**](https://t.me/botfather). If you don't know how to do so, use [**this guide**](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) for reference. Additionally, you will need to change the following settings in BotFather:

    1. `/mybots` -> `<your_bot_name>` -> `Bot Settings` -> `Group Privacy` -> `Turn off`

    2. `/mybots` -> `<your_bot_name>` -> `Bot Settings` -> `Allow Groups` -> `Turn on`

### Quick Setup

Although there isn't a completely simple way to set up this bot, the easiest way to do so is by deploy the Docker image on Google Cloud Platform. If you don't know what a Docker image is, don't worry, the following steps will guide you through the process of deploying the bot to the cloud using Google Cloud Platform:

[**🔗VIEW THE GUIDE HERE**](docs/gcp-deploy/gcp-deploy.md)


### Advanced Setup

If you'd prefer to deploy the bot manually, follow the folowing steps in your preferred local or cloud environment. For the sake of this guide, we will be deploying the bot locally from source and docker in a UNIX environment (On a MacOS or Linux machine).

#### Option 1: Run Locally using Docker

> If you don't have docker installed, you can use [Option 2](#option-2-run-locally-from-source) to run the bot locally from source.

1. Pull the Docker image from Docker Hub:

   ```sh
   docker pull hschickdevs/telegram-translate-ai
   ```

2. Run the Docker image:

    You will need to specify your OpenAI API key and Telegram bot token as environment variables. Additionally, you can specify the GPT model to use (e.g., `gpt-3.5-turbo` or `gpt-4`, or any desired model [listed on their website](https://platform.openai.com/docs/models/continuous-model-upgrades)). You can leave the `MODEL` environment variable empty to use the default model (3.5 turbo).

    ```sh
    docker run -d --name telegram-translate-ai \
      -e OPENAI_TOKEN=<YOUR_APIKEY> \
      -e BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN> \
      -e MODEL=<GPT-MODEL> \
      hschickdevs/telegram-translate-ai
    ```

  3. If you want to see the logs, you can use the following command:

      ```sh
      docker logs -f telegram-translate-ai
      ```

      You can also attach to the container to see the logs in real-time:

      ```sh
      docker attach telegram-translate-ai
      ```

      If you don't see any errors, the bot should now be running! Head to your bot on Telegram and test it out.

#### Option 2: Run Locally from Source

1. Before you begin, make sure you have Python 3.9+ and pip installed on your system.

    Check your Python version in your command prompt using:

    * **MacOS/Linux:**
      ```sh
      python3 -V
      ```

    * **Windows:**
      ```sh
      python -V
      ```
      _or_
      ```sh
      py -V
      ```

    If you do not have Python 3.9+ installed, you can download it [**🔗 here**](https://www.python.org/downloads/).

2. Clone the repo:

   ```sh
   git clone https://github.com/hschickdevs/Telegram-Translate-AI.git
   ```

3. CD into the project directory:

   ```sh
   cd Telegram-Translate-AI
   ```
   
4. Install pip packages:
   
   ```sh
   pip install -r requirements.txt
   ```

3. Set environment variables. The following environment variables should be set:

   ```sh
   OPENAI_TOKEN=<YOUR_APIKEY>
   BOT_TOKEN=<YOUR_TOKEN>
   MODEL=<GPT-MODEL>
   ```

   > **Note:** The `MODEL` variable is optional and defaults to `gpt-3.5-turbo`. If you have the plus subscription, you can set this to `gpt-4` for better results.

   To set your environment variables, rename the file called [`.env.example`](/.env.example) in the root directory of the project to `.env`, and then replace the value contents with your tokens and model.

    > **Note:** The existing values in the `.env.example` file are placeholders and are for demonstration purposes only. You should **never** share your API keys or tokens with anyone.

4. Make sure that you are in the root directory of the project (_type `pwd`_), and then run the following command to start the bot:

    ```sh
    python3 -m src
    ```

    > **Note:** If you are using Windows, you may need to use `python -m src` or `py -m src` instead.

If you don't see any errors, the bot should now be running! Head to your bot on Telegram and test it out.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Bot Commands

#### `/help`

Returns all available commands and their descriptions.

___

#### `/t <source (context)> - <target (context)> - <text>`

(Use **/t** or **/translate**) 📖 Translate text from one language to another. 

> The first two "-" symbols are used as the delimiter/separator for the source language & context, target language & context, and text. As long as you provide the first two "-" symbols between source & target and target & text, you can use as many as you want in the text.

| Parameter          | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| source (context)   | The source language and context (e.g., dialect) from which you want to translate.                |
| target (context)   | The target language and context (e.g., dialect) to which you want to translate.                  |
| text               | The text you want to translate.                                                                  |

_For example, the following command translates English to Spanish in the dialect of Madrid, Spain (as opposed to Mexico City dialect):_

`/t English - Spanish (Madrid Dialect) - Hi there, I'm a bot!`

___

#### `/s <language1 (context)> - <language2 (context)>`

(Use **/s** or **/session**) 🔄 Start a continuous translation session. In this mode, every following message you send will be automatically language detected and translated to the other language in the pair.

| Parameter          | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| language1 (context)   | The first language and context (e.g., dialect) in the translation pair.   |
| language2 (context)   | The second language and context (e.g., dialect) in the translation pair.     |

_For example, the following command starts a continuous translation session with English and Spanish in the Mexico City dialect:_

`/session English - Spanish (Mexico City Dialect)`

🛑 To end a continuous session, click the "Quit Session" button on the inline keyboard below any of the translated messages.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Acknowledgements

Thanks to these awesome tools and frameworks for aiding in the development of this project!

* [PyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* [OpenAI Python Library](https://pypi.org/project/openai/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Add translation sessions
- [x] Add detailed documentation
- [x] Add Docker image
- [x] Add bot Demo feature 
- [X] Add group translation sessions
- [ ] Multi-platform Support
    - [ ] Whatsapp
    - [ ] Discord

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GPLv3.0 License. See `LICENSE.txt` for more information.

In summary, the GNU General Public License v3 (GPLv3) is a free software license that allows you to use, modify, and distribute the software for personal and commercial use. 

However, any changes you make must also be open-sourced under the same license. This ensures that derivative work remains free and open, promoting collaboration and transparency. Importantly, if you distribute the software or any modifications, you must make the source code available and clearly state any changes you've made.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

**Telegram:** [@hschickdevs](https://t.me/hschickdevs)