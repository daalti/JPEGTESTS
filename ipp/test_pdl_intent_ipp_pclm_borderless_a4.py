import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, NeutralAxisType, HalftoneType, PlexSide, TrappingLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value media_size_A4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_pdl_intent_ipp_pclm_borderless_a4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pclm_borderless_a4
        +guid:a97f2d28-9879-4fa5-93f0-c260f1ed5c1b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & NeutralAxisIntentByObject=True & ColorTrapLevel=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pclm_borderless_a4(setup_teardown, printjob, outputverifier, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'application/PCLm', 'media': 'iso_a4_210x297mm','media-left-margin':0,'media-right-margin':0,'media-top-margin':0,'media-bottom-margin':0,'x-dimension':21000,'y-dimension':29700, 'ipp-attribute-fidelity': 'False', 'media-type': 'stationery'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_text_obj_neutral_axis_intent(Intents.printintent, NeutralAxisType.neutral_k_only)
    outputverifier.verify_vector_obj_neutral_axis_intent(Intents.printintent, NeutralAxisType.neutral_k_only)
    outputverifier.verify_text_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
    outputverifier.verify_vector_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
    outputverifier.verify_plex_side(Intents.printintent, PlexSide.first)
    outputverifier.verify_color_trap_level(Intents.printintent, TrappingLevel.level_2)
    tray.reset_trays()
