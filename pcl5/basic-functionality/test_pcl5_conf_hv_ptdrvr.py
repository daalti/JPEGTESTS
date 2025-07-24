import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **ptdrvr.cht
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:140
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:ptdrvr.cht=7a9a8d0aa77ee2c0e71ef7e8a2f133592f5897edcc2194e32bc7ced201f49e36
    +name:test_pcl5_conf_hv_ptdrvr
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_ptdrvr
        +guid:929141dd-ece5-4b86-b4ae-ff016dcd9531
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_ptdrvr(setup_teardown, printjob, outputverifier):
    printjob.print_verify_multi('7a9a8d0aa77ee2c0e71ef7e8a2f133592f5897edcc2194e32bc7ced201f49e36',expected_jobs=5)
    outputverifier.save_and_parse_output()
