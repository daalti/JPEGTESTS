# map setting of scan app ui value with understandable setting name for function verify_setting_string
"""
structure of option dict. There are three files record this parameter:
1. EWS file: src/test/dunetuf/dunetuf/ews/copy_scan_ews_option_dict.py
2. UI file:  src/test/dunetuf/dunetuf/ui/uioperations/WorkflowOperations/copy_scan_ui_option_dict.py
3. CDM file: src/test/dunetuf/dunetuf/cdm/copy_scan_cdm_option_dict.py
The key must be consistent in both EWS, UI and CDM, while the value corresponds to their respective values
"""

scan_sides_option_dict = lambda: {
    "1-sided": "simplex",
    "2-sided": "duplex"
}

scan_sides_auto_option_dict = lambda: {
    "false": "false",
    "true": "true"
}

scan_original_size_option_dict = lambda: {
    "custom": "custom", # "Custom"
    "b2_500x707_mm": "b2", # "B2 (ISO) (500x707 mm)"
    "b3_353x500_mm": "b3", # "B3 (ISO) (353x500 mm)"
    "jis_b4": "jis_b4",  # "B4 (JIS) (257x364 mm)"
    "a0_841x1189_mm": "a0",  # "A0 (841x1189 mm)"
    "a1_594x841_mm": "a1",  # "A1 (594x841 mm)"
    "a2_420x594_mm": "a2", # "A2 (420x594 mm)"
    "a3_297x420_mm": "a3", # "A3 (297x420 mm)"
    "a4_210x297_mm": "a4", # "A4 (210x297 mm)"
    "sef_a4_210x297_mm": "iso_a4_rotated_210x297mm",  # "A4 ▭ (210x297 mm)"
    "a5_148x210_mm": "a5", # "A5 (148x210 mm)"
    "sef_a5_148x210_mm": "iso_a5_rotated_148x210mm",  # "A5 ▭ (210x297 mm)"
    "a6_105x148_mm": "a6", # "A6 (105x148 mm)"
    "envelope_b5_176x250_mm": "b5_envelope", # "Envelope B5 (176x250 mm)"
    "b6_jis_128x182_mm": "jis_b6", # "B6 (JIS) (128x182 mm)"
    "envelop_monarch": "envelope_monarch", # "Envelope Monarch (3.9x7.5 in.)"
    "envelope_c5_162x229_mm": "envelope_c5", # "Envelope C5 (162x229 mm)"
    "envelope_c6_114x162_mm": "iso_c6", # "Envelope C6 (114x162 mm)"
    "envelope_dl_110x220_mm": "envelope_dl", # "Envelope DL (110x220 mm)"
    "b5_jis": "jis_b5", # "B5 (JIS) (182x257 mm)"
    "sef_b5_jis": "jis_b5_rotated_182x257mm",  # "B5 ▭ (JIS) (182x257 mm)"
    "japanese_envelope_chou_3_120x235_mm": "chou_3_envelope", # "Japanese Envelope Chou #3 (120x235 mm)"
    "postcard_jis": "jpostcard", # "Postcard (JIS) (100x148 mm)"
    "double_postcard_jis": "jdoublepostcard", # Double Postcard (JIS) (148x200 mm)
    "executive_7_25x10_5in": "executive", # "Executive (7.25x10.5 in.)"
    "oficio_8_5x13in": "oficio_8_5x13", # "Oficio (8.5x13 in.)"
    "oficio_8_5x13_4in": "oficio_8_5x13_4in", # "Oficio (216x340 mm)"
    "3x5in": "index_3x5in",  # "3x5 in."
    "4x6in": "4x6in", # "4x6 in."
    "5x7in": "5x7in", # "5x7 in."
    "5x8in": "5x8in",  # "5x8 in."
    "8x10in": "letter_8x10in", # "letter (8x10 in.)"
    "legal_8.5x14in": "legal", # "Legal (8.5x14 in.)"
    "ledger_11x17in": "ledger",  # "Ledger (11x17 in.)"
    "letter_8.5x11in": "letter", # "Letter (8.5x11 in.)"
    "sef_letter_8_5x11in":"letter_rotated_8.5x11in",  # "Letter ▭ (8.5x11 in.)"
    "envelope_10_4.1x9.5in": "envelope_10", # "Envelope #10 (4.1x9.5 in.)"
    "oficio_216x340_mm": "oficio_8_5x13_4in", # "Oficio (216x340 mm)"
    "16k_184x260_mm": "16k_184x260mm", # "16K (184x260 mm)"
    "16k_195x270_mm": "16k_195x270mm", # "16K (195x270 mm)"
    "16k_197x273_mm": "16k", # "16K (197x273 mm)"
    "100x150mm" : "100x150mm", #  "10x15 cm"
    "statement_8.5x5.5in": "na_invoice_5.5x8.5in", # "Statement (8.5x5.5 in.)"
    "na_personal_3_625x6_5in": "personal_3_625x6_5in", # "personal_3_625x6_5in"
    "photo_4x11": "photo4x11", # "photo_4x11"
    "photo_5x5": "photo5x5", # "photo_5x5"
    "photo_5x11": "photo5x11", # "photo_5x11"
    "photo_8x8": "photo8x8", # "photo_8x8"
    "envelope_a2": "envelope_a2", # "envelope_a2"
    "oe_photo-l_3.5x5in": "l_89x127mm", # "L (89x127 mm)"
    "long_scan": "long_scan" # "Long Scan"
}

