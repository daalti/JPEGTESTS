import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669454 IPP test for printing a JPG file using attribute value printer_resolution_1200x1200dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:900
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_ipp_jpg_printer_resolution_1200x1200dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_printer_resolution_1200x1200dpi
        +guid:9e5a0d7e-7eaf-4f63-baf1-14e00f36f57e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & PrintResolution=Print1200 & MediaSizeSupported=Any

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_printer_resolution_1200x1200dpi(setup_teardown, printjob, outputsaver):
    ipp_test_attribs = {'document-format': 'image/jpeg', 'resolution': '1200x1200dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc',timeout=900)
    outputsaver.save_output()

