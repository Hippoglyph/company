import re
from bs4 import BeautifulSoup

class Parse:

    @staticmethod
    def action(message : str) -> dict[str, str]:
        xml_string = Parse._stip_to_xml(message)
        soup = BeautifulSoup(xml_string, 'xml')
        result = {}
        for tag in soup.find_all():
            if not tag.name:
                continue
            if tag.name == "action":
                continue
            pattern = f"<{tag.name}>(.*?)</{tag.name}>"
            match = re.search(pattern, xml_string, re.DOTALL)
            content = match.group(1).strip()
            if content:
                result[tag.name] = content
        return result

    @staticmethod
    def _stip_to_xml(message : str) -> str:
        start_tag = "<action>"
        end_tag = "</action>"
        start_idx = message.find(start_tag)
        end_idx = message.rfind(end_tag)
        return message[start_idx:end_idx+len(end_tag)]