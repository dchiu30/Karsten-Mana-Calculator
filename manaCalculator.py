import csv
import json

# Derek Chiu
# January 21, 2020
# For more info on how the calculation methodology, please refer to the article below:
# https://www.channelfireball.com/all-strategy/articles/how-many-colored-mana-sources-do-you-need-to-consistently-cast-your-spells-a-guilds-of-ravnica-update/
# All of the probabilities used in this program come from Frank Karsten in the previously linked article

manaDict = {  # Dictionary mapping Mana cost to probablity for a given amount of lands
    "C": [],
    "1C": [],
    "CC": [],
    "2C": [],
    "1CC": [],
    "CCC": [],
    "3C": [],
    "2CC": [],
    "1CCC": [],
    "4C": [],
    "3CC": [],
    "2CCC": [],
    "5C": [],
    "4CC": [],
    "3CCC": []
}

colors = ["W", "U", "B", "R", "G", "C"]  # Colors

costs = {  # Dictionary of all the costs calculated for
    1: ["C"],
    2: ["1C", "CC"],
    3: ["2C", "1CC", "CCC"],
    4: ["3C", "2CC", "1CCC"],
    5: ["4C", "3CC", "2CCC"],
    6: ["5C", "4CC", "3CCC"]
}

with open('karstenManaProbabilities.csv') as csvfile:
    probReader = csv.reader(csvfile, delimiter=',')
    for row in probReader:
        if row[0] != "sources":
            manaDict["C"].append(row[1])
            manaDict["1C"].append(row[2])
            manaDict["CC"].append(row[3])
            manaDict["2C"].append(row[4])
            manaDict["1CC"].append(row[5])
            manaDict["CCC"].append(row[6])
            manaDict["3C"].append(row[7])
            manaDict["2CC"].append(row[8])
            manaDict["1CCC"].append(row[9])
            manaDict["4C"].append(row[10])
            manaDict["3CC"].append(row[11])
            manaDict["2CCC"].append(row[12])
            manaDict["5C"].append(row[13])
            manaDict["4CC"].append(row[14])
            manaDict["3CCC"].append(row[15])

deckInfo = json.load(open('deckInfo.json'))
universalInfo = deckInfo["Universal"]


class ProbabilityMap:

    @staticmethod
    def deckInfoToSources(universal, color, cmc):
        # We count fastlands as a full source, since a fastland will be a fully untapped source for cmc 1-3, then a tapland for cmc 4+, and our assumption for taplands is that as the game progresses, they approach a full mana source
        sources = color["Untapped Sources"] + color["Fastlands"]
        if (cmc > 2):
            sources += ProbabilityMap.cmcGreaterThanTwo(universal, color, cmc)
        if (cmc > 3):
            sources += ProbabilityMap.cmcGreaterThanThree(universal, color, cmc)
        if (cmc > 4):
            sources += ProbabilityMap.cmcGreaterThanFour(universal, color, cmc)
        if(cmc > 1):
            sources += ProbabilityMap.cmcGreaterThanOne(universal, color, cmc)
            sources += ProbabilityMap.scries(universal, sources) + ProbabilityMap.cantrips(universal, sources)
        return sources

    @staticmethod
    def sourcesToProbability(sources,cost):
        sources -= 5
        if(sources < 0):
            return "n/a"
        elif (sources > 24):
            return "100"
        else:
            return manaDict[cost][int(sources)]

    @staticmethod
    def cmcGreaterThanOne(universal, color, cmc):
        # As a simplification, taplands are considered a full source for spells of cmc > 1. It should be noted that as we progress more and more through the game, a tapland will approach a full mana source. A checkland for simplicities sake is also counted with taplands. The number of taplands in a given color are calculated separately
        sources = color["Taplands"] + color["Checklands"]
        # As a simplification, fabled passage and evolving wilds are treated the same, unsure how to approach differences for now.
        if ((universal["Evolving Wilds"] or universal["Fabled Passage"]) and color["Basics"]):
            if(universal["Colors"] > 2):  # Calculating colors for a fabled passage/evolving wilds is somewhat uncertain, it's known that for a deck with 1GG, 1BB, 2RR an evolving wild can be counted as 2/3rds a source, so we've kinda just run with that evaluation to be 2/N where N = number of colours where N >= 3
                sources += (universal["Evolving Wilds"] + universal["Fabled Passage"]) * 2 / universal["Colors"]
            else:
                sources += universal["Evolving Wilds"] + universal["Fabled Passage"]
        if(color["Fragile Sources"]):
            sources += color["Fragile Sources"] * 0.5
        return sources

    @staticmethod
    def cmcGreaterThanTwo(universal, color, cmc):
        return color["2CMC Sources"]

    @staticmethod
    def cmcGreaterThanThree(universal, color, cmc):
        return color["3CMC Sources"]

    @staticmethod
    def cmcGreaterThanFour(universal, color, cmc):
        if (color["Basics"]):
            return universal["Field of Ruin"]*1/2
        return 0

    @staticmethod
    def taplandCount(universal, color):
        tapland = color["Taplands"] + universal["Evolving Wilds"] + color["Checklands"]/pow(2, color["Typed Sources"]/4)
        return tapland

    @staticmethod
    def scries(universal, sources):
        return universal["Scry1"]*sources/80 + universal["Scry2"]*sources/48

    @staticmethod
    def cantrips(universal, sources):
        return universal["Cantrips"]*sources/60

class FormattedOutput:

    @staticmethod
    def turnXSources(x):
        output = [[str(x)+"CMC Sources"], colors]
        stats = []
        for color in colors:
            stats.append(ProbabilityMap.deckInfoToSources(
                universalInfo, deckInfo[color], x))
        output.append(stats)
        return output

    @staticmethod
    def colorProbabilities(color):
        output = [[color], [], []]
        for i in range(1, 7):
            for cost in costs[i]:
                output[1].append(cost)
                output[2].append(ProbabilityMap.sourcesToProbability(
                    ProbabilityMap.deckInfoToSources(universalInfo, deckInfo[color], i),cost))
        return output

    @staticmethod
    def taplandCount():
        output = [colors, []]
        for color in colors:
            output[1].append(ProbabilityMap.taplandCount(
                universalInfo, deckInfo[color]))
        return output


masterManaInfo = []
for i in range(1, 7):
    masterManaInfo.append(FormattedOutput.turnXSources(i))
for color in colors:
    masterManaInfo.append(FormattedOutput.colorProbabilities(color))
masterManaInfo.append(FormattedOutput.taplandCount())

with open('manaInfo.csv', 'w') as csvfile:
    manaInfoWriter = csv.writer(
        csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for section in masterManaInfo:
        for row in section:
            manaInfoWriter.writerow(row)
