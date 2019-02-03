# -*- coding: utf-8-*-
import logging
from . import plugin_loader
from . import config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Brain(object):

    def __init__(self, conversation):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of plugins. Note that the order of brain.plugins
        matters, as the Brain will cease execution on the first plugin
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        """
        self.plugins = plugin_loader.get_plugins()
        self.handling = False
        self.conversation = conversation

    def query(self, texts):
        """
        Passes user input to the appropriate plugin, testing it against
        each candidate plugin's isValid function.

        Arguments:
        texts -- user input, typically speech, to be parsed by a plugin
        """

        for plugin in self.plugins:
            for text in texts:
                if not plugin.isValid(text):
                    continue

                logger.debug("'%s' is a valid phrase for plugin " +
                                   "'%s'", text, plugin.__name__)
                continueHandle = False
                try:
                    self.handling = True
                    continueHandle = plugin.handle(text, self.conversation, config.getConfig())
                    self.handling = False
                except Exception:
                    logger.critical('Failed to execute plugin',
                                       exc_info=True)
                    reply = u"抱歉，插件{}出故障了，晚点再试试吧".format(plugin.SLUG)
                    self.conversation.say(reply)
                else:
                    logger.debug("Handling of phrase '%s' by " +
                                       "plugin '%s' completed", text,
                                       plugin.__name__)                    
                finally:
                    if not continueHandle:
                        return True

        logger.debug("No plugin was able to handle any of these " +
                     "phrases: %r", texts)
        return False
