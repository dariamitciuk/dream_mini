# %%
import logging
import os
from functools import partial

import sentry_sdk

import common.dialogflow_framework.stdm.dialogflow_extention as dialogflow_extention
import common.dialogflow_framework.utils.state as state_utils

import dialogflows.common.shared_memory_ops as gaming_memory
import dialogflows.flows.gaming.intents as gaming_intents
import dialogflows.flows.gaming.nlg as gaming_nlg
import dialogflows.scopes as scopes
from dialogflows.common.intents import user_doesnt_say_yes_request, user_says_yes_request
from dialogflows.common.nlg import error_response, link_to_other_skills_response
from dialogflows.flows.gaming.states import State as GamingState
from dialogflows.flows.minecraft.intents import is_game_candidate_minecraft, is_minecraft_mentioned_in_user_uttr
from dialogflows.flows.minecraft.states import State as MinecraftState

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))

logger = logging.getLogger(__name__)


##################################################################################################################
# error
##################################################################################################################


##################################################################################################################
##################################################################################################################
# linking
##################################################################################################################
##################################################################################################################

simplified_dialogflow = dialogflow_extention.DFEasyFilling(GamingState.USR_START)
##################################################################################################################
#  START
# ######### transition State.USR_START -> State.SYS_HI if hi_request==True (request returns only bool values) ####
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_START,
    {
        GamingState.SYS_USER_MAYBE_WANTS_TO_TALK_ABOUT_PARTICULAR_GAME:
            gaming_intents.user_maybe_wants_to_talk_about_particular_game_request,
        GamingState.SYS_USER_DEFINITELY_WANTS_TO_TALK_ABOUT_GAME_BOT_NEVER_PLAYED:
            partial(
                gaming_intents.user_definitely_wants_to_talk_about_particular_game_request,
                additional_check=lambda n, v: not is_minecraft_mentioned_in_user_uttr(n, v),
            ),
        (scopes.MINECRAFT, MinecraftState.USR_START):
            partial(
                gaming_intents.user_definitely_wants_to_talk_about_particular_game_request,
                additional_check=is_minecraft_mentioned_in_user_uttr),
    },
)
# ######### if all *_request==False then transition State.USR_START -> State.SYS_ERR  #########
simplified_dialogflow.set_error_successor(GamingState.USR_START, GamingState.SYS_ERR)

##################################################################################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_MAYBE_WANTS_TO_TALK_ABOUT_PARTICULAR_GAME,
    GamingState.USR_CHECK_WITH_USER_GAME_TITLE,
    gaming_nlg.check_game_name_with_user_response,
)
simplified_dialogflow.set_error_successor(
    GamingState.SYS_USER_MAYBE_WANTS_TO_TALK_ABOUT_PARTICULAR_GAME, GamingState.SYS_ERR)
################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_DEFINITELY_WANTS_TO_TALK_ABOUT_GAME_BOT_NEVER_PLAYED,
    GamingState.USR_CONFESS_BOT_NEVER_PLAYED_GAME_ASK_USER_IF_HE_PLAYED,
    partial(
        gaming_nlg.confess_bot_never_played_game_and_ask_user_if_he_played_response,
        candidate_game_id_is_already_set=False
    ),
)
simplified_dialogflow.set_error_successor(
    GamingState.SYS_USER_DEFINITELY_WANTS_TO_TALK_ABOUT_GAME_BOT_NEVER_PLAYED, GamingState.SYS_ERR)

################
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_CHECK_WITH_USER_GAME_TITLE,
    {
        GamingState.SYS_USER_CONFIRMS_GAME_BOT_NEVER_PLAYED: partial(
            user_says_yes_request,
            additional_check=lambda n, v: not is_game_candidate_minecraft(n, v),
        ),
        (scopes.MINECRAFT, MinecraftState.USR_START): partial(
            user_says_yes_request,
            additional_check=is_game_candidate_minecraft
        ),
        GamingState.SYS_USER_DOESNT_CONFIRM_GAME: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(GamingState.USR_CHECK_WITH_USER_GAME_TITLE, GamingState.SYS_ERR)
#########################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_DOESNT_CONFIRM_GAME,
    GamingState.USR_START,
    partial(
        link_to_other_skills_response,
        shared_memory_actions=[gaming_memory.clean_candidate_game_id],
        prefix="Sorry, never mind.",
    )
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_DOESNT_CONFIRM_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_CONFIRMS_GAME_BOT_NEVER_PLAYED,
    GamingState.USR_CONFESS_BOT_NEVER_PLAYED_GAME_ASK_USER_IF_HE_PLAYED,
    partial(
        gaming_nlg.confess_bot_never_played_game_and_ask_user_if_he_played_response,
        candidate_game_id_is_already_set=True
    ),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_CONFIRMS_GAME_BOT_NEVER_PLAYED, GamingState.SYS_ERR)
##############################################################

simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_CONFESS_BOT_NEVER_PLAYED_GAME_ASK_USER_IF_HE_PLAYED,
    {
        GamingState.SYS_USER_PLAYED_GAME: user_says_yes_request,
        GamingState.SYS_USER_DIDNT_PLAY_GAME: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(
    GamingState.USR_CONFESS_BOT_NEVER_PLAYED_GAME_ASK_USER_IF_HE_PLAYED, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_PLAYED_GAME,
    GamingState.USR_TELL_ABOUT_WHAT_BOT_LIKES_AND_ASK_IF_USER_RECOMMENDS_GAME,
    gaming_nlg.tell_about_what_bot_likes_and_ask_if_user_recommends_game_response,
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_PLAYED_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_TELL_ABOUT_WHAT_BOT_LIKES_AND_ASK_IF_USER_RECOMMENDS_GAME,
    {
        GamingState.SYS_USER_RECOMMENDS_GAME: user_says_yes_request,
        GamingState.SYS_USER_DOESNT_RECOMMEND_GAME: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(
    GamingState.USR_TELL_ABOUT_WHAT_BOT_LIKES_AND_ASK_IF_USER_RECOMMENDS_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_RECOMMENDS_GAME,
    (scopes.MAIN, scopes.State.USR_ROOT),
    partial(link_to_other_skills_response, prefix="Thank you, I will definitely check it up!"),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_RECOMMENDS_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_DOESNT_RECOMMEND_GAME,
    (scopes.MAIN, scopes.State.USR_ROOT),
    partial(link_to_other_skills_response, prefix="Thank you for saving my time!"),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_DOESNT_RECOMMEND_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_DIDNT_PLAY_GAME,
    GamingState.USR_SUGGEST_USER_GAME_DESCRIPTION,
    gaming_nlg.suggest_user_game_description_response,
)
simplified_dialogflow.set_error_successor(
    GamingState.SYS_USER_DIDNT_PLAY_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_SUGGEST_USER_GAME_DESCRIPTION,
    {
        GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_AND_2_OR_MORE_TURNS_OF_DESCRIPTION_REMAIN: partial(
            user_says_yes_request,
            additional_check=gaming_memory.are_there_2_or_more_turns_left_in_game_description,
        ),
        GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_LAST_TURN_OF_DESCRIPTION: partial(
            user_says_yes_request,
            additional_check=lambda n, v: not gaming_memory.are_there_2_or_more_turns_left_in_game_description(n, v),
        ),
        GamingState.SYS_USER_DOESNT_WANT_GAME_DESCRIPTION: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(GamingState.USR_SUGGEST_USER_GAME_DESCRIPTION, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_AND_2_OR_MORE_TURNS_OF_DESCRIPTION_REMAIN,
    GamingState.USR_DESCRIBE_GAME_TO_USER_AND_ASK_IF_HE_WANTS_MORE,
    partial(gaming_nlg.describe_game_to_user_response, ask_if_user_wants_more=True),
)
simplified_dialogflow.set_error_successor(
    GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_AND_2_OR_MORE_TURNS_OF_DESCRIPTION_REMAIN, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_LAST_TURN_OF_DESCRIPTION,
    GamingState.USR_DESCRIBE_GAME_TO_USER_AND_ASK_HE_WANTS_TO_PLAY_GAME,
    partial(gaming_nlg.describe_game_to_user_response, ask_if_user_wants_more=False),
)
simplified_dialogflow.set_error_successor(
    GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_LAST_TURN_OF_DESCRIPTION, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_DESCRIBE_GAME_TO_USER_AND_ASK_IF_HE_WANTS_MORE,
    {
        GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_AND_2_OR_MORE_TURNS_OF_DESCRIPTION_REMAIN: partial(
            user_says_yes_request,
            additional_check=gaming_memory.are_there_2_or_more_turns_left_in_game_description
        ),
        GamingState.SYS_USER_WANTS_GAME_DESCRIPTION_LAST_TURN_OF_DESCRIPTION: partial(
            user_says_yes_request,
            additional_check=lambda n, v: not gaming_memory.are_there_2_or_more_turns_left_in_game_description(n, v),
        ),
        GamingState.SYS_USER_DOESNT_WANT_GAME_DESCRIPTION: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(
    GamingState.USR_DESCRIBE_GAME_TO_USER_AND_ASK_IF_HE_WANTS_MORE, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_user_serial_transitions(
    GamingState.USR_DESCRIBE_GAME_TO_USER_AND_ASK_HE_WANTS_TO_PLAY_GAME,
    {
        GamingState.SYS_USER_SAYS_HE_WANTS_TO_PLAY_GAME: user_says_yes_request,
        GamingState.SYS_USER_SAYS_HE_DOESNT_WANT_TO_PLAY_GAME: user_doesnt_say_yes_request,
    },
)
simplified_dialogflow.set_error_successor(GamingState.USR_SUGGEST_USER_GAME_DESCRIPTION, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_DOESNT_WANT_GAME_DESCRIPTION,
    (scopes.MAIN, scopes.State.USR_ROOT),
    partial(
        link_to_other_skills_response,
        prefix="Okay.",
        shared_memory_actions=[lambda vars: state_utils.save_to_shared_memory(vars, curr_summary_sent_index=0)],
    ),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_RECOMMENDS_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_SAYS_HE_WANTS_TO_PLAY_GAME,
    (scopes.MAIN, scopes.State.USR_ROOT),
    partial(link_to_other_skills_response, prefix="Cool! Hope you will have good time."),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_SAYS_HE_WANTS_TO_PLAY_GAME, GamingState.SYS_ERR)
##############################################################
simplified_dialogflow.add_system_transition(
    GamingState.SYS_USER_SAYS_HE_DOESNT_WANT_TO_PLAY_GAME,
    (scopes.MAIN, scopes.State.USR_ROOT),
    partial(link_to_other_skills_response, prefix="Cool! I am glad I could help."),
)
simplified_dialogflow.set_error_successor(GamingState.SYS_USER_SAYS_HE_DOESNT_WANT_TO_PLAY_GAME, GamingState.SYS_ERR)
##############################################################

simplified_dialogflow.add_global_user_serial_transitions(
    {
        GamingState.SYS_ERR: (lambda x, y: True, -1.0),
    },
)
simplified_dialogflow.add_system_transition(
    GamingState.SYS_ERR,
    (scopes.MAIN, scopes.State.USR_ROOT),
    error_response,
)

dialogflow = simplified_dialogflow.get_dialogflow()