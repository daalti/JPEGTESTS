import pytest
import logging
from time import sleep


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
    +external_files:R600_pcl_letter_Simplex_43761-Manualfeed_a.prn=1969fa9cbf3b1882b73456c9d013270c534d1938f9ff072268716f8d0499d4cf
    +name:test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn
        +guid:71922dab-dca1-401b-8044-01006f24013e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5 & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn(setup_teardown, printjob, outputsaver,tray,media):
    default = tray.get_default_source()
    jobid = printjob.start_print("1969fa9cbf3b1882b73456c9d013270c534d1938f9ff072268716f8d0499d4cf")

    media.wait_for_alerts('mediaManualLoadFlow')
    tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    tray.load_media(default)
    sleep(5)
    printjob.wait_verify_job_completion(jobid)
    outputsaver.save_output()
    tray.reset_trays()
