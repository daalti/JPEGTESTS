import pytest
import logging

from dunetuf.print.output.intents import Intents, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing PDF file using attribute values single-sided, 600x600dpi, RGB, Normal, roll_z_917.00x229.25mm, auto
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-152671
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files: MediaSizeTest_PDF_917x229.25mm.pdf=1e210be55fe0a9428180ba42bb70db84fa3e273d3d121d1b67deebf806f5c41d
    +test_classification:System
    +name: test_pdl_intent_ipp_pdf_media_source_must_honor_autoselect
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pdf_media_source_must_honor_autoselect
        +guid:d92e83fb-b703-46f1-97dc-f04968fb6790
        +dut:
            +type: Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & PrintColorMode=Color & Print=Normal
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_media_source_must_honor_autoselect(setup_teardown, printjob, outputsaver, tray, outputverifier):
    outputsaver.operation_mode('TIFF')

    printjob.ipp_print_using_attribute_file('mediasrc_musthonor_with_authselect.test', '1e210be55fe0a9428180ba42bb70db84fa3e273d3d121d1b67deebf806f5c41d')
    outputverifier.save_and_parse_output()
    if any(tray.is_tray_supported(roll) for roll in ['main-roll', 'roll' , 'roll-1']):
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    else:
        default = tray.get_default_source()
        if tray.is_size_supported('any', default):
            tray.configure_tray(default, 'any', 'any')