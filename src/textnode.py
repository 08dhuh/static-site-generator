from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    

class TextNode:
    def __init__(self, text:str, type:TextType, url:str|None=None):
        self.text:str = text
        self.text_type:TextType = type
        self.url = url
        
    def __eq__(self, tn):
        return self.text == tn.text and self.text_type == tn.text_type\
            and self.url == tn.url
            
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"