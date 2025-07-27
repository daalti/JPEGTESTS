from dunetuf.localization.LocalizationHelper import LocalizationHelper

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print of a job wider than supported in Jupiter Clamato_42.pcl of 42 inches (square shaped, auto rotate does not allow printing either) vs 36 inches of max and check it can be cancelled when mismatch screen is prompted.
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3387
    +timeout:180
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Clamato_42.pcl=9c7dc590009b3a2175e987621626cde907dbb6112a011eaa1ec07fc089064ffa
    +test_classification:System
    +name:test_when_printing_42_inches_job_wider_than_supported_then_size_mismatch_prompts_and_job_is_canceled_by_user
    +test:
        +title:test_when_printing_42_inches_job_wider_than_supported_then_size_mismatch_prompts_and_job_is_canceled_by_user
        +guid:44969b01-790d-439f-b1ed-814dff1873c0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI & DeviceClass=LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_when_printing_42_inches_job_wider_than_supported_then_size_mismatch_prompts_and_job_is_canceled_by_user(setup_teardown, printjob, job, spice, net, locale: str = "en"):
    
    # Send job to print
    job_id = printjob.start_print('9c7dc590009b3a2175e987621626cde907dbb6112a011eaa1ec07fc089064ffa')
    
    # Cancel job from mismatch prompt
    spice.job_ui.mismatch_alert_cancel_job()
    job.wait_canceled_job(job_id, job_wait_time = 60)

