import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cusrprog.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cusrprog.pcl=a49cb9666bd9f30d62f9504519376236b7a211bd2a37e5a3a8b8b5d90ce1ef02
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_cusrprog
    +test:
        +title: test_pcl5_testfiles_pattern_cusrprog
        +guid:fb8986ae-e4b4-4dd7-9200-bf35b4452ad2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_cusrprog(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a49cb9666bd9f30d62f9504519376236b7a211bd2a37e5a3a8b8b5d90ce1ef02', timeout=600)
    outputsaver.save_output()
