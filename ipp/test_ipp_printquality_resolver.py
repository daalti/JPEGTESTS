import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a 1200 JPG file using attribute value printquality normal.
    +test_tier:1
    +is_manual:False
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +reqid:DUNE-115947
    +test_framework:TUF
    +external_files:test_file_16Meg6.jpg=211995c4853e73292d67d7a4eb85161090318b23cf516b3469aaee3874720d56
    +test_classification:System
    +name:test_ipp_jpg_printquality_resolver_pqNormal
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_printquality_resolver_pqNormal
        +guid:50bfd0ed-f438-4854-87e9-5e3a64f359dc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & PrintResolution=Print1200

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_printquality_resolver_pqNormal(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('NONE')

    ipp_test_attribs = {'document-format': 'image/jpeg', 'print-quality': 4}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()

    printjob.ipp_print(ipp_test_file, '211995c4853e73292d67d7a4eb85161090318b23cf516b3469aaee3874720d56',timeout=600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()