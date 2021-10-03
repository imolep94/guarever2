import math, re


class build:
    def __init__(self):
        self.COST_COEF = {
            '🏤': (500, 200, 200),
            '🏚': (200, 100, 100),
            '🏘': (200, 100, 100),
            '🌲': (100, 50, 50),
            '⛏': (100, 50, 50),
            '🌻': (100, 50, 50),
            '🛡': (200, 100, 100),
            '🏰': (5000, 500, 1500),
            'Trebuchet': (8000, 1000, 300)
        }

        self.buildings = {
            '🏤': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🏚': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🏘': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🌻': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🌲': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '⛏': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🛡': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            },
            '🏰': {
                'lvl': 0,
                'ppl': 0,
                'max_ppl': 0
            }
        }

    # Update build information
    def Update(self, new_buildings):
        if isinstance(new_buildings, dict):
            buildings = new_buildings
        else:
            try:
                buildings = re.findall(
                    "([^\s]{1,5})\s{3,5}(\d{1,4})(?:\D{1,9}(\d{1,9})\/(\d{1,9}))?",
                    new_buildings)
                buildings = dict(
                    (build[0], {
                        "lvl": int(0 if not build[1] else build[1]),
                        "ppl": int(0 if not build[2] else build[2]),
                        "max_ppl": int(0 if not build[3] else build[3])
                    }) for build in buildings)
            except:
                buildings = self.buildings
        if isinstance(buildings, dict):
            if len(buildings) == 8:
                self.buildings = buildings
                return self.buildings
        else:
            return self.buildings

    # Required warehouse level for upgrade to lvlsUp levels
    def getStorReq(self, building, lvlsUp=1):
        preTargetLvl = self.buildings[building]['lvl'] + lvlsUp - 1
        return math.ceil(
            math.sqrt(
                max(self.COST_COEF[building][1:3]) *
                (preTargetLvl**2 + 3 * preTargetLvl + 2) / 100 + 100) - 10)

    # Checking the level of the warehouse for the possibility of an upgrade
    def isStorEnough(self, building):
        return True if (self.buildings['🏚']['lvl'] >=
                        self.getStorReq(building)) else False

    # The cost of upgrading to lvlsUp levels
    def getUpgrCost(self, building, lvlsUp=1):
        # Current building level
        srcLvl = self.buildings[building]['lvl']
        # Level BEFORE which we consider the cost of the upgrade
        dstLvl = srcLvl + lvlsUp
        # We determine two members of the polynomial, depending on the current(Poly2) and target levels(Poly1)
        #Sn, Sm - partial sums of a series from 0 to n and from 0 to m. Then Snm = Sm - Sn is the sum of the series from n to m
        Sm = round(dstLvl * (dstLvl - 1) * ((2 * dstLvl + 8) / 6 + 2 / dstLvl))
        # If the current level is 0, then -Sn / 2 should go to 1, then Sn = -2
        if srcLvl == 0: Sn = -2
        else:
            Sn = round(srcLvl * (srcLvl - 1) *
                       ((2 * srcLvl + 8) / 6 + 2 / srcLvl))
        gold = round(self.COST_COEF[building][0] * (Sm - Sn) / 2)
        wood = round(self.COST_COEF[building][1] * (Sm - Sn) / 2)
        stone = round(self.COST_COEF[building][2] * (Sm - Sn) / 2)
        return {
            'gold': gold,
            'wood': wood,
            'stone': stone,
            'total': gold + wood * 2 + stone * 2
        }

    # Calc the payback of a building upgrade
    def getROI(self, building):
        # add ROI calculation for simultaneous app of several buildings
        incomUp = self.getIncUp(building)
        storLvlsUp = self.getStorReq(building) - self.buildings['🏚']['lvl']
        # To build, you need to upgrade the warehouse to storLvlsUp levels
        if storLvlsUp > 0:
            totalUpgrCost = self.getUpgrCost(
                building)['total'] + self.getUpgrCost('🏚', storLvlsUp)['total']
        # Up warehouse not required
        else:
            totalUpgrCost = self.getUpgrCost(building)['total']
        if incomUp > 0:
            return totalUpgrCost / incomUp
            # If income is less than or equal to 0, then the payback is infinity
        else:
            return math.inf

    # revenue increase upon upgrade
    def getIncUp(self, building):
        if building == '🏤': return self.buildings['🏘']['lvl'] * 2
        elif building == '🏘':
            if min(self.buildings['🌻']['lvl'],
                   self.buildings['🏚']['lvl']) > self.buildings['🏘']['lvl']:
                consumptFarm = 5
            else:
                consumptFarm = 20
            return 10 + self.buildings['🏤']['lvl'] * 2 - consumptFarm
        elif building == '🌻':
            if self.buildings['🌻']['lvl'] >= self.buildings['🏚']['lvl']:
                return 0
            else:
                if self.buildings['🌻']['lvl'] >= self.buildings['🏘']['lvl']:
                    return 5
                else:
                    return 20
        elif building == '🌲' or building == '⛏':
            if self.buildings[building]['lvl'] < self.buildings['🏚']['lvl']:
                return 20
            else:
                return 0
        elif building == '🏚':
            incomUp = 0
            if self.buildings['🏚']['lvl'] < self.buildings['🌻']['lvl']:
                if self.buildings['🏚']['lvl'] < self.buildings['🏘']['lvl']:
                    incomUp += 20
                else:
                    incomUp += 5
            if self.buildings['🏚']['lvl'] < self.buildings['🌲']['lvl']:
                incomUp += 20
            if self.buildings['🏚']['lvl'] < self.buildings['⛏']['lvl']:
                incomUp += 20
            return incomUp
        else:
            return 0

    #Select Next Building to Upgrade
    def getNextUpgrBld(self):
        # The first three buildings of the 🏘, 🏚, 🌻
        #if self.buildings['🏘']['lvl'] == 0: return '🏘' #original
        if self.buildings['🏘']['lvl'] == 0: return '💭'
        if self.buildings['🏚']['lvl'] == 0: return '🏚'
        if self.buildings['🌻']['lvl'] == 0: return '🌻'

        # Then we consider the payback

        # 🏘 + 🌻
        storLvlUp = max(self.getStorReq('🏘'),
                        self.getStorReq('🌻')) - self.buildings['🏚']['lvl']
        incomUp = 10 + self.buildings['🏤']['lvl'] * 2
        # If there is not enough warehouse, we subtract food expenses from income
        if self.buildings['🏚']['lvl'] <= self.buildings['🌻']['lvl']:
            incomUp -= 20
        upgrCost = self.getUpgrCost('🏘')['total'] + self.getUpgrCost(
            '🌻')['total']
        # If you need up warehouses, then we consider
        if storLvlUp > 0: upgrCost += self.getUpgrCost('🏚', storLvlUp)['total']
        if incomUp <= 0: hausfarm = math.inf
        else: hausfarm = upgrCost / incomUp

        # 🏘 + 🏤
        storLvlUp = max(self.getStorReq('🏘'),
                        self.getStorReq('🏤')) - self.buildings['🏚']['lvl']
        incomUp = self.getIncUp('🏘') + (self.buildings['🏘']['lvl'] + 1) * 2
        upgrCost = self.getUpgrCost('🏘')['total'] + self.getUpgrCost(
            '🏤')['total']
        # If you need up warehouses, then we consider
        if storLvlUp > 0: upgrCost += self.getUpgrCost('🏚', storLvlUp)['total']
        if incomUp <= 0: haushall = math.inf
        else: haushall = upgrCost / incomUp

        # 🏘 + 🌲 + ⛏
        skld1 = (self.getUpgrCost('🏚')['total'] + self.getUpgrCost('🌲')
                 ['total'] + self.getUpgrCost('⛏')['total']) / 40
        # 🏚 + 🌲 + ⛏ + 🌻
        if self.buildings['🌻']['lvl'] + 1 >= self.buildings['🏘']['lvl']:
            skld2 = (self.getUpgrCost('🏚')['total'] + self.getUpgrCost(
                '🌲')['total'] + self.getUpgrCost('⛏')['total'] +
                     self.getUpgrCost('🌻')['total']) / 45
        else:
            skld2 = (self.getUpgrCost('🏚')['total'] + self.getUpgrCost(
                '🌲')['total'] + self.getUpgrCost('⛏')['total'] +
                     self.getUpgrCost('🌻')['total']) / 60
        # 🏚 + 🏘 + 🌻
        skld3 = (self.getUpgrCost('🏚')['total'] + self.getUpgrCost('🏘')
                 ['total'] + self.getUpgrCost('🌻')['total']) / (
                     10 + self.buildings['🏤']['lvl'] * 2)

        storROI = min(
            skld1, skld2, skld3,
            self.getROI('🏚'))  # minimum of all options with a warehouse
        hallROI = self.getROI('🏤')
        hausROI = self.getROI('🏘')
        farmROI = self.getROI('🌻')
        sawmROI = self.getROI('🌲')
        mineROI = self.getROI('⛏')
        
        minROI = min(storROI, hallROI, hausROI, farmROI, sawmROI, mineROI,
                     haushall, hausfarm)
        
        # Keep 🌻 at same level of production than 🏘:
        if self.buildings['🏘']['lvl'] > self.buildings['🌻']['lvl'] or self.buildings['🏘']['lvl'] > self.buildings['🏚']['lvl']:
            if self.buildings['🌻']['lvl']+1 > self.buildings['🏚']['lvl']: return '🏚'
            elif self.isStorEnough('🌻'): return '🌻'
            else: return '🏚'
        elif minROI == hausROI and self.buildings['🏘']['lvl']+1 > self.buildings['🌻']['lvl']:
            if self.buildings['🌻']['lvl']+1 > self.buildings['🏚']['lvl']: minROI = storROI
            else: minROI = farmROI
        
        # For 🏘 + 🏤, choose what is more profitable
        if minROI == haushall:
            if hausROI == min(hausROI, hallROI): hausROI = minROI
            else: hallROI = minROI
        # Or for 🏘 + 🌻, choose what is more profitable
        elif minROI == hausfarm:
            if hausROI == min(hausROI, farmROI): hausROI = minROI
            else: farmROI = minROI

        if minROI == storROI:
            return '🛡' if self.isStorEnough('🛡') else '🏚'
        elif minROI == hallROI:
            if self.isStorEnough('🏤'): return '🏤'
            else: return '🛡' if self.isStorEnough('🛡') else '🏚'
        elif minROI == hausROI:
            if self.isStorEnough('🏘'): return '🏘'
            else: return '🛡' if self.isStorEnough('🛡') else '🏚'
        elif minROI == farmROI:
            if self.isStorEnough('🌻'): return '🌻'
            else: return '🛡' if self.isStorEnough('🛡') else '🏚'
        elif minROI == sawmROI:
            if self.isStorEnough('🌲'):
                return '🛡' if self.isStorEnough('🛡') else '🌲'
            else:
                return '🛡' if self.isStorEnough('🛡') else '🏚'
        elif minROI == mineROI:
            if self.isStorEnough('⛏'):
                return '🛡' if self.isStorEnough('🛡') else '⛏'
            else:
                return '🛡' if self.isStorEnough('🛡') else '🏚'

        # Something went wrong and we ended up here
        return None
