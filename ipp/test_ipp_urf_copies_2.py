import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value copies_2
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_ipp_urf_copies_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_copies_2
        +guid:c7020169-b2ea-42d3-a87b-a6759ad45900
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & Print=NumberOfCopies

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_copies_2(setup_teardown, printjob, outputsaver,udw):
    outputsaver.operation_mode('TIFF')
    REQUIRED_MEMORY = 52428800
    if printjob.printer_has_enough_pdl_memory(udw, REQUIRED_MEMORY):
        ipp_test_attribs = {'document-format': 'image/urf', 'copies': 2}
    else:
        ipp_test_attribs = {'document-format': 'image/urf', 'copies': 1}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
