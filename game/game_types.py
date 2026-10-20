from enum import Enum



class Unknown(Enum):
    UNKNOWN = 'Unknown'


class ItemType(Enum):       # The full list of item types dumped from game source code
    SEED = 'Seed'
    PET = 'Pet'
    PLANT = 'Plant'
    TOOL = 'Tool'
    DECOR = 'Decor'
    EGG = 'Egg'
    PRODUCE = 'Produce'
    CRYSTAL= 'Crystal'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

## ItemIds

class Species(Enum):        # The full list of species dumped from game source code
    ALOE = 'Aloe'
    APPLE = 'Apple'
    BAMBOO = 'Bamboo'
    BANANA = 'Banana'
    BEET = 'Beet'
    BLUEBERRY = 'Blueberry'
    BURROS_TAIL = 'BurrosTail'
    CABBAGE = 'Cabbage'
    CACAO = 'Cacao'
    CACTUS = 'Cactus'
    CAMELLIA = 'Camellia'
    CARDOON = 'Cardoon'
    CARROT = 'Carrot'
    CATTAIL = 'Cattail'
    CHRYSANTHEMUM = 'Chrysanthemum'
    CLOVER = 'Clover'
    COCONUT = 'Coconut'
    CORN = 'Corn'
    DAFFODIL = 'Daffodil'
    DAISY = 'Daisy'
    DATE = 'Date'
    DAWN_CELESTIAL = 'DawnCelestial'
    DAWNBREAKER = 'Dawnbreaker'
    DEADLY_NIGHTSHADE = 'DeadlyNightshade'
    DELPHINIUM = 'Delphinium'
    DRAGON_FRUIT = 'DragonFruit'
    ECHEVERIA = 'Echeveria'
    EGGPLANT = 'Eggplant'
    EMBERBLOOM = 'Emberbloom'
    FAVA_BEAN = 'FavaBean'
    FOXFIRE = 'Foxfire'
    GENTIAN = 'Gentian'
    GHOST_PLANT = 'GhostPlant'
    GRAPE = 'Grape'
    HABANERO = 'Habanero'
    LAVENDER = 'Lavender'
    LEEK = 'Leek'
    LEMON = 'Lemon'
    LILY = 'Lily'
    LYCHEE = 'Lychee'
    MARIGOLD = 'Marigold'
    MILKCAP = 'Milkcap'
    MOON_CELESTIAL = 'MoonCelestial'
    MUSHROOM = 'Mushroom'
    PASSION_FRUIT = 'PassionFruit'
    PEACH = 'Peach'
    PEAR = 'Pear'
    PEPPER = 'Pepper'
    PERSIMMON = 'Persimmon'
    PINECONE = 'Pinecone'
    POINSETTIA = 'Poinsettia'
    PRICKLY_PEAR = 'PricklyPear'
    PUMPKIN = 'Pumpkin'
    ROSE = 'Rose'
    SAFFRON = 'Saffron'
    SNOWDROP = 'Snowdrop'
    SQUASH = 'Squash'
    STARWEAVER = 'Starweaver'
    STRAWBERRY = 'Strawberry'
    SUNFLOWER = 'Sunflower'
    THUNDER_CELESTIAL = 'ThunderCelestial'
    TOMATO = 'Tomato'
    TULIP = 'Tulip'
    UBE = 'Ube'
    VIOLET_CORT = 'VioletCort'
    WATERMELON = 'Watermelon'
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


class EggId(Enum):                  # The full list of egg names dumped from game source code
    COMMON = 'CommonEgg'
    UNCOMMON = 'UncommonEgg'
    RARE = 'RareEgg'
    LEGENDARY = 'LegendaryEgg'
    MYTHTICAL = 'MythicalEgg'
    DAWN = 'DawnEgg'
    SNOW = 'SnowEgg'
    SPOOKY = 'SpookyEgg'
    THUNDER = 'ThunderEgg'
    WINTER = 'WinterEgg'            # May be deprecated
    HORSE = 'HorseEgg'              # May be deprecated
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

## 

class PetSpecies(Enum):            # The full list of pet species dumped from game source code
    BEE = 'Bee'
    BUNNY = 'Bunny'
    CAPYBARA = 'Capybara'
    CHICKEN = 'Chicken'
    COW = 'Cow'
    GOAT = 'Goat'
    OSTRICH = 'Ostrich'
    PIG = 'Pig'
    SHEEP = 'Sheep'
    SNAIL = 'Snail'
    SQUIRREL = 'Squirrel'
    TURTLE = 'Turtle'
    WORM = 'Worm'
    BUTTERFLY = 'Butterfly'
    DRAGONFLY = 'Dragonfly'
    FIRE_HORSE = 'FireHorse'
    HORSE = 'Horse'
    PONY = 'Pony'
    TURKEY = 'Turkey'
    PEACOCK = 'Peacock'
    PHOENIX = 'Phoenix'
    RED_FOX = 'RedFox'
    ROOSTER = 'Rooster'
    SNOW_FOX = 'SnowFox'
    STOAT = 'Stoat'
    WHITE_CARIBOU = 'WhiteCaribou'
    BAT = 'Bat'
    PLATYPUS = 'Platypus'
    THUNDER_WOLF = 'ThunderWolf'
    MOTH = 'Moth'
    SNAKE = 'Snake'
    TOAD = 'Toad'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Shops(Enum):          # The full list of shop names dumped from game source code
    SEED = 'seed'
    EGG = 'egg'
    TOOL = 'tool'
    DECOR = 'decor'
    RAIN = 'rain'
    DAWN = 'dawn'
    AMBER = 'amber'
    SNOW = 'snow'
    THUNDER = 'thunder'
    SPOOKY = 'spooky'
    APOLOGY = 'apology'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class CommandType(Enum):
    HARVEST_CROP = 'HarvestCrop'
    PURCHASE_SHOP_ITEM = 'PurchaseShopItem'
    APPLY_PET_TEAM = 'ApplyPetTeam'


class Weather(Enum):        # The full list of weather names dumped from game source code
    CLEAR = None
    RAIN = 'Rain'
    FROST = 'Frost'
    THUNDERSTORM = 'Thunderstorm'
    DAWN = 'Dawn'
    AMBER_MOON = 'AmberMoon'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
