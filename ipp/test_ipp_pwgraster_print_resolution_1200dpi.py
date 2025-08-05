import pytest
from dunetuf.print.output.intents import Intents, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a PWG file using attribute value print_resolution_1200x1200
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-240989
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:renderFile1200DPI.pwg=ae052609931c411c0b472ea4e7a887122a5c45270a61d146e567213a00222a3d
    +test_classification:System
    +name:test_ipp_pwgraster_print_resolution_1200dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwgraster_print_resolution_1200dpi
        +guid:1158dd6f-6857-4307-9c42-8a2862d5ff23
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & PrintResolution=Print1200 & MediaSizeSupported=iso_a4_210x297mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwgraster_print_resolution_1200dpi(setup_teardown, printjob, outputsaver, outputverifier, tray):
    outputsaver.operation_mode('TIFF')

    trays = tray.get_tray_configuration()
    tray1 = trays[0]["mediaSourceId"]
    if tray.is_size_supported('iso_a4_210x297mm', tray1):
        tray.configure_tray(tray1, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/pwg-raster', 'resolution': '1200x1200dpi', 'media-size': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'ae052609931c411c0b472ea4e7a887122a5c45270a61d146e567213a00222a3d')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_resolution(Intents.printintent, 1200)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
