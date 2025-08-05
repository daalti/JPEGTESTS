import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value sides_one-sided
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
    +name:test_ipp_sides_one_sided
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_sides_one_sided
        +guid:dc89a8f4-0f6b-43ad-a7d1-265b07595028
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_sides_one_sided(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'image/urf', 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
