from enum import Enum



class Unknown(Enum):
    UNKNOWN = 'Unknown'


class ItemType(Enum):
    SEED = 'Seed'
    PET = 'Pet'
    PLANT = 'Plant'
    TOOL = 'Tool'
    DECOR = 'Decor'
    EGG = 'Egg'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Species(Enum):
    CARROT = 'Carrot'
    BEET = 'Beet'
    ECHEVERIA = 'Echeveria'
    CACTUS = 'Cactus'
    BAMBOO = 'Bamboo'
    SUNFLOWER = 'Sunflower'
    STARWEAVER = 'Starweaver'
    CATTAIL = 'Cattail'
    SNOWDROP = 'Snowdrop'
    CLOVER = 'Clover'
    MILKCAP = 'Milkcap'
    THUNDER_CELESTIAL = 'ThunderCelestial'
    DAWNBREAKER = 'Dawnbreaker'
    EMBERBLOOM = 'Emberbloom'
    MARIGOLD = 'Marigold'
    UBE = 'Ube'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ToolId(Enum):
    WATERING_CAN = 'WateringCan'
    PLANTER_POT = 'PlanterPot'
    CROP_CLEANER = 'CropCleanser'
    SHOVEL = 'Shovel'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class DecorId(Enum):
    FEEDING_TROUGH = 'FeedingTrough'
    DECOR_SHED = 'DecorShed'
    PET_HUTCH = 'PetHutch'
    SEED_SILO = 'SeedSilo'
    TOOL_SHACK = 'ToolShack'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class EggId(Enum):
    COMMON = 'CommonEgg'
    UNCOMMON = 'UncommonEgg'
    RARE = 'RareEgg'
    LEGENDARY = 'LegendaryEgg'
    MYTHTICAL = 'MythicalEgg'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class PetSpecies(Enum):
    WORM = 'Worm'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Shops(Enum):
    SEED = 'seed'
    EGG = 'egg'
    TOOL = 'tool'
    DECOR = 'decor'
    RAIN = 'rain'
    DAWN = 'dawn'
    AMBER = 'amber'
    SNOW = 'snow'
    THUNDER = 'thunder'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class CommandType(Enum):
    HARVEST_CROP = 'HarvestCrop'
    PURCHASE_SHOP_ITEM = 'PurchaseShopItem'
    APPLY_PET_TEAM = 'ApplyPetTeam'


class Weather(Enum):
    CLEAR = None
    FROST = 'Frost'
    RAIN = 'Rain'
    THUNDERSTORM = 'Thunderstorm'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
