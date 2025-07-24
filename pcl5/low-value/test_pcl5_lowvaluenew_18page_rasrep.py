import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 18Page_rasrep.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:18Page-rasrep.obj=5f7514c7f04430955ae6585da427a968161765d01ffda7b81330e1e990b6e7dc
    +test_classification:System
    +name: test_pcl5_lowvaluenew_18page_rasrep
    +test:
        +title: test_pcl5_lowvaluenew_18page_rasrep
        +guid:f5d29f96-1642-4427-8aad-41e6321caab3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_18page_rasrep(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('5f7514c7f04430955ae6585da427a968161765d01ffda7b81330e1e990b6e7dc',timeout=600,expected_jobs=19)
    outputsaver.save_output()
