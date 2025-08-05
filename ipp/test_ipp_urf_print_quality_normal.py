import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value print-quality-normal
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
    +name:test_ipp_urf_print_quality_normal
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_print_quality_normal
        +guid:66a41c88-4c09-43a5-ae9f-c0eca56e6d26
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
def test_ipp_urf_print_quality_normal(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    # print-quality: 4 = normal
    ipp_test_attribs = {'document-format': 'image/urf', 'print-quality': 4}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
