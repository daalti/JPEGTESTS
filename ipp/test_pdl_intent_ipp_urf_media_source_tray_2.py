import pytest

from dunetuf.print.output.intents import Intents, MediaSource, MediaSize, ColorMode, ContentOrientation, Plex, PrintQuality, ColorRenderingType, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-source_tray-2
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-131696
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_pdl_intent_ipp_urf_media_source_tray_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_urf_media_source_tray_2
        +guid:952a7af2-95b9-4092-a217-ebfb81f5a10c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=Tray2 & Print=Normal
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_urf_media_source_tray_2(setup_teardown, printjob, outputverifier, tray, cdm):
    trays = tray.get_tray_configuration()
    tray2 = trays[1]["mediaSourceId"]
    if tray.is_size_supported('iso_a4_210x297mm', tray2):
        tray.configure_tray(tray2, 'iso_a4_210x297mm', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/urf', 'media-source': tray2, 'media': 'iso_a4_210x297mm', 'print-color-mode': 'color', 'print_quality': 4, 'sides': 'one-sided', 'orientation-requested': 3}
    else:
        ipp_test_attribs = {'document-format': 'image/urf', 'media-source': tray2, 'media': 'iso_a4_210x297mm', 'print-color-mode': 'monochrome', 'print_quality': 4, 'sides': 'one-sided', 'orientation-requested': 3}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputverifier.save_and_parse_output()
    tray2 = "tray2" if tray2 == "tray-2" else tray2
    outputverifier.verify_media_source(Intents.printintent, getattr(MediaSource,f"{tray2}"))
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    tray.reset_trays()