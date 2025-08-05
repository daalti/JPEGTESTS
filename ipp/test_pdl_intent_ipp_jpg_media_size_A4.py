import pytest
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, ColorRenderingType, ContentOrientation, PrintQuality, Plex, PlexBinding, PlexSide, MediaType, NeutralAxisType, HalftoneType, TrappingLevel
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value media_size_A4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_media_size_A4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_media_size_A4
        +guid:88b3af91-abe8-477a-9bdb-6939eb953630
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=Color & Print=Normal & NeutralAxisIntentByObject=True & ColorTrapLevel=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_media_size_A4(setup_teardown, printjob, outputsaver, tray, outputverifier, configuration):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'iso_a4_210x297mm', 'print-color-mode': 'color', 'copies':4, 'print-quality': 4, 'sides': 'one-sided', 'media-type': 'stationery', 'orientation-requested': 3}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 4)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)

    # The name of this test was changed from 'test_ipp_jpg_media_size_A4' to 'test_pdl_intent_ipp_jpg_media_size_A4'.
    # Before the name change, only successful job completion was verified. After renaming, various print intents started being verified.
    # Below print intents which are not available on designjet products, shouldn't be verified on designjet products.
    if configuration.familyname != "designjet":
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_text_obj_neutral_axis_intent(Intents.printintent, NeutralAxisType.neutral_k_only)
        outputverifier.verify_vector_obj_neutral_axis_intent(Intents.printintent, NeutralAxisType.neutral_k_only)
        outputverifier.verify_text_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
        outputverifier.verify_vector_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
        outputverifier.verify_color_trap_level(Intents.printintent, TrappingLevel.level_2)

    tray.reset_trays()