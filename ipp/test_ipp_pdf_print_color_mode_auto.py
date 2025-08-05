import pytest

from dunetuf.print.output.intents import Intents, ColorMode


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value print_color_mode_auto
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_print_color_mode_auto
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_print_color_mode_auto
        +guid:f2430b0e-0a1a-476b-8b07-fdb104acc7e0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_print_color_mode_auto(setup_teardown, printjob, outputverifier, outputsaver, cdm):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'application/pdf', 'print-color-mode': 'auto'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputsaver.operation_mode('NONE')