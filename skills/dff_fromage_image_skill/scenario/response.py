import logging
from df_engine.core import Context, Actor
import common.dff.integration.context as int_ctx

logger = logging.getLogger(__name__)

SUPER_CONFIDENCE = 1.0


def generic_response(ctx: Context, actor: Actor, excluded_skills=None, *args, **kwargs) -> str:
    caption = int_ctx.get_last_human_utterance(ctx, actor).get("annotations", {}).get("fromage", None)
    if caption:
        return caption
    return "An error occured while trying to read image caption annotation from service payload."