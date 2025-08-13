from enum import Enum

class MediaType(Enum):
    Plain = 'Plain'
    Stationery = 'stationery'
    Any = 'any'

class MediaSize(Enum):
    Any = "any"
    Custom = "custom"
    AnyCustom = "anycustom"
    Letter = "na_letter_8.5x11in"
    iso_a3_297x420mm = "iso_a3_297x420mm"
    iso_a4_210x297mm = "iso_a4_210x297mm"
    iso_a0_841x1189mm = "iso_a0_841x1189mm"
    ThreeXFive = "3x5in"
    A4 = "A4"
    EightPointFiveByThirteen = "na_foolscap_8.5x13in"
    Size16K195x270 = "om_16k_195x270mm"
    Legal = "na_legal_8.5x14in"


class MediaInputIds(Enum):
    MultipurposeTray = 0
    Tray1 = "tray-1"
    Tray2 = "tray-2"
    Tray3 = "tray-3"
    Tray4 = "tray-4"
    Tray5 = "tray-5"
    Tray6 = "tray-6"
    Tray7 = "tray-7"
    Tray8 = "tray-8"
    Tray9 = "tray-9"
    Tray10 = "tray-10"
    MainRoll = "main-roll"
    Main = "main"
    Roll1 = "roll-1"
    Roll2 = "roll-2"

class MediaOrientation(Enum):
    Default = 1
    Portrait = 2
    Landscape = 3