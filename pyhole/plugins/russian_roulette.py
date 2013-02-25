#   Copyright 2011 Jason Koelker
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

"""Pyhole Russian Roulette Plugin"""

try:
    import randomdotorg
    random = randomdotorg.RandomDotOrg()
except ImportError:
    import random

from pyhole import plugin


class RussianRoulette(plugin.Plugin):
    """Provide access to dice games"""

    def __init__(self, *args, **kwargs):
        super(RussianRoulette, self).__init__(*args, **kwargs)
        self.game = None

    def _gun(self, size=6):
        chamber = [0] * (size - 1)
        chamber.append(1)
        random.shuffle(chamber)
        return chamber

    @plugin.hook_add_command("russian")
    def roulette(self, params=None, **kwargs):
        """Play russian roulette:
            play the game: .russian play
            stop the game: .russian wuss
        """
        if params:
            cmd = params.split(' ', 1)[0].lower()
            if cmd == 'play':
                if not self.game:
                    self.game = self._gun()
                if self.game.pop() == 1:
                    result = 'BANG!'
                    self.game = None
                else:
                    result = 'click'
            elif cmd == 'wuss':
                result = 'Come on man, you chicken?'
                self.game = None
            elif cmd == 'thorn':
                result = 'http://i.imgur.com/fNE4h.jpg'
            else:
                result = self.roulette.__doc__
        else:
            result = self.roulette.__doc__

        self.irc.reply(result)
