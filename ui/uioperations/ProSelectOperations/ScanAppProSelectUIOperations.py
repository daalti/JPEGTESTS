#########################################################################################
# @file      ScanAppProSelectUIOperations.py
# @author    Anu Sebastian (anu.sebastian@hp.com)
# @date      11-02-2021
# @brief     Implementation for all the Scan settings UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import  sys
import time
import logging
from enum import Enum
from dunetuf.ui.uioperations.BaseOperations.IScanAppUIOperations import IScanAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

_logger = logging.getLogger(__name__)

class ScanAppProSelectUIOperations(IScanAppUIOperations):
    SCAN_APP = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32"
    # Scan settings object name constants
    SCAN_SETTINGS_VIEW = "#MenuListscanSettingsPage"
    SCAN_FILE_TYPE = "#scan_fileFormatButton"
    SCAN_RESOLUTION = "#scan_resolutionButton"
    SCAN_QUALITY = "#scan_qualityAndFileSizeButton"
    SCAN_SIDES = "#scan_inputPlexModeButton"
    SCAN_COLOR_FORMAT = "#scan_colorMode_Button"
    SCAN_ORIGINAL_SIZE = "#scan_inputMediaSizeButton"
    SCAN_ORIENTATION = "#scan_inputContentOrientationButton"
    SCAN_LIGHTER_DARKER_SLIDER = "#scan_exposureMenuSlider"
    SCAN_TIFF_COMPRESSION_COLOR ="#scan_colorGrayScaleTiffCompressionButton"
    SCAN_TIFF_COMPRESSION_MONO ="#scan_monoTiffCompressionButton"

    SCAN_ADD_PAGE_BUTTON = "#Add Page"
    SCAN_ADD_PAGE_FINISH_BUTTON = "#Finish"
    SCAN_ADD_PAGE_START_SCAN_BUTTON = "#Start Scan"

    SCAN_SETTINGS_FILETYPE_VIEW = "#MenuSelectionListscan_fileFormat"
    filetype_dict = {
        "pdf": ["cDSFileTypePdf", "#option_pdf"],
        "tiff": ["cDSFileTypeTiff", "#option_mtiff"],
        #"mtiff": ["cDSFileTypeTiff", "#option_mtiff"],
        "jpeg": ["cDSFileTypeJpeg", "#option_jpeg"],
        "pdfa": ["cDSFileTypePdfAShort", "#option_pdfa"],
        "ppm": ["cPPM", "#ppm"],
        "pgm": ["cPGM", "#pgm"],
        "png": ["cPNG", "#png"],
        "raw": ["cRAW", "#raw"]
    }
    SCAN_DESCRIPTIVE_BUTTON = "#DescriptiveButtonListLayout"
    SCAN_PDF_ENCRYPTION_PROMPT_VIEW = "#pdfEncryptionPromptView"
    SCAN_PDF_ENCRYPTION_PROMPT = "#pdfEncryptionPrompt"
    SCAN_PDF_ENCRYPTION = "#scan_pdfEncryptionMenuSwitch"
    SCAN_PDF_ENCRYPTION_PASSWORD = "#EnterPasswordButton"
    SCAN_PDF_ENCRYPTION_REENTER_PASSWORD = '#ReEnterPasswordButton'
    SPICE_KEYBOARD_VIEW = "#spiceKeyboardView"
    SAVE_BUTTON = "#Save"
    CANCEL_BUTTON = "#Cancel"
    SCAN_HIGH_COMPRESSION = "#scan_highCompressionMenuSwitch"

    SCAN_SETTINGS_RESOLUTION_VIEW = "#MenuSelectionListscan_resolution"
    resolution_dict = {
        "e75dpi": ["cDSImageResolutionE75Dpi", "#option_e75Dpi"],
        "e100dpi": ["cDSImageResolutionE100Dpi", "#option_e100Dpi"],
        "e150dpi": ["cDSImageResolutionE150Dpi", "#option_e150Dpi"],
        "e200dpi": ["cDSImageResolutionE200Dpi", "#option_e200Dpi"],
        "e240dpi": ["cDSImageResolutionE240Dpi", "#option_e240Dpi"],
        "e300dpi": ["cDSImageResolutionE300Dpi", "#option_e300Dpi"],
        "e400dpi": ["cDSImageResolutionE400Dpi", "#option_e400Dpi"],
        "e500dpi": ["cDSImageResolutionE500Dpi", "#option_e500Dpi"],
        "e600dpi": ["cDSImageResolutionE600Dpi", "#option_e600Dpi"],
        "e1200dpi": ["cDSImageResolutionE1200Dpi", "#option_e1200Dpi"]
    }

    SCAN_SETTINGS_QUALITY_VIEW = "#MenuSelectionListscan_qualityAndFileSize"
    quality_dict = {
        "best": ["cBestLabel", "#option_high"],
        "draft": ["cDraft", "#option_low"],
        "standard": ["cStandard", "#option_medium"]
    }

    SCAN_SETTINGS_SIDES_VIEW = "#MenuSelectionListscan_inputPlexMode"
    sides_dict = {
        "simplex": ["cNumeral1", "#option_simplex"],
        "duplex": ["cNumeral2", "#option_duplex"]
    }

    SCAN_SETTINGS_COLOR_FORMAT_VIEW = "#MenuSelectionListscan_colorMode_"
    colorformat_dict = {
        "color": ["cColor", "#option_color"],
        "blackonly": ["cBlackOnly", "#option_monochrome"],
        "grayscale": ["cChromaticModeGrayscale", "#option_grayscale"],
        "autodetect": ["cAutomatic", "#option_autoDetect"]
    }

    SCAN_SETTINGS_ORIGINAL_SIZE_VIEW = "#MenuSelectionListscan_inputMediaSize"
    orgsize_dict = {
        "b2": ["cMediaSizeIdISOB2", "#option_iso_b2_500x707mm"],
        "b3": ["cMediaSizeIdISOB3", "#option_iso_b3_353x500mm"],
        "jis_b4": ["cMediaSizeIdJisB4", "#option_iso_b4_250x353mm"],
        "b5_envelope": ["cMediaSizeIdB5Envelope", "#option_iso_b5_176x250mm"],
        "jis_b6": ["cMediaSizeIdJisB6", "#option_iso_b6_125x176mm"],
        "a0": ["cMediaSizeIdA0", "#option_iso_a0_841x1189mm"],
        "a1": ["cMediaSizeIdA1",  "#option_iso_a1_594x841mm"],
        "a2": ["cMediaSizeIdA2",  "#option_iso_a2_420x594mm"],
        "a3": ["cMediaSizeIdA3", "#option_iso_a3_297x420mm"],
        "a4": ["cMediaSizeIdA4", "#option_iso_a4_210x297mm"],
        "a5": ["cMediaSizeIdA5", "#option_iso_a5_148x210mm"],
        "a6": ["cMediaSizeIdA6", "#option_iso_a6_105x148mm"],
        "letter": ["cMediaSizeIdLetter", "#option_na_letter_8.5x11in"],
        "legal": ["cMediaSizeIdLegal", "#option_na_legal_8.5x14in"],
        "ledger": ["cMediaSizeIdLedger", "#option_na_ledger_11x17in"],
        "custom": ["cMediaSizeIdCustom", "#option_custom"],
        "anycustom": ["cMediaSizeIdAny", "#option_anycustom"],
        "executive": ["cMediaSizeIdExecutive", "#option_na_executive_7_25x10_5in"],
        "oficio_8_5x13": ["cMediaSizeIdOficio", "#option_na_foolscap_8_5x13in"],
        "oficio_8_5x13_4in": ["cMediaSizeIdOficio216x340", "#option_na_oficio_8_5x13_4in"],
        "4x6in": ["cMediaSizeIdFourXSix", "#option_na_index_4x6_4x6in"],
        "5x7in": ["cMediaSizeIdFiveXSeven", "#option_na_index_5x7_5x7in"],
        "5x8in": ["cMediaSizeIdFiveXEight", "#option_na_index_5x8_5x8in"],
        "jis_b5": ["cMediaSizeIdJisB5", "#option_jis_b5_182x257mm"],
        "jis_b6": ["cMediaSizeIdJisB6", "#option_jis_b6_128x182mm"],
        "100x150mm": ["cMediaSizeId10x15cm", "#option_om_small_photo_100x150mm"],
        "16k_195x270mm": ["cMediaSizeIdSize16k195x270", "#option_prc_16k_195x270mm"],
        "16k_184x260mm": ["cMediaSizeIdSize16K184x260", "#option_prc_16k_184x260mm"],
        "16k": ["cMediaSizeIdSixteenK", "#option_roc_16k_7_75x10_75in"],
        "jpostcard": ["cMediaSizeIdHagaki", "#option_jpn_hagaki_100x148mm"],
        "jdoublepostcard": ["cMediaSizeIdOfukuHagaki", "#option_jpn_oufuku_148x200mm"],
        "envelope_10": ["cMediaSizeIdCOM10Envelope", "#option_na_number_10_4_125x9_5in"],
        "envelope_monarch": ["cMediaSizeIdMonarchEnvelope", "#option_na_monarch_3_87x7_5in"],
        "envelope_c5": ["cMediaSizeIdC5Envelope", "#option_iso_c5_162x229mm"],
        "envelope_dl": ["cMediaSizeIdDLEnvelope", "#option_iso_dl_110x220mm"],
        "iso_c6": ["cMediaSizeIdEnvelopeC6", "#option_iso_c6_114x162mm"],
        "chou_3_envelope": ["cMediaSizeIdJChou3Envelope", "#option_jpn_chou3_120x235mm"],
        "na_invoice_5.5x8.5in": ["cMediaSizeIdStatement", "#option_statement"],
        "index_3x5in": ["cMediaSizeIdThreeXFive", "#option_na_index_3x5_3x5in"],
        "any": ["cMediaTypeIdAnySupportedType", "#option_any"],
        "letter_8x10in": ["cMediaSizeLetter8x10", "#option_na_govt_letter_8x10in"]
    }

    SCAN_SETTINGS_ORIENTATION_VIEW = "#MenuSelectionListscan_inputContentOrientation"
    orientation_dict = {
        "landscape": ["cLandscape", "#option_landscape"],
        "portrait": ["cPortrait", "#option_portrait"]
    }

    SCAN_SETTINGS_TIFF_COMPRESSION_COLOR_VIEW = "#MenuSelectionListscan_colorGrayScaleTiffCompression"
    tiffcompression_color_dict = {
        "g3": ["cTiffCompressionG3", "#option_lzw"],
        "tiffpost6": ["cTiffCompressionTiffPost6", "#option_postTiff6"],
        "tiff6": ["cTiffCompressionTiff6", "#option_tiff6"]
    }
    
    SCAN_SETTINGS_TIFF_COMPRESSION_MONO_VIEW = "#MenuSelectionListscan_monoTiffCompression"
    tiffcompression_mono_dict = {
        "undefined": ["cUndefined", "#option_lzw"],
        "g3": ["cTiffCompressionG3", "#option_g3"],
        "g4": ["cTiffCompressionG4", "#option_g4"],
        "automatic": ["cAutomatic", "#option_automatic"]
    }

    SCAN_PROGRESS_VIEW = "#SystemProgressView"
    SCAN_PROGRESS_CANCEL = "#SystemProgressButton"

    SCAN_LIGHTER_DARKER_MIN = 1
    SCAN_LIGHTER_DARKER_MAX = 9

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.dial_keyboard_operations = ProSelectKeyboardOperations(self._spice)

    # Scan App
    def goto_scan_app(self):
        '''
        UI should be in Homescreen
        Navigates to Scan App screen starting from Home screen.
        UI Flow is Home->Scan
        '''
        #Uncomment once bug on homescreen activefocus DUNE-35036 is fixed
        self._spice.goto_homescreen()
        home_app = self._spice.query_item("#HomeScreenView")
        self._spice.wait_until(lambda: home_app["activeFocus"] == True)
        logging.info("At Home Screen")
        start_time = time.time()
        time_spent_waiting = time.time() - start_time

        # make sure that you are in left most App - Menu
        while (self._spice.query_item("#CurrentAppText")["text"] != "Menu" and time_spent_waiting < self.maxtimeout):
            home_app.mouse_wheel(0,0)
            time_spent_waiting = time.time() - start_time
        time.sleep(2)
        # scroll till you reach the Scan option (TODO - Need to avoid use of text)
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (self._spice.query_item("#CurrentAppText")["text"] != "Scan" and time_spent_waiting < self.maxtimeout):
            home_app.mouse_wheel(180,180)
            time_spent_waiting = time.time() - start_time
        time.sleep(2)

        current_button = self._spice.wait_for(self.SCAN_APP)
        current_button.mouse_click()
        logging.info("At Scan App")
        time.sleep(2)
        
    # Navigations from Scan settings/Options list screen
    def goto_filetype_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is File Type-> (File Type Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_FILE_TYPE, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_FILETYPE_VIEW)
        logging.info("UI: At File Type settings screen")

    def goto_pdf_encryption_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is PDF Encrytion-> (PDF Encrytion toggle).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_PDF_ENCRYPTION, "#MenuListLayout", dial_value=dial_val, select_option=False)
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW)
        logging.info("UI: At PDF Encryption toggle")

    def goto_high_compression_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is High Compression-> (High Compression toggle).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_HIGH_COMPRESSION, "#MenuListLayout", dial_value=dial_val, select_option=False)
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW)
        logging.info("UI: At High compression toggle")

    def goto_resolution_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Resolution-> (Resolution Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_RESOLUTION, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_RESOLUTION_VIEW)
        logging.info("UI: At Resolution settings screen")

    def goto_quality_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen
        UI Flow is Quality-> (Quality Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_QUALITY, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_QUALITY_VIEW)
        logging.info("UI: At Quality settings screen")

    def goto_sides_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Sides-> (Sides Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_SIDES, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_SIDES_VIEW)
        logging.info("UI: At Sides settings screen")

    def goto_color_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Color-> (Color Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_COLOR_FORMAT, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_COLOR_FORMAT_VIEW)
        logging.info("UI: At Color settings screen")

    def goto_original_size_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Original Size-> (Original Size Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_ORIGINAL_SIZE, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_ORIGINAL_SIZE_VIEW)
        logging.info("UI: At Original size settings screen")

    def goto_orientation_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Orientation-> (Orientation Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_ORIENTATION, "#MenuListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_ORIENTATION_VIEW)
        logging.info("UI: At Orientation settings screen")

    def goto_lighter_darker_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is Lighter/Darker-> (Lighter/Darker slider).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_LIGHTER_DARKER_SLIDER, "#MenuListLayout")
        assert self._spice.wait_for(self.SCAN_LIGHTER_DARKER_SLIDER)
        logging.info("UI: At Lighter/Darker settings slider")

    def goto_tiff_compression_color_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is tiff Compression-> (Tiff Compression Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_TIFF_COMPRESSION_COLOR, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_COLOR_VIEW)
        logging.info("UI: At tiff compression setting")
    
    def goto_tiff_compression_mono_settings(self, dial_val: int = 180):
        '''
        UI should be on Scan options list screen.
        UI Flow is tiff Compression-> (Tiff Compression Settings screen).
        Args:
            dial_value: Direction for dialing.
        '''
        self.dial_common_operations.goto_item(self.SCAN_TIFF_COMPRESSION_MONO, "#MenuListLayout", dial_value=dial_val)
        assert self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_MONO_VIEW)
        logging.info("UI: At tiff compression setting")

    # Scan settings functional operations
    def set_scan_settings_filetype(self, filetype: str):
        '''
        UI should be on File type settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        '''
        # Get the object name in ui for the filetype passed
        assert self._spice.wait_for(self.SCAN_SETTINGS_FILETYPE_VIEW, timeout = 9.0)
        filetype_id = self.filetype_dict[filetype.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_FILETYPE_VIEW)
        for i in range(8):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(filetype_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_pdf_encryption(self, encryption: bool = False):
        '''
        UI should be on Scan settings view.
        Args:
            encryption: PDF encryption toggle - True/False
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)
        encryption_toggled_state = self._spice.query_item(self.SCAN_PDF_ENCRYPTION + " #SpiceSwitch")["checked"]
        if encryption != encryption_toggled_state:
            self.dial_common_operations.goto_item(self.SCAN_PDF_ENCRYPTION, "#MenuListLayout")

        encryption_toggled_state = self._spice.query_item(self.SCAN_PDF_ENCRYPTION + " #SpiceSwitch")["checked"]
        assert encryption_toggled_state == encryption

    def set_scan_settings_resolution(self, resolution: str):
        '''
        UI should be on Resolution settings screen.
        Args:
            resolution: The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                        e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
        '''
        # Get the object name in ui for the resolution passed
        assert self._spice.wait_for(self.SCAN_SETTINGS_RESOLUTION_VIEW, timeout = 9.0)
        resolution_id = self.resolution_dict[resolution.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_RESOLUTION_VIEW)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(resolution_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_quality(self, quality: str):
        '''
        UI should be on Quality settings screen.
        Args:
            quality: The quality to set - best, draft, standard
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_QUALITY_VIEW, timeout = 9.0)
        # Get the object name in ui for the quality passed
        quality_id = self.quality_dict[quality.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_QUALITY_VIEW)
        for i in range(3):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(quality_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_high_compression(self, compression: bool = False):
        '''
        UI should be on Scan settings view.
        Args:
            compression: The compression toggle value - True/False
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW)
        compression_toggled_state = self._spice.query_item(self.SCAN_HIGH_COMPRESSION + " #SpiceSwitch")["checked"]
        if compression != compression_toggled_state:
            self.dial_common_operations.goto_item(self.SCAN_HIGH_COMPRESSION, "#MenuListLayout")

        compression_toggled_state = self._spice.query_item(self.SCAN_HIGH_COMPRESSION + " #SpiceSwitch")["checked"]
        assert compression_toggled_state == compression, "High compressuion setting mismatch"

    def set_scan_settings_sides(self, sides: str):
        '''
        UI should be on Sides settings screen.
        Args:
            sides: The sides to set - simplex, duplex
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_SIDES_VIEW, timeout = 9.0)
        # Get the object name in ui for the sides value passed
        sides_id = self.sides_dict[sides.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_SIDES_VIEW)
        for i in range(2):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(sides_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_color(self, color: str):
        '''
        UI should be on Color format settings screen.
        Args:
            color: The color to set - color, blackonly, grayscale, autodetect
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_COLOR_FORMAT_VIEW, timeout = 9.0)
        # Get the object name in ui for the color value passed
        color_id = self.colorformat_dict[color.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_COLOR_FORMAT_VIEW)
        for i in range(4):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(color_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_original_size(self, size: str):
        '''
        UI should be on Original size settings screen.
        Args:
            size: The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_ORIGINAL_SIZE_VIEW, timeout = 9.0)
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_ORIGINAL_SIZE_VIEW)
        # Get the object name in ui for the original size value passed
        size_id = self.orgsize_dict[size.lower()][1]
        #Go to top-most item and then navigate to reach the item
        for i in range(49):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_screen = self._spice.wait_for("#RadioButtonListLayout")
        while (self._spice.query_item(size_id)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        #self.dial_common_operations.goto_item(size_id, "#RadioButtonListLayout")
        current_button = self._spice.query_item(size_id + " SpiceText")
        current_button.mouse_click()
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_orientation(self, orientation: str):
        '''
        UI should be on Orienation settings screen.
        Args:
            orientation: The orientation to set - portrait, landscape
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_ORIENTATION_VIEW, timeout = 9.0)
        # Get the object name in ui for the orientation value passed
        orientation_id = self.orientation_dict[size.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_ORIENTATION_VIEW)
        for i in range(2):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(orientation_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        assert self._spice.wait_for(self.SCAN_LIGHTER_DARKER_SLIDER)
        current_value = self._spice.query_item(self.SCAN_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]
        logging.info("Current lighter_darker value is " + current_value)

        assert lighter_darker >= self.SCAN_LIGHTER_DARKER_MIN and lighter_darker <= self.SCAN_LIGHTER_DARKER_MAX, "Lighter/Darker value is out of range"

        if (lighter_darker != current_value): #int(current_value))
            if (lighter_darker > int(current_value)):
                dial_value = 180
            else:
                dial_value = 0

            currentButton = self._spice.query_item(self.SCAN_LIGHTER_DARKER_SLIDER + " SpiceText")
            while (int(current_value) != lighter_darker):
                currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
                time.sleep(1)
                if (lighter_darker < int(current_value)):
                    currentButton.mouse_press(dial_value,dial_value)
                elif (lighter_darker > int(current_value)):
                    currentButton.mouse_wheel(dial_value,dial_value)    
                time.sleep(1)
                current_value = self._spice.query_item(self.SCAN_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]

            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
            time.sleep(1)
            logging.info("Current lighter_darker value is " + current_value)

        assert int(current_value) == lighter_darker, "Lighter/Darker setting is not successful"
    
    def set_scan_settings_tiff_color_compression(self, compression: str):
        '''
        UI should be on tiff_compression settings screen.
        Args:
            tiff compression color: The tiff_compression to set - G3, tiff6 and tiff post
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_COLOR_VIEW, timeout = 9.0)
        # Get the object name in ui for the tiff compression value passed
        compression_id = self.tiffcompression_color_dict[compression.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_COLOR_VIEW)
        for i in range(3):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(compression_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_settings_tiff_mono_compression(self, compression: str):
        '''
        UI should be on tiff_compression settings screen.
        Args:
            tiff compression Mono: The tiff_compression to set - G3, G4 and Automatic
        '''
        assert self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_MONO_VIEW, timeout = 9.0)
        # Get the object name in ui for the tiff compression value passed
        compression_id = self.tiffcompression_mono_dict[compression.lower()][1]
        #Go to top-most item and then navigate to reach the item
        current_screen = self._spice.wait_for(self.SCAN_SETTINGS_TIFF_COMPRESSION_MONO_VIEW)
        for i in range(3):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        self.dial_common_operations.goto_item(compression_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def set_scan_setting(self, setting, setting_value):
        '''
        UI should be on specific settings screen.
        Args:
            setting: The setting that has to be set - filetype, resolution, quality, sides, color,
            size, orientation
            setting_value: Value to set for the setting
                The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
                The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                    e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
                The quality to set - best, draft, standard
                The sides to set - simplex, duplex
                The color to set - color, blackonly, grayscale, autodetect
                The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
                The orientation to set - portrait, landscape
                The tiff compression color- Tiff6 and Tiff post
                The tiff compression Mono- G3, G4 and Automatic                
        '''
        setting_id = ""
        items = 2
        if (setting.lower() == "filetype"):
            screen = self.SCAN_SETTINGS_FILETYPE_VIEW
            setting_id = self.filetype_dict[setting_value.lower()][1]
            items = 8
        elif (setting.lower() == "resolution"):
            screen = self.SCAN_SETTINGS_RESOLUTION_VIEW
            setting_id = self.resolution_dict[setting_value.lower()][1]
            items = 10
        elif (setting.lower() == "quality"):
            screen = self.SCAN_SETTINGS_QUALITY_VIEW
            setting_id = self.quality_dict[setting_value.lower()][1]
            items = 3
        elif (setting.lower() == "sides"):
            screen = self.SCAN_SETTINGS_SIDES_VIEW
            setting_id = self.sides_dict[setting_value.lower()][1]
            items = 2
        elif (setting.lower() == "color"):
            screen = self.SCAN_SETTINGS_COLOR_FORMAT_VIEW
            setting_id = self.colorformat_dict[setting_value.lower()][1]
            items = 4
        elif (setting.lower() == "size"):
            screen = self.SCAN_SETTINGS_ORIGINAL_SIZE_VIEW
            setting_id = self.orgsize_dict[setting_value.lower()][1]
            items = 49
        elif (setting.lower() == "tiffcompression_color"):
            screen = self.SCAN_SETTINGS_TIFF_COMPRESSION_COLOR_VIEW
            setting_id = self.tiffcompression_color_dict[setting_value.lower()][1]
            items = 4
        elif (setting.lower() == "tiffcompression_mono"):
            screen = self.SCAN_SETTINGS_TIFF_COMPRESSION_MONO_VIEW
            setting_id = self.tiffcompression_mono_dict[setting_value.lower()][1]
            items = 5
        elif (setting.lower() == "orientation"):
            screen = self.SCAN_SETTINGS_ORIENTATION_VIEW
            setting_id = self.orientation_dict[setting_value.lower()][1]
            items = 2
        
        else:
            assert False, "Setting not existing"

        assert self._spice.wait_for(screen, timeout = 9.0)
        current_screen = self._spice.wait_for(screen)
        # Go to the top menu
        for i in range(items):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)

        current_screen = self._spice.wait_for("#RadioButtonListLayout")
        while (self._spice.query_item(setting_id)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)

        self._spice.query_item(setting_id)["activeFocus"] == True, "Active focus for setting value is false"
        current_button = self._spice.query_item(setting_id + " SpiceText")
        current_button.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for(self.SCAN_SETTINGS_VIEW, timeout = 9.0)

    def pdf_encryption_enter_password(self, text:str):
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        self.dial_common_operations.goto_item(self.SCAN_PDF_ENCRYPTION_PASSWORD, "#ButtonListLayout")
        assert self._spice.wait_for(self.SPICE_KEYBOARD_VIEW, timeout = 9.0)
        self.dial_keyboard_operations.keyboard_enter_text(text)
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)

    def pdf_encryption_reenter_password(self, text:str):
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        self.dial_common_operations.goto_item(self.SCAN_PDF_ENCRYPTION_REENTER_PASSWORD, "#ButtonListLayout")
        assert self._spice.wait_for(self.SPICE_KEYBOARD_VIEW, timeout = 9.0)
        self.dial_keyboard_operations.keyboard_enter_text(text)
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)

    def pdf_encryption_save(self):
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        self.dial_common_operations.goto_item(self.SAVE_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_PROGRESS_VIEW, timeout = 9.0)

    def pdf_encryption_cancel(self):
        '''
        This method clicks the cancel button in pdf encryption prompt
        UI Flow is pdf encryption prompt -> cancel button
        '''
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        self.dial_common_operations.goto_item(self.CANCEL_BUTTON, "#ButtonListLayout")

    def verify_string(self, net, string_oid, expected_id, menu_level: int = 0):
        '''This method verifies the string on the screen with the expected string from  string id
        Args:
            string_oid: Object Id of string on the screen to be validated
            expected_id: String Id of the of the expected string
            menu_level: Menu level number
        '''
        ui_string = self._spice.query_item(string_oid, menu_level)["text"]
        # Get string translation for English "en-US"
        expected_string = LocalizationHelper.get_string_translation(net, expected_id)
        assert ui_string == expected_string, "String mismatch"

    def verify_setting_is_selected(self, net, setting, setting_value, menu_level: int = 0):
        '''This method compares the selected setting value is checked and at activefocus
        Args:
            UI should be in specific Setting(e.g.: Resolution) value selection screen
            setting: Setting to be validated
            setting_value: setting value
            menu_level: Menu level number
        '''
        setting_id = ""
        #Get the ui object name of the passed setting
        if (setting.lower() == "filetype"):
            setting_id = self.filetype_dict[setting_value.lower()][1]
        elif (setting.lower() == "resolution"):
            setting_id = self.resolution_dict[setting_value.lower()][1]
        elif (setting.lower() == "quality"):
            setting_id = self.quality_dict[setting_value.lower()][1]
        elif (setting.lower() == "sides"):
            setting_id = self.sides_dict[setting_value.lower()][1]
        elif (setting.lower() == "color"):
            setting_id = self.colorformat_dict[setting_value.lower()][1]
        elif (setting.lower() == "size"):
            setting_id = self.orgsize_dict[setting_value.lower()][1]
            time.sleep(1)
        elif (setting.lower() == "orientation"):
            setting_id = self.orientation_dict[setting_value.lower()][1]
        else:
            assert False, "Setting not existing"

        time.sleep(1)
        #Check if the passed setting is the selected option
        assert self._spice.query_item(setting_id)["activeFocus"] == True
        assert self._spice.query_item(setting_id)["checked"] == True

    def verify_setting_string(self, net, setting, setting_value, screen_id = "#MenuListLayout"):
        '''This method compares the selected setting string with the expected string from  string id
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
            setting_value: Value of the setting
            menu_level: Menu level number
        '''
        cstring_id = ""
        setting_id = ""
        #Get the ui object name of the passed setting
        #Get the cstring id for the value string
        if (setting.lower() == "filetype"):
            setting_id = self.SCAN_FILE_TYPE
            cstring_id = self.filetype_dict[setting_value.lower()][0]
        elif (setting.lower() == "resolution"):
            setting_id = self.SCAN_RESOLUTION
            cstring_id = self.resolution_dict[setting_value.lower()][0]
        elif (setting.lower() == "quality"):
            setting_id = self.SCAN_QUALITY
            cstring_id = self.quality_dict[setting_value.lower()][0]
        elif (setting.lower() == "sides"):
            setting_id = self.SCAN_SIDES
            cstring_id = self.sides_dict[setting_value.lower()][0]
        elif (setting.lower() == "color"):
            setting_id = self.SCAN_COLOR_FORMAT
            cstring_id = self.colorformat_dict[setting_value.lower()][0]
        elif (setting.lower() == "size"):
            setting_id = self.SCAN_ORIGINAL_SIZE
            cstring_id = self.orgsize_dict[setting_value.lower()][0]
        elif (setting.lower() == "orientation"):
            setting_id = self.SCAN_ORIENTATION
            cstring_id = self.orientation_dict[setting_value.lower()][0]
        else:
            assert False, "Setting not existing"

        self.dial_common_operations.goto_item(setting_id, screen_id, select_option = False)
        ui_setting_string = self._spice.query_item(setting_id + " SpiceText")["text"]
        expected_string =  LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"

    def flatbed_scan_more_pages(self, number_of_pages=1):
        #DUNE-52561 : after defect resolve need to work on if condition
        if number_of_pages > 1:
            while (number_of_pages>=1):
                self._spice.wait_for("#MessageLayout", timeout = 9.0)
                self.dial_common_operations.goto_item(self.SCAN_ADD_PAGE_BUTTON, "#MessageLayout")
                self.dial_common_operations.goto_item(self.SCAN_ADD_PAGE_START_SCAN_BUTTON, "#MessageLayout")
                time.sleep(2)
                number_of_pages= number_of_pages - 1
            self.dial_common_operations.goto_item(self.SCAN_ADD_PAGE_FINISH_BUTTON, "#MessageLayout")
        elif number_of_pages == 1:                   
            self._spice.wait_for("#MessageLayout", timeout = 9.0)
            self.dial_common_operations.goto_item(self.SCAN_ADD_PAGE_FINISH_BUTTON, "#MessageLayout")
            
    def goto_sharepoint_from_scanapp(self):
        """
        Go to sharepoint from scanapp screen
        """
        # make sure in scanapp
        self._spice.common_operations.goto_item("#a3d696df-b7ff-4d3d-9969-5cd7f18c0c92","#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32")

    def select_sharepoint_by_property_text(self, text):
        """
        Select sharepoint by property text
        """
        self._spice.common_operations.goto_item(f"#{text}", "#SharePointAppApplicationStackView")

    def send_scan_to_share_point_job(self,dial_value=0):
        """
        Send scan to share point job on sharepoint screen
        """
        # make sure in scan to sharepoint screen
        self._spice.common_operations.goto_item("#FolderSaveButton", "#SharePointAppApplicationStackView",dial_value=dial_value)

    def goto_network_folder_from_scanapp(self):
        """
        Go to network folder from scanapp screen
        """
        # make sure in scanapp
        self._spice.common_operations.goto_item("#65acca51-619d-4e29-b1d0-6414e52f908b","#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32")

    def select_network_folder_by_property_text(self, text):
        """
        Select network folder by property text
        """
        self._spice.common_operations.goto_item(f"#{text}", "#FolderAppApplicationStackView")

    def send_scan_to_network_folder_job(self):
        """
        Send scan to folder job on network folder screen
        """
        # make sure in scan to network folder screen
        self._spice.common_operations.goto_item("#FolderSaveButton", "#FolderAppApplicationStackView")
