class DecisionTreeNode():

    def makeDecision(self):
        pass

class Action():

    def makeDecision(self):
        return self

class Decision(DecisionTreeNode):

    def __init__(self, trueNode, falseNode, value):
        self.trueNode = trueNode
        self.falseNode = falseNode
        self.value = value

    def getBranch(self):
        return self.trueNode

    def makeDecision(self):
        return self.getBranch().makeDecision()