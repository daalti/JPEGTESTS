import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using Dumppage2.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:Dumppage2.pcl=47db0f170f67523649e9a68cb9553a7edb0e8361267a831cc70c5ff6884c82a7
    +test_classification:System
    +name: test_pcl5_testfiles_text_dumppage2
    +test:
        +title: test_pcl5_testfiles_text_dumppage2
        +guid:407b4d57-a127-459a-9037-1d5d730cc72d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_dumppage2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('47db0f170f67523649e9a68cb9553a7edb0e8361267a831cc70c5ff6884c82a7', timeout=600)
    outputsaver.save_output()
