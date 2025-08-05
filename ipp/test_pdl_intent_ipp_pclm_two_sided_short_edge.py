import pytest
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, ColorRenderingType, ContentOrientation, MediaType, Plex, PlexBinding, PrintQuality

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-129624
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_A4_600_cjpeg_H64_PgCnt2_GRAY.pdf=545dc0ec40f3024ca0c3b369d252292f76daab8ad5fc4370b70811e81ac6c351
    +name:test_pdl_intent_ipp_pclm_two_sided_short_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pclm_two_sided_short_edge
        +guid:608497c9-1e9d-412b-bc9c-65bc82c59156
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & Print=Normal & Duplexer=True

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pclm_two_sided_short_edge(setup_teardown, printjob, outputverifier, outputsaver, tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            print_emulation.tray.load(tray_id, 'A4', 'Plain')
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'application/PCLm', 'media': 'iso_a4_210x297mm', 'orientation-requested': 3, 'media-type': 'stationery', 'print_quality': 4, 'sides': 'two-sided-short-edge'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '545dc0ec40f3024ca0c3b369d252292f76daab8ad5fc4370b70811e81ac6c351')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 2)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    tray.reset_trays()
