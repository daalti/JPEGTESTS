import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, ContentOrientation, ColorRenderingType, Plex, PrintQuality, MediaType, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-size_legal
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-131696
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Legal_Color_600.urf=e9de59dd51a3ee051177230df3724570b15da790a4b0371a46c9f855a8b0e947
    +name:test_pdl_intent_ipp_urf_media_size_legal
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_urf_media_size_legal
        +guid:bf42a8ed-5541-485d-95c1-49a394fe0bb1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in & Print=Normal & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_urf_media_size_legal(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/urf', 'media': 'na_legal_8.5x14in', 'print-color-mode': 'color', 'orientation-requested': 3, 'print_quality': 4, 'copies':2, 'media-type': 'stationery', 'sides': 'one-sided'}
    else:
        ipp_test_attribs = {'document-format': 'image/urf', 'media': 'na_legal_8.5x14in', 'print-color-mode': 'monochrome', 'orientation-requested': 3, 'print_quality': 4, 'copies':2, 'media-type': 'stationery', 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'e9de59dd51a3ee051177230df3724570b15da790a4b0371a46c9f855a8b0e947')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.legal)
    tray.reset_trays()
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')