scan_original_size_cdm_to_ui_dict = lambda: {
    "custom": "custom",
    "iso_b2_500x707mm": "b2",
    "iso_b3_353x500mm": "b3",
    "jis_b4_257x364mm": "jis_b4",
    "iso_a0_841x1189mm": "a0",
    "iso_a1_594x841mm": "a1",
    "iso_a2_420x594mm": "a2",
    "iso_a3_297x420mm": "a3",
    "iso_a4_210x297mm": "a4",
    "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated": "iso_a4_rotated_210x297mm",
    "iso_a5_148x210mm": "a5",
    "com.hp.ext.mediaSize.iso_a5_148x210mm.rotated": "iso_a5_rotated_148x210mm",
    "iso_a6_105x148mm": "a6",
    "iso_b5_176x250mm": "b5_envelope",
    "jis_b6_128x182mm": "jis_b6",
    "na_monarch_3.875x7.5in": "envelope_monarch",
    "iso_c5_162x229mm": "envelope_c5",
    "iso_c6_114x162mm": "iso_c6",
    "iso_dl_110x220mm": "envelope_dl",
    "jis_b5_182x257mm": "jis_b5",
    "com.hp.ext.mediaSize.jis_b5_182x257mm.rotated": "jis_b5_rotated_182x257mm",
    "jpn_chou3_120x235mm": "chou_3_envelope",
    "jpn_hagaki_100x148mm": "jpostcard",
    "jpn_oufuku_148x200mm": "jdoublepostcard",
    "na_executive_7.25x10.5in": "executive",
    "na_foolscap_8.5x13in": "oficio_8_5x13",
    "na_oficio_8.5x13.4in": "oficio_8_5x13_4in",
    "na_index-3x5_3x5in": "index_3x5in",
    "na_index-4x6_4x6in": "4x6in",
    "na_5x7_5x7in": "5x7in",
    "na_index-5x8_5x8in": "5x8in",
    "na_govt-letter_8x10in": "letter_8x10in",
    "na_legal_8.5x14in": "legal",
    "na_ledger_11x17in": "ledger",
    "na_letter_8.5x11in": "letter",
    "com.hp.ext.mediaSize.na_letter_8.5x11in.rotated": "letter_rotated_8.5x11in",
    "na_number-10_4.125x9.5in": "envelope_10",
    "om_16k_184x260mm": "16k_184x260mm",
    "om_16k_195x270mm": "16k_195x270mm",
    "roc_16k_7.75x10.75in": "16k",
    "om_small-photo_100x150mm": "100x150mm",
    "na_invoice_5.5x8.5in": "na_invoice_5.5x8.5in",
    "oe_photo-l_3.5x5in": "l_89x127mm",
    "com.hp.ext.mediaSize.long-scan": "long_scan",
    "any": "any",
    "com.hp.ext.mediaSize.mixed-letter-ledger": "mixed_letter_ledger",
    "com.hp.ext.mediaSize.mixed-a4-a3":"mixed_a4_a3",
    "com.hp.ext.mediaSize.mixed-letter-legal": "mixed_letter_legal"
}

