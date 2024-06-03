import re
from node import Node, TextNode

class MarkdownTokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.ast = Node(node_type="root", childs=[])
        self.tokenize(self.text, self.ast)
        self.prettify_ast(self.ast.get_childs())
        # print("ds", self.ast.get_last_child().get_childs()[1].get_content())
        print(len(self.ast.get_childs()))
    
    def tokenize(self, markdown_text, parent_node):
        header_re = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)
        list_re = re.compile(r'^(\*|\-|\+|\d+\.)\s+(.*)', re.MULTILINE)
        block_quote_re = re.compile(r'^> ?(.*)', re.MULTILINE)

        bold_re = re.compile(r'\*\*(.*?)\*\*', re.MULTILINE)
        italic_re = re.compile(r'\*(.*?)\*', re.MULTILINE)
        link_re = re.compile(r'\[(.*?)\]\((.*?)\)', re.MULTILINE)
        new_line_re = re.compile(r'\n')
        patterns = [
            (list_re, True),
            (bold_re, False),
            (italic_re, False),
            (link_re, True),
            (block_quote_re, True),
            (header_re, True),
            (new_line_re, False)

        ]
        
        pos = 0
        text_len = len(markdown_text)
        found_text = ""
        # at this point only god understands this code
        while pos < text_len:
            found_match = False
            for pattern, is_special in patterns:
                match = pattern.match(string=markdown_text[pos:])
                if match:
                    found_match = True
                    # get prev text
                    if found_text != "":
                        print("TEXT before match:", found_text.strip())
                        parent_node.add_child(TextNode(found_text.strip()))
                        found_text = ""
                    # print("MATCH:", match)
                    if match.group() == "\n":
                        pos += 1
                        break
                    n = Node(node_type="node", childs=[])
                    parent_node.add_child(n)

                    if is_special:
                        print(match.group(2))
                        self.tokenize(match.group(2), n)                    
                    pos += match.end()

                    break
            if not found_match:
                found_text += markdown_text[pos]
                pos += 1
        
        parent_node.add_child(TextNode(found_text))

    def prettify_ast(self, childs, is_from=0):
        for node in childs:
            if isinstance(node, TextNode):
                print("text node with content:", node.get_content(), is_from)
            else:
                self.prettify_ast(node.get_childs(), is_from=is_from+1)

# Example usage
sec = """
# Header first
something else **other** wow
## other header
- nice **very** cool
[this](http://example.com)
"""

MarkdownTokenizer(sec)
