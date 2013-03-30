#   Copyright 2011 Chris Behrens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Pyhole RegEx Plugin"""

import random
import re

from pyhole import plugin
from pyhole import utils


class RegEx(plugin.Plugin):
    """Catch regular expression substituation in IRC"""

    def __init__(self, irc, *args, **kwargs):
        super(RegEx, self).__init__(irc, *args, **kwargs)
        self.irc_history = []

    def history_update(self, source, message):
        self.irc_history.insert(0, (source, message))
        try:
            lookback = utils.get_config("Regex").get("lookback")
        except:
            lookback = 10
        if len(self.irc_history) > int(lookback):
            self.irc_history.pop()

    def _history_push(self, message):
        """Pushes messages onto the stack"""

    @plugin.hook_add_msg_regex('.*')
    def regex(self, params=None, **kwargs):
        """All message hook"""

        try:
            private = kwargs['private']
            full_message = kwargs['full_message']
        except TypeError:
            return

        m = re.search('^s\/(.*)\/(.*)\/(.*)(\s|$)', full_message)
        if not m:
            if private:
                return
            # ignore people messing up and missing the last /
            if re.search('^s\/(.*)\/', full_message):
                return
            self.history_update(self.irc.source.split('!')[0], full_message)
            return

        if 'g' in m.group(3):
            count = 0
        else:
            count = 1

        for source, message in self.irc_history:
            str = re.sub(m.group(1), m.group(2), message, count)
            if str != message:
                self.irc.reply("<%s> %s" % (source, str))
                # pretend this really happened
                if not private:
                    self.history_update(source, str)
                return

    @plugin.hook_add_command('dietz')
    def dietz(self, params=None, **kwargs):
        """Docking"""
        try:
            private = kwargs['private']
        except TypeError:
            return

        # Get last message from IRC history
        if private:
           return
        source, message = self.irc_history[0]
        str_buf = []
        for word in message.split(" "):
            sperms = ""
            if random.randint(0, 10) > 9:
                num_sperms = random.randint(1,3)
                condom = []
                for i in xrange(num_sperms):
                    velocity = random.randint(0, 3)
                    condom.append("%s~o" % (" " * velocity))
                sperms = "".join(condom)
            shaft = ('=' * len(word))
            dick = "8%sD %s" % (shaft, sperms)

            str_buf.append(dick)
        self.irc.reply("<%s> %s" % (source, ' '.join(str_buf)))
