from claravy.taxonomy import *


class Parse_Virusbuster: # Acquired by Agnitum, which was acuired by Yandex

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK!TOK": self.parse_fmt3,
            "TOK.TOK.TOK!TOK": self.parse_fmt4,
            "TOK/TOK": self.parse_fmt5,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt6,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        if tokens[3].isnumeric() and tokens[2].startswith("b"):
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen" or tokens[2].isnumeric() or len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[1].isupper():
                fmt = [PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK!TOK
    def parse_fmt3(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK.TOK!TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[2] == "Gen":
            fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, PRE, FAM, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt5(self, tokens):
        return [PRE, PACK]

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt6(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

