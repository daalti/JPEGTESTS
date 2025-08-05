import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669447 Ipp test for printing a URF file using attribute value printer-resolution_1200dpi
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
    +name:test_ipp_urf_printer_resolution_1200dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_printer_resolution_1200dpi
        +guid:a737ab45-6d06-459f-b6dd-6daf299924c5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & PrintResolution=Print1200

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_printer_resolution_1200dpi(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    ipp_test_attribs = {'document-format': 'image/urf', 'resolution': '1200x1200dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0','FAILED')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
