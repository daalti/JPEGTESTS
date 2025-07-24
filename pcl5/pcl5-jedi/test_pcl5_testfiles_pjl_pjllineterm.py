import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pjllineterm.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pjllineterm.pcl=546c27604072ccd927258eb5b4fa74947310c7816f2e05872520715a9397d373
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_pjllineterm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pjl_pjllineterm
        +guid:23021a14-5355-4fd0-96e0-e38432cb2b01
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_pjllineterm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('546c27604072ccd927258eb5b4fa74947310c7816f2e05872520715a9397d373', timeout=600)
    outputsaver.save_output()