scan_output_size_option_dict = lambda: {
    "automatic" : "automatic", # "Automatic"
    "a0" : "a0", # "A0 (841x1189 mm)"
    "a1" : "a1", # "A1 (594x841 mm)"
    "a2" : "a2", # "A2 (420x594 mm)"
    "a3" : "a3", # "A3 (297x420 mm)"
    "a4" : "a4", # "A4 (210x297 mm)"
    "b0_iso": "b0_iso", #"B0 (ISO) (1000x1414 mm)"
    "b1_iso": "b1_iso", #"B1 (ISO) (707x1000 mm)"
    "b2_iso": "b2_iso", #"B2 (ISO) (500x707 mm)"
    "b3_iso": "b3_iso", #"B3 (ISO) (353x500 mm)"
    "b4_iso": "b4_iso", #"B4 (ISO) (250x353 mm)"
    "ansi_a": "ansi_a", #"ANSI A (216x279 mm)"
    "ansi_b" : "ansi_b", # "ANSI B (279x432 mm)"
    "ansi_c" : "ansi_c", # "ANSI C (432x559 mm)"
    "ansi_d" : "ansi_d", # "ANSI D (559x864 mm)"
    "ansi_e" : "ansi_e", # "ANSI E (864x1118 mm)"
    "arch_a" : "arch_a", # "Arch A (229x305 mm)
    "arch_b" : "arch_b", # "Arch B (305x457 mm)"
    "arch_c" : "arch_c", # "Arch C (457x610 mm)"
    "arch_d" : "arch_d", # "Arch D (610x914 mm)"
    "arch_e" : "arch_e", # "Arch E (914x1919 mm)"
    "roll_1" : "roll_1", # "Roll 1"
    "roll_2" : "roll_2", # "Roll 2"
    "custom" : "custom", # "Custom"
}

scan_positioning_option_dict = lambda: {
    "top_left" : "top_left", # "Top-left"
    "top_right" : "top_right", # "Top-right"
    "top_center" : "top_center", # "Top-center"
    "middle_left" : "middle_left", # "Middle-left"
    "middle_center" : "middle_center", # Middle-center
    "middle_right" : "middle_right", # Middle-right
    "bottom_left" : "bottom_left", # Bottom-left
    "bottom_center" : "bottom_center", # Bottom-center
    "bottom_right" : "bottom_right", # Bottom-right
}

scan_output_canvas_orientation_option_dict = lambda: {
    "landscape": "landscape", # "Landscape"
    "portrait": "portrait" # "Portrait"
}

scan_scan_resolution_option_dict = lambda: {
    "75_dpi": "e75dpi", # "75 dpi"
    "100_dpi": "e100dpi", # "100 dpi"
    "150_dpi": "e150dpi", # "150 dpi"
    "200_dpi": "e200dpi", # "200 dpi"
    "240_dpi": "e240dpi", # "240 dpi"
    "300_dpi": "e300dpi", # "300 dpi"
    "400_dpi": "e400dpi", # "400 dpi"
    "600_dpi": "e600dpi", # "600 dpi"
    "1200_dpi": "e1200dpi" # "1200 dpi"
}

scan_content_type_option_dict = lambda: {
    "mixed": "mixed", # "Mixed"
    "photograph": "photograph", # "Photograph"
    "text": "text", # "Text"
    "automatic": "autoDetect", # "Automatic"
    "fine": "", # "Fine"
    "image": "image", # "Image"
    "lines": "lines", # "Lines"
    "glossy": "", # "Glossy"
    "best": "" # "Best"   
}

scan_original_paper_type_option_dict = lambda: {
    "white" : "white", # "White"
    "blueprint" : "blueprint", # "Blueprint"
    "translucent" : "translucent", # "Translucent"
    "photo" : "photo", # "Photo"
    "ammonia_blueprint" : "ammonia_blueprint", # "Ammonia (Old) Blueprint"
    "old" : "old", # "Old"
}

scan_color_mode_option_dict = lambda: { 
    "color": "color", # "Color"
    "grayscale": "grayscale", # "Grayscale"
    "automatic": "autodetect", # "Automatic"
    "black_only": "blackonly" # "Black Only"
}

scan_file_type_option_dict = lambda: {
    "jpeg": "jpeg", # "JPEG"
    "pdf": "pdf", # "PDF"
    "tiff": "tiff", # "TIFF"
    "pdf_a": "pdfa", # "PDF/A"
    "mtiff": "mtiff" # "MTIFF"
}

