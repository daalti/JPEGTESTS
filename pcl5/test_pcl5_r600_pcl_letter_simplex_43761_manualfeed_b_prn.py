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
    +external_files:R600_pcl_letter_Simplex_43761-Manualfeed_b.prn=d531678fb2fa78b475719b83003f2ff2930a64b248518412cfd7907f00957d89
    +name:test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_b_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_b_prn
        +guid:7bee5010-373f-440c-b719-78124cc8f4fb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5 & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_b_prn(setup_teardown, printjob, outputsaver,tray,media):
    default = tray.get_default_source()
    jobid = printjob.start_print("d531678fb2fa78b475719b83003f2ff2930a64b248518412cfd7907f00957d89")

    media.wait_for_alerts('mediaManualLoadFlow')
    tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    tray.load_media(default)
    sleep(5)
    printjob.wait_verify_job_completion(jobid)
    outputsaver.save_output()
    tray.reset_trays()