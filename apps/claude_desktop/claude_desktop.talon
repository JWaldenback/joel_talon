app: claude_desktop
-

# Conversations
chat new: key(ctrl-n)
conversation new: key(ctrl-n)

# Sidebar / navigation
sidebar toggle: key(ctrl-b)
search chats: key(ctrl-k)
command bar: key(ctrl-k)

# Submission / cancellation
message send: key(enter)
message cancel: key(esc)
stop it: key(esc)

# Slash commands
# Full reference: https://code.claude.com/docs/en/commands
# Note: a free-form `slash <text>` rule doesn't work reliably (dictation
# eats the word "slash"), so each command gets its own explicit rule.

# User-requested
slash clear: insert("/clear")        # start a new conversation, empty context
slash init: insert("/init")          # initialize CLAUDE.md for the project
slash mcp: insert("/mcp")            # manage MCP servers and OAuth

# Commonly useful
slash help: insert("/help")          # list every available command
slash compact: insert("/compact")    # free up context by summarizing the conversation
slash model: insert("/model")        # switch model / adjust effort
slash config: insert("/config")      # open settings (theme, output style, etc.)
slash plan: insert("/plan")          # enter plan mode
slash resume: insert("/resume")      # resume a previous conversation
slash rewind: insert("/rewind")      # rewind conversation/code to a checkpoint
slash usage: insert("/usage")        # show session cost and plan limits
slash review: insert("/review")      # review a pull request
slash context: insert("/context")    # visualize current context usage
slash agents: insert("/agents")      # manage subagent configurations
slash memory: insert("/memory")      # edit CLAUDE.md memory files
slash diff: insert("/diff")          # open the interactive diff viewer

# Quick side-question (no /-prefix dictation needed)
by the way: insert("/btw")

# App
open settings: key(ctrl-comma)
shortcuts help: key(ctrl-/)
reload it: key(ctrl-r)
zoom in: key(ctrl-=)
zoom out: key(ctrl--)
zoom reset: key(ctrl-0)