scan_file_size_option_dict = lambda: {
    "large": "large", # "Large"
    "small": "small", # "Small"
    "medium": "medium", # "Medium"
    "largest": "highest", # "Largest(Highest Quality)"
    "smallest": "lowest" # "Smallest(Highest Compression)"
}

scan_orientation_option_dict = lambda: {
    "landscape": "landscape", # "Landscape"
    "portrait": "portrait", # "Portrait"
    "automatic": "autodetect" # "Automatic"
}

scan_blank_page_suppression_dict = lambda: {
    "true": "true", # "True"
    "false": "false" # "False"
}

scan_tiff_compression_option_dict = lambda: {
    "tiff_6_0": "tiff6", # "TIFF 6.0"
    "tiff_post_6_0": "tiffpost6", # "TIFF (Post 6.0)"
    #For black only settings when file type as tiff
    "automatic": "Automatic", # "Automatic"
    "g_4": "g4" # "G4"
}

# map setting of copy app ui value with understandable setting name for function verify_copy_settings_selected_option
# common for copy
copy_original_size_option_dict = lambda: {
    # """String id for element value"""
    "custom": "Custom", # "Custom"
    "a2_420x594_mm": "A2 (420x594 mm)", # "A2 (420x594 mm)"
    "a3_297x420_mm": "A3 (297x420 mm)", # "A3 (297x420 mm)"
    "a4_210x297_mm": "A4", # "A4 (210x297 mm)"
    "sef_a4_210x297_mm": "A4_SEF",  # "A4 ▭ (210x297 mm)"
    "a5_148x210_mm": "A5", # "A5 (148x210 mm)"
    "sef_a5_148x210_mm": "A5_SEF",  # "A5 ▭ (210x297 mm)"
    "a6_105x148_mm": "A6 (105x148 mm)", # "A6 (105x148 mm)"
    "envelope_b5_176x250_mm": "Envelope B5 (176x250 mm)", # "Envelope B5 (176x250 mm)"
    "b6_jis_128x182_mm": "B6 (JIS) (128x182 mm)", # "B6 (JIS) (128x182 mm)"
    "envelop_monarch": "Envelope Monarch (3.9x7.5 in.)", # "Envelope Monarch (3.9x7.5 in.)"
    "envelope_c5_162x229_mm": "Envelope C5 (162x229 mm)", # "Envelope C5 (162x229 mm)"
    "envelope_c6_114x162_mm": "Envelope C6 (114x162 mm)", # "Envelope C6 (114x162 mm)"
    "envelope_dl_110x220_mm": "Envelope DL (110x220 mm)", # "Envelope DL (110x220 mm)"
    "b5_jis": "jis_b5", # "B5 (JIS) (182x257 mm)"
    "sef_b5_jis": "B5_SEF",  # "B5 ▭ (JIS) (182x257 mm)"
    "japanese_envelope_chou_3_120x235_mm": "Japanese Envelope Chou #3 (120x235 mm)", # "Japanese Envelope Chou #3 (120x235 mm)"
    "postcard_jis": "Postcard (JIS) (100x148 mm)", # "Postcard (JIS) (100x148 mm)"
    "double_postcard_jis": "Double Postcard (JIS) (148x200 mm)", # Double Postcard (JIS) (148x200 mm)
    "executive_7_25x10_5in": "Executive", # "Executive (7.25x10.5 in.)"
    "oficio_8_5x13in": "oficio_8_5x13", # "Oficio (8.5x13 in.)"
    "4x6in": "4x6 in.", # "4x6 in."
    "5x7in": "5x7 in.", # "5x7 in."
    "5x8in": "5x8 in.", # "5x8 in."
    "legal_8.5x14in": "Legal", # "Legal (8.5x14 in.)"
    "letter_8.5x11in": "Letter", # "Letter (8.5x11 in.)"
    "sef_letter_8_5x11in":"Letter_SEF",  # "Letter ▭ (8.5x11 in.)"
    "envelope_10_4.1x9.5in": "Envelope #10 (4.1x9.5 in.)", # "Envelope #10 (4.1x9.5 in.)"
    "oficio_216x340_mm": "Oficio_8_5x13_4", # "Oficio (216x340 mm)"
    "16k_184x260_mm": "16K (184x260 mm)", # "16K (184x260 mm)"
    "16k_195x270_mm": "16K (195x270 mm)", # "16K (195x270 mm)"
    "16k_197x273_mm": "16K (197x273 mm)", # "16K (197x273 mm)"
    "statement_8.5x5.5in": "Statement (8.5x5.5 in.)" # "Statement (8.5x5.5 in.)"
}

