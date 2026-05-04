"""
This module gives us the list {user.additional_words} to easily refer to system paths in talon and python files
"""
from talon import Context, Module

from ..user_settings import track_csv_list

mod = Module()
mod.list("additional_words", desc="List of additional words")

additional_words_defaults = {
    #"Spoken form": "Words(s)",
}

ctx = Context()


@track_csv_list(
    "additional_words.csv",
    headers=("Word(s)", "Spoken Form (If Different)"),
    default=additional_words_defaults,
)
def on_additional_words(values):
    ctx.lists["self.additional_words"] = values

"""
# We need to wait for ready before we can call "actions.path.talon_home()" and
# "actions.path.talon_user()"
def on_ready():
    additional_words = get_list_from_csv(
        "additional_words.csv", headers=("Word(s)", "Spoken Form (If Different)"), default=additional_words_defaults
    )

    ctx.lists["user.additional_words"] = additional_words

@mod.capture(rule="{user.additional_words}")
def additional_words(m) -> str:
    return m.additional_words

app.register("ready", on_ready)
"""