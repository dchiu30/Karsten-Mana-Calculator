# Karsten-Mana-Calculator
This is a calculator to give you mana sources and the probabilities you cast your spells on-curve.
This calculator is based on the article [How Many Colored Mana Sources Do You Need to Consistently Cast Your Spells? A Guilds of Ravnica Update](https://www.channelfireball.com/all-strategy/articles/how-many-colored-mana-sources-do-you-need-to-consistently-cast-your-spells-a-guilds-of-ravnica-update/)
And uses the article as a basis for most of the calculations made. As a result, a lot of the limitations of this calculator will be due to ommisions from that article.

**Disclaimer**
The numbers from this calculator are approximations and not exact and will work best with decks that have 20-28 lands and 0-8 non-land sources

## Instructions
1. Fill out `deckInfo.json` with all your relevant information using the text editor of your choice
2. Run `manaCalculator.py`
3. Read the results from `manaInfo.csv`

### FAQ

**How do I count urborg?**

Basic Swamp

**What are `Fragile Sources`**

Fragile sources are turn 1 mana dorks like `Birds of Paradise` or `Noble Hierarch`

**What are `Typed Sources`**

Lands with the correct type (`Plains`, `Island`, `Swamp`, `Mountain`, `Forest`), but not necessarily basics

**What is Mishra's Bauble?**

Just treat it as scry 1 + cantrip, it shouldn't count towards turn 1 sources, but it will for now

**How are Bouncelands Counted?**

Bouncelands would be considered a tapland

**What isn't Supported?**
* Once Upon a Time
* Ponder
* Brainstorm
* Sol Lands
* Cloudpost
* Tron Lands
* Probably a bunch of other stuff