copy_content_type_option_dict = lambda: {
    # """String id for element value"""
    "mixed": "mixed", # "Mixed"
    "photograph": "photograph", # "Photograph"
    "text": "text", # "Text"
    "automatic": "automatic", # "Automatic"
    "fine": "fine", # "Fine"
    "image": "image", # "Image"
    "glossy": "glossy", # "Glossy"
    "best": "best" # "Best"   
}

copy_color_mode_option_dict = lambda: {
    "color": "color", # "Color"
    "grayscale": "grayscale", # "Grayscale"
    "automatic": "autodetect", # "Automatic"
    "black_only": "blackonly" # "Black Only"
}

copy_file_quality_option_dict = lambda: {
    "best": "best", # "Best"
    "draft": "draft", # "Draft"
    "standard": "standard" # "Standard"
}

copy_output_scale_option_dict = lambda: {
    # """String id for element value"""
    "none": "none", # "None"
    "custom": "Custom", # "Custom"
    "fit_to_page": "fit_to_page", # "Fit to Page"
    "full_page": "full_page", # Full Page (91%)"
    "A4_to_letter":"A4_to_letter", # "A4 to Letter (91%)"
    "legal_to_letter": "legal_to_letter", # "Legal to Letter (72%)"
    "letter_to_A4": "letter_to_a4" # "Letter to A4 (94%)"  #scaleSelection
}

copy_paper_type_option_dict = lambda: {
    # """String id for element value"""
    "any_type": "Any Type", # "Any Type"
    "plain": "Plain", # "Plain"
    "hp_ecofficient": "HP EcoFFICIENT", # "HP EcoFFICIENT"
    "hp_matte_90g": "HP Matte (90g)", # "HP Matte (90g)"
    "hp_matte_105g": "HP Matte (105g)", # "HP Matte (105g)"
    "hp_matte_120g": "HP Matte (120g)", # "HP Matte (120g)"
    "hp_matte_150g": "HP Matte (150g)", # "HP Matte (150g)"
    "hp_matte_200g": "HP Matte (200g)", # "HP Matte (200g)"
    "comhpbrochurematter": "comHpBrochureMatte", # "comHpBrochureMatte"
    "brochure_glossy": "Brochure Glossy", #"Brochure Glossy"
    "hp_prem_matte": "HP Prem Matte Photo Paper", # "HP Prem Matte Photo Paper"
    "hp_glossy_120g": "HP Glossy (120g)", # "HP Glossy (120g)"
    "hp_glossy_150g": "HP Glossy (150g)", # "HP Glossy (150g)"
    "hp_glossy_200g": "HP Glossy (200g)", # "HP Glossy (200g)"
    "hp_trifold_glossy": "HP Tri-Fold Glossy (150g)", # "HP Tri-Fold Glossy (150g)"
    "light": "Light (60-74g)", # "Light (60-74g)"
    "intermediate": "Intermediate (85-95g)", # "Intermediate (85-95g)"
    "midweight": "Mid-Weight (96-110g)", # "Mid-Weight (96-110g)"
    "heavy": "Heavy (111-130g)", # "Heavy (111-130g)"
    "extra_heavy": "Extra Heavy (131-175g)", # "Extra Heavy (131-175g)"
    "cardstock": "Cardstock (176-220g)", # "Cardstock (176-220g)"
    "heavy_glossy": "Heavy Glossy (111-130g)", # "Heavy Glossy (111-130g)"
    "extra_heavy_glossy": "Extra Heavy Glossy (131-175g)", # "Extra Heavy Glossy (131-175g)"
    "cardstock_glossy": "Cardstock Glossy", # "Cardstock Glossy (176-220g)"
    "labels": "Labels", # "Labels"
    "letterhead": "Letterhead", # "Letterhead"
    "envelope": "Envelope", # "Envelope"
    "heavy_envelope": "Heavy Envelope", # "Heavy Envelope"
    "preprinted": "Preprinted", # "Preprinted"
    "prepunched": "Prepunched", # "Prepunched"
    "colored": "Colored", # "Colored"
    "bond": "Bond", # "Bond"
    "lightbond": "Light Bond", #"Light Bond"
    "recycled": "Recycled", # "Recycled"
    "rough": "Rough", # "Rough"
    "heavy_rough": "Heavy Rough", # "Heavy Rough"
    "light_rough": "Light Rough", #"Light Rough"
    "opaque_film": "Opaque Film", # "Opaque Film"
    "transparency": "Transparency", # "Transparency"
    "hp_photographic_glossy": "HP Photographic Glossy", # "HP Photographic Glossy"
    "hp_trifold_brochure_glossy_180gsm": "HP Tri-fold Brochure Paper Glossy", # "HP Tri-fold Brochure Paper, Glossy"
    "heavy_paperboard": "Paperboard (301g+)", #"Paperboard (301g+)"
    "paperboard": "Paperboard (256-300g)", #"Paperboard (256-300g)"
    "light_paperboard": "Paperboard (221-255g)", #"Paperboard (221-255g)"
    "tab_stock":"Tab", #"Tab"
    "hp_advanced_photo":"HP Advanced Photo", #"HP Advanced Photo"
	"hp_soft_gloss_120g": "HP Soft Glossy (120g)", #"HP Soft Glossy (120g)"
    "hp_midweight_glossy": "Mid-Weight Glossy (96-110g)", # "Mid-Weight Glossy (96-110g)"
    "hp_film_opaque": "Opaque Film", # "Opaque Film"
    "hp_photographic_inkjet": "Other Photo Inkjet Papers", # "Other Photo Inkjet Papers"
    "hp_matte_brochure": "HP Matte Brochure or Professional Paper", # "HP Matte Brochure or Professional Paper"
    "hp_matte_presentation": "HP Matte Presentation Paper", # "HP Matte Presentation Paper"
    "hp_matte_inkjet": "Other Matte Inkjet Papers", # "Other Matte Inkjet Papers"
    "hp_specialty_glossy": "HP Glossy Brochure or Professional Paper", # "HP Glossy Brochure or Professional Paper"
    "hp_specialty_glossy_inkjet": "Other Glossy Inkjet Papers", # "Other Glossy Inkjet Papers"
    "hp_specialty_hagaki": "Inkjet Hagaki", # "Inkjet Hagaki"
    "hp_matte_photo_duplex": "HP Matte Photo Paper", # "HP Matte Photo Paper"
    "com_hp_usertype_10": "com.hp.usertype-10" # "UserDefined10"
}

