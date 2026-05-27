from talon import Module

mod = Module()

mod.tag("emoji", desc="Emoji, ascii emoticons and kaomoji")

mod.list("emoticon", desc="Western emoticons (ascii)")
mod.list("emoji", desc="Emoji (unicode)")
mod.list("emoji_colon_wrapped", desc="Emoji shortcodes wrapped in colons (e.g. :+1:) for GitHub/Slack/Discord")
mod.list("kaomoji", desc="Eastern kaomoji (unicode)")
