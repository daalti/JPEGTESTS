import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_colorlib.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:3Page-colorlib.obj=ae2b66e7db056951c408c4f93f607d80e2f0945adc941b490b7b93272ff5d85f
    +test_classification:System
    +name: test_pcl5_highvalue_3page_colorlib
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_3page_colorlib
        +guid:ae73cde9-859e-46f1-a3b3-17b993df23cd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_3page_colorlib(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('ae2b66e7db056951c408c4f93f607d80e2f0945adc941b490b7b93272ff5d85f', timeout=600,expected_jobs=2)
    outputsaver.save_output()