copy_paper_tray_option_dict = lambda: {
    # """String id for element value"""
    "tray1": "tray1",  # "Tray 1"
    "tray2": "tray2",  # "Tray 2"
    "tray3": "tray3",  # "Tray 3"
    "automatic": "automatic" # "Automatic"  # dest print mediaSource
}

copy_pagesper_sheet_option_dict = lambda: {
    # """String id for element value"""
    "one": "one", # "1"
    "two": "two" # "2"
}

copy_sides_option_dict = lambda: {
    # """String id for element value"""
    "1_to_1_sided": "1_1_sided", # "1 to 1-Sided"
    "1_to_2_sided": "1_2_sided", # "1 to 2-Sided"
    "2_to_1_sided": "2_1_sided", # "2 to 1-Sided"
    "2_to_2_sided": "2_2_sided" # "2 to 2-Sided"
}

copy_paper_size_option_dict = lambda: {
     # """String id for element value"""
    "custom": "Custom", # "Custom"
    "arch_a_229x305mm": "Arch A (229x305 mm)", #Arch A (229x305 mm)"
    "arch_b_305x457mm": "Arch B (305x457 mm)", #Arch B (305x457 mm)"
    "arch_c_457x610mm": "Arch C (457x610 mm)", #Arch C (457x610 mm)"
    "arch_d_610x914mm": "Arch D (610x914 mm)", #"Arch D (610x914 mm)"
    "arch_e_914x1919mm": "Arch E (914x1919 mm)", #"Arch E (914x1919 mm)"
    "arch_e2_660x965mm": "Arch E2 (660x965 mm)", #"Arch E2 (660x965 mm)"
    "arch_e3_686x991mm": "Arch E3 (686x991 mm)", #"Arch E3 (686x991 mm)"
    "a2_420x594_mm": "A2 (420x594 mm)", # "A2 (420x594 mm)"
    "a3_297x420_mm": "A3 (297x420 mm)", # "A3 (297x420 mm)"
    "a4_210x297_mm": "A4", # "A4 (210x297 mm)"
    "sef_a4_210x297_mm": "A4_SEF",  # "A4 ▭ (210x297 mm)"
    "a5_148x210_mm": "A5 (148x210 mm)", # "A5 (148x210 mm)"
    "sef_a5_148x210_mm": "A5_SEF",  # "A5 ▭ (210x297 mm)"
    "a6_105x148_mm": "A6 (105x148 mm)", # "A6 (105x148 mm)"
    "b0_1000x1414mm": "B0 (ISO) (1000x1414 mm)", #"B0 (ISO) (1000x1414 mm)"
    "b1_707x1000mm": "B1 (ISO) (707x1000 mm)", #"B1 (ISO) (707x1000 mm)"
    "b2_500x707mm": "B2 (ISO) (500x707 mm)", #"B2 (ISO) (500x707 mm)"
    "b3_353x500mm": "B3 (ISO) (353x500 mm)", #"B3 (ISO) (353x500 mm)"
    "b4_250x353mm": "B4 (ISO) (250x353 mm)", #"B4 (ISO) (250x353 mm)"
    "envelope_b5_176x250_mm": "Envelope B5 (176x250 mm)", # "Envelope B5 (176x250 mm)"
    "b6_jis_128x182_mm": "B6 (JIS) (128x182 mm)", # "B6 (JIS) (128x182 mm)"
    "envelop_monarch": "Envelope Monarch (3.9x7.5 in.)", # "Envelope Monarch (3.9x7.5 in.)"
    "c0_917x1297mm": "C0 (917x1297 mm)", #"C0 (917x1297 mm)"
    "c1_648x917mm": "C1 (648x917 mm)", #"C1 (648x917 mm)"
    "c2_458x648mm": "C2 (458x648 mm)", #"C2 (458x648 mm)"
    "c3_324x458mm": "C3 (324x458 mm)", #"C3 (324x458 mm)"
    "c4_229x324mm": "C4 (229x324 mm)", #"C4 (229x324 mm)"
    "envelope_c5_162x229_mm": "Envelope C5 (162x229 mm)", # "Envelope C5 (162x229 mm)"
    "envelope_c6_114x162_mm": "Envelope C6 (114x162 mm)", # "Envelope C6 (114x162 mm)"
    "envelope_dl_110x220_mm": "Envelope DL (110x220 mm)", # "Envelope DL (110x220 mm)"
    "b5_jis": "jis_b5", # "B5 (JIS) (182x257 mm)"
    "sef_b5_jis": "B5_SEF",  # "B5 ▭ (JIS) (182x257 mm)"
    "japanese_envelope_chou_3_120x235_mm": "Japanese Envelope Chou #3 (120x235 mm)", # "Japanese Envelope Chou #3 (120x235 mm)"
    "japanese_envelope_chou_4_90x205_mm": "Japanese Envelope Chou #4 (90x205 mm)",#"Japanese Envelope Chou #4 (90x205 mm)"
    "postcard_jis": "Postcard (JIS) (100x148 mm)", # "Postcard (JIS) (100x148 mm)"
    "double_postcard_jis": "Double Postcard (JIS) (148x200 mm)", # Double Postcard (JIS) (148x200 mm)
    "2l_127x178_mm": "2L (127x178 mm)", # "2L (127x178 mm)
    "executive_7_25x10_5in": "Executive", # "Executive (7.25x10.5 in.)"
    "oficio_8_5x13in": "oficio_8_5x13", # "Oficio (8.5x13 in.)"
    "4x6in": "4x6 in.", # "4x6 in."
    "5x7in": "5x7 in.", # "5x7 in."
    "5x8in": "5x8 in.", # "5x8 in."
    "legal_8.5x14in": "Legal", # "Legal (8.5x14 in.)"
    "letter_8.5x11in": "Letter", # "Letter (8.5x11 in.)"
    "sef_letter_8_5x11in":"Letter_SEF",  # "Letter ▭ (8.5x11 in.)"
    "envelope_10_4.1x9.5in": "Envelope #10 (4.1x9.5 in.)", # "Envelope #10 (4.1x9.5 in.)"
    "oficio_216x340_mm": "Oficio_8_5x13_4", # "Oficio (216x340 mm)"
    "16k_184x260_mm": "16K (184x260 mm)", # "16K (184x260 mm)"
    "16k_195x270_mm": "16K (195x270 mm)", # "16K (195x270 mm)"
    "16k_197x273_mm": "16K (197x273 mm)", # "16K (197x273 mm)"
    "statement_8.5x5.5in": "Statement (8.5x5.5 in.)", # "Statement (8.5x5.5 in.)"
    "ledger_11x17in": "ledger",  # "Ledger (11x17 in.)"
    "100x150mm" : "100x150mm", #  "10x15 cm"
    "d_22x34in": "D 22x34 in.", # "D 22x34 in."
    "e_34x44in": "E 34x44 in.", # "E 34x44 in."
    "envelope_6_three_quarter": "Envelope 6 3/4 (3.63x6.5 in.)", # "Envelope 6 3/4 (3.63x6.5 in.)"
    "super_b_13x19in": "Super B (13x19 in.)", # "Super B (13x19 in.)"
    "wide_format_30x42in": "Arch E1 (762x1067 mm)", # "Arch E1 (762x1067 mm)"
    "l_3_5x5in": "L (9x13 cm)", # "L (9x13 cm)"
    "photo_12x16in": "12x16 in", # "12x16 in."
    "photo_14x17in": "14x17 in", # "14x17 in."
    "photo_18x22in": "18x22 in", # "18x22 in."
    "photo_10x12in": "10x12 in", # "10x12 in."
    "envelope_9": "Envelope 9", # "Envelope 9"
    "photo_14x18in": "14x18 in", # "14x18 in."
    "photo_16x20in": "16x20 in", # "16x20 in."
    "photo_20x24in": "20x24 in", # "20x24 in."
    "photo_22x28in": "22x28 in", # "22x28 in."
    "photo_24x30in": "24x30 in", # "24x30 in."
    "photo_4x12in": "4x12 in", # "4x12 in."
    "photo_4x5in": "4x5 in", # "4x5 in."
    "photo_5x5in": "5x5 in", # "5x5 in."
    "8K_260x368mm": "8K (260x368 mm)", # "8K (260x368 mm)"
    "8K_270x390mm": "8K (270x390 mm)", # "8K (270x390 mm)"
    "photo_30x40cm": "Photo 30X40cm", # "Photo 30X40cm"
    "photo_30x45cm": "Photo 30X45cm", # "Photo 30X45cm"
    "photo_35x46cm": "Photo 35X46cm", # "Photo 35X46cm"
    "photo_40x60cm": "Photo 40x60cm", # "Photo 40x60cm"
    "photo_50x76cm": "Photo 50x76cm", # "Photo 50x76cm"
    "photo_60x90cm": "Photo 60x90cm", # "Photo 60x90cm"
    "8K_273x394mm": "8K (273x394 mm)", # "8K (273x394 mm)"
    "ra3_305x430mm": "RA3 (305x430 mm)", # "RA3 (305x430 mm)"
    "ra4_215x305mm": "RA4 (215x305 mm)", # "RA4 (215x305 mm)"
    "sra3_320x450mm": "SRA3 (320x450 mm)", # "SRA3 (320x450 mm)"
    "sra4_225x320mm": "SRA4 (225x320 mm)", # "SRA4 (225x320 mm)"
    "b0_jis_1030x1456mm": "B0 (JIS) (1030x1456 mm)", # "B0 (JIS) (1030x1456 mm)"
    "b1_jis_728x1030mm": "B1 (JIS) (728x1030 mm)", # "B1 (JIS) (728x1030 mm)"
    "b2_jis_515x728mm": "B2 (JIS) (515x728 mm)", # "B2 (JIS) (515x728 mm)"
    "b3_jis_364x515mm": "B3 (JIS) (364x515 mm)", # "B3 (JIS) (364x515 mm)"
    "b4_jis_257x364mm": "B4 (JIS) (257x364 mm)", # "B4 (JIS) (257x364 mm)"
    "ansi_c_17x22in": "ANSI C (432x559 mm)", # "ANSI C (432x559 mm)"
    "11x14in": "11x14 in.", # "11x14 in."
    "8x10in": "letter_8x10in", # "letter (8x10 in.)"
    "3x5in": "index_3x5in"  # "3x5 in."
}
##################################################################################
