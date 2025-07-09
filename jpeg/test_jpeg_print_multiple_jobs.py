from dunetuf.localization.LocalizationHelper import LocalizationHelper

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test print multiple jobs
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6717
    +timeout:300
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +external_files:lenna_without_resolution_info_EXIF_NONE.jpg=0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19
    +test_classification:System
    +name:test_jpeg_print_multiple_jobs
    +test:
        +title:test_jpeg_print_multiple_jobs
        +guid:b6fe77e5-9fb0-437c-bdd6-b4674692b3bf
        +dut:
            +type:Simulator, Emulator
            +configuration:DocumentFormat=JPEG & PrintEngineType=Maia

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_print_multiple_jobs(setup_teardown, printjob, spice, job, net, locale: str = "en"):
    
    # Go to Job Queue App screen
    spice.cleanSystemEventAndWaitHomeScreen()
    spice.main_app.get_home()
    spice.main_app.goto_job_queue_app()
    
    # Send job to print
    printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')
    
    # Get last job in queue by CDM
    queue = job.get_job_queue()
    first_job_id = queue[-1]["jobId"]
    
    # Send job to print
    printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')
    
    # Get last job in queue by CDM
    queue = job.get_job_queue()
    second_job_id = queue[-1]["jobId"]
    
    # Send job to print
    printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')
    
    # Get last job in queue by CDM
    queue = job.get_job_queue()
    third_job_id = queue[-1]["jobId"]
    
    #Wait for first job completion
    job.wait_for_job_completion_cdm(first_job_id)
    spice.job_ui.goto_job(first_job_id)
    assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)
    
    #Wait for second job completion
    job.wait_for_job_completion_cdm(second_job_id)
    spice.job_ui.goto_job(second_job_id)
    assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)
    
    #Wait for third job completion
    job.wait_for_job_completion_cdm(third_job_id)
    spice.job_ui.goto_job(third_job_id)
    assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)
    
    # Go to homescreen
    spice.goto_homescreen()
