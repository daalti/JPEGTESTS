import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464	
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:AC6ZQHDM_Netconx.pcl.0600.9500.prn=f266c7af1c5ef346dcdfdab354aae6702b72fdd684e71ec41c697a09f62a905f
    +name:test_pcl5_ac6zqhdm_netconx_pcl_0600_9500_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_ac6zqhdm_netconx_pcl_0600_9500_prn
        +guid:07ec517e-4be8-46e3-8cce-aa827457aa80
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_ac6zqhdm_netconx_pcl_0600_9500_prn(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('f266c7af1c5ef346dcdfdab354aae6702b72fdd684e71ec41c697a09f62a905f')
    outputsaver.save_output()