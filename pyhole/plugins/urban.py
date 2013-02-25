#   Copyright 2013 Matt Dietz
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
#   limitations under the License.import urllib

import json
import urllib

from BeautifulSoup import BeautifulSoup

from pyhole import plugin
from pyhole import utils


class UrbanDictionary(plugin.Plugin):
    @plugin.hook_add_command("urban")
    @utils.spawn
    def urban(self, params=None, **kwargs):
        """Search Urban Dictionary (ex: .urban <query>)"""
        config = utils.get_config("Urban")

        if not params:
            self.irc.reply(self.urban.__doc__)

        # Check locals first
        entries = json.loads(config.get("local_entries"))
        if entries.get(params):
            self.irc.reply(entries[params])
            return

        query = urllib.urlencode({"term": params})
        url = "http://www.urbandictionary.com/define.php?%s" % query
        response = self.irc.fetch_url(url, self.name)
        if not response:
            return

        soup = BeautifulSoup(response.read())
        results = soup.findAll("div", {"class": "definition"})

        urban = ""
        if len(results):
            urban = " ".join(str(x) for x in soup.findAll(
                    "div", {"class": "definition"})[0].contents)

        if len(urban) > 0:
            for i, line in enumerate(urban.split("<br/>")):
                if i <= 4:
                    self.irc.reply(utils.decode_entities(line))
                else:
                    self.irc.reply("[...] %s" % url)
                    break
        else:
            self.irc.reply("No results found: '%s'" % params)
