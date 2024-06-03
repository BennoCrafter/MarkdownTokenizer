import re
from node import Node, TextNode

class MarkdownTokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.ast = Node(node_type="root", childs=[])
        self.tokenize(self.text, self.ast)
        #self.prettify_ast(self.ast.get_childs())
        # print("ds", self.ast.get_last_child().get_childs()[1].get_content())
        # print(self.ast.get_childs())
    
    def tokenize(self, markdown_text, parent_node):
        header_re = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)
        list_re = re.compile(r'^(\*|\-|\+|\d+\.)\s+(.*)', re.MULTILINE)
        block_quote_re = re.compile(r'^> ?(.*)', re.MULTILINE)

        bold_re = re.compile(r'\*\*(.*?)\*\*', re.MULTILINE)
        italic_re = re.compile(r'\*(.*?)\*', re.MULTILINE)
        link_re = re.compile(r'\[(.*?)\]\((.*?)\)', re.MULTILINE)
        patterns = [
            list_re,
            bold_re,
            italic_re,
            link_re,
            block_quote_re,
            header_re

        ]
        
        pos = 0
        text_len = len(markdown_text)
        found_text = None
        # at this point only god understands this code
        while pos < text_len:
            chunk = markdown_text[pos:]
            found_match = False
            if text[pos] == "\n":
                curr_line += 1
            for pattern in patterns:
                match = pattern.match(string=chunk)
                if match:
                    found_match = True
                    print("Found match!")
                    # get prev text
                    if (prev_pos + prev_span_end + 1 != pos):
                        print("TEXT BEFORE MATCH:", markdown_text[prev_pos+prev_span_end:pos])

                    print("MATCH:", match)
                    print("Current line:", curr_line)
                    prev_pos = pos
                    prev_span_end = match.end()
                    pos += match.end()
                    break
            if not found_match:
                found_text += markdown_text[pos]
                pos += 1
            

    def prettify_ast(self, childs, is_from=0):
        for node in childs:
            if isinstance(node, TextNode):
                print("text node with content:", node.get_content(), is_from)
            else:
                print(node.get_childs())
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
