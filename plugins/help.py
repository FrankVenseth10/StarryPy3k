import traceback

from base_plugin import SimpleCommandPlugin
from utilities import syntax, Command, send_message


class HelpPlugin(SimpleCommandPlugin):
    name = "help_plugin"
    depends = ["command_dispatcher"]

    def activate(self):
        super().activate()
        cd = self.plugins.command_dispatcher
        self.commands = cd.commands
        self.command_prefix = cd.plugin_config.command_prefix

    @Command("help", doc="Help command.")
    def _help(self, data, protocol):
        if not data:
            commands = []
            for c, f in self.commands.items():
                if f.roles - protocol.player.roles:
                    continue
                commands.append(c)
            send_message(protocol,
                         "Available commands: %s" % " ".join(
                             [command for command in commands]))
        else:
            try:
                docstring = self.commands[data[0]].__doc__
                send_message(protocol,
                             "Help for %s: %s" % (data[0], docstring),
                             syntax(data[0],
                                    self.commands[data[0]],
                                    self.command_prefix))
            except:
                traceback.print_exc()
                send_message(protocol,
                             "Unknown command %s." % data[0])
