from sublime_plugin import TextCommand
import sublime
import logging
import re

logger = logging.getLogger(__name__)

class SemanticLinefeedCommand(TextCommand):

    def run(self, edit, syntax_sensitive=False):
        if self.region_set_empty(self.view.sel()):
            self.parse_region(edit, sublime.Region(0, self.view.size()))
        else:
            region_set = self.view.sel()
            for region in region_set:
                self.parse_region(edit, region)

    def region_set_empty(self, region_set):
        for region in region_set:
            if not region.empty():
                return False
        return True

    def parse_region(self, edit, region):
        content = self.view.substr(region)

        try:
            output = self.wrap_lines(content)
            self.view.replace(
                edit,
                region,
                output
            )
        except Exception as e:
            logger.error(e, exc_info=True)

    def wrap_lines(self, content):
        return re.sub(
            r'(.{8,9999}?)(\.|\?|!) (\w)',
            r'\1\2\n\3',
            content
        )