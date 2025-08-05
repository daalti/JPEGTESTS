import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value print_rendering_intent_relative_bpc
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_print_rendering_intent_relative_bpc
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_print_rendering_intent_relative_bpc
        +guid:19999af7-dc6a-4cef-a154-8e9fa7d78fd1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_print_rendering_intent_relative_bpc(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'application/pdf', 'print-rendering-intent': 'relative-bpc'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
