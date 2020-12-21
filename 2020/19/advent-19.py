from collections import defaultdict
import itertools
from typing import List

from tqdm import tqdm


class Rule:
    def __init__(self, lefthand: str, righthands: list):
        self.lhs = lefthand
        self.rhs = righthands

    @classmethod
    def from_string(cls, string: str):
        lhs, rh = string.split(": ")
        if rh.startswith('"'):
            rhs = [rh.strip('"')]
        else:
            if "|" in rh:
                rh = rh.split(" | ")
            else:
                rh = [rh]
            rhs = [tuple(r.split(" ")) for r in rh]
        return cls(lhs, rhs)


class Grammar:
    def __init__(self):
        self.updict = defaultdict(list)

    @classmethod
    def from_list(cls, input_list: List[str]):
        obj = Grammar()
        ruleslist = []
        for line in input_list:
            ruleslist.append(Rule.from_string(line))
        for rule in ruleslist:
            for item in rule.rhs:
                obj.updict[item].append(rule.lhs)
        obj.fix_ternary()
        return obj

    def fix_ternary(self):
        offenders = [
            key for key in self.updict if isinstance(key, tuple) and len(key) > 2
        ]
        for off in offenders:
            lefthands = self.updict.pop(off)
            bigram = off[1:]
            self.updict[bigram].append("PL")
            self.updict[(off[0], "PL")].extend(lefthands)

    def recognize(self, string: str, sigma: str = "0"):
        # print(string)
        term_list = [char for char in string]
        parse_tree = [[]]
        for i, c in enumerate(term_list):
            parse_tree[0].append(set())
            if c in self.updict:
                parse_tree[0][i].update(self.updict[c])
            again = True
            while again:
                again = False
                for item in list(parse_tree[0][i]):
                    if (rule := (item,)) in self.updict:
                        for lefthand in self.updict[rule]:
                            if lefthand not in parse_tree[0][i]:
                                again = True
                                parse_tree[0][i].add(lefthand)
        nl = len(term_list)
        for i in range(1, nl):
            parse_tree.append([])
            for j in range(0, nl - i):
                parse_tree[i].append(set())
                for p in range(i):
                    vertical = parse_tree[i - (p + 1)][j]
                    diagonal = parse_tree[p][i + j - p]
                    if vertical and diagonal:
                        all_combos = itertools.product(vertical, diagonal)
                        for combo in all_combos:
                            if combo in self.updict:
                                for thing in self.updict[combo]:
                                    parse_tree[i][j].add(thing)
                again = True
                while again:
                    again = False
                    for item in list(parse_tree[i][j]):
                        if (rule := (item,)) in self.updict:
                            for lefthand in self.updict[rule]:
                                if lefthand not in parse_tree[i][j]:
                                    again = True
                                    parse_tree[i][j].add(lefthand)
                # print(f"({i},{j}): {parse_tree[i][j]}")

        # print(parse_tree)
        return sigma in parse_tree[nl - 1][0]

    def validate(self, messages: List[str]):
        return len([m for m in tqdm(messages) if self.recognize(m)])


with open("input.txt") as f:
    content = [x.strip() for x in f.readlines()]

rule_list = []
sent_list = []
rules_done = False
for line in content:
    if line == "":
        rules_done = True
    elif rules_done:
        sent_list.append(line)
    else:
        rule_list.append(line)

# part one

grammar = Grammar.from_list(rule_list)
print(grammar.validate(sent_list))

# part two
rule_list.remove("8: 42")
rule_list.remove("11: 42 31")
rule_list.extend(["8: 42 | 42 8", "11: 42 31 | 42 11 31"])
new_grammar = Grammar.from_list(rule_list)
print(new_grammar.validate(sent_list))
