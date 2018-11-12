#!/usr/bin/python
#-*-coding:utf-8-*-

import random
from .user_agents import user_agents

DESKTOP = 'desktop'
MOBILE = 'mobile'
TV = 'tv'
TABLET = 'tablet'
ANY = 'any'

class RotateUserAgentMiddleware():
    all_agents = []
    filtered_user_agent_list = []

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def __init__(self, settings):
        self.type = settings.get('ROTATE_USER_AGENTS_TYPE', DESKTOP)
        self.all_agents = user_agents
        self.filtered_user_agent_list = self.collect_user_agents()

    def process_request(self, request, spider):
        ua = random.choice(self.filtered_user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    def collect_user_agents(self):
        if self.type == DESKTOP:
            return self.collect_desktop_agents()
        if self.type != ANY:
            return self.collect_other_agents_by_type(self.type)
        return self.all_agents

    def collect_desktop_agents(self):
        agents = set()
        for agent in self.all_agents:
            if self._is_non_desktop(agent):
                agents.add(agent)
        return list(agents)

    _non_desktop_types = [MOBILE, TV, TABLET, 'android', 'ipad', 'iphone', 'tv', 'blackberry', ]

    def _is_non_desktop(self, agent):
        for agent_type in self._non_desktop_types:
            if agent_type in agent.lower():
                return False
        return True

    def collect_other_agents_by_type(self, type):
        return [ x for x in self.all_agents if type in x.lower() ]