import re
from tokens import *

class MarkdownTokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        lines = self.text.split('\n')
        for line in lines:
            self.tokenize_line(line)
            self.tokens.append(NewLineToken())  # Add a NewLineToken for each new line

    def tokenize_line(self, line):
        # Header
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if header_match:
            level = len(header_match.group(1))
            value = header_match.group(2)
            self.tokens.append(HeaderToken(level, value))
            return

        # List Item (ordered or unordered)
        list_match = re.match(r'^(\*|\-|\+|\d+\.)\s+(.*)', line)
        if list_match:
            ordered = bool(re.match(r'^\d+\.', list_match.group(1)))
            value = list_match.group(2)
            self.tokens.append(ListToken(value, ordered))
            self.tokenize_inline(value)  # Tokenize inline elements within the list item
            return
        
        block_quote_match = re.search(r'^> ?(.*)', line)
        if block_quote_match:
            value = block_quote_match.group(1)
            self.tokens.append(BlockquoteToken(value))
            self.tokenize_inline(value)
            return


        # Process other inline elements
        self.tokenize_inline(line)

    def tokenize_inline(self, text):
        pos = 0
        length = len(text)
        while pos < length:
            bold_match = re.search(r'\*\*(.*?)\*\*', text[pos:])
            italic_match = re.search(r'\*(.*?)\*', text[pos:])
            link_match = re.search(r'\[(.*?)\]\((.*?)\)', text[pos:])

            if bold_match:
                # handle text if theres something before bold match **hing****new** ll **www** kgj
                if bold_match.start() > 0:
                    self.tokens.append(TextToken(text[pos:pos + bold_match.start()]))
                self.tokens.append(BoldToken(bold_match.group(1)))
                pos += bold_match.end()
            elif link_match:
                # handle text if theres something before link match
                if link_match.start() > 0:
                    self.tokens.append(TextToken(text[pos:pos + link_match.start()]))
                self.tokens.append(LinkToken(link_match.group(1), link_match.group(2)))
                pos += link_match.end()
            else:
                self.tokens.append(TextToken(text[pos:]))
                break

    def get_tokens(self):
        return self.tokens

# Example usage
markdown_text = """
# Header 1
## Header 2
Some **bold** text and a [link](http://example.com).

Directly 2 tokens **like** [this](http://example.com)    
- Unordered list item
1. Ordered list item
2. Ordered **with** bold text! How **cool**!
> Thats **cool** shit!
"""

tokenizer = MarkdownTokenizer(markdown_text)
tokens = tokenizer.get_tokens()
for token in tokens:
    print(token)
