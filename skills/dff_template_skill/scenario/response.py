from argparse import ArgumentParser
import logging
from typing import Any

from dff.core import Context, Actor
from programy.clients.args import ClientArguments
from programy.clients.client import BotClient
from programy.clients.config import ClientConfigurationData
import uuid

from utils.normalizer import PreProcessor
class AIBotClient(BotClient):
    def __init__(self, botid: str, argument_parser: ArgumentParser = None):
        BotClient.__init__(self, botid, argument_parser)

    def get_client_configuration(self):
        return ClientConfigurationData("rest")

    def parse_arguments(self, argument_parser: ArgumentParser):
        client_args = AIBotArguments(self, parser=argument_parser)
        client_args.parse_args(self)
        return client_args

    def ask_question(self, userid: str, question: str, metadata: Any = None):
        response = ""
        try:
            self._questions += 1
            client_context = self.create_client_context(userid)
            response = client_context.bot.ask_question(client_context, question, responselogger=self)

        except Exception as e:
            logging.exception(e)

        return response


class AIBotArguments(ClientArguments):
    def __init__(self, client: AIBotClient, parser: ArgumentParser = None):
        self.args = None

        ClientArguments.__init__(self, client)
        self._config_name = "/src/data/config.aibot.yaml"
        self._config_format = "yaml"
        self._logging = None
        if parser is None:
            self.parser = ArgumentParser()
        else:
            self.parser = parser
        client.add_client_arguments(self.parser)

    def parse_args(self, client: AIBotClient):
        client.parse_args(self, self.args)


try:
    logging.info("Start to load model")

    model = AIBotClient("AIBot")
    preprocessor = PreProcessor(fpath="/src/data/storage/lookups/normal.txt")

    logging.info("Load model")
except Exception as e:
    logging.exception(e)
    raise (e)


def programy_reponse(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    # user_sentences = user_sentences[0] if user_sentences else [""]

    # replace_phrases = ["thanks.", "thank you.", "please."]
    # for phrase in replace_phrases:
    #     if user_sentences[-1] != phrase:
    #         user_sentences[-1] = user_sentences[-1].replace(phrase, "").strip()

    userid = uuid.uuid4().hex
    # if user said let's chat at beginning of a dialogue, that we
    # should response with greeting
    response = ""
    for _, sentence in enumerate(ctx.requests.values()):
        # s = s if i != 0 else f"BEGIN_USER_UTTER {s}"
        response = model.ask_question(userid, preprocessor.process(sentence))
        import sys
        print(response, file=sys.stderr, flush=True)

    # if "DEFAULT_SORRY_RESPONCE" in response:
    #     response = (
    #         " "
    #         "Sorry, I don't have an answer for that! "
    #         ""
    #     )

    # untagged_text, ssml_tagged_text = create_amazon_ssml_markup(answer)

    # responses = f"{responses} {untagged_text.strip()}"
    return response