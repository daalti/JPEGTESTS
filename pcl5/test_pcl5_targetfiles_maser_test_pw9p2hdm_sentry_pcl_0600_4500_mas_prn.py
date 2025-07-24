import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:targetfiles_maser_test.pw9p2hdm_sentry.pcl.0600.4500.mas.prn=41523808be9123726eb8063a1c9910774935b5ac2655990487314364ce4b1866
    +name:test_pcl5_targetfiles_maser_test_pw9p2hdm_sentry_pcl_0600_4500_mas_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_targetfiles_maser_test_pw9p2hdm_sentry_pcl_0600_4500_mas_prn
        +guid:3ed2f4d4-2eda-4382-b55b-1f9e70b084aa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5 & JobStorageMedium=HardDisk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_targetfiles_maser_test_pw9p2hdm_sentry_pcl_0600_4500_mas_prn(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('41523808be9123726eb8063a1c9910774935b5ac2655990487314364ce4b1866', timeout=200)
    outputsaver.save_output()