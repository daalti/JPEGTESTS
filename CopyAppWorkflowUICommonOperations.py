import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.BaseOperations.ICopyAppUIOperations import ICopyAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.copy_scan_ui_option_dict import *
from dunetuf.udw import DuneUnderware
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.print.tray import TrayHandler
from dunetuf.print.media import MediaHandler
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
import dunetuf.common.commonActions as CommonActions

class CopyAppWorkflowUICommonOperations(ICopyAppUIOperations):

    WAIT_TIMEOUT: ClassVar[float] = 7
    """Default wait timeout (s)."""

    def __init__(self, spice):
        self.CopyAppWorkflowObjectIds = CopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.maxtimeout = 120
        self.spice = spice
        self.id_card_copy = IDCardCopyAppWorkflowUICommonOperations(self.spice)
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)


    color_format_dict = {
        "automatic": [CopyAppWorkflowObjectIds.copy_color_automatic_str_id, CopyAppWorkflowObjectIds.combo_color_option_automatic],
        "color": [CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color],
        "grayscale": [CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale]
    }

    content_type_option_dict = {
        # """String id for element value"""
        "mixed": [CopyAppWorkflowObjectIds.copy_content_type_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed], # "Mixed"
        "photograph": [CopyAppWorkflowObjectIds.copy_content_type_photo_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_photograph], # "Photograph"
        "text": [CopyAppWorkflowObjectIds.copy_content_type_text_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_text], # "Text"
        "automatic": [CopyAppWorkflowObjectIds.copy_content_type_auto_str_id],
        "fine": [CopyAppWorkflowObjectIds.copy_content_type_fine_str_id],
        "image": [CopyAppWorkflowObjectIds.copy_content_type_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image],
        "glossy": [CopyAppWorkflowObjectIds.copy_content_type_glossy_str_id]
    }

    output_scale_dict = {
        "none": [CopyAppWorkflowObjectIds.copy_outputScale_none_str_id, CopyAppWorkflowObjectIds.radio_outputScale_none],
        "custom": [CopyAppWorkflowObjectIds.copy_outputScale_custom_str_id, CopyAppWorkflowObjectIds.spinbox_copySettings_outputScale_custom],
        "fit_to_page": [CopyAppWorkflowObjectIds.copy_outputScale_fitToPage_str_id, CopyAppWorkflowObjectIds.radio_outputScale_fitToPage],
        "full_page": [CopyAppWorkflowObjectIds.copy_outputScale_fullPage_str_id, CopyAppWorkflowObjectIds.radio_outputScale_fullPage],
        "legal_to_letter": [CopyAppWorkflowObjectIds.copy_outputScale_legalToletter_str_id, CopyAppWorkflowObjectIds.radio_outputScale_legalToLetter],
        "a4_to_letter": [CopyAppWorkflowObjectIds.copy_outputScale_A4Toletter_str_id, CopyAppWorkflowObjectIds.radio_outputScale_a4ToLetter_91],
        "letter_to_a4": [CopyAppWorkflowObjectIds.copy_outputScale_letterToA4_str_id, CopyAppWorkflowObjectIds.radio_outputScale_letterToA4_94]
    }

    sides_dict = {
        "1_1_sided": [CopyAppWorkflowObjectIds.copy_sides_1to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided],
        "1_2_sided": [CopyAppWorkflowObjectIds.copy_sides_1to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided],
        "2_1_sided": [CopyAppWorkflowObjectIds.copy_sides_2to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided],
        "2_2_sided": [CopyAppWorkflowObjectIds.copy_sides_2to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided]
    }
    
    original_dict = {
        "100x150mm":[CopyAppWorkflowObjectIds.copy_mediasize_100x150mm_str_id,CopyAppWorkflowObjectIds.row_original_size_10x15],
        "Custom":[CopyAppWorkflowObjectIds.copy_mediasize_custom_str_id],
        "A2 (420x594 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a2_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a2_420x594mm],
        "A3 (297x420 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a3_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a3_297x420mm],
        "A4": [CopyAppWorkflowObjectIds.copy_mediasize_a4_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a4_210x297mm],
        "A4_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_a4_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a4_210x297mm],
        "A5": [CopyAppWorkflowObjectIds.copy_mediasize_a5_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a5_148x210mm],
        "A5_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_a5_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a5_148x210mm],
        "A6 (105x148 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a6_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a6_105x148mm],
        "Envelope B5 (176x250 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_b5_str_id],
        "B6 (JIS) (128x182 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_jis_b6_str_id, CopyAppWorkflowObjectIds.row_media_size_jis_b6_128x182mm],
        "Envelope Monarch (3.9x7.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_monarch_str_id],
        "Envelope C5 (162x229 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_c5_str_id],
        "Envelope C6 (114x162 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_c6_str_id],
        "Envelope DL (110x220 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_dl_str_id],
        "jis_b5": [CopyAppWorkflowObjectIds.copy_mediasize_b5_str_id, CopyAppWorkflowObjectIds.row_media_size_jis_b5_182x257mm],
        "B5_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_b5_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_jis_b5_182x257mm],
        "Japanese Envelope Chou #3 (120x235 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_j_envelope_chou3_str_id],
        "Postcard (JIS) (100x148 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_hagaki_str_id],
        "Double Postcard (JIS) (148x200 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_double_postcard_str_id],
        "Executive": [CopyAppWorkflowObjectIds.copy_mediasize_executive_str_id, CopyAppWorkflowObjectIds.row_original_size_executive_7_25x10_5in],
        "oficio_8_5x13": [CopyAppWorkflowObjectIds.copy_mediasize_oficio_str_id, CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13in],
        "4x6 in.": [CopyAppWorkflowObjectIds.copy_mediasize_4x6_str_id],
        "5x7 in.": [CopyAppWorkflowObjectIds.copy_mediasize_5x7_str_id , CopyAppWorkflowObjectIds.row_media_size_index_5x7_5x7in],
        "5x8 in.": [CopyAppWorkflowObjectIds.copy_mediasize_5x8_str_id, CopyAppWorkflowObjectIds.row_media_size_index_5x8_5x8in],
        "Legal": [CopyAppWorkflowObjectIds.copy_mediasize_legal_str_id, CopyAppWorkflowObjectIds.row_media_size_na_legal_8_5x14in],
        "Letter": [CopyAppWorkflowObjectIds.copy_mediasize_letter_str_id, CopyAppWorkflowObjectIds.row_media_size_na_letter_8_5x11in],
        "Letter_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_letter_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_na_letter_8_5x11in],
        "Envelope #10 (4.1x9.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_com10_id],
        "Oficio_8_5x13_4": [CopyAppWorkflowObjectIds.copy_mediasize_oficio_8_5x13_4_str_id, CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13_4in],
        "16K (184x260 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_184x260_str_id],
        "16K (195x270 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_195x270_str_id],
        "16K (197x273 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_str_id],
        "Statement (8.5x5.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_statement_str_id, CopyAppWorkflowObjectIds.row_media_size_invoice_5_5x8_5in],
        "Envelope 9": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_9_str_id],
        "Any":[CopyAppWorkflowObjectIds.copy_mediasize_any_str_id],
        "2L (127x178 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_2l_127x178_str_id],
        "5x5 in": [CopyAppWorkflowObjectIds.copy_mediasize_5x5in_str_id],
        "letter_8x10in": [CopyAppWorkflowObjectIds.copy_mediasize_letter_8x10in_str_id],
        "Ofuku Hagaki (200x148 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_double_postcard_str_id],
        "L (89x127 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_l_3_5x5in_str_id],
        "Hagaki (100x148 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_hagaki_str_id],
        "Envelope A2(111x146 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_a2_str_id],
        "Tabloid (11x17 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_ledger_11x17_str_id],
        "Envelope 6 3/4 (3.63x6.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_6_three_quarter_str_id],
        "3x5 in.": [CopyAppWorkflowObjectIds.copy_mediasize_index_3x5in_str_id, CopyAppWorkflowObjectIds.row_media_size_index_3x5_3x5in],
        "Japanese Envelope Chou #4 (90x205 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_j_envelope_chou4_str_id],
        "4x12 in": [CopyAppWorkflowObjectIds.copy_mediasize_4x12in_str_id],
        "B4 (JIS) (257x364 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b4_jis_257x364mm_str_id],
        "11x14 in.": [CopyAppWorkflowObjectIds.copy_mediasize_11x14in_str_id],
        "MIXED_LETTER_LEGAL": [CopyAppWorkflowObjectIds.copy_mediasize_mixed_letter_legal],
        "MIXED_LETTER_LEDGER": [CopyAppWorkflowObjectIds.copy_mediasize_mixed_letter_ledger],
        "MIXED_A4_A3": [CopyAppWorkflowObjectIds.copy_mediasize_mixed_a4_a3]
    }


    paper_dict = {
        "Custom":[CopyAppWorkflowObjectIds.copy_mediasize_custom_str_id, CopyAppWorkflowObjectIds.row_media_size_custom],
        "Arch A (229x305 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_a_str_id],
        "Arch B (305x457 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_b_str_id],
        "Arch C (457x610 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_c_str_id],
        "Arch D (610x914 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_d_str_id],
        "Arch E (914x1919 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_e_str_id],
        "Arch E2 (660x965 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_e2_str_id],
        "Arch E3 (686x991 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_arch_e3_str_id],
        "A2 (420x594 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a2_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a2_420x594mm],
        "A3 (297x420 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a3_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a3_297x420mm],
        "A4": [CopyAppWorkflowObjectIds.copy_mediasize_a4_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a4_210x297mm],
        "A4_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_a4_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a4_210x297mm],
        "A5": [CopyAppWorkflowObjectIds.copy_mediasize_a5_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a5_148x210mm],
        "A5_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_a5_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a5_148x210mm],
        "A6 (105x148 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_a6_str_id, CopyAppWorkflowObjectIds.row_media_size_iso_a6_105x148mm],
        "B0 (ISO) (1000x1414 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_iso_b0_str_id],
        "B1 (ISO) (707x1000 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_iso_b1_str_id],
        "B2 (ISO) (500x707 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_iso_b2_str_id],
        "B3 (ISO) (353x500 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_iso_b3_str_id],
        "B4 (ISO) (250x353 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_iso_b4_str_id],
        "Envelope B5 (176x250 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_b5_str_id,CopyAppWorkflowObjectIds.row_media_size_envelope_b5],
        "B6 (JIS) (128x182 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_jis_b6_str_id, CopyAppWorkflowObjectIds.row_media_size_jis_b6_128x182mm],
        "Envelope Monarch (3.9x7.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_monarch_str_id,CopyAppWorkflowObjectIds.row_media_size_envelope_monarch],
        "C0 (917x1297 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_c0_str_id],
        "C1 (648x917 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_c1_str_id],
        "C2 (458x648 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_c2_str_id],
        "C3 (324x458 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_c3_str_id],
        "C4 (229x324 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_c4_str_id],
        "Envelope C5 (162x229 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_c5_str_id,CopyAppWorkflowObjectIds.row_media_size_envelope_c5],
        "Envelope C6 (114x162 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_c6_str_id,CopyAppWorkflowObjectIds.row_media_size_envelope_c6],
        "Envelope DL (110x220 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_dl_str_id,CopyAppWorkflowObjectIds.row_media_size_envelope_dl],
        "jis_b5": [CopyAppWorkflowObjectIds.copy_mediasize_b5_str_id, CopyAppWorkflowObjectIds.row_media_size_jis_b5_182x257mm],
        "B5_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_b5_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_jis_b5_182x257mm],
        "Japanese Envelope Chou #3 (120x235 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_j_envelope_chou3_str_id, CopyAppWorkflowObjectIds.row_media_size_jpn_chou3_120x235mm],
        "Japanese Envelope Chou #4 (90x205 mm)":[CopyAppWorkflowObjectIds.copy_mediasize_j_envelope_chou4_str_id, CopyAppWorkflowObjectIds.row_media_size_jpn_chou4_90x205mm],
        "Postcard (JIS) (100x148 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_hagaki_str_id,CopyAppWorkflowObjectIds.row_media_size_postcard_jis_100x148mm],
        "Double Postcard (JIS) (148x200 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_double_postcard_str_id,CopyAppWorkflowObjectIds.row_media_size_double_postcard_jis_148x200mm],
        "2L (127x178 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_2l_127x178_str_id],
        "Executive": [CopyAppWorkflowObjectIds.copy_mediasize_executive_str_id, CopyAppWorkflowObjectIds.row_media_size_executive_7_25x10_5in],
        "oficio_8_5x13": [CopyAppWorkflowObjectIds.copy_mediasize_oficio_str_id, CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13in],
        "4x6 in.": [CopyAppWorkflowObjectIds.copy_mediasize_4x6_str_id,CopyAppWorkflowObjectIds.row_media_size_index_4x6_4x6in],
        "5x7 in.": [CopyAppWorkflowObjectIds.copy_mediasize_5x7_str_id,CopyAppWorkflowObjectIds.row_media_size_index_5x7_5x7in],
        "5x8 in.": [CopyAppWorkflowObjectIds.copy_mediasize_5x8_str_id,CopyAppWorkflowObjectIds.row_media_size_index_5x8_5x8in],
        "Legal": [CopyAppWorkflowObjectIds.copy_mediasize_legal_str_id, CopyAppWorkflowObjectIds.row_media_size_na_legal_8_5x14in],
        "Letter": [CopyAppWorkflowObjectIds.copy_mediasize_letter_str_id, CopyAppWorkflowObjectIds.row_media_size_na_letter_8_5x11in],
        "Letter_SEF": [CopyAppWorkflowObjectIds.copy_mediasize_letter_rotate_str_id, CopyAppWorkflowObjectIds.row_media_size_rotate_na_letter_8_5x11in],
        "Envelope #10 (4.1x9.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_com10_id,CopyAppWorkflowObjectIds.row_media_size_envelope_10],
        "Oficio_8_5x13_4": [CopyAppWorkflowObjectIds.copy_mediasize_oficio_8_5x13_4_str_id, CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13_4in],
        "16K (184x260 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_184x260_str_id,CopyAppWorkflowObjectIds.row_media_size_16k_184x260],
        "16K (195x270 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_195x270_str_id,CopyAppWorkflowObjectIds.row_media_size_16k_195x270],
        "16K (197x273 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_16k_str_id,CopyAppWorkflowObjectIds.row_media_size_16k_197x273],
        "Statement (5.5x8.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_statement_str_id, CopyAppWorkflowObjectIds.row_media_size_invoice_5_5x8_5in],
        "ledger": [CopyAppWorkflowObjectIds.copy_mediasize_ledger_11x17_str_id],
        "100x150mm": [CopyAppWorkflowObjectIds.copy_mediasize_100x150mm_str_id,CopyAppWorkflowObjectIds.row_media_size_10x15],
        "D 22x34 in.": [CopyAppWorkflowObjectIds.copy_mediasize_d_22x34in_str_id],
        "E 34x44 in.": [CopyAppWorkflowObjectIds.copy_mediasize_e_34x44in_str_id],
        "Envelope 6 3/4 (3.63x6.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_envelope_6_three_quarter_str_id],
        "Super B (13x19 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_super_b_13x19in_str_id],
        "Arch E1 (762x1067 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_arch_e1_762x1067mm_str_id],
        "L (89x127 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_l_3_5x5in_str_id,CopyAppWorkflowObjectIds.row_media_size_l_89x127],
        "4x12 in": [CopyAppWorkflowObjectIds.copy_mediasize_4x12in_str_id],
        "4x5 in": [CopyAppWorkflowObjectIds.copy_mediasize_4x5in_str_id],
        "5x5 in": [CopyAppWorkflowObjectIds.copy_mediasize_5x5in_str_id],
        "8K (260x368 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_8k_260x368mm_str_id],
        "8K (270x390 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_8k_270x390mm_str_id],
        "8K (273x394 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_8k_273x394mm_str_id],
        "RA3 (305x430 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_ra3_305x430mm_str_id],
        "RA4 (215x305 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_ra4_215x305mm_str_id],
        "SRA3 (320x450 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_sra3_320x450mm_str_id],
        "SRA4 (225x320 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_sra4_225x320mm_str_id],
        "B0 (JIS) (1030x1456 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b0_jis_1030x1456mm_str_id],
        "B1 (JIS) (728x1030 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b1_jis_728x1030mm_str_id],
        "B2 (JIS) (515x728 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b2_jis_515x728mm_str_id],
        "B3 (JIS) (364x515 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b3_jis_364x515mm_str_id],
        "B4 (JIS) (257x364 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_b4_jis_257x364mm_str_id],
        "Statement (8.5x5.5 in.)": [CopyAppWorkflowObjectIds.copy_mediasize_statement_str_id],
        "ANSI C (432x559 mm)": [CopyAppWorkflowObjectIds.copy_mediasize_ansi_c_17x22in_str_id],
        "11x14 in.": [CopyAppWorkflowObjectIds.copy_mediasize_11x14in_str_id],
        "letter_8x10in": [CopyAppWorkflowObjectIds.copy_mediasize_letter_8x10in_str_id],
        "3x5 in.": [CopyAppWorkflowObjectIds.copy_mediasize_index_3x5in_str_id, CopyAppWorkflowObjectIds.row_media_size_index_3x5_3x5in]
    }

    paper_type_option_dict = {
        # dictionary key is element key,value is a list (0:strid  1:itemid(radio) 2:rowid)
        "Any Type": [CopyAppWorkflowObjectIds.copy_paper_type_any_str_id, CopyAppWorkflowObjectIds.radio_paperType_any, CopyAppWorkflowObjectIds.row_paper_type_any],
        "Plain": [CopyAppWorkflowObjectIds.copy_paper_type_plain_str_id, CopyAppWorkflowObjectIds.radio_paperType_plain, CopyAppWorkflowObjectIds.row_paper_type_plain],
        "HP EcoFFICIENT": [CopyAppWorkflowObjectIds.copy_paperType_ecoEfficient_str_id, CopyAppWorkflowObjectIds.radio_paperType_ecoEfficient, CopyAppWorkflowObjectIds.row_paper_type_hp_ecofficient],
        "HP Matte (90g)": [CopyAppWorkflowObjectIds.copy_paperType_matte_90_str_id, CopyAppWorkflowObjectIds.radio_paperType_matte_90gsm, CopyAppWorkflowObjectIds.row_paper_type_matte_dash_90gsm],
        "HP Matte (105g)": [CopyAppWorkflowObjectIds.copy_paperType_matte_105_str_id, CopyAppWorkflowObjectIds.radio_paperType_matte_105gsm, CopyAppWorkflowObjectIds.row_paper_type_matte_dash_105gsm],
        "HP Matte (120g)": [CopyAppWorkflowObjectIds.copy_paperType_matte_120_str_id, CopyAppWorkflowObjectIds.radio_paperType_matte_120gsm, CopyAppWorkflowObjectIds.row_paper_type_matte_dash_120gsm],
        "HP Matte (150g)": [CopyAppWorkflowObjectIds.copy_paperType_matte_150_str_id, CopyAppWorkflowObjectIds.radio_paperType_matte_150gsm, CopyAppWorkflowObjectIds.row_paper_type_brochure_matte_150gsm],
        "HP Matte (200g)": [CopyAppWorkflowObjectIds.copy_paperType_matte_200_str_id, CopyAppWorkflowObjectIds.radio_paperType_matte_200gsm, CopyAppWorkflowObjectIds.row_paper_type_hp_matte_200g],
        "HP Prem Matte Photo Paper": [CopyAppWorkflowObjectIds.copy_paperType_prem_matte_str_id, 'dummy', 'dummy'],
        "Brochure Glossy": [CopyAppWorkflowObjectIds.copy_paperType_brochure_glossy_str_id, 'dummy', 'dummy'],
        "HP Glossy (120g)": [CopyAppWorkflowObjectIds.copy_paperType_glossy_120_str_id, CopyAppWorkflowObjectIds.radio_paperType_glossy_130gsm, CopyAppWorkflowObjectIds.row_paper_type_hp_glossy_120g],
        "HP Glossy (150g)": [CopyAppWorkflowObjectIds.copy_paperType_glossy_150_str_id, CopyAppWorkflowObjectIds.radio_paperType_glossy_160gsm, CopyAppWorkflowObjectIds.row_paper_type_hp_glossy_150gsm],
        "HP Glossy (200g)": [CopyAppWorkflowObjectIds.copy_paperType_glossy_200_str_id, CopyAppWorkflowObjectIds.radio_paperType_glossy_200gsm, CopyAppWorkflowObjectIds.row_paper_type_hp_glossy_200g],
        "HP Tri-Fold Glossy (150g)": [CopyAppWorkflowObjectIds.copy_paperType_glossy_tri_fold_str_id, CopyAppWorkflowObjectIds.radio_paperType_glossy_tri_fold, CopyAppWorkflowObjectIds.row_paper_type_hp_tri_fold_glossy_150g],
        "Light (60-74g)":  [CopyAppWorkflowObjectIds.copy_paperType_light_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_light],
        "Intermediate (85-95g)": [CopyAppWorkflowObjectIds.copy_paperType_intermediate_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_intermediate],
        "Mid-Weight (96-110g)": [CopyAppWorkflowObjectIds.copy_paperType_mid_weight_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_mid_weight],
        "Heavy (111-130g)": [CopyAppWorkflowObjectIds.copy_paperType_heavy_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_heavy],
        "Extra Heavy (131-175g)": [CopyAppWorkflowObjectIds.copy_paperType_extra_heavy_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_extra_heavy],
        "Cardstock (176-220g)": [CopyAppWorkflowObjectIds.copy_paperType_card_stock_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_cardstock],
        "Heavy Glossy (111-130g)": [CopyAppWorkflowObjectIds.copy_paperType_heavy_glossy_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_heavy_glossy],
        "Extra Heavy Glossy (131-175g)": [CopyAppWorkflowObjectIds.copy_paperType_extra_heavy_glossy_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_extra_heavy_glossy],
        "Cardstock Glossy": [CopyAppWorkflowObjectIds.copy_paperType_cardstock_glossy_str_id, CopyAppWorkflowObjectIds.radio_paperType_cardstock_glossy, CopyAppWorkflowObjectIds.row_paper_type_cardstock_glossy],
        "Labels": [CopyAppWorkflowObjectIds.copy_paperType_labels_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_lables],
        "Letterhead": [CopyAppWorkflowObjectIds.copy_paperType_letterhead_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_letterhead],
        "Envelope": [CopyAppWorkflowObjectIds.copy_paperType_envelope_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_envelope],
        "Heavy Envelope": [CopyAppWorkflowObjectIds.copy_paperType_heavy_envelope_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_heavy_envelope],
        "Preprinted": [CopyAppWorkflowObjectIds.copy_paperType_preprinted_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_preprinted],
        "Prepunched": [CopyAppWorkflowObjectIds.copy_paperType_prepunched_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_prepunched],
        "Colored": [CopyAppWorkflowObjectIds.copy_paperType_colored_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_colored],
        "Bond": [CopyAppWorkflowObjectIds.copy_paperType_bond_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_bond],
        "Light Bond":[CopyAppWorkflowObjectIds.copy_paperType_light_bond_str_id, 'dummy', 'dummy'],
        "Recycled": [CopyAppWorkflowObjectIds.copy_paperType_recycled_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_recycled],
        "Rough": [CopyAppWorkflowObjectIds.copy_paperType_rough_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_rough],
        "Heavy Rough": [CopyAppWorkflowObjectIds.copy_paperType_heavy_rough_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_heavy_rough],
        "Light Rough": [CopyAppWorkflowObjectIds.copy_paperType_light_rough_str_id, 'dummy', 'dummy'],
        "Opaque Film": [CopyAppWorkflowObjectIds.copy_paperType_opaque_film_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_opaque_film],
        "Transparency": [CopyAppWorkflowObjectIds.copy_paperType_transparency_str_id, 'dummy', CopyAppWorkflowObjectIds.row_paper_type_color_Transparency],
        "HP Photographic Glossy": [CopyAppWorkflowObjectIds.copy_paperType_photographic_glossy_str_id, 'dummy', 'dummy'],
        "HP Tri-fold Brochure Paper Glossy": [CopyAppWorkflowObjectIds.copy_paperType_trifold_brochure_glossy_str_id, 'dummy', 'dummy'],
        "Paperboard (301g+)":[CopyAppWorkflowObjectIds.copy_paperType_heavy_paperboard_str_id, 'dummy', 'dummy'],
        "Paperboard (256-300g)":[CopyAppWorkflowObjectIds.copy_paperType_paperboard_str_id, 'dummy', 'dummy'],
        "Paperboard (221-255g)":[CopyAppWorkflowObjectIds.copy_paperType_light_paperboard_str_id, 'dummy', 'dummy'],
        "Tab":[CopyAppWorkflowObjectIds.copy_paperType_tab_stock_str_id, 'dummy', 'dummy'],
    	"HP Advanced Photo": [CopyAppWorkflowObjectIds.copy_paperType_hp_advanced_photo_str_id, 'dummy', 'dummy'],
	    "HP Soft Glossy (120g)": [CopyAppWorkflowObjectIds.copy_paperType_hp_soft_gloss_120g_str_id, 'dummy', 'dummy'],
        "Mid-Weight Glossy (96-110g)": [CopyAppWorkflowObjectIds.copy_paperType_hp_midweight_glossy_str_id, 'dummy', 'dummy'],
        "Other Photo Inkjet Papers": [CopyAppWorkflowObjectIds.copy_paperType_hp_photographic_inkjet_str_id, 'dummy', 'dummy'],
        "HP Matte Brochure or Professional Paper": [CopyAppWorkflowObjectIds.copy_paperType_hp_matte_brochure_str_id, 'dummy', 'dummy'],
        "HP Matte Presentation Paper": [CopyAppWorkflowObjectIds.copy_paperType_hp_matte_presentation_str_id, 'dummy', 'dummy'],
        "Other Matte Inkjet Papers": [CopyAppWorkflowObjectIds.copy_paperType_hp_matte_inkjet_str_id, 'dummy', 'dummy'],
        "HP Glossy Brochure or Professional Paper": [CopyAppWorkflowObjectIds.copy_paperType_hp_specialty_glossy_str_id, 'dummy', 'dummy'],
        "Other Glossy Inkjet Papers": [CopyAppWorkflowObjectIds.copy_paperType_hp_specialty_glossy_inkjet_str_id, 'dummy', 'dummy'],
        "Inkjet Hagaki": [CopyAppWorkflowObjectIds.copy_paperType_hp_specialty_hagaki_str_id, 'dummy', 'dummy'],
        "HP Matte Photo Paper": [CopyAppWorkflowObjectIds.copy_paperType_hp_matte_photo_duplex_str_id, 'dummy', 'dummy'],
        "UserType10": ["dummy", CopyAppWorkflowObjectIds.radio_paperType_user_defined_10, CopyAppWorkflowObjectIds.row_paper_type_user_defined_10]
    }

    paper_tray_option_dict = {
        # """String id for element value""" combo_paperTray_option_tray1
        "tray1": [CopyAppWorkflowObjectIds.copy_paperTray_tray1_str_id, CopyAppWorkflowObjectIds.combo_paperTray_option_tray1],  # "Tray 1"
        "tray2": [CopyAppWorkflowObjectIds.copy_paperTray_tray2_str_id, CopyAppWorkflowObjectIds.combo_paperTray_option_tray2],  # "Tray 2"
        "tray3": [CopyAppWorkflowObjectIds.copy_paperTray_tray3_str_id, CopyAppWorkflowObjectIds.combo_paperTray_option_tray3],  # "Tray 3"
        "automatic": [CopyAppWorkflowObjectIds.copy_paperTray_auto_str_id, CopyAppWorkflowObjectIds.combo_paperTray_option_auto] # "Automatic"  # dest print mediaSource
    }

    file_quality_option_dict = {
        # """String id for element value"""
        "best": [CopyAppWorkflowObjectIds.copy_quality_best_str_id, CopyAppWorkflowObjectIds.combo_quality_option_best], # "Best"
        "draft": [CopyAppWorkflowObjectIds.copy_quality_draft_str_id, CopyAppWorkflowObjectIds.combo_quality_option_draft], # "Draft"
        "standard": [CopyAppWorkflowObjectIds.copy_quality_standard_str_id, CopyAppWorkflowObjectIds.combo_quality_option_standard] # "Standard"
    }

    pages_per_sheet_option_dict = {
        # """String id for element value"""
        "one": [CopyAppWorkflowObjectIds.copy_pagesPerSheet_oneup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1], # "ONE"
        "two": [CopyAppWorkflowObjectIds.copy_pagesPerSheet_twoup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2], # "TWO"
        # "4_rightThenDown": [CopyAppWorkflowObjectIds.copy_pagesPerSheet_fourup_right_then_down_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_4_rightThenDown], # "4_rightThenDown"
        "fourup_right_then_down": [CopyAppWorkflowObjectIds.copy_pagesPerSheet_fourup_right_then_down_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_4_rightThenDown], # "4_rightThenDown"
        "fourup_down_then_right": [CopyAppWorkflowObjectIds.copy_pagesPerSheet_fourup_down_then_right_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_4_downThenRight] # "4_downThenRight"
    }

    sides_options_dict = {
        "1_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided}",
        "1_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided}",
        "2_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided}",
        "2_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided}",
    }
    
    scan_mode_options_dict = {
        "standard": f"{CopyAppWorkflowObjectIds.scan_mode_option_standard_document}",
        "jobBuild": f"{CopyAppWorkflowObjectIds.scan_mode_option_job_build}",
        "idCard"  : f"{CopyAppWorkflowObjectIds.scan_mode_option_id_card}",
        "bookMode": f"{CopyAppWorkflowObjectIds.scan_mode_option_book_mode}"
    }
    
    blank_page_suppression_dict = {
        "on": [CopyAppWorkflowObjectIds.copy_blank_page_suppression_on_str_id, CopyAppWorkflowObjectIds.combo_option_blankPageSuppression_on],
        "off": [CopyAppWorkflowObjectIds.copy_blank_page_suppression_off_str_id, CopyAppWorkflowObjectIds.combo_option_blankPageSuppression_off]
    }

    staple_dict = {
        "none": [CopyAppWorkflowObjectIds.copy_staple_none_str_id, CopyAppWorkflowObjectIds.row_staple_none],
        "lefttwopoints": [CopyAppWorkflowObjectIds.copy_staple_leftTwoPoints_str_id, CopyAppWorkflowObjectIds.row_staple_leftTwoPoints],
        "topRightOnePointAngled": [CopyAppWorkflowObjectIds.copy_staple_topRightOnePointAngled_str_id, CopyAppWorkflowObjectIds.row_staple_topRightOnePointAngled]
    }

    punch_dict = {
        "none": [CopyAppWorkflowObjectIds.copy_punch_none_str_id, CopyAppWorkflowObjectIds.row_punch_none],
        "leftTwoPointDin": [CopyAppWorkflowObjectIds.copy_punch_leftTwoPointDin_str_id, CopyAppWorkflowObjectIds. row_punch_leftTwoPointDin],
        "rightTwoPointDin": [CopyAppWorkflowObjectIds.copy_punch_rightTwoPointDin_str_id, CopyAppWorkflowObjectIds.row_punch_rightTwoPointDin]
    }

    fold_dict = {
        "none": [CopyAppWorkflowObjectIds.copy_fold_none_str_id, CopyAppWorkflowObjectIds.row_fold_none],
        "vinwardtop": [CopyAppWorkflowObjectIds.copy_fold_vInwardTop_str_id, CopyAppWorkflowObjectIds.row_fold_Vfold]
    }
    
    watermark_text_options_dict = {
        "none": [CopyAppWorkflowObjectIds.copy_watermark_text_none_str_id],
        "draft": [CopyAppWorkflowObjectIds.copy_watermark_text_draft_str_id],
        "confidential"  : [CopyAppWorkflowObjectIds.copy_watermark_text_confidential_str_id],
        "secret": [CopyAppWorkflowObjectIds.copy_watermark_text_secret_str_id],
        "top_secret": [CopyAppWorkflowObjectIds.copy_watermark_text_top_secret_str_id],
        "urgent": [CopyAppWorkflowObjectIds.copy_watermark_text_urgent_str_id]
    }
    
    tray_media_dict = {
        "Any": MediaSize.Any.name,
        "A4": MediaSize.A4.name,
        "Letter": MediaSize.Letter.name,
        "Legal": MediaSize.Legal.name,
        "Executive": MediaSize.Executive.name,
        "oficio_8_5x13": MediaSize.EightPointFiveByThirteen.name,
        "5x8 in.": MediaSize.FiveXEight.name,
        "A5": MediaSize.A5.name,
        "jis_b5": MediaSize.JisB5.name,
        "B6 (JIS) (128x182 mm)": MediaSize.JisB6.name,
        "16K (195x270 mm)": MediaSize.Size16K195x270.name,
        "16K (184x260 mm)": MediaSize.Size16K184x260.name,
        "16K (197x273 mm)": MediaSize.SixteenK.name,
        "Double Postcard (JIS) (148x200 mm)": MediaSize.JDoublePostcard.name,
        "Statement (8.5x5.5 in.)": MediaSize.Statement.name,
        "Oficio_8_5x13_4": MediaSize.Oficio216x340.name,
        "A6 (105x148 mm)": MediaSize.A6.name,
        "100x150mm": MediaSize.Size10x15cm.name,
        "Postcard (JIS) (100x148 mm)": MediaSize.JPostcard.name,
        "Envelope #10 (4.1x9.5 in.)": MediaSize.COM10Envelope.name,
        "Envelope Monarch (3.9x7.5 in.)": MediaSize.MonarchEnvelope.name,
        "Envelope B5 (176x250 mm)": MediaSize.B5Envelope.name,
        "Envelope C5 (162x229 mm)": MediaSize.C5Envelope.name,
        "Envelope DL (110x220 mm)": MediaSize.DLEnvelope.name,
        "4x6 in.": MediaSize.FourXSix.name,
        "2L (127x178 mm)": MediaSize.Any.name,
        "5x5 in": MediaSize.Any.name,
        "5x7 in.": MediaSize.FiveXSeven.name,
        "letter_8x10in": MediaSize.Any.name,
        "Ofuku Hagaki (200x148 mm)": MediaSize.Any.name,
        "L (89x127 mm)": MediaSize.SizeL9x13cm.name,
        "Envelope 6 3/4 (3.63x6.5 in.)": MediaSize.Any.name,
        "3x5 in.": MediaSize.ThreeXFive.name,
        "Japanese Envelope Chou #4 (90x205 mm)": MediaSize.JChou4Envelope.name,
        "Hagaki (100x148 mm)": MediaSize.Any.name,
        "4x12 in": MediaSize.Any.name,
        "Envelope A2(111x146 mm)": MediaSize.Any.name,
        "Japanese Envelope Chou #3 (120x235 mm)": MediaSize.JChou3Envelope.name,
        "B4 (JIS) (257x364 mm)": MediaSize.Any.name,
        "11x14 in.": MediaSize.Any.name,
        "Tabloid (11x17 in.)": MediaSize.Any.name,
        "A3 (297x420 mm)": MediaSize.A3.name,
        "Custom": MediaSize.Custom.name,
    }

    metadata_to_ui_media_sizes_map = {'na_letter_8.5x11in': {"ui": "Letter"},
                                      'na_legal_8.5x14in': {"ui": "Legal"},
                                      'na_executive_7.25x10.5in': {"ui": "Executive"},
                                      'na_foolscap_8.5x13in': {"ui": "oficio_8_5x13"},
                                      'na_index-4x6_4x6in': {"ui": "4x6 in."},
                                      'na_index-5x8_5x8in': {"ui": "5x8 in."},
                                      'iso_a4_210x297mm': {"ui": "A4"},
                                      'iso_a5_148x210mm': {"ui": "A5"},
                                      'iso_a6_105x148mm': {"ui": "A6 (105x148 mm)"},
                                      'jis_b5_182x257mm': {"ui": "jis_b5"},
                                      'jis_b6_128x182mm': {"ui": "B6 (JIS) (128x182 mm)"},
                                      'om_small-photo_100x150mm': {"ui": "100x150mm"},
                                      'na_oficio_8.5x13.4in': {"ui": "Oficio_8_5x13_4"},
                                      'om_16k_195x270mm': {"ui": "16K (195x270 mm)"},
                                      'om_16k_184x260mm': {"ui": "16K (184x260 mm)"},
                                      'roc_16k_7.75x10.75in': {"ui": "16K (197x273 mm)"},
                                      'jpn_hagaki_100x148mm': {"ui": "Postcard (JIS) (100x148 mm)"},
                                      'jpn_oufuku_148x200mm': {"ui": "Double Postcard (JIS) (148x200 mm)"},
                                      'na_number-10_4.125x9.5in': {"ui": "Envelope #10 (4.1x9.5 in.)"},
                                      'na_monarch_3.875x7.5in': {"ui": "Envelope Monarch (3.9x7.5 in.)"},
                                      'iso_b5_176x250mm': {"ui": "Envelope B5 (176x250 mm)"},
                                      'iso_c5_162x229mm': {"ui": "Envelope C5 (162x229 mm)"},
                                      'iso_dl_110x220mm': {"ui": "Envelope DL (110x220 mm)"},
                                      'com.hp.ext.mediaSize.iso_a5_148x210mm.rotated': {"ui": "A5_SEF"},
                                      'custom': {"ui": "Custom"},
                                      'any': {"ui": "Any"},
                                      'na_index-3x5_3x5in': {"ui": "3x5 in."},
                                      'na_a2_4.375x5.75in': {"ui": "Envelope A2(111x146 mm)"},
                                      'jpn_chou3_120x235mm': {"ui": "Japanese Envelope Chou #3 (120x235 mm)"},
                                      'jpn_chou4_90x205mm': {"ui": "Japanese Envelope Chou #4 (90x205 mm)"},
                                      'jis_b4_257x364mm': {"ui": "B4 (JIS) (257x364 mm)"},
                                      'iso_a3_297x420mm': {"ui": "A3 (297x420 mm)"},
                                      'na_govt-letter_8x10in': {"ui": "letter_8x10in"},
                                      'na_5x7_5x7in': {"ui": "5x7 in."},
                                      'oe_square-photo_5x5in': {"ui": "5x5 in"},
                                      'oe_photo-l_3.5x5in': {"ui": "L (89x127 mm)"},
                                      'jpn_photo-2l_127x177_8mm': {"ui": "2L (127x178 mm)"},
                                      'na_invoice_5.5x8.5in': {"ui": "Statement (5.5x8.5 in.)"},}

    metadata_to_ui_media_types_map = {'cardstock': {"ui": "Cardstock (176-220g)"},
                                      'labels': {"ui": "Labels"},
                                      'stationery': {"ui": "Plain"},
                                      'any': {"ui": "Any Type"},
                                      'com.hp-trifold-brochure-glossy-150gsm': {"ui": "HP Tri-Fold Glossy (150g)"},
                                      'com.hp.EcoSMARTLite': {"ui": "HP EcoFFICIENT"},
                                      'com.hp.cardstock-glossy': {"ui": "Cardstock Glossy"},
                                      'com.hp.extra-heavy': {"ui": "Extra Heavy (131-175g)"},
                                      'com.hp.extra-heavy-gloss': {"ui": "Extra Heavy Glossy (131-175g)"},
                                      'com.hp.film-opaque': {"ui": "Opaque Film"},
                                      'com.hp.glossy-130gsm': {"ui": "HP Glossy (120g)"},
                                      'com.hp.glossy-160gsm': {"ui": "HP Glossy (150g)"},
                                      'com.hp.glossy-220gsm': {"ui": "HP Glossy (200g)"},
                                      'com.hp.heavy-glossy': {"ui": "Heavy Glossy (111-130g)"},
                                      'com.hp.heavy-rough': {"ui": "Heavy Rough"},
                                      'com.hp.intermediate': {"ui": "Intermediate (85-95g)"},
                                      'com.hp.matte-105gsm': {"ui": "HP Matte (105g)"},
                                      'com.hp.matte-120gsm': {"ui": "HP Matte (120g)"},
                                      'com.hp.matte-160gsm': {"ui": "HP Matte (150g)"},
                                      'com.hp.matte-200gsm': {"ui": "HP Matte (200g)"},
                                      'com.hp.matte-90gsm': {"ui": "HP Matte (90g)"},
                                      'com.hp.midweight': {"ui": "Mid-Weight (96-110g)"},
                                      'com.hp.recycled': {"ui": "Recycled"},
                                      'com.hp.rough': {"ui": "Rough"},
                                      'envelope': {"ui": "Envelope"},
                                      'envelope-heavyweight': {"ui": "Heavy Envelope"},
                                      'stationery-bond': {"ui": "Bond"},
                                      'stationery-colored': {"ui": "Colored"},
                                      'stationery-heavyweight': {"ui": "Heavy (111-130g)"},
                                      'stationery-letterhead': {"ui": "Letterhead"},
                                      'stationery-lightweight': {"ui": "Light (60-74g)"},
                                      'stationery-preprinted': {"ui": "Preprinted"},
                                      'stationery-prepunched': {"ui": "Prepunched"},
                                      'transparency': {"ui": "Transparency"}
                                      }
    
    booklet_format_dict = {
        "on": [CopyAppWorkflowObjectIds.copy_booklet_format_on_str_id],
        "off": [CopyAppWorkflowObjectIds.copy_booklet_format_off_str_id],
        "saddlestitch":[CopyAppWorkflowObjectIds.copy_booklet_format_saddleStitch_str_id]
    }

    stamp_location_dict = {
        "main": (CopyAppWorkflowObjectIds.list_stamp_menu, CopyAppWorkflowObjectIds.list_stamp_value),
        "topLeft": (CopyAppWorkflowObjectIds.list_stamp_topLeft, CopyAppWorkflowObjectIds.list_stamp_topLeft_value),
        "topCenter": (CopyAppWorkflowObjectIds.list_stamp_topCenter, CopyAppWorkflowObjectIds.list_stamp_topCenter_value),
        "topRight": (CopyAppWorkflowObjectIds.list_stamp_topRight, CopyAppWorkflowObjectIds.list_stamp_topRight_value),
        "bottomLeft": (CopyAppWorkflowObjectIds.list_stamp_bottomLeft, CopyAppWorkflowObjectIds.list_stamp_bottomLeft_value),
        "bottomCenter": (CopyAppWorkflowObjectIds.list_stamp_bottomCenter, CopyAppWorkflowObjectIds.list_stamp_bottomCenter_value),
        "bottomRight": (CopyAppWorkflowObjectIds.list_stamp_bottomRight, CopyAppWorkflowObjectIds.list_stamp_bottomRight_value),
    }
    
    stamp_content_checkbox_dict = {
        "ipAddress": (CopyAppWorkflowObjectIds.row_stamp_ipAddress_checkBox, CopyAppWorkflowObjectIds.stamp_ipAddress_checkBox),
        "userName": (CopyAppWorkflowObjectIds.row_stamp_userName_checkBox, CopyAppWorkflowObjectIds.stamp_userName_checkBox),
        "productInformation": (CopyAppWorkflowObjectIds.row_stamp_productInformation_checkBox, CopyAppWorkflowObjectIds.stamp_productInformation_checkBox),
        "pageNumber": (CopyAppWorkflowObjectIds.row_stamp_page_number_checkBox, CopyAppWorkflowObjectIds.stamp_page_number_checkBox),
        "dateAndTime": (CopyAppWorkflowObjectIds.row_stamp_dateAndTime_checkBox, CopyAppWorkflowObjectIds.stamp_dateAndTime_checkBox),
        "date": (CopyAppWorkflowObjectIds.row_stamp_date_checkBox, CopyAppWorkflowObjectIds.stamp_date_checkBox),
        "userDefined1": (CopyAppWorkflowObjectIds.row_stamp_user_defined_1_checkBox, CopyAppWorkflowObjectIds.stamp_user_defined_1_checkBox),
        "userDefined2": (CopyAppWorkflowObjectIds.row_stamp_user_defined_2_checkBox, CopyAppWorkflowObjectIds.stamp_user_defined_2_checkBox),
        "userDefined3": (CopyAppWorkflowObjectIds.row_stamp_user_defined_3_checkBox, CopyAppWorkflowObjectIds.stamp_user_defined_3_checkBox),
        "adminDefined1": (CopyAppWorkflowObjectIds.row_stamp_admin_defined_1_checkBox, CopyAppWorkflowObjectIds.stamp_admin_defined_1_checkBox),
        "adminDefined2": (CopyAppWorkflowObjectIds.row_stamp_admin_defined_2_checkBox, CopyAppWorkflowObjectIds.stamp_admin_defined_2_checkBox),
        "adminDefined3": (CopyAppWorkflowObjectIds.row_stamp_admin_defined_3_checkBox, CopyAppWorkflowObjectIds.stamp_admin_defined_3_checkBox)
    }
    
    stamp_content_radio_dict = {
        "ipAddress": (CopyAppWorkflowObjectIds.row_stamp_ipAddress_radioButton, CopyAppWorkflowObjectIds.stamp_ipAddress_radioButton),
        "userName": (CopyAppWorkflowObjectIds.row_stamp_userName_radioButton, CopyAppWorkflowObjectIds.stamp_userName_radioButton),
        "productInformation": (CopyAppWorkflowObjectIds.row_stamp_productInformation_radioButton, CopyAppWorkflowObjectIds.stamp_productInformation_radioButton),
        "pageNumber": (CopyAppWorkflowObjectIds.row_stamp_page_number_radioButton, CopyAppWorkflowObjectIds.stamp_page_number_radioButton),
        "dateAndTime": (CopyAppWorkflowObjectIds.row_stamp_dateAndTime_radioButton, CopyAppWorkflowObjectIds.stamp_dateAndTime_radioButton),
        "date": (CopyAppWorkflowObjectIds.row_stamp_date_radioButton, CopyAppWorkflowObjectIds.stamp_date_radioButton),
        "userDefined1": (CopyAppWorkflowObjectIds.row_stamp_user_defined_1_radioButton, CopyAppWorkflowObjectIds.stamp_user_defined_1_radioButton),
        "userDefined2": (CopyAppWorkflowObjectIds.row_stamp_user_defined_2_radioButton, CopyAppWorkflowObjectIds.stamp_user_defined_2_radioButton),
        "adminDefined1": (CopyAppWorkflowObjectIds.row_stamp_admin_defined_1_radioButton, CopyAppWorkflowObjectIds.stamp_admin_defined_1_radioButton),
        "adminDefined2": (CopyAppWorkflowObjectIds.row_stamp_admin_defined_2_radioButton, CopyAppWorkflowObjectIds.stamp_admin_defined_2_radioButton),
    }
    
    stamp_content_format_string_dict = {
        "None": [CopyAppWorkflowObjectIds.stamp_none_string_id],
        "Multiple": [CopyAppWorkflowObjectIds.stamp_multiple_string_id],
        "Required": [CopyAppWorkflowObjectIds.stamp_required_string_id],
        "IP Address": [CopyAppWorkflowObjectIds.stamp_ipAddress_string_id],
        "User Name": [CopyAppWorkflowObjectIds.stamp_userName_string_id],
        "Product Information": [CopyAppWorkflowObjectIds.stamp_productInformation_string_id],
        "Page Number": [CopyAppWorkflowObjectIds.stamp_pageNumber_string_id],
        "Date And Time": [CopyAppWorkflowObjectIds.stamp_dateAndTime_string_id],
        "Date": [CopyAppWorkflowObjectIds.stamp_date_string_id]
    }
    
    stamp_page_numbering_format_string_dict = {
        "number": [CopyAppWorkflowObjectIds.stamp_number_strig],
        "pageplusnumber": [CopyAppWorkflowObjectIds.stamp_page_plus_number_strig],
        "hyphennumber": [CopyAppWorkflowObjectIds.stamp_hyphen_number_strig]
    }
    
    stamp_text_font_format_string_dict = {
        "antique": [CopyAppWorkflowObjectIds.stamp_antique_string],
        "century": [CopyAppWorkflowObjectIds.stamp_century_string],
        "garamond": [CopyAppWorkflowObjectIds.stamp_garamond_string],
        "letter": [CopyAppWorkflowObjectIds.stamp_letter_string]
    }
    
    stamp_text_size_format_string_dict = {
        "8point": [CopyAppWorkflowObjectIds.stamp_eight_point_string],
        "12point": [CopyAppWorkflowObjectIds.stamp_twelve_point_string],
        "20point": [CopyAppWorkflowObjectIds.stamp_twenty_point_string]
    }
    
    stamp_text_color_format_string_dict = {
        "black": [CopyAppWorkflowObjectIds.stamp_black_text_color_string],
        "blue": [CopyAppWorkflowObjectIds.stamp_blue_text_color_string],
        "green": [CopyAppWorkflowObjectIds.stamp_green_text_color_string],
        "purple": [CopyAppWorkflowObjectIds.stamp_purple_text_color_string],
        "red": [CopyAppWorkflowObjectIds.stamp_red_text_color_string],
        "skyblue": [CopyAppWorkflowObjectIds.stamp_skyBlue_text_color_string],
        "yellow": [CopyAppWorkflowObjectIds.stamp_yellow_text_color_string]
    }

    def goto_menu_mainMenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
        logging.info("At Home Screen")
        # TODO - Need to check the menu app is visible or not
        # check whether the menu is visible on the screen
        if self.spice.uitype == "Workflow2" :
            # WorkFlow2 does not have menu button
            pass
        else:
            menuApp = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp)
            self.spice.wait_until(lambda: menuApp["visible"] == True)
            

    def goto_copy_from_copyapp_at_home_screen(self):
        """
        Purpose: Navigates to Copy app screen by clicking copy icon on Home screen
        Ui Flow: Any screen -> Home screen -> Copy app
        :param spice : Takes 0 arguments
        :return: None
        """
        self.goto_copyapp_at_home_screen()
        copy_home = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        self.spice.wait_until(lambda: copy_home["visible"] == True)
        logging.info("At Copy Landing Screen")

    def goto_copyapp_at_home_screen(self):
        """
        Purpose: Navigates to Copy app screen by clicking copy icon on Home screen
        Ui Flow: Any screen -> Home screen -> Copy app
        :param spice : Takes 0 arguments
        :return: None
        """
        self.spice.home.goto_home_copy()
    
    def check_cartridge_error_is_shown(self):
        """
        Purpose: Check cartridge error is shown
        :param spice: Takes 0 arguments
        :return: None
        """
        button = self.spice.query_item(CopyAppWorkflowObjectIds.button_startCopy)
        button.mouse_click()
        assert self.spice.wait_for("#cartridgeMissing1Window")
        assert self.spice.wait_for("#alertStatusImage")
        self.spice.suppliesapp.press_alert_button("#Hide")

    def goto_copy(self):  
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: None
        """
        current_button = self.get_copy_app()
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        logging.info("At Copy Landing Screen")

    def get_copy_app(self):
        """
        Purpose: Click on copy App from home screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: None
        """
        try:
            #self.goto_menu_mainMenu()
            #CopyApp = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyApp + " MouseArea")
            #CopyApp.mouse_click()
            #self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
            self.homemenu.goto_menu(self.spice)
            self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
            logging.info(f"Get Copy App button from home screen")
            self.workflow_common_operations.scroll_to_position_vertical(0, "#landingPageMenuAppListScrollBar")
            copy_app = self.spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy + " MouseArea")
            #return copy_app  
            copy_app.mouse_click()
            # changes made here because the screen is of ButtonTemplate Model. Right Now there is only few options 
            # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
            #self.workflow_common_operations.scroll_position(CopyAppWorkflowObjectIds.view_menu_copy_screen, CopyAppWorkflowObjectIds.button_menu_copy_copy , CopyAppWorkflowObjectIds.scrollBar_menucopyFolderLanding , CopyAppWorkflowObjectIds.copyFolderPage_column_name , CopyAppWorkflowObjectIds.copyFolderPage_Content_Item)
        except:
            logging.info("Copy Menu List not available")
        finally:
            return self.spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")

    def wait_for_copy_landing_view(self):
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        logging.info("Inside Copy Successful Screen")

    def wait_for_copy_landing_view_from_widget_or_one_touch_quickset(self):
        self.wait_for_copy_landing_view()

    def ui_select_copy_page(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Copy
        :return: None
        """
        currentScreen = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        time.sleep(15)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy)
        current_button.mouse_click()

    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions, timeout = 10)
        assert setting_view
        self.spice.wait_until(lambda: setting_view["enabled"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: setting_view["visible"] == True, timeout = 15.0)

        if (setting_view["enabled"] == True and setting_view["visible"] == True):
            button_middle_width  = setting_view["width"] / 2
            button_middle_height = setting_view["height"] / 2
            setting_view.mouse_click(button_middle_width, button_middle_height)
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 15.0)
        time.sleep(3)

    def goto_copy_options_list_from_preview(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions, timeout = 10)
        assert setting_view
        self.spice.wait_until(lambda: setting_view["enabled"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: setting_view["visible"] == True, timeout = 15.0)

        assert setting_view["enabled"] == True
        assert setting_view["visible"] == True
        setting_view.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(3)

    def close_option_mode(self):
        """
        Closes the menu opened by `goto_copy_options_list`
        """
        self.spice.wait_for(CopyAppWorkflowObjectIds.close_copy_settings_button) \
                        .mouse_click()

    def goto_edge_to_edge_settings(self):
        """
        UI should be on Copy options list screen.
        UI Flow is Edge To Edge-> (Edge To Edge settings screen).
        """
        self.workflow_common_operations.goto_item([CopyAppWorkflowObjectIds.settings_edgeToEdge_option, CopyAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output],
                                                  CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)

    def verify_edge_to_edge_setting_constraint_applied(self):
        """
        Query edge to edge switch and check for constrained and checked property
        """

        edge_to_edge_button = self.spice.query_item(CopyAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output)
        assert edge_to_edge_button["constrained"] is True
        assert edge_to_edge_button["checked"] is True

    def goto_long_plot_settings(self):
        """
        UI should be on Copy options list screen.
        UI Flow is Long Plot-> (Long Plot settings screen).
        """
        self.workflow_common_operations.goto_item([CopyAppWorkflowObjectIds.settings_longPlot_option, CopyAppWorkflowObjectIds.toggle_button_scan_long_original_output],
                                                  CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)

    def goto_long_plot_settings_toggle(self, long_plot_state = True):
        """
        Go to long plot and toggle the switch
        Args: long_plt_state: bool True or False
        """
        self.goto_long_plot_settings()
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_scan_long_original_output)
        self.spice.wait_until(lambda: setting_view["visible"] == True, timeout = 10.0)

        actual_state = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_scan_long_original_output)["checked"]
        if long_plot_state != actual_state:
            long_plot_button = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_scan_long_original_output + " MouseArea")
            long_plot_button.mouse_click()
            if long_plot_state:
            #When try to enable the long plot, there will be a confirm screen pop up. 
            #If try to disable, there will be not the confirm screen.
                assert self.spice.wait_for(CopyAppWorkflowObjectIds.long_plot_confirmation_screen)
                okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.long_plot_confirmation_screen_ok_button)
                okButton.mouse_click()
            time.sleep(3)
        else:
            logging.info(f"Current long original state is {long_plot_state}")

    def goto_auto_straighten_settings(self):
        """
        UI should be on Copy options list screen.
        UI Flow is Auto Straighten-> (Automatic Straighten Setting).
        """
        self.workflow_common_operations.goto_item([CopyAppWorkflowObjectIds.settings_scan_auto_straighten, CopyAppWorkflowObjectIds.toggle_button_scan_auto_straighten],
                                                  CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)

    def wait_for_copy_status_toast(self, net, configuration, message: str = "Complete", timeout= 60, wait_for_toast_dismiss=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, Starting... -> Scanning... -> Copying... -> Copy complete
        """
        copy_toast_message=""
        toast_status=""
        if message == "Starting":
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
        elif message == 'Scanning':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
        elif message == 'Copying':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopying')
        elif message == 'Complete':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyComplete')
        elif message == 'Cancel':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyCanceledMessage')
        elif message == 'Canceling':
            copy_toast_message= self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cJobStateTypeCanceling')
        elif message == 'SomeSettingsChangedBetweenPages':
            copy_toast_message= self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cNewSettingsScan')
        elif message == 'preparingToCopy':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cProgressJobQueue')
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                self.spice.wait_for(CopyAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=15)
                toast_status = self.spice.query_item(CopyAppWorkflowObjectIds.text_toastInfoText)["text"]
                logging.info("Current Toast message is : %s" % toast_status)
            except:
                logging.info("Still finding corresponding status.")
            if copy_toast_message in toast_status:
                break
        if copy_toast_message not in toast_status:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)

        if wait_for_toast_dismiss:
                start_time = time.time()
                toast_status = ""
                while time.time()-start_time < timeout:
                    try:
                        toast_status = self.spice.wait_for(CopyAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=2)["text"]
                        logging.info(f"Still corresponding status <{toast_status}> dispay in screen")
                    except Exception as err:
                        logging.info("Toast screen already dismiss")
                        break
        
    def wait_for_copy_status_toast_is_not_visible(self, timeout = 5):
        """
        Purpose: Wait for the toast to disappear
        Args: timeout: int
        """
        
        toast_status = ""
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                toast_status = self.spice.query_item(CopyAppWorkflowObjectIds.text_toastInfoText)["text"]
                logging.info("Current Toast message is : %s" % toast_status)
                
                if toast_status == "":
                    logging.info("Toast dissapeared")
                    break
            except:
                logging.info("Still finding corresponding status.")

    def check_job_toast_or_modal_not_appear(self, net, configuration, message: str = "Complete", timeout= 10):
        """
        Purpose: Wait for the given toast not appears
        Args: message: str, Starting... -> Scanning... -> Copying... -> Copy complete
        """
        try:
            self.wait_for_copy_job_status_toast_or_modal(net, configuration, message, timeout) 
            logging.info("Toast appeared when it shouldn't.")
            raise NameError("Toast appeared when it shouldn't.")
        except TimeoutError:
            logging.info("Toast not found.")

    def wait_for_copy_job_status_modal(self,net ,configuration, message: str = "Complete", timeout= 60, locale: str = "en"):
        """
         Purpose: Wait for the given activejobmodal to appear in non concurrent products
        """
        active_job_modal_message = ""
        modal_status = ""
        modalType = "progressModal"
        header_modal_status = ""
        active_job_modal_header = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopy')
        header_loactor = CopyAppWorkflowObjectIds.copy_active_job_modal_header_text_locator
        locator = CopyAppWorkflowObjectIds.copy_active_job_modal_text_locator
        if message == 'Starting':
            active_job_modal_message = str(LocalizationHelper.get_string_translation(net, ["cStringEllipsis", str(LocalizationHelper.get_string_translation(net, "cStarting", locale))], locale))
        elif message == 'Scanning':
            active_job_modal_message = str(LocalizationHelper.get_string_translation(net, ["cStringEllipsis", str(LocalizationHelper.get_string_translation(net, "cScanning", locale))], locale))
        elif message == 'Copying':
            active_job_modal_message = str(LocalizationHelper.get_string_translation(net, ["cStringEllipsis", str(LocalizationHelper.get_string_translation(net, "cCopying", locale))], locale))
        elif message == 'Cancel':
            active_job_modal_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyCanceledMessage')
            modalType  = "completionModal"
        elif message == 'Canceling':
            active_job_modal_message = str(LocalizationHelper.get_string_translation(net, ["cStringEllipsis", str(LocalizationHelper.get_string_translation(net, "cJobStateTypeCanceling", locale))], locale))
        elif message == 'Complete':
            modalType  = "completionModal"
            if configuration.productname in ["moreto","moretohi", "victoria", "victoriaplus","beam/beammfp_power","kebin","eddington","elion"]:
                active_job_modal_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyCompleteMessage')
            else:
                active_job_modal_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyingCompleteMessage') + '!'
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                modal_status = self.spice.wait_for(locator , timeout=15.0)["text"] 
                header_modal_status = self.spice.query_item(header_loactor)["text"]
                logging.info("Current Modal message is : %s" % modal_status)
            except:
                logging.info("Still finding corresponding status.")
            if active_job_modal_message == modal_status and active_job_modal_header == header_modal_status:
                if modalType  == "completionModal":
                    button = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_wizard_completion_active_job_modal_ok_button)
                    button.mouse_click()
                break
        if active_job_modal_message != modal_status:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    def wait_for_copy_job_status_toast_or_modal(self, net, configuration, message: str = "Complete", timeout= 60):
        if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power","moreto","moretohi","kebin","eddington","elion", "victoria", "victoriaplus"]:
            self.wait_for_copy_job_status_modal( net, configuration, message, timeout, )
        else:
            self.wait_for_copy_status_toast(net, configuration, message, timeout)
    def goto_sides_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView), "Error: Not in Copy Settings View"
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_sides, CopyAppWorkflowObjectIds.combo_copySettings_sides]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list)

    def goto_scan_mode_option(self):
        '''
        UI should be in Option screen.
        Navigates to scan mode screen starting from Option screen.
        UI Flow is CopyOptions->scan mode options
        '''
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.scan_mode_settings_option,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = True)
        scan_mode_settings_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_scan_mode_settings_view)
        self.spice.wait_until(lambda: scan_mode_settings_view["visible"] == True, timeout = 10.0)
        logging.info("At scan mode screen")

    def goto_quality_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_quality, CopyAppWorkflowObjectIds.combo_copySettings_quality]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_quality)

    def goto_color_option(self):
        """
        Go to color option menu
        @return:
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_color, CopyAppWorkflowObjectIds.combo_copySettings_color]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_color)
        
    def check_familyname(self, udw, familyname=""):
        
        if familyname == "":
            try:
                self.cdm = CDM(udw.get_target_ip(), timeout=5.0)
                self.configuration = Configuration(self.cdm)
                familyname = self.configuration.familyname
            except:
                logging.info("There is no information about the device.")
        return familyname
    
    def goto_copy_pages_per_sheet(self, udw, familyname=""):
        """
        Go to pages per sheet option menu
        @return:
        """
        familyname = self.check_familyname(udw)

        if familyname == "enterprise":
            logging.info("Go to pages per sheet option menu")
            self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_pagesPerSheet, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet)
        else:
            logging.info("Go to pages per sheet option menu")
            menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_pagesPerSheet, CopyAppWorkflowObjectIds.combo_copySettings_pagesPerSheet]
            self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_pagesPerSheet)
        time.sleep(3)

    def validate_pages_persheet_constraint_message(self, udw, net, familyname=""):
        # Go to pages per sheet option menu
        self.goto_copy_pages_per_sheet(udw)

        # Click on PagesPerSheet Two option
        pages_per_sheet2_option = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2 +" "+ CopyAppWorkflowObjectIds.text_view)
        pages_per_sheet2_option.mouse_click()

        # Validate the string id for constraint messgae
        self.validate_string_id_in_current_view(CopyAppWorkflowObjectIds.view_constraint_message, 'cFeatureCurrentNotAvailable', net)

        # Click on OK Button to dismiss the modal
        okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        # Click on PagesPerSheet One option
        pages_per_sheet1_option = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1 +" "+ CopyAppWorkflowObjectIds.text_view, timeout=30)
        pages_per_sheet1_option.mouse_click()
        
    def validate_string_id_in_current_view(self, object_name, expected_string, net):
        # Verify the message string id in view
        actual_result = self.spice.wait_for(object_name)["message"]
        expected_result = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, expected_string)
        assert actual_result == expected_result, "String mismatch"

    def select_pages_per_sheet_option(self, udw, option):
        #pagesPerSheet
        familyname = self.check_familyname(udw)
        self.goto_copy_pages_per_sheet(udw, familyname)

        if option == "1":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1 + " SpiceText")
            current_button.mouse_click()
        elif option == "2":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2 + " SpiceText")
            current_button.mouse_click()
        elif option == "4_rightThenDown":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_4_rightThenDown + " SpiceText")
            current_button.mouse_click()
        elif option == "4_downThenRight":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_4_downThenRight + " SpiceText")
            current_button.mouse_click()
        time.sleep(2)

        if familyname == "enterprise":
            back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet +" "+ CopyAppWorkflowObjectIds.button_back)
            back_button.mouse_click()

        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def verify_copy_pages_per_sheet_constrained(self, udw, net, familyname="", constrained_message : str = ""):
        """
        Go to pages per sheet option menu and verify that option is cosntrained
        @return:
        """
        familyname = self.check_familyname(udw, familyname)
        
        if familyname == "enterprise":
            logging.info("Go to pages per sheet option menu")
            self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_pagesPerSheet, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

        else:
            self.goto_copy_pages_per_sheet(udw)
            logging.info("Go to pages per sheet option menu")
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2 + " SpiceText[visible=true]")
            current_button.mouse_click()
            
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)
        
        self.verify_constrained_message(net, constrained_message)

        okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(3)
        
        if familyname != "enterprise":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1 + " SpiceText[visible=true]")
            current_button.mouse_click()

    def verify_copy_add_page_borders_constrained(self, udw, constrained: bool = True):
        """
        Go to pages per sheet option menu and verify that option is cosntrained
        @return:
        """
        self.goto_copy_pages_per_sheet(udw)
        # self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet, CopyAppWorkflowObjectIds.check_addPageBorders_option, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_pagesPerSheet_options_scrollbar, select_option=False)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet, menu_item_id=CopyAppWorkflowObjectIds.check_addPageBorders_option, top_item_id=CopyAppWorkflowObjectIds.check_addPageBorders_option,select_option = True)
        add_page_borders_button = self.spice.wait_for(CopyAppWorkflowObjectIds.row_addPageBorders_option)
        if constrained == False:
            assert add_page_borders_button["constrained"] == False
        else:
            assert add_page_borders_button["constrained"] == True
            assert add_page_borders_button["checked"] == False
            logging.info("Go to output scale option menu")
            add_page_borders_button = self.spice.wait_for(CopyAppWorkflowObjectIds.row_addPageBorders_option + " SpiceText")
            add_page_borders_button.mouse_click()
            time.sleep(3)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
            time.sleep(3)

        back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet +" "+ CopyAppWorkflowObjectIds.button_back)
        back_button.mouse_click()

    def select_add_page_borders_option(self, udw):
        """
        Go to pages per sheet option menu and verify that option is cosntrained
        @return:
        """
        self.goto_copy_pages_per_sheet(udw)
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet, CopyAppWorkflowObjectIds.check_addPageBorders_option, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_pagesPerSheet_options_scrollbar, select_option=False)
        add_page_borders_button = self.spice.wait_for(CopyAppWorkflowObjectIds.row_addPageBorders_option)    
        if add_page_borders_button["checked"] is False:
            add_page_borders_button.mouse_click()
            assert add_page_borders_button["checked"] is True
        else:
            add_page_borders_button.mouse_click()
            assert add_page_borders_button["checked"] is False

        back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.list_view_copySettings_pagesPerSheet +" "+ CopyAppWorkflowObjectIds.button_back)
        back_button.mouse_click()

    def verify_copy_collate_constrained(self):
        """
        Go to collate option menu and verify that option is cosntrained
        @return:
        """
        logging.info("Go to collate option menu")
        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_collate, CopyAppWorkflowObjectIds.toggle_copySettings_collate ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False)
        
        collate_constraints = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_copySettings_collate)["constrained"]
        collate_toggle_btn = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_copySettings_collate + " MouseArea")
        if collate_constraints == True:
            collate_toggle_btn.mouse_click()
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)
            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(3)

    def goto_copy_option_output_scale(self):
        """
        Go to output scale option menu
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        logging.info("Go to output scale option menu")
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_outputScale)

    def verify_copy_option_output_scale_constrained(self, configuration = None):
        """
        Go to output scale option menu and verify output scale is constrained
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        time.sleep(2)
        logging.info("Go to output scale option menu")
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)

        if configuration is not None and configuration.familyname == "enterprise":
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_outputScale)
            menu_item_id = [CopyAppWorkflowObjectIds.row_copySettings_outputScale_custom,CopyAppWorkflowObjectIds.radio_copySettings_outputScale_custom]
            self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_resize_scrollbar, select_option = True)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)
            
            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
            
            time.sleep(2)
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_outputScale_back_button) \
                        .mouse_click()
        

        else:
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)
            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
        
        
    
    def verify_copy_option_output_scale_fit_to_page_include_margin(self, value=True):
        """
        Go to output scale option menu and verify output scale is constrained
        @return:
        """
        logging.info("Go to output scale option menu")
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        
        time.sleep(5)
        
        logging.info("Check CheckBoxOptionsfitToPageIncludeMargin true or false")
        fitToPageIncludeMargin = self.spice.wait_for("#fitToPageIncludeMargin")["checked"]

        assert fitToPageIncludeMargin == value

    def goto_copy_output_scale_custom_menu(self, select_option = True):
        """
        Go to output scale custom option menu
        @return:
        """
        time.sleep(5)
        logging.info("Go to output scale custom option menu")
        menu_item_id = [CopyAppWorkflowObjectIds.row_copySettings_outputScale_custom,CopyAppWorkflowObjectIds.radio_copySettings_outputScale_custom]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_resize_scrollbar, select_option = select_option)

    def set_copy_custom_value_option(self, input_value=0):
        """
        set output scale custom value
        @return:
        """
        time.sleep(2)
        logging.info("set output scale custom value")
        custom_Element = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.spinbox_copySettings_outputScale_custom} {CopyAppWorkflowObjectIds.spinBox_numberOfCopies_textArea}")
        custom_Element.mouse_click()
        time.sleep(2)
        ok_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        time.sleep(2)
        custom_Element["text"] = input_value
        ok_button.mouse_click()
        time.sleep(2)

    def goto_copy_option_content_type_screen(self):
        """
        Go into option content type screen
        @return:
        """
        time.sleep(3)
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_contentType, CopyAppWorkflowObjectIds.combo_copySettings_contentType]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_contentType)
    
    def goto_copy_option_blank_page_suppression(self):
        """
        Go into option blank page suppression
        @return:
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_blankPageSuppression, CopyAppWorkflowObjectIds.combo_copySettings_blankPageSuppression]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_blankPageSuppression)

    def goto_copy_option_copy_margins_screen(self):
            """
            Go into option copy margins screen
            @return:
            """
            logging.info("Go to copy margins menu")
            self.workflow_common_operations.goto_item([CopyAppWorkflowObjectIds.row_combo_copySettings_copyMargins, CopyAppWorkflowObjectIds.combo_copySettings_copyMargins],
                                                             CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_copyMargins,timeout=9.0)

    def goto_copy_option_folding_style_list(self):
            """
            Go into option copy folding style list
            @return:
            """
            logging.info("Go to copy folding style list")
            self.workflow_common_operations.goto_item([CopyAppWorkflowObjectIds.copy_settings_folding_style, CopyAppWorkflowObjectIds.copy_settings_folding_style_combobox],
                                                             CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_folding_style_combobox_list,timeout=9.0)


    def goto_copy_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        time.sleep(3)
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        logging.info("Go to color option menu")
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_color, CopyAppWorkflowObjectIds.combo_copySettings_color]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_color)

    def goto_copy_landing_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        logging.info("Go to color option menu")
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout =9.0)
        self.workflow_common_operations.scroll_to_position_vertical(.2, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
        time.sleep(2)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_color)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_color)

    def goto_quality_option(self):
        """
        Go into quality option screen
        @return:
        """
        logging.info("Go into quality option screen")
        option_screen = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        self.spice.wait_until(lambda: option_screen["visible"] is True, 20)
        time.sleep(2)
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_quality, CopyAppWorkflowObjectIds.combo_copySettings_quality]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_quality)

    def goto_copy_option_original_size_screen(self):
        """
        Go to original size screen
        :return:
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.list_copySettings_originalSize,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = True)
        time.sleep(5)
        original_size_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_originalSize)
        self.spice.wait_until(lambda: original_size_view["visible"] == True, timeout = 10.0)
        logging.info("at original size list screen")

    def go_to_paper_selection(self):
        #PaperSelection
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        logging.info("Go to paper Selection option menu")
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_paperSelection, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection)
        time.sleep(7)

    def check_paper_selection(self, net, locale, expected_string_selected_first = "", expected_string_selected_second = ""):
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_paperSelection,  scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        self.spice.wait_for(CopyAppWorkflowObjectIds.list_copySettings_paperSelection + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cPaperSelectTitle", locale))

        if expected_string_selected_first != "":
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_paperSetting_first_option + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, expected_string_selected_first, locale))
        if expected_string_selected_second != "":
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_paperSetting + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, expected_string_selected_second, locale))
        
    def goto_copy_paper_size_screen(self):
        """
        Go to media size screen
        :return:
        """
        screen_id = CopyAppWorkflowObjectIds.view_copySettings_paperSelection
        menu_item_id = CopyAppWorkflowObjectIds.view_copySettings_paperSize
        current_button = self.spice.query_item(screen_id + " " + menu_item_id)
        current_button.mouse_click()
        time.sleep(10)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize)

    def goto_copy_paper_type_screen(self):
        """
        Go to paper type screen
        :return:
        """
        screen_id = CopyAppWorkflowObjectIds.view_copySettings_paperSelection
        menu_item_id = CopyAppWorkflowObjectIds.list_copySettings_paperType
        current_button = self.spice.query_item(screen_id + " " + menu_item_id)
        current_button.mouse_click()
        time.sleep(10)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperType)

    def goto_copy_paper_tray_screen(self):
        """
        Go to paper tray screen
        :return:
        """
        # Paper Tray
        self.spice.wait_for(CopyAppWorkflowObjectIds.row_combo_copySettings_paperTray)
        screen_id = CopyAppWorkflowObjectIds.view_copySettings_paperSelection
        menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_paperTray, CopyAppWorkflowObjectIds.combo_copySettings_paperTray]
        current_button = self.spice.query_item(screen_id + " " + menu_item_id[0] + " " + menu_item_id[1])
        middle_width = current_button["width"] / 2
        middle_height = current_button["height"] / 2
        current_button.mouse_click(middle_width, middle_height)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperTray)
        
    def goto_contrast_option(self):
        """
        go to contrast option
        """
        logging.info("Go to contrast option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_slider_contrast, CopyAppWorkflowObjectIds.slider_contrast]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)

    def goto_sharpness_option(self):
        """
        go to contrast option
        """
        logging.info("Go to contrast option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_slider_sharpness, CopyAppWorkflowObjectIds.slider_sharpness]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)    
    
    def goto_background_cleanup_option(self):
        """
        go to background cleanup option
        """
        logging.info("Go to background cleanup option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_slider_backGroundCleanup, CopyAppWorkflowObjectIds.slider_backGroundCleanup]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        
    def set_background_cleanup_setting_value(self, value: int):
        """
        UI should be on Copy settings view.
        Args:
            value: The background cleanup value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView), "Error: Not in Copy All Options view"
        self.goto_background_cleanup_option()
        current_slider_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_backGroundCleanup)
        logging.info("Current background cleanup value is: %s" % current_slider_value["value"])

        background_cleanup_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_backGroundCleanup)
        background_cleanup_slider.__setitem__('value', value)

        current_slider_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_backGroundCleanup)["value"]
        logging.info("After setting background cleanup value is: %s" % current_slider_value)

    def verify_background_cleanup_setting_value(self, value):
        """
        verify the background cleanup setting value
        Args:
            value: The background cleanup value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView), "Error: Not in Copy All Options view"
        self.goto_background_cleanup_option()
        current_slider_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_backGroundCleanup)
        logging.info("Current background cleanup value is: %s" % current_slider_value["value"])
        assert current_slider_value["value"] == int(value), f"Background cleanup value mismatch {value} != {current_slider_value['value']}"

    def goto_lighter_darker_option(self):
        """
        go to lighter darker option
        """
        logging.info("Go to lighter darker option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_slider_lighterDarker, CopyAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)

    def verify_copy_image_adjustment_options_constrained(self, activated_option = "none"):
        """
        Verify image adjustment options are constrained
        """
        # Define constraints mapping
        option_constraints = {
            "none": (False, False, False, "Auto Tone and Auto Paper Color Removal are Off"),
            "auto_tone": (True, True, True, "Auto Tone is On and Auto Paper Color Removal is Off"),
            "auto_paper_color_removal": (False, False, True, "Auto Tone is Off and Auto Paper Color Removal is On"),
            "both": (True, True, True, "Auto Tone is On and Auto Paper Color Removal are On")
        }

        # Fetch constraints based on the activated option
        constraints = option_constraints.get(activated_option, option_constraints["none"])
        lighter_darker_constraint, contrast_constraint, background_cleanup_removal_constraint, log_message = constraints

        # Log the constraint information
        logging.info(log_message)

        # Verify Lighter/Darker constraint
        self.goto_lighter_darker_option()
        lighter_darker_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_lighterDarker)
        assert lighter_darker_slider["constrained"] == lighter_darker_constraint, "Lighter Darker options should" + (" not" if not lighter_darker_constraint else "") + " be constrained."

        # Verify Contrast constraint
        self.goto_contrast_option()
        contrast_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_contrast)
        assert contrast_slider["constrained"] == contrast_constraint, "Contrast options should" + (" not" if not contrast_constraint else "") + " be constrained."

        # Verify Background Cleanup/Removal constraint
        self.goto_background_cleanup_option()
        background_cleanup_removal_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_backGroundCleanup)
        assert background_cleanup_removal_slider["constrained"] == background_cleanup_removal_constraint, "Background Color Removal options should" + (" not" if not background_cleanup_removal_constraint else "") + " be constrained."

    def goto_auto_tone_option(self):
        """
        go to the auto tone option
        """
        logging.info("Go to auto tone option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_scanSettings_autoTone, CopyAppWorkflowObjectIds.checkbox_autoTone]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
 
    def verify_copy_auto_tone_slider_constrained(self, constrained = True):
        """
        verify auto tone slider option is cosntrained
        @return:
        """
        time.sleep(3)
        auto_tone_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoTone)
        if constrained == False:
            assert auto_tone_slider["constrained"] == False
        else:
            assert auto_tone_slider["constrained"] == True
            logging.info("Click auto tone slider and verify constraint message")
            auto_tone_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoTone + " #sliderHandle")
            auto_tone_slider.mouse_click()
            time.sleep(3)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
            time.sleep(3)
       
    def goto_auto_paper_color_removal_option(self):
        """
        go to the auto paper color removal option
        """
        logging.info("Go to auto paper color removal option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, CopyAppWorkflowObjectIds.copy_options_scrollbar)
        menu_item_id = [CopyAppWorkflowObjectIds.row_scanSettings_autoPaperColorRemoval, CopyAppWorkflowObjectIds.checkbox_autoPaperColorRemoval]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)

    def verify_copy_auto_paper_color_removal_slider_constrained(self, constrained= True):
        """
        verify auto paper color removal slider option is cosntrained
        @return:
        """
        time.sleep(3)
        auto_paper_color_removal_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval)
        if constrained == False:
            assert auto_paper_color_removal_slider["constrained"] == False
        else:
            assert auto_paper_color_removal_slider["constrained"] == True
            logging.info("Click auto tone slider and verify constraint message")
            auto_paper_color_removal_slider = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval + " #sliderHandle")
            auto_paper_color_removal_slider.mouse_click()
            time.sleep(3)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

            okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
            okButton.mouse_click()
            time.sleep(3)
    
    def select_copy_side(self, side_mode:str):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to side mode screen.
        UI Flow is setting option->side mode->select side
        '''
        #self.goto_copy_options_list()
        self.goto_sides_option()
        time.sleep(2)
        to_select_item = self.sides_options_dict.get(side_mode)
        current_button = self.spice.query_item(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)
        # wait for screen load fully. 
        time.sleep(2)

    def select_scan_mode_option(self, scan_mode:str, checkBox_for_scan_mode_prompt:bool = False):
        '''
        UI should be in copy Settings view screen.
        Navigates to scanModeView screen starting from setting option to scanMode mode screen.
        UI Flow is setting option->scan mode->select scan mode
        '''
        self.goto_scan_mode_option()

        scan_mode_option = self.scan_mode_options_dict.get(scan_mode)
        self.workflow_common_operations.goto_item(menu_item_id=scan_mode_option, screen_id=CopyAppWorkflowObjectIds.view_scan_mode_settings_view, select_option=True, scrolling_value=1,scrollbar_objectname=CopyAppWorkflowObjectIds.scan_mode_settings_scrollbar)
        self.workflow_common_operations.scroll_to_position_vertical(1, CopyAppWorkflowObjectIds.scan_mode_settings_scrollbar)
        if scan_mode == "standard":
            check_box_additional_pages_button = self.spice.wait_for(CopyAppWorkflowObjectIds.scan_mode_option_prompt_for_additonal_pages_checkbox)
            if(checkBox_for_scan_mode_prompt != check_box_additional_pages_button["checked"]):
                check_box_additional_pages_button.mouse_click()
        elif scan_mode == "idCard":
            check_box_scan_both_sides_button = self.spice.wait_for(CopyAppWorkflowObjectIds.scan_mode_option_prompt_for_scan_both_sided)
            if(checkBox_for_scan_mode_prompt != check_box_scan_both_sides_button["checked"]):
                check_box_scan_both_sides_button.mouse_click()
        button = self.spice.query_item(CopyAppWorkflowObjectIds.scan_mode_done_button)
        button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def validate_add_page_media_sizes(self, cdm):
        """
        UI should be in AddPage prompt screen.
        Validate the media sizes in AddPage prompt
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_add_page_prompt_view)
        logging.info("At AddPage prompt with original media sizes screen")

        scroll_bar_step_value = 0
        add_page_prompt_media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)
        for media in add_page_prompt_media_sizes_list:
            scroll_bar_step_value = scroll_bar_step_value + 0.03

            media_size_id_radio_button = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.add_page_content_id} " + media)
            self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True, timeout = 10.0)
            assert media_size_id_radio_button
            media_size_id_radio_button.mouse_click()

            # scroll to next media size
            self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, CopyAppWorkflowObjectIds.add_page_prompt_scroll_bar)

    def get_add_page_media_sizes_list_from_cdm(self, cdm):
        logging.info("Get the media sizes list from CDM")
        media_sizes_object_names_list = []
        response = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)

        for data in response["validators"]:
            if data["propertyPointer"] == "src/scan/mediaSize":
                media_sizes_options_list_from_cdm = data["options"]
                break

        media_sizes_object_names_list = list(map(lambda media: "#"+media.get("seValue").replace(".","_dot_").replace('-','_dash_'), media_sizes_options_list_from_cdm))

        if len(media_sizes_object_names_list) == 0:
            logging.error("Media sizes list is empty")
        else:
            return media_sizes_object_names_list
    
    def validate_add_page_prompt_media_size_list_content(self, cdm):
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_add_page_prompt_view, timeout = 15)
        logging.info("At AddPage prompt with original media sizes screen")

        # In SSQ it takes time to load adding wait
        time.sleep(5)

        media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)
        
        first_media_size_id_add_page_prompt = self.spice.wait_for(media_sizes_list[0])
        assert first_media_size_id_add_page_prompt["visible"] == True

        second_media_size_id_add_page_prompt = self.spice.wait_for(media_sizes_list[1])
        assert second_media_size_id_add_page_prompt["visible"] == True
    
    def select_media_size_in_add_page_prompt(self, media_size_id: str):
        """
        UI should be in AddPage prompt screen.
        Select the media size in AddPage prompt
        Args:
            media_size_id: The media size id to select from AddPage prompt
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_add_page_prompt_view, timeout = 15)
        logging.info("At AddPage prompt with original media sizes screen")

        media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_na_letter_8_5x11in

        if media_size_id == "A4":
            media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_iso_a4_210x297mm
        elif media_size_id == "A5":
            media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_iso_a5_148x210mm
        elif media_size_id == "B5":
            media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_jis_b5_182x257mm
        elif media_size_id == "Letter":
            media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_na_letter_8_5x11in
        elif media_size_id == "Legal":
            media_size_object_id = CopyAppWorkflowObjectIds.radio_paperSize_na_legal_8_5x14in

        media_size_id_radio_button = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.add_page_content_id} " + media_size_object_id)
        self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True)
        assert media_size_id_radio_button
        media_size_id_radio_button.mouse_click()

    def scroll_to_copy_option_original_size_item(self):
        """
        scroll to original size item
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.list_copySettings_originalSize,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option=False)
        time.sleep(5)
    
    def check_copy_side_not_visible(self, side_mode:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        check is option available or not
        UI Flow is Landing->option->side mode
        '''
        self.goto_sides_option()
        time.sleep(2)
        to_select_item = self.sides_options_dict.get(side_mode)

        current_button = self.spice.query_item(to_select_item)
        assert current_button["visible"] == False
        # Select 1-1sided option
        select_side_option = self.spice.query_item(CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided)
        select_side_option.mouse_click()
    
    def check_copy_side_constrained(self, net, side_mode:str, constrained_message: str = ""):
        self.goto_sides_option()
        time.sleep(2)
        to_select_item = self.sides_options_dict.get(side_mode)
        to_select_item = to_select_item + "RadioButtonModel"
        current_button = self.spice.query_item(to_select_item)
        assert current_button["constrained"] == True

        current_button.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.constraint_string_msg)
        self.verify_constrained_message(net, constrained_message)
        okButton = self.spice.wait_for("#okButton")
        okButton.mouse_click()
        self.workflow_common_operations.back_or_close_button_press(f"{CopyAppWorkflowObjectIds.view_copySettings_sides_popup} {CopyAppWorkflowObjectIds.button_back}", CopyAppWorkflowObjectIds.view_copySettingsView)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)
        
    def set_copy_settings_auto_tone(self, auto_tone = True, auto_tone_level = None):
        '''
        UI should be on auto tone checkbox in copy settings screen.
        Args:
            auto_tone: The auto_tone value to set - On / Off
        '''
        auto_tone_switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoTone)
        if auto_tone is True:
            if auto_tone_switch_button["checked"] is False:
                auto_tone_switch_button.mouse_click()
                assert auto_tone_switch_button["checked"] is True
            if auto_tone_level is not None:
                self.set_copy_settings_auto_tone_level(auto_tone_level)
                
        else:
            if auto_tone_switch_button["checked"] is True:
                auto_tone_switch_button.mouse_click()
                assert auto_tone_switch_button["checked"] is False
        
        logging.info("auto tone value changed to %s" % auto_tone_switch_button)
    
    def set_copy_settings_auto_tone_level(self, auto_tone_level):
        '''
        UI should be on auto tone slider in copy settings screen.
        Args:
            auto_tone: The auto tone level value to set - ( Range is 1 to 5)
        '''
        auto_tone_switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoTone)
        assert auto_tone_switch_button["checked"] is True, "To set the auto tone level, the Auto tone checkbox must be on."
                
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoTone)["value"]
        logging.info("Current auto tone level value is %s" % current_value)
        current_element = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoTone)
        current_element.__setitem__('value', auto_tone_level)
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoTone)["value"]
        
        logging.info("auto tone level value changed to %s" % current_value)
        
    def set_copy_settings_auto_paper_color_removal(self, auto_paper_color_removal = True, auto_paper_color_removal_level = None):
        '''
        UI should be on auto paper color removal checkbox in Scan settings screen.
        Args:
            auto_paper_color_removal: The auto paper color removal value to set - On / Off
        '''
            
        auto_paper_color_removal_switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoPaperColorRemoval)
        if auto_paper_color_removal is True:
            if auto_paper_color_removal_switch_button["checked"] is False:
                auto_paper_color_removal_switch_button.mouse_click()
                assert auto_paper_color_removal_switch_button["checked"] is True
            if auto_paper_color_removal_level is not None:
                self.set_copy_settings_auto_paper_color_removal_level(auto_paper_color_removal_level)
                
        else:
            if auto_paper_color_removal_switch_button["checked"] is True:
                auto_paper_color_removal_switch_button.mouse_click()
                assert auto_paper_color_removal_switch_button["checked"] is False
        
        logging.info("auto paper color removal value changed to %s" % auto_paper_color_removal_switch_button)

    def set_copy_settings_auto_paper_color_removal_level(self, auto_paper_color_removal_level):
        '''
        UI should be on auto paper color removal slider in copy settings screen.
        Args:
            auto_paper_color_removal_level: The auto paper color removal level value to set - ( Range is 1 to 5)
        '''
        auto_paper_color_removal_switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoPaperColorRemoval)
        assert auto_paper_color_removal_switch_button["checked"] is True, "To set the auto paper color level, the Auto paper color checkbox must be on."
                
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval)["value"]
        logging.info("Current auto paper color removal_level value is %s" % current_value)
        current_element = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval)
        current_element.__setitem__('value', auto_paper_color_removal_level)
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval)["value"]
        
        logging.info("auto paper color removal level value changed to %s" % current_value)
    
    def select_copy_quality(self, quality:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_quality_option()
        time.sleep(3)
        if quality == "Standard":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_standard)
        elif quality == "Draft":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_draft)
        elif quality == "Best":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_best)
        else:
            raise Exception(f"Invalid quality type <{quality}>")
        
        self.spice.wait_until(lambda: current_button["visible"] is True, 20)
        time.sleep(2)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)
        # current_button.mouse_click()
        # assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_content_type(self, option):
        #contentType
        self.goto_copy_option_content_type_screen()
        time.sleep(3)
        content_options_dict = {
            "Mixed": f"{CopyAppWorkflowObjectIds.combo_contentType_option_mixed}",
            "Photograph": f"{CopyAppWorkflowObjectIds.combo_contentType_option_photograph}",
            "Text": f"{CopyAppWorkflowObjectIds.combo_contentType_option_text}",
            "Lines": f"{CopyAppWorkflowObjectIds.combo_contentType_option_linedraw}",
            "Image": f"{CopyAppWorkflowObjectIds.combo_contentType_option_image}",
        }
        to_select_item = content_options_dict.get(option)
        time.sleep(2)
        self.workflow_common_operations.goto_item(to_select_item, CopyAppWorkflowObjectIds.view_copySettings_contentType, 
            scrollbar_objectname = CopyAppWorkflowObjectIds.standard_sizes_scrollbar, select_option=False)
        current_button = self.spice.query_item(to_select_item + "")
        current_button.mouse_click()
        time.sleep(2)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)
    
    def select_blank_page_suppression(self, option = "on"):
        self.goto_copy_option_blank_page_suppression()
        time.sleep(3)
        if option == "on":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_option_blankPageSuppression_on)
        elif option == "off":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_option_blankPageSuppression_off)
        else:
            raise Exception(f"Invalid color type <{option}>")
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_copy_margins(self, option):
        #printMargins
        time.sleep(10)
        self.goto_copy_option_copy_margins_screen()
        time.sleep(3)
        if option == "Clip from Contents":
                current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copyMargins_option_clipContents)
        if option == "Add to Contents":
                current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copyMargins_option_addToContents)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_output_scale(self, size: str, net):
        """
        Set the output scale of the copy. The UI has to be on the copy priperties UI before calling this.
        :param size: Standard output scale. For example: `a4`, `arch_b`, `letter`...
        :param net:
        """
        # open the resize menu
        self.goto_copy_option_output_scale()

        # select output scale
        self.set_output_scale_options(net, output_scale_options='standard_sizes', detail_option=size)

        # go back to the copy properties UI
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_outputScale_back_button) \
                        .mouse_click()

    def select_copy_paper_category(self, option_button):
        """
        Go to paper category option menu and select the option_button object name passed as parameter.
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.copy_settings_paper_selection_family, CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_combobox],
             CopyAppWorkflowObjectIds.view_copySettings_paperSelection,
             scrollbar_objectname = CopyAppWorkflowObjectIds.view_copySettings_paperSelection_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_list_combobox, timeout = 9.0)

        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_list_combobox, option_button, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_PaperCategory)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)

    def select_copy_paper_source(self, option_button):
        """
        Go to paper source menu and verify option_button is constrained
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.copy_settings_paper_selection_source, CopyAppWorkflowObjectIds.copy_settings_paper_selection_source_combobox],
             CopyAppWorkflowObjectIds.view_copySettings_paperSelection,
             scrollbar_objectname = CopyAppWorkflowObjectIds.view_copySettings_paperSelection_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_source_list_combobox, timeout = 9.0)

        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.copy_settings_paper_selection_source_list_combobox, option_button, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_PaperSource)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)

    def verify_copy_paper_category_constrained(self, option_button):
        """
        Go to paper category menu and verify option_button is constrained
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.copy_settings_paper_selection_family, CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_combobox],
             CopyAppWorkflowObjectIds.view_copySettings_paperSelection,
             scrollbar_objectname = CopyAppWorkflowObjectIds.view_copySettings_paperSelection_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_list_combobox, timeout = 9.0)

        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.copy_settings_paper_selection_family_list_combobox, option_button, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_PaperCategory)
        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)

    def verify_copy_paper_source_combobox_constrained(self):
        """
        Go to paper source menu and verify option_button is constrained
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.copy_settings_paper_selection_source, CopyAppWorkflowObjectIds.copy_settings_paper_selection_source_combobox],
             CopyAppWorkflowObjectIds.view_copySettings_paperSelection,
             scrollbar_objectname = CopyAppWorkflowObjectIds.view_copySettings_paperSelection_scrollbar)
        
        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)

    def check_copy_rotation(self, net, locale, expected_string_selected = ""):
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.copy_settings_rotation,  scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cRotate", locale))

        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_combobox + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, expected_string_selected, locale))

    def select_copy_rotation(self, option_button):
        """
        Go to rotation option menu and select the option_button object name passed as parameter.
        """
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.copy_settings_rotation, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
            
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_combobox).mouse_click()    
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_list_combobox, timeout = 9.0)

        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.copy_settings_rotation_list_combobox, option_button, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_PaperCategory)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def verify_copy_rotation_constrained(self, option_button):
        """
        Go to rotation menu and verify option_button is constrained
        """
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.copy_settings_rotation, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
            
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_combobox).mouse_click()    
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_list_combobox, timeout = 9.0)

        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.copy_settings_rotation_list_combobox, option_button, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_PaperCategory)
        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def verify_copy_rotation_combobox_constrained(self):
        """
        Go to rotation menu and verify the combobox is constrained
        """
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.copy_settings_rotation, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_rotation_combobox).mouse_click()    

        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_folding_style(self, expected_folding_style_selected):
        """
        Go to folding style list and select a combobox option 
        """
        self.goto_copy_option_folding_style_list()
        
        if expected_folding_style_selected == "FoldingStyle1":
                current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_option_folding_style_256)
        if expected_folding_style_selected == "FoldingStyle2":
                current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_option_folding_style_259)
        
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def verify_folding_style_combobox_constrained(self):
        """
        Go to folding style menu and verify the combobox is constrained
        """
        self.homemenu.menu_navigation(self.spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.copy_settings_folding_style, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option = False)
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_folding_style_combobox).mouse_click()    

        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_copy_printing_order(self, option_button):
        """
        Go to printing order option menu and select the option_button object name passed as parameter.
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.row_combo_copySettings_copyPrintingOrder, CopyAppWorkflowObjectIds.combo_copySettings_copyPrintingOrder],
             CopyAppWorkflowObjectIds.view_copySettingsView,
             scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_copyPrintingOrder, timeout = 9.0)

        current_button = self.spice.query_item(option_button)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def verify_copy_printing_order_constrained(self):
        """
        Go to printing order option menu and verify it is constrained
        """
        self.workflow_common_operations.goto_item(
            [CopyAppWorkflowObjectIds.row_combo_copySettings_copyPrintingOrder, CopyAppWorkflowObjectIds.combo_copySettings_copyPrintingOrder],
             CopyAppWorkflowObjectIds.view_copySettingsView,
             scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_copyPrintingOrder, timeout = 9.0)

        ok_constrained_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_constrained_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_color_mode(self, option):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to color mode screen.
        UI Flow is setting option->color mode->select color
        '''
        self.goto_copy_option_color_screen()
        time.sleep(5)
        if option == "Automatic":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_automatic)
        elif option == "Color":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_color)
        elif option == "Grayscale":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_grayscale)
        elif option == "Black Only":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_blackonly)
        else:
            raise Exception(f"Invalid color type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_color_mode_landing(self, option):
        #colorMode on landing
        self.goto_copy_landing_option_color_screen()
        time.sleep(5)
        if option == "Automatic":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_automatic)
        elif option == "Color":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_color)
        elif option == "Grayscale":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_color_option_grayscale)
        else:
            raise Exception(f"Invalid color type <{option}>")
            
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout =9.0)

    def select_original_size(self, option):
        self.goto_copy_option_original_size_screen()
        time.sleep(5)
        #change originalSize
        copy_originalSize_options_dict = {
            "Any": {
                "item_id": CopyAppWorkflowObjectIds.radio_original_size_any,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_any
                },
            "A4": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_iso_a4_210x297mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_iso_a4_210x297mmn
                },
            "Letter": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_na_letter_8_5x11in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_na_letter_8_5x11in
                },
            "Legal": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_na_legal_8_5x14in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_na_legal_8_5x14in
                },
            "Letter_SEF": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_rotate_na_letter_8_5x11in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_rotate_na_letter_8_5x11in
                },
            "A4_SEF": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_rotate_iso_a4_210x297mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_rotate_iso_a4_210x297mmn
                },
            "A5_SEF": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_rotate_iso_a5_148x210mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_rotate_iso_a5_148x210mm
                },
            "B5_SEF": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_rotate_jis_b5_182x257mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_rotate_jis_b5_182x257mm
                },
            "MIXED_LETTER_LEGAL": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_letter_legal,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_letter_legal
                },
            "MIXED_LETTER_LEDGER": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_letter_ledger,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_letter_ledger
                },
            "MIXED_A4_A3": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_a4_a3,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_a4_a3
                },
            "Executive": {
                "item_id": CopyAppWorkflowObjectIds.radio_paperSize_na_executive_7_25x10_5in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_executive_7_25x10_5in
                },
            "oficio_8_5x13": {
                "item_id": CopyAppWorkflowObjectIds.radio_paperSize_na_foolscap_8_5x13in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_foolscap_8_5x13in
                },
            "5x8 in.": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_index_5x8_5x8in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_index_5x8_5x8in
                },
            "A5": {
                "item_id": CopyAppWorkflowObjectIds.radio_paperSize_iso_a5_148x210mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_iso_a5_148x210mm
                },
            "jis_b5": {
                "item_id": CopyAppWorkflowObjectIds.radio_paperSize_jis_b5_182x257mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_jis_b5_182x257mm
                },
            "B6 (JIS) (128x182 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_jis_b6_128x182mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_jis_b6_128x182mm
                },
            "16K (195x270 mm)": {
                "item_id": CopyAppWorkflowObjectIds.row_original_size_16k_195x270,
                "row_id": CopyAppWorkflowObjectIds.radio_originalSize_16k_195x270
                },
            "16K (184x260 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_16k_184x260,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_16k_184x260
                },
            "16K (197x273 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_16k_197x273,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_16k_197x273
                },
            "Double Postcard (JIS) (148x200 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_double_ostcard_jis_148x200mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_double_ostcard_jis_148x200mm
                },
            "Statement (8.5x5.5 in.)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_invoice_5_5x8_5in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_invoice_5_5x8_5in
                },
            "Oficio_8_5x13_4": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_oficio_216x340,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_oficio_216x340
                },
            "A6 (105x148 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_paperSize_iso_a6_105x148mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_iso_a6_105x148mm
                },
            "100x150mm": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_10x15,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_10x15
                },
            "Postcard (JIS) (100x148 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_postcard_jis_100x148mm,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_postcard_jis_100x148mm
                },
            "Envelope #10 (4.1x9.5 in.)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_10,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_10
                },
            "Envelope Monarch (3.9x7.5 in.)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_monarch,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_monarch
                },
            "Envelope B5 (176x250 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_b5,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_b5
                },
            "Envelope C5 (162x229 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_c5,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_c5
                },
            "Envelope DL (110x220 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_dl,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_dl
                },
            "4x6 in.": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_index_4x6_4x6in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_index_4x6_4x6in
                },
            "2L (127x178 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_2l_127x178,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_2l_127x178
                },
            "5x5 in": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_5x5in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_5x5in
                },
            "5x7 in.": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_5x7in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_5x7in
                },
            "letter_8x10in": {  #8x10in
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_8x10in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_8x10in
                },
            "Ofuku Hagaki (200x148 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_ofuku_hagaki,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_ofuku_hagaki
                },
            "L (89x127 mm)": { #L (89x127 mm)
                "item_id": CopyAppWorkflowObjectIds.row_original_size_l_89x127,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_l_89x127
                },
            "Envelope 6 3/4 (3.63x6.5 in.)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_6,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_6
                },
            "3x5 in.": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_3x5in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_3x5in
                },
            "Japanese Envelope Chou #4 (90x205 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_chou4,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_chou4
                },
            "Hagaki (100x148 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_hagaki_100x148,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_hagaki_100x148
                },
            "4x12 in": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_4x12in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_4x12in
                },
            "Envelope A2(111x146 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_envelope_a2,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_envelope_a2
                },
            "Japanese Envelope Chou #3 (120x235 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_chou3,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_chou3
                },
            "B4 (JIS) (257x364 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_b4,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_b4
                },
            "11x14 in.": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_11x14in,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_11x14in
                },
            "Tabloid (11x17 in.)": { 
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_tabloid_11x17,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_tabloid_11x17
                },
            "A3 (297x420 mm)": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_a3,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_a3
                },
            "Custom": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_custom,
                "row_id": CopyAppWorkflowObjectIds.row_original_size_custom
                }
        }

        to_select_item = copy_originalSize_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item["row_id"],
            CopyAppWorkflowObjectIds.view_copySettings_originalSize,
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_originalSize_scrollbar,
            select_option=True)
    
    def check_original_size_value(self, option, net):
        """
        Check if the selected value is expected
        """
        #In BTF constraint takes time to reload
        time.sleep(2)
        select_original_size = self.spice.wait_for(CopyAppWorkflowObjectIds.view_originalSetting+' #contentItem')
        self.spice.wait_until(lambda: select_original_size["visible"] == True, timeout = 10.0)
        logging.info("The selected original size is " + select_original_size['text'])
        expected_string = LocalizationHelper.get_string_translation(net, self.original_dict[option][0])
        assert select_original_size['text'] == expected_string
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def check_preview_configuration_selected_option(self, option):
        """
        Check if the selected value is expected
        """
        #In BTF constraint takes time to reload
        time.sleep(2)
        select_preview_configuration = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copy_preview_configuration+' #contentItem')
        self.spice.wait_until(lambda: select_preview_configuration["visible"] == True, timeout = 10.0)
        logging.info("The selected preview configuration is " + select_preview_configuration['text'])
        assert select_preview_configuration['text'] == option

    def select_quality_option(self, option):
        # quality
        self.goto_quality_option()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_quality)
        if option == "Standard":
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_quality_option_standard)
        elif option == "Draft":
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_quality_option_draft)
        elif option == "Best":
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_quality_option_best)
        else:
            raise Exception(f"Invalid quality type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_paper_tray_option(self, selected_option):
        # Paper Tray
        #self.go_to_paper_selection()
        self.goto_copy_paper_tray_screen()
        time.sleep(2)
        tray_dict = {
            "Automatic" : CopyAppWorkflowObjectIds.combo_paperTray_option_auto,
            "Manual feed" : CopyAppWorkflowObjectIds.combo_paperTray_option_manual,
            "Tray 1" : CopyAppWorkflowObjectIds.combo_paperTray_option_tray1,
            "Tray 2" : CopyAppWorkflowObjectIds.combo_paperTray_option_tray2,
            "Tray 3" : CopyAppWorkflowObjectIds.combo_paperTray_option_tray3,
            "Tray Alternate" : CopyAppWorkflowObjectIds.combo_paperTray_option_alternate,
            "Tray Main" : CopyAppWorkflowObjectIds.combo_paperTray_option_main
        }

        to_select_item = tray_dict.get(selected_option)
        self.workflow_common_operations.goto_item(to_select_item, 
            CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperTray, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_paperTray_scrollbar,
            select_option=False)        
        current_button = self.spice.wait_for(to_select_item, timeout = 9.0)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)

    def select_paper_type_option(self, option):
        # Paper Type
        #self.go_to_paper_selection()
        self.goto_copy_paper_type_screen()
        time.sleep(10)
        self.workflow_common_operations.goto_item(self.paper_type_option_dict[option][2], CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperType, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_paperType_scrollbar, select_option=False, scrolling_value=0.05)
        if (option.startswith("UserType")):
            current_button = self.spice.wait_for(self.paper_type_option_dict[option][1], timeout = 9.0)
        else:
            current_button = self.spice.wait_for(self.paper_type_option_dict[option][2], timeout = 9.0)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperType + " SpiceText[visible=true]")
    
    def verify_paper_type_visible(self, option, visible = True):
        if (option.startswith("UserType")):
            row_id = self.paper_type_option_dict[option][1]
        else:
            row_id = self.paper_type_option_dict[option][2]

        if visible == False:
            try:
                self.workflow_common_operations.goto_item(row_id, CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperType, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_paperType_scrollbar, select_option=False, scrolling_value=0.05)
                assert self.spice.wait_for(row_id, timeout=5.0) == False, f"{row_id} is visible in the Stamp content view. but it should not be."
            except:
                logging.info(f"{row_id} is not visible in the Stamp content view.")
        else:      
            self.workflow_common_operations.goto_item(row_id, CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperType, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_paperType_scrollbar, select_option=False, scrolling_value=0.05)
            stamp_content = self.spice.wait_for(row_id)
            self.spice.wait_until(lambda: stamp_content["visible"] == visible, timeout=10.0)
    
    def verify_copy_paper_source_constrained(self):
        """
        Go to paper source option menu and verify that option is cosntrained
        @return:
        """
        self.go_to_paper_selection()
        self.goto_copy_paper_tray_screen()
        logging.info("Go to paper source option menu")
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.combo_paperTray_option_tray1)["constrained"] == True, "tray-1 not constrained"
        time.sleep(1)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.combo_paperTray_option_tray2)["constrained"] == True, "tray-2 not constrained"
        time.sleep(1)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.combo_paperTray_option_tray3)["constrained"] == True, "tray-3 not constrained"
        time.sleep(1)
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_paperTray_option_auto + "")
        current_button.mouse_click() 
        self.go_back_to_setting_from_paper_selection()
        time.sleep(3)
        
    def select_media_size_option(self, option):
        # # media size
        self.go_to_paper_selection()
        self.goto_copy_paper_size_screen()
        time.sleep(10)
        copy_paper_size_options_dict = {
            "Match Original Size":CopyAppWorkflowObjectIds.row_media_size_any,
            "A2 (420x594 mm)":CopyAppWorkflowObjectIds.row_media_size_iso_a2_420x594mm,
            "A3 (297x420 mm)":CopyAppWorkflowObjectIds.row_media_size_iso_a3_297x420mm,
            "A4": CopyAppWorkflowObjectIds.row_media_size_iso_a4_210x297mm,
            "A4_SEF": CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a4_210x297mm,
            "A5": CopyAppWorkflowObjectIds.row_media_size_iso_a5_148x210mm,
            "A5_SEF": CopyAppWorkflowObjectIds.row_media_size_rotate_iso_a5_148x210mm,
            "A6 (105x148 mm)":CopyAppWorkflowObjectIds.row_media_size_iso_a6_105x148mm,
            "Letter": CopyAppWorkflowObjectIds.row_media_size_na_letter_8_5x11in,
            "Letter_SEF": CopyAppWorkflowObjectIds.row_media_size_rotate_na_letter_8_5x11in,
            "Legal": CopyAppWorkflowObjectIds.row_media_size_na_legal_8_5x14in,
            "B5_SEF": CopyAppWorkflowObjectIds.row_media_size_rotate_jis_b5_182x257mm,
            "B6 (JIS) (128x182 mm)": CopyAppWorkflowObjectIds.row_media_size_jis_b6_128x182mm,
            "Statement (8.5x5.5 in.)": CopyAppWorkflowObjectIds.row_media_size_invoice_5_5x8_5in,
            "jis_b5": CopyAppWorkflowObjectIds.row_media_size_jis_b5_182x257mm,
            "Executive": CopyAppWorkflowObjectIds.row_media_size_executive_7_25x10_5in,
            "oficio_8_5x13": CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13in,
            "Oficio_8_5x13_4": CopyAppWorkflowObjectIds.row_media_size_oficio_8_5x13_4in,
            "4x6 in.": CopyAppWorkflowObjectIds.row_media_size_index_4x6_4x6in,
            "5x7 in.": CopyAppWorkflowObjectIds.row_media_size_index_5x7_5x7in, 
            "5x8 in.": CopyAppWorkflowObjectIds.row_media_size_index_5x8_5x8in,
            "Envelope B5 (176x250 mm)": CopyAppWorkflowObjectIds.row_media_size_envelope_b5,
            "Envelope Monarch (3.9x7.5 in.)": CopyAppWorkflowObjectIds.row_media_size_envelope_monarch,
            "Envelope C5 (162x229 mm)": CopyAppWorkflowObjectIds.row_media_size_envelope_c5,
            "Envelope DL (110x220 mm)": CopyAppWorkflowObjectIds.row_media_size_envelope_dl,
            "16K (184x260 mm)": CopyAppWorkflowObjectIds.row_media_size_16k_184x260,
            "16K (195x270 mm)": CopyAppWorkflowObjectIds.row_media_size_16k_195x270,
            "16K (197x273 mm)": CopyAppWorkflowObjectIds.row_media_size_16k_197x273,
            "100x150mm": CopyAppWorkflowObjectIds.row_media_size_10x15,
            "Double Postcard (JIS) (148x200 mm)": CopyAppWorkflowObjectIds.row_media_size_double_postcard_jis_148x200mm,
            "Envelope #10 (4.1x9.5 in.)": CopyAppWorkflowObjectIds.row_media_size_envelope_10,
            "Postcard (JIS) (100x148 mm)": CopyAppWorkflowObjectIds.row_media_size_postcard_jis_100x148mm,
            "Custom size": CopyAppWorkflowObjectIds.row_media_size_custom,
            "Japanese Envelope Chou #3 (120x235 mm)": CopyAppWorkflowObjectIds.row_media_size_jpn_chou3_120x235mm,
            "Japanese Envelope Chou #4 (90x205 mm)": CopyAppWorkflowObjectIds.row_media_size_jpn_chou4_90x205mm,
            "Envelope C6 (114x162 mm)": CopyAppWorkflowObjectIds.row_media_size_envelope_c6,
            "L (89x127 mm)": CopyAppWorkflowObjectIds.row_media_size_l_89x127,
            "3x5 in.": CopyAppWorkflowObjectIds.row_media_size_index_3x5_3x5in

        }
        to_select_item = copy_paper_size_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, 
            CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar,
            select_option=False, scrolling_value = 0.07)        
        current_button = self.spice.wait_for(to_select_item, timeout = 9.0)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSize + " SpiceText[visible=true]")


    def select_media_size_option_constrained(self, option, constrained_message_string= ""):
        self.goto_copy_paper_size_screen()
        option_ = self.workflow_common_operations.convertfbsExtendedToCppEnumValue(option)
        option_ = "#" + option_ + "copy_mediaSize"
        self.workflow_common_operations.goto_item(option_, 
            CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar)        
        current_button = self.spice.query_item(option_)
        current_button.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.constraint_string_msg)
        if(constrained_message_string != ""):
            assert self.spice.wait_for("#constraintDescription")
            textContent = self.spice.wait_for("#constraintDescription #textColumn #contentItem") 
            assert textContent["text"] == constrained_message_string
            
        okButton = self.spice.wait_for("#okButton")
        okButton.mouse_click()
        back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize +" "+ CopyAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        
    def verify_original_size_option_constrained(self, option):
        copy_originalSize_options_dict = {
            "MIXED_LETTER_LEGAL": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_letter_legal,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_letter_legal
                },
            "MIXED_LETTER_LEDGER": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_letter_ledger,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_letter_ledger
                },
            "MIXED_A4_A3": {
                "item_id": CopyAppWorkflowObjectIds.radio_originalSize_mixed_a4_a3,
                "row_id": CopyAppWorkflowObjectIds.row_originalSize_mixed_a4_a3
                }
            }
        
        to_select_item = copy_originalSize_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item["row_id"], 
            CopyAppWorkflowObjectIds.view_copySettings_originalSize, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_originalSize_scrollbar,
            select_option=False)
         
        current_button = self.spice.query_item(to_select_item["item_id"])
        assert current_button["constrained"] == True

        back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_originalSize +" "+ CopyAppWorkflowObjectIds.button_back)
        back_button.mouse_click()


    def enable_pageflipUp(self):
        #flipup
        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_pageFlipup, CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar )

    def change_collate(self, collate_option="off"):
        """
        Set the status of collate option
        @param collate_option:str -> on/off
        @return:
        """
        logging.info(f"Set collate option to value <{collate_option}>")

        self.workflow_common_operations.goto_item(CopyAppWorkflowObjectIds.row_toggle_copySettings_collate, 
            CopyAppWorkflowObjectIds.view_copySettingsView, scrolling_value=1,
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_options_scrollbar,
            select_option=False)        
        
        collate_constraints = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_copySettings_collate)["constrained"]
        collate_toggle_btn = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_copySettings_collate + " MouseArea")
        is_collate_toggle_btn_checked = self.get_copy_collate_status()

        if not collate_constraints == True:
            if collate_option == "off" and is_collate_toggle_btn_checked:
                logging.info("need to turn off collate option")
                collate_toggle_btn.mouse_click()
                time.sleep(3)
            elif collate_option == "on" and not is_collate_toggle_btn_checked:
                logging.info("need to turn on collate option")
                collate_toggle_btn.mouse_click()
                time.sleep(3)

    def get_copy_collate_status(self):
        """
        Get the option status of collate
        @return:
        """
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        collate_toggle_btn_status = self.spice.query_item(CopyAppWorkflowObjectIds.toggle_copySettings_collate)["checked"]
        logging.info(f"The current status of collate is <{collate_toggle_btn_status}>")
        return collate_toggle_btn_status

    def select_resize_option(self, option):
        #resize
        self.goto_copy_option_output_scale()
        copy_resize_options_dict = {
            "None": [CopyAppWorkflowObjectIds.row_outputScale_none, CopyAppWorkflowObjectIds.radio_outputScale_none],
            "Fit To Page":[CopyAppWorkflowObjectIds.row_outputScale_fitToPage, CopyAppWorkflowObjectIds.radio_outputScale_fitToPage],
            "Custom":[CopyAppWorkflowObjectIds.row_copySettings_outputScale_custom, CopyAppWorkflowObjectIds.radio_copySettings_outputScale_custom],
            "FullPage(91%)":[CopyAppWorkflowObjectIds.row_outputScale_fullPage, CopyAppWorkflowObjectIds.radio_outputScale_fullPage],
            "Legal to letter(72%)": [CopyAppWorkflowObjectIds.row_outputScale_legalToLetter, CopyAppWorkflowObjectIds.radio_outputScale_legalToLetter],
            "A4 to Letter(91%)":[CopyAppWorkflowObjectIds.row_outputScale_a4ToLetter_91, CopyAppWorkflowObjectIds.radio_outputScale_a4ToLetter_91],
            "Letter to A4(94%)":[CopyAppWorkflowObjectIds.row_outputScale_letterToA4_94, CopyAppWorkflowObjectIds.radio_outputScale_letterToA4_94],
            "Include Margins":[CopyAppWorkflowObjectIds.row_outputScale_includeMargins, CopyAppWorkflowObjectIds.check_outputScale_includeMargins]
        }
        to_select_item = copy_resize_options_dict.get(option)
        menu_item_id = to_select_item
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettings_outputScale, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_resize_scrollbar )
        time.sleep(10)
        self.back_to_copy_options_list_view("Back_to_options_list")

    def go_back_to_setting_from_paper_selection(self):
        self.workflow_common_operations.back_or_close_button_press(f"{CopyAppWorkflowObjectIds.view_copySettings_paperSelection} {CopyAppWorkflowObjectIds.button_back}", CopyAppWorkflowObjectIds.view_copySettingsView)
      
    def back_to_landing_view(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen to landing screen.
        UI Flow is Option screen->Landing screen
        '''
        self.workflow_common_operations.back_or_close_button_press(CopyAppWorkflowObjectIds.setings_close_option, CopyAppWorkflowObjectIds.view_copyScreen)
        time.sleep(3)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)

    def back_to_homescreen(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen to Option screen.
        UI Flow is Landing screen->Home screen
        '''
        self.workflow_common_operations.back_button_press(CopyAppWorkflowObjectIds.view_copyScreen,MenuAppWorkflowObjectIds.view_homeScreen)

    def start_copy(self, dial_value=0, familyname="", adfLoaded=True, sided="1_1_sided", pages_per_sheet="1", operation_type="Continue", loadmedia=""):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button.
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout =9.0)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy)
        self.spice.wait_until(lambda: current_button["enabled"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout = 15.0)
        current_button.mouse_click()
        if ((adfLoaded == False) and (loadmedia != "ADF_PROMPT")) :
            self.copy_duplex_continue(familyname, sided, pages_per_sheet, operation_type)



    def check_copy_start_button_disabled(self):
        """
        Check Copy start button disabled while copy job in progress
        """
        logging.info("Checking copy start button is disabled")
        assert self.spice.query_item(CopyAppWorkflowObjectIds.button_startCopy)["enabled"] is False, 'Button is enabled'
        time.sleep(10)
    
    def check_copy_action_button_enabled(self):
        """
        Check Copy start button enabled while copy job in Idle
        """
        logging.info("Checking copy start button is disabled")
        time.sleep(10)
        assert self.spice.query_item(CopyAppWorkflowObjectIds.button_startCopy)["enabled"] is True, 'Copy Button is disabled'


    def get_copy_pages_per_sheet_options(self):
        """
        Get the pages sheet option
        @return:
        """
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        current_pages_sheet_options = self.workflow_common_operations.get_actual_str(CopyAppWorkflowObjectIds.combo_copySettings_pagesPerSheet)
        logging.info("Current pages sheet settings is: " + current_pages_sheet_options)
        return current_pages_sheet_options

    def get_copy_2sided_pages_flip_up_status(self):
        """
        Get the option status of 2 sided pages flip_up
        @return:
        """
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        try:
            is_2sided_pages_flip_options_checked = self.spice.query_item(CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp)["checked"]
            logging.info(f"The current status of 2 sided pages flip_up is <{is_2sided_pages_flip_options_checked}>")
            return is_2sided_pages_flip_options_checked
        except:
            return False

    def get_copy_custom_value_option(self):
        """
        Get the custom value option
        @return:
        """
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_outputScale)
        current_custom_value = str(self.spice.query_item(CopyAppWorkflowObjectIds.spinbox_copySettings_outputScale_custom)["value"])
        logging.info("Current custom value settings is: " + current_custom_value)
        return current_custom_value
    
    def convert_media_source_ids(self, tray_list):
        converted_tray_list = [] 
        if not tray_list:
            return []

        for tray in tray_list:
            if 'mediaSourceId' in tray and tray['mediaSourceId'].startswith("tray-"):
                converted_id = tray['mediaSourceId'].replace("tray-", "Tray")
                converted_tray_list.append(converted_id)
            else:
                converted_tray_list.append(tray)
    
        return converted_tray_list

    def back_to_copy_options_list_view(self,option_mode: str):
        """
        UI should be in the screen where the option of output scale is set.
        UI flow: Click back button in Output Scale option screen -> Option view
        Navigates to Option screen
        @param option_mode:
        @return:
        """
        back_btn = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.view_copySettings_outputScale} {CopyAppWorkflowObjectIds.button_back}")
        self.spice.validate_button(back_btn)
        back_btn.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)

    def select_copy_2sided_operation(self, operation_type:str):
        '''
        UI should be in Prompt screen.
        Navigates to Side screen starting from Prompt screen.
        UI Flow is Prompt screen->select option
        @param: operation_type: "#Continue" or "#CopyCancelButton"
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.copy_2sided_prompt, timeout = 15.0)
        selected_button = self.spice.query_item(operation_type + " SpiceText[visible=true]")
        selected_button.mouse_click()
        time.sleep(5)

    def cancel_copy_2sided_operation(self, familyname=""):
        if familyname == "homepro":
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.more_pages_collate_window_copy_cancel_button)
            current_button.mouse_click()
        elif familyname == "enterprise":
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.flatbed_two_sided_screen)
            logging.info("At Duplex Add Page Pop Up")
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_duplex_add_page_cancel)
            current_button.mouse_click()
            add_page_cancel_yes_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copy_add_page_cancel_yes)
            assert add_page_cancel_yes_button
            add_page_cancel_yes_button.mouse_click()

    def goto_no_of_copies(self):
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView), "Current screen not at copy settings view"
        # Scroll to the number of copies
        menu_item = [CopyAppWorkflowObjectIds.row_spinBox_numberOfCopies, CopyAppWorkflowObjectIds.spinBox_numberOfCopies] 
        self.workflow_common_operations.goto_item(menu_item, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False )
        no_of_copies = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies, timeout=9.0)
        assert no_of_copies, "Number of copies not found"

    def ui_copy_set_no_of_pages(self, value):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: Copy screen -> Set number of pages
        :return: None
        """
        time.sleep(10)
        numCopiesElement = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)
        numCopiesElement.__setitem__('value', value)

    def ui_set_width_no_with_numkeypad(self, value, unit):
        """
        Purpose: Input number in x or y diemesion area
        return: None
        """
        digits = [int(digit) for digit in str(value)]
        for i in digits:
            self.spice.wait_for(f"#key{i}PositiveIntegerKeypad").mouse_click() if unit == "mm" else self.spice.wait_for(f"#key{i}PositiveDecimalKeypad").mouse_click()
            time.sleep(1)
        self.spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() if unit == "mm" else self.spice.wait_for("#enterKeyPositiveDecimalKeypad").mouse_click()

    def set_copy_custom_size_value(self, unit, value_x, value_y, configuration, button="back"):

        # Unit
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view, timeout=9.0), "Error: Current screen is not at Custom Paper Size view."
        unit_combo_box = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_unit_measurement_combo_box, timeout=9.0)
        unit_combo_box.mouse_click()
        time.sleep(2)
        if unit=="mm":
            self.spice.wait_for("#comboListMillimeter", timeout=9.0).mouse_click()
        elif unit == 'inch':
            self.spice.wait_for("#comboListInches", timeout=9.0).mouse_click()
        time.sleep(2)

        # x
        time.sleep(10)
        btn = self.spice.wait_for("#CopySettingsPaperSizeCustomView #xDimexsionSpinBox #SpinBoxTextFieldMouseArea", timeout=9.0)
        time.sleep(2)
        btn.mouse_click()
        time.sleep(2)
        self.ui_set_width_no_with_numkeypad(value_x, unit)

        # y 
        time.sleep(2)
        if (self.spice.uisize == "XS" or self.spice.uisize == "S"):
            scrollbar = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view_scroll)
            scrollbar.__setitem__("position", str(0.2))
            # self.workflow_common_operations.goto_item("#CopySettingsPaperSizeCustomView #yDimexsionSpinBox #SpinBoxTextFieldMouseArea", 
            # CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view, 
            # scrollbar_objectname=CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view_scroll,
            # select_option=False)
            time.sleep(2)
        btn = self.spice.wait_for("#CopySettingsPaperSizeCustomView #yDimexsionSpinBox #SpinBoxTextFieldMouseArea", timeout=9.0)
        time.sleep(2)
        btn.mouse_click()
        time.sleep(2)
        self.ui_set_width_no_with_numkeypad(value_y, unit)

        if button == "back":
            # back
            btn = self.spice.wait_for("#CopySettingsPaperSizeCustomView #BackButton", timeout=9.0)
            time.sleep(2)
            btn.mouse_click()
        elif button == "done":
            btn = self.spice.wait_for("#FooterView #FooterViewRight #copySettingsPaperSizeCustomViewDoneBtn", timeout=9.0)
            time.sleep(2)
            btn.mouse_click()

    def check_spec_on_copy_home(self, net):
        """
        check spec on COPY HOME
        @param net:
        @return:
        """
        logging.info("check the str on Home Copy screen")
        time.sleep(10)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_button_copy_str_id, CopyAppWorkflowObjectIds.button_startCopy)

    def check_spec_on_copy_options_list(self, net):
        """
        check spec on OPTIONS_LIST
        @param net:
        @return:
        """
        logging.info("check the str on options screen")
        #TBD Verify more strings available in this
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.scan_contentType_str_id, CopyAppWorkflowObjectIds.row_combo_copySettings_contentType)

    def check_spec_copy_options_pages_per_sheet(self, net):
        """
        check spec on copy_OptionsPagesPerSheet
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsPagesPerSheet")
        logging.info("check the string about pages per sheet, (1, 2)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_pagesPerSheet_oneup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_pagesPerSheet_twoup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2)
        logging.info("verify the back button existed")
        back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.close_button)
        back_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout = 9.0)

    def check_copy_options_sides_and_select_side(self, net, side = "1_1_sided"):
        """
        check spec on copy_OptionsSides
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsSides")
        logging.info("check the string about Sides, (1 to 1-Sided, 1 to 2-Sided, 2 to 1-Sided, 2 to 2-Sided)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_1to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_1to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_2to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_2to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided)
        logging.info("Click on the Copy sides Option")
        side_option = self.sides_options_dict.get(side)
        combo_box_side_option = self.spice.wait_for(side_option, timeout = 9.0)
        combo_box_side_option.mouse_click()
        logging.info("verify the back button existed")
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout = 9.0)

    def select_scan_settings_lighter_darker(self, lighter_darker, dial_value=0):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        menu_item_id = [CopyAppWorkflowObjectIds.row_slider_lighterDarker, CopyAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView, menu_item_id=CopyAppWorkflowObjectIds.row_slider_lighterDarker, top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section , select_option=False)
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_lighterDarker)["value"]
        logging.info("Current lighter_darker value is %s" % current_value)
        current_element = self.spice.query_item(CopyAppWorkflowObjectIds.slider_lighterDarker)
        current_element.__setitem__('value', lighter_darker)
        current_value = self.spice.query_item(CopyAppWorkflowObjectIds.slider_lighterDarker)["value"]
        logging.info("lighter_darker value changed to %s" % current_value)
    
    def goto_background_noise_removal_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy background noise removal-> (copy background noise removal settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.row_copy_background_noise_removal,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At Scan background noise removal settings")
    
    def goto_edge_to_edge_output_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy edge to edge output-> (copy edge to edge output settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.settings_edgeToEdge_option,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At Scan edge to edge output settings")
    

    def set_scan_settings_edge_to_edge_output(self, value: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy edge to edge output: copy edge to edge output - True/False  
        True: open edge_to_edge_output switch
        False: close edge_to_edge_output switch
        """
        switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output)
        self.spice.wait_until(lambda: switch_button["visible"] is True)
        time.sleep(1.5)
        switch_button_state = switch_button["checked"]
        if switch_button_state:
            logging.info("current edge to edge output state is ON")
        else:
            logging.info("current edge to edge output state is OFF")
        if value != switch_button_state:
            switch_button.mouse_click()
            time.sleep(2)
            switch_button_state = switch_button["checked"]
            assert switch_button_state == value, "edge to edge output setting mismatch"
        else:
            logging.info("The current settings are correct and do not need to be modified")

    
    def set_scan_settings_background_noise_removal(self, noise_removal: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy background noise removal: copy background noise removal toggle - True/False
        """
        switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.row_copy_background_noise_removal_switch)
        self.spice.wait_until(lambda: switch_button["visible"] is True)
        time.sleep(1.5)
        noise_removal_toggled_state = switch_button["checked"]
        if noise_removal_toggled_state:
            logging.info("current background noise removal state is ON")
        else:
            logging.info("current background noise removal state is OFF")
        if noise_removal != noise_removal_toggled_state:
            switch_button.mouse_click()
            time.sleep(2)
            noise_removal_toggled_state = switch_button["checked"]
            assert noise_removal_toggled_state == noise_removal, "background noise removal setting mismatch"
        else:
            logging.info("The current settings are correct and do not need to be modified")
    
    def goto_background_color_removal_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy background Color removal-> (copy background Color removal settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.row_object_copy_background_color_removal,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At Scan background Color removal settings")

    def goto_original_paper_type_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy original paper type-> (copy original paper type settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.setings_originalPaper_option,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At original paper type settings")

    def set_copy_settings_background_color_removal(self, colorremoval: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy background Color removal: copy background Color removal toggle - True/False
        """
        switch_button = self.spice.wait_for(CopyAppWorkflowObjectIds.switch_button_copy_background_color_removal)
        self.spice.wait_until(lambda: switch_button["visible"] is True)
        time.sleep(1.5)
        colorremoval_toggled_state = switch_button["checked"]
        if colorremoval_toggled_state:
            logging.info("current background color removal state is ON")
        else:
            logging.info("current background color removal state is OFF")
        if colorremoval != colorremoval_toggled_state:
            switch_button.mouse_click()
            time.sleep(2)
            colorremoval_toggled_state = switch_button["checked"]
            assert colorremoval_toggled_state == colorremoval, "background Color removal setting mismatch"
        else:
            logging.info("The current settings are correct and do not need to be modified")
        


    def check_spec_on_copy_options_content_type(self, net, configuration):
        """
        Check spec on COPY_OptionsContentType
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsContentType")
        if configuration.productname in ["jupiter", "beam/beamsfp_power", "beam/beammfp_power"]:
            logging.info("check the string about Content Type, (Mixed, Lines, Image)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_lines_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_linedraw)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
        if configuration.productname in ["hpMfp", "canonMfp", "jindo" , "jiri"]:
            logging.info("check the string about Content Type, (Mixed, Text, PhotoGraph, Image)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_text_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_text)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_photo_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_photograph)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image)
        else:   
            logging.info("check the string about Content Type, (Mixed, Text, PhotoGraph)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_text_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_text)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_photo_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_photograph)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
        #logging.info("verify the back button existed")
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_contentType)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_back, 120)
        current_button.mouse_click()

    def check_spec_on_copy_options_color(self,net,checkoption="all"):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        if checkoption == "color":
            logging.info("check the string about Color, (color)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            time.sleep(2)
        elif checkoption == "grayscale":
            logging.info("check the string about Color, (Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            time.sleep(2)
        elif checkoption == "all":
            logging.info("check the string about Color, (color, Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            time.sleep(2) 
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_back)
        middle_width = current_button["width"] / 2
        middle_height = current_button["height"] / 2
        current_button.mouse_click(middle_width, middle_height)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)


    def check_spec_on_copy_options_auto_color(self, net):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        logging.info("check the string about Color, (Automatic, Color, Grayscale)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_automatic_str_id, CopyAppWorkflowObjectIds.combo_color_option_automatic)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
        #logging.info("verify the back button existed")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.close_button)
        current_button.mouse_click()

    def check_spec_copy_options_output_scale(self, net):
        """
        check spec on copy_OptionsOutputScale
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsOutputScale")
        logging.info("check the string about output scale, (None, Custom 100%, Fit to Page, Full Page/A4 to Letter (91%), Legal to Letter(72%), Letter to A4(94%))")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_outputScale_none_str_id, CopyAppWorkflowObjectIds.radio_outputScale_none)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_outputScale_fitToPage_str_id, CopyAppWorkflowObjectIds.radio_outputScale_fitToPage)
        #TODO :Verify more strings in this screen.
        #logging.info("verify the back button existed")
        self.workflow_common_operations.back_button_press(CopyAppWorkflowObjectIds.view_copySettings_outputScale,CopyAppWorkflowObjectIds.view_copySettingsView)

    def check_spec_on_copy_options_quality(self, net):
        """
        Check spec on COPY_OptionsQuality
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsQuality")
        logging.info("check the string about Quality, (Standard, Draft, Best)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_standard_str_id, CopyAppWorkflowObjectIds.combo_quality_option_standard)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_best_str_id, CopyAppWorkflowObjectIds.combo_quality_option_best)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_draft_str_id, CopyAppWorkflowObjectIds.combo_quality_option_draft)
        #logging.info("verify the back button existed")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_back, 3)
        current_button.mouse_click()
        # to make sure the next screen displayed
        option_screen = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        self.spice.wait_until(lambda: option_screen["visible"] is True, 20)
        time.sleep(2)

    def set_copy_2sided_flip_up_options(self, two_sided_options="off"):
        """
        Set the status of 2side flip up option
        @param two_sided_options:str -> on/off
        @return:
        """
        msg = f"Set 2sided_options to {two_sided_options}"
        logging.info(msg)

        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_pageFlipup, CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False )
        active_item = self.spice.query_item(CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp)
        is_2sided_options_checked = self.get_copy_2sided_pages_flip_up_status()

        if two_sided_options == "off" and is_2sided_options_checked:
            logging.info("need to turn off 2 sided option")
            active_item.mouse_click()

        if two_sided_options == "on" and not is_2sided_options_checked:
            logging.info("need to turn on 2 sided option")
            active_item.mouse_click()

    #Copy Widget Functions
    def start_copy_widget(self, familyname = "", adfLoaded = True):
        '''
        Change the number of copies for a copy job on the widget.
        '''
        time.sleep(4)
        self.goto_menu_mainMenu()
        CopyApp = self.spice.wait_for(CopyAppWorkflowObjectIds.button_widget_startCopy)
        CopyApp.mouse_click()
        if familyname == "enterprise":
            try:
                if adfLoaded == False:
                    current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copy_add_page_done)
                    current_button.mouse_click()
            except Exception:
                logging.info("flatbed Add page is not available")

    def check_cartridge_error_is_shown_click_on_widget(self):

        CopyApp = self.spice.wait_for(CopyAppWorkflowObjectIds.button_widget_startCopy)
        CopyApp.mouse_click()
        assert self.spice.wait_for("#cartridgeMissing1Window")
        assert self.spice.wait_for("#alertStatusImage")
        self.spice.suppliesapp.press_alert_button("#Hide")

    def change_num_copies(self, num_copies=1):
        numCopiesElement = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_widget_numberOfCopies)
        numCopiesElement.__setitem__('value', num_copies)
        
    def change_num_copyApp_copies(self, num_copies=1):
        numCopiesElement = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)
        numCopiesElement.__setitem__('value', num_copies)
        
    def increase_widget_num_copies(self, num_increment=1):
        """
        Clicks on the upBtn on the Copy Widget to increment the number of copies in the number_of_copies spinBox
        """
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_widget_incrementCopyCount)
        button_middle_width  = current_button["width"] / 2
        button_middle_height = current_button["height"] / 2
        for i in range(0, num_increment):
            current_button.mouse_click(button_middle_width, button_middle_height)

    def decrease_widget_num_copies(self, num_decrement=1):
        """
        Clicks on the downBtn on the Copy Widget to increment the number of copies in the number_of_copies spinBox
        """
        decrementCopiesElement = self.spice.wait_for(
            CopyAppWorkflowObjectIds.button_widget_decrementCopyCount)
        button_middle_width  = decrementCopiesElement["width"] / 2
        button_middle_height = decrementCopiesElement["height"] / 2
        for i in range(0, num_decrement):
            decrementCopiesElement.mouse_click(button_middle_width, button_middle_height)

    def increase_copyApp_num_copies(self, num_increment=1):
        """
        Clicks on the upBtn on the Copy Widget to increment the number of copies in the number_of_copies spinBox
        Note: It has the same ObjectName as the Copy Widget. Must be on Copy App for this to work in the Copy App.
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_spinBox_numberOfCopies, CopyAppWorkflowObjectIds.spinBox_numberOfCopies]
        self.workflow_common_operations.goto_item(menu_item_id, 
                                                  CopyAppWorkflowObjectIds.detailPanel_layout, scrollbar_objectname = CopyAppWorkflowObjectIds.vertical_layout_scrollbar, select_option = False)
        incrementCopiesElement = self.spice.wait_for(
           CopyAppWorkflowObjectIds.spinBox_numberOfCopies_plus)
        for i in range(0, num_increment):
            incrementCopiesElement.mouse_click(4,4)

    def decrease_copyApp_num_copies(self, num_decrement=1):
        """
        Clicks on the downBtn inside the Copy App to increment the number of copies in the number_of_copies spinBox
        Note: It has the same ObjectName as the Copy Widget. Must be on Copy App for this to work in the Copy App.
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_spinBox_numberOfCopies, CopyAppWorkflowObjectIds.spinBox_numberOfCopies]
        self.workflow_common_operations.goto_item(menu_item_id, 
                                                  CopyAppWorkflowObjectIds.detailPanel_layout, scrollbar_objectname = CopyAppWorkflowObjectIds.vertical_layout_scrollbar, select_option = False)
        decrementCopiesElement = self.spice.wait_for(
            CopyAppWorkflowObjectIds.spinBox_numberOfCopies_minus)
        for i in range(0, num_decrement):
            decrementCopiesElement.mouse_click(4,4)

    def launch_copyapp_from_widget_more_options(self):
        self.goto_menu_mainMenu()
        CopyApp = self.spice.wait_for(CopyAppWorkflowObjectIds.button_widget_gotoCopyApp)
        CopyApp.mouse_click(0, 10)
        self.spice.copy_ui().wait_for_copy_landing_view()
    
    def get_number_of_copies(self):
        numCopiesElement = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)
        value = numCopiesElement.__getitem__('value')
        return value
        
    def get_number_of_widget_copies(self):
        numCopiesElement = self.spice.wait_for(CopyAppWorkflowObjectIds.spinBox_widget_numberOfCopies)
        value = numCopiesElement.__getitem__('value')
        return value
        
    def check_copy_delete_quickset_successfully(self, copy_name):
        """
        Check corresponding quickset is deleted from FP UI.
        @param copy_name:
        """
        try:
            copy_quickset_option = self.spice.wait_for(f"#{copy_name}")
            assert not copy_quickset_option, f"Fail to delete quickset <{copy_name}>"
        except TimeoutError:
            logging.info(f"Success to delete quickset <{copy_name}>")
        
        #need to click ok button in menu->quickset screen when no quickset created
        try:
            logging.info("Click ok button to dismiss current screen, then next step can go back to Home screen")
            ok_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_menu_quickset_no_quickset)
            ok_button.mouse_click()
        except:
            # no need to do anything
            pass
            
    def check_copy_home_screen_under_menu_app(self, spice, net):
        excepted_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cCopy")
        currentScreen = spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy + " SpiceText" ,20)
        assert excepted_str == currentScreen["text"],"Failed to find copy item"
        logging.info("copy item is shown at copy screen")
    
    def check_copy_default_screen(self,spice,net):
        excepted_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cDefault")
        currentScreen = spice.wait_for(CopyAppWorkflowObjectIds.default_quickset_button + " SpiceText" ,20)
        assert excepted_str == currentScreen["text"],"Failed to find default"
        logging.info("default is shown at copy screen")
    
    def verify_selected_quickset_name(self, net, stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check Copy QuicksetSelected Button
        '''
        text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, stringId)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout=15)
        search_item = self.spice.wait_for(f"#{text}")
        time.sleep(2)
        assert search_item["checked"]
    
    def verify_selected_quickset(self, stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check Copy QuicksetSelected Button
        '''
        text = stringId
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout=15)
        search_item = self.spice.wait_for(f"#{text}")
        time.sleep(2)
        assert search_item["checked"]
        logging.info("Quickset checked")
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
    
    def is_quickset_existing(self):
        '''
        This is helper method to verify is quickset existing
        '''
        try:
            # Need to wait for the copyLandingScreen to update if delete quickset with cdm
            time.sleep(2)
            self.spice.wait_for(CopyAppWorkflowObjectIds.default_quickset_button, 5)
            return True
        except:
            logging.info("No copy quicksets in copy screen")
            return False


    def goto_copy_quickset_view(self):
        '''
        This is helper method to goto copy quickset view list
        '''
        
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return 

        scrollbar = self.spice.wait_for('#qsScrollhorizontalScroll')
        
        #Make sure scroll bar is at initial zero position
        scrollbar.__setitem__("position", str(0))

        #Scroll to near end of list so that view_all button is visible
        scrollbar.scroll_right(.5)

        #Attempt to press the view all button
        view_all_btn = self.spice.wait_for(CopyAppWorkflowObjectIds.view_all_locator)
        view_all_btn.mouse_click()

        self.spice.wait_for(CopyAppWorkflowObjectIds.defaults_and_quick_sets_view,timeout=15)

    def select_copy_quickset(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        if quickset_name == CopyAppWorkflowObjectIds.default_quickset_button:
            # for workflow, default quickset will not displayed in quickset list view, have to select it on copy home screen
            self.spice.query_item(CopyAppWorkflowObjectIds.close_button_under_quick_sets_view).mouse_click()
            time.sleep(2)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
            #Make sure scroll bar is at initial zero position for quickset scroll bar
            scrollbar = self.spice.wait_for('#qsScrollhorizontalScroll')
            scrollbar.__setitem__("position", str(0))
            default_quickset_item = self.spice.wait_for(quickset_name)
            default_quickset_item.mouse_click()
            assert self.spice.wait_for(quickset_name)["checked"]
            return

        logging.info("Select quickset by quickset name")
        quickset_item = self.spice.wait_for(CopyAppWorkflowObjectIds.quickset_list_box + " " + quickset_name, 1)
        quickset_item.mouse_click()
        
        time.sleep(2)
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)

        #Make sure scroll bar is at initial zero position for quickset scroll bar
        scrollbar = self.spice.wait_for('#qsScrollhorizontalScroll')
        scrollbar.__setitem__("position", str(0))

    def copy_quickset_wait_enable_and_select(self, stringId):
        text = stringId
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout=15)
        quickset_item = self.spice.wait_for(f"#{text}")
        self.spice.wait_until(lambda: quickset_item['enabled'] == True, 10.0)
        quickset_item.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)

    def copy_quickset_wait_enable_and_select_array(self, arrayStringId):
        for i, quicksetId in enumerate(arrayStringId):
            self.copy_quickset_wait_enable_and_select(quicksetId)

    def select_copy_quickset_landing(self, quickset_name):
        self.select_copy_quickset(quickset_name)
    
    def save_as_default_copy_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        copy_save_button = self.spice.wait_for(CopyAppWorkflowObjectIds.save_as_default_button)
        copy_save_button.mouse_click()
        time.sleep(3)
        try:
            (self.spice.query_item(MenuAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_credentials(True, "12345678")
            time.sleep(3)
        finally:
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_menu_save_options)
        if (self.spice.query_item(CopyAppWorkflowObjectIds.copy_as_defaults_option)["visible"] == True):
            current_option = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_as_defaults_option)
            current_option.mouse_click()
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.ok_under_save_option_veiw, 0)
        current_button.mouse_click()
        time.sleep(3)
        self.spice.wait_for(CopyAppWorkflowObjectIds.save_as_default_alert_view)
        save_button = self.spice.query_item(CopyAppWorkflowObjectIds.save_as_default_alert_save_button)
        save_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        # to make sure have enough time updating
        time.sleep(2)

    def verify_copy_settings_selected_option(self, net, setting, setting_value, screen_id = CopyAppWorkflowObjectIds.view_copySettingsView):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated -> color mode/output_scale.
            setting_value: Value of the setting ->if setting_value is custom type, please refer to custom paragraph, eg: Custom 400%
            screen_id: screen_id of the string
        """
        cstring_id = ""
        setting_id = ""
        familyname = ""
        self.udw = DuneUnderware(self.spice.ipaddress)
        #Get the ui object name of the passed setting
        #Get the cstring id for the value string
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(2)
        # Can add more option when need
        if (setting.lower() == "color"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_color
            cstring_id = self.color_format_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_color
        elif (setting.lower() == "content_type"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_contentType
            cstring_id = self.content_type_option_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_contentType
        elif (setting.lower() == "output_scale"):
            setting_id = CopyAppWorkflowObjectIds.list_copySettings_outputScale_value
            row_object_id = CopyAppWorkflowObjectIds.list_copySettings_outputScale
            if 'Custom' in setting_value:
                logging.info(f"The expected value is {setting_value}")
                cstring_id = self.output_scale_dict["custom"][0]
            else:
                cstring_id = self.output_scale_dict[setting_value.lower()][0]           
        elif (setting.lower() == "sides"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_sides
            cstring_id = self.sides_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_sides
        elif (setting.lower() == "quality"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_quality
            cstring_id = self.file_quality_option_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_quality
        elif (setting.lower() == "pages_per_sheet"):
            familyname = self.check_familyname(self.udw)
            if(familyname == "enterprise"):
                setting_id = CopyAppWorkflowObjectIds.list_copySettings_pagesPerSheet_value
                cstring_id = self.pages_per_sheet_option_dict[setting_value.lower()][0]
                row_object_id = CopyAppWorkflowObjectIds.list_copySettings_pagesPerSheet
            else:
                setting_id = CopyAppWorkflowObjectIds.combo_copySettings_pagesPerSheet
                cstring_id = self.pages_per_sheet_option_dict[setting_value.lower()][0]
                row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_pagesPerSheet
        elif (setting.lower() == "blank_page_suppression"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_blankPageSuppression
            cstring_id = self.blank_page_suppression_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.row_combo_copySettings_blankPageSuppression
        elif(setting.lower() == "finisher_staple"):
            setting_id = CopyAppWorkflowObjectIds.list_copy_staple_value
            cstring_id = self.staple_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.list_copy_staple       
        elif(setting.lower() == "finisher_punch"):
            setting_id = CopyAppWorkflowObjectIds.list_copy_punch_value
            cstring_id = self.punch_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.list_copy_punch  
        elif(setting.lower() == "finisher_fold"):
            setting_id = CopyAppWorkflowObjectIds.list_copy_fold_value
            cstring_id = self.fold_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.list_copy_fold
        elif(setting.lower() == "finisher_booklet"):
            setting_id = CopyAppWorkflowObjectIds.list_copySettings_booklet_value
            cstring_id = self.booklet_format_dict[setting_value.lower()][0]
            row_object_id = CopyAppWorkflowObjectIds.list_copySettings_booklet        
        else:
            assert False, "Setting not existing"

        self.workflow_common_operations.goto_item([row_object_id, setting_id], screen_id, select_option=False, scrollbar_objectname=CopyAppWorkflowObjectIds.copy_options_scrollbar)
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)

        if 'Custom' in setting_value:
            expected_string = expected_string.replace("%1$d%%", setting_value.split(" ")[1].strip())

        assert ui_setting_string == expected_string, "Setting value mismatch"
    
    def verify_copy_setting_lighter_darker_value(self, setting_value):
        """
        UI should be on lighter_darker slider in Copy settings screen.
        """
        slider_bar = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_lighterDarker)
        lighter_darker = slider_bar["value"]
        logging.info(f"Get value of lighter darker: <{lighter_darker}>")
        assert str(lighter_darker) == str(setting_value), "lighter/darker value is unexpected."
    
    def verify_copy_setting_collate_status(self, setting_value):
        """
        UI should be on Copy settings screen.
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_collate, CopyAppWorkflowObjectIds.toggle_copySettings_collate ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False)
        
        collate_toggle_btn_status = self.get_copy_collate_status()
        logging.info(f"Get status of collate toggle button: <{collate_toggle_btn_status}>")
        assert collate_toggle_btn_status == setting_value, "collate toggle button value is unexpected."
    
    def verify_copy_setting_2sided_pages_flip_up_status(self, setting_value):
        """
        UI should be on Copy settings screen.
        """
        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_pageFlipup, CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False)
        
        toggle_btn_status = self.get_copy_2sided_pages_flip_up_status()
        logging.info(f"Get status of 2sided pages flip up toggle button: <{toggle_btn_status}>")
        assert toggle_btn_status == setting_value, "2sided pages flip up toggle button value is unexpected."

    def verify_item_unavailable(self,objname):
        item_found = False
        try:
            self.spice.query_item(objname)
        except Exception as e:
            if str(e) == "Query selection returned no items":
                item_found = True
                pass
        options_view_back_button = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_originalSize +" "+ CopyAppWorkflowObjectIds.button_back)
        time.sleep(2)
        options_view_back_button.mouse_click()
        self.back_to_landing_view()
        assert item_found, ("item with object name "+objname+" is found, while expected to be unavailable")
    
    def verify_copy_landing_selected_option(self, net, setting, setting_value):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Copy Landing view
            setting: Setting to be validated -> e.g.: color mode.
            setting_value: Value of the setting
            screen_id: screen_id of the string
        """
        cstring_id = ""
        setting_id = ""
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        time.sleep(2)
        # Can add other options when need
        if (setting.lower() == "color"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_color
            cstring_id = self.color_format_dict[setting_value.lower()][0]
        elif (setting.lower() == "sides"):
            setting_id = CopyAppWorkflowObjectIds.combo_copySettings_sides
            cstring_id = self.sides_dict[setting_value.lower()][0]
        else:
            assert False, "Setting not existing"

        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"
    
    def verify_copy_setting_auto_tone_status(self, status):
        """
        Get the option status of auto tone checkbox
        """
        checkbox = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoTone)
        auto_tone_checkbox_status = checkbox["checked"]
        logging.info(f"The current status of auto tone is <{auto_tone_checkbox_status}>")
        assert auto_tone_checkbox_status == status, "Auto tone checkbox status is unexpected."
        
    def verify_copy_setting_auto_tone_level_value(self, setting_value):
        """
        Get the option value of auto tone level
        """
        slider_bar = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoTone)
        auto_tone_level = slider_bar["value"]
        logging.info(f"Get value of auto tone level: <{auto_tone_level}>")
        assert str(auto_tone_level) == str(setting_value), "Auto tone level value is unexpected."
        
    def verify_copy_setting_auto_paper_color_removal_status(self, status):
        """
        Get the option status of auto paper color removal checkbox
        """
        checkbox = self.spice.wait_for(CopyAppWorkflowObjectIds.checkbox_autoPaperColorRemoval)
        auto_paper_color_removal_checkbox_status = checkbox["checked"]
        logging.info(f"The current status of auto paper color removal is <{auto_paper_color_removal_checkbox_status}>")
        assert auto_paper_color_removal_checkbox_status == status, "Auto paper color removal checkbox status is unexpected."  
    
    def verify_copy_setting_auto_paper_color_removal_level_value(self, setting_value):
        """
        Get the option value of auto paper color removal level
        """
        slider_bar = self.spice.wait_for(CopyAppWorkflowObjectIds.slider_autoPaperColorRemoval)
        auto_paper_color_removal_level = slider_bar["value"]
        logging.info(f"Get value of auto paper color removal level: <{auto_paper_color_removal_level}>")
        assert str(auto_paper_color_removal_level) == str(setting_value), "Auto paper color removal level value is unexpected."

    
    def verify_copy_auto_tone_paper_color_option(self, auto_tone_checkbox_val = None, auto_tone_slider_val = None,
                                                 auto_paper_color_checkbox_val = None, auto_paper_color_slider_val = None):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Copy Landing view
            setting: Setting to be validated -> e.g.: color mode.
            setting_value: Value of the setting
            screen_id: screen_id of the string
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(2)

        if (auto_tone_checkbox_val is not None):
            self.goto_auto_tone_option()       
            if (auto_tone_checkbox_val == False):
                self.verify_copy_setting_auto_tone_status(False)
            else:
                self.verify_copy_setting_auto_tone_status(True)
                if (auto_tone_slider_val is not None):
                    self.verify_copy_setting_auto_tone_level_value(auto_tone_slider_val)

        if (auto_paper_color_checkbox_val is not None):
            self.goto_auto_paper_color_removal_option()
            if (auto_paper_color_checkbox_val == False):
                self.verify_copy_setting_auto_paper_color_removal_status(False)
            else:
                self.verify_copy_setting_auto_paper_color_removal_status(True)
                if (auto_paper_color_slider_val is not None):
                    self.verify_copy_setting_auto_paper_color_removal_level_value(auto_paper_color_slider_val)