import pytest

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check 2nd job is printing before 1st job with same PM is finished (tailgating)
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-213703
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
    +test_classification:System
    +name:test_rs_color_2_jobs_tailgating
    +test:
        +title:test_rs_color_2_jobs_tailgating
        +guid:ac8858e8-18b4-4eb9-ba27-2678840515f9
        +dut:
            +type:Emulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & DeviceClass=LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_color_2_jobs_tailgating(setup_teardown, spice, printjob, job):
    
    # Go to Job Queue App screen
    spice.homeMenuUI().goto_job_queue_app_floating_dock(spice)
    
    # Send first job to print
    first_job_id = printjob.start_print('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
    
    # Send second job to print
    second_job_id = printjob.start_print('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
    
    ## Check 2nd job is printing before 1st job is finished 
    # Wait for 1st job "Printing" state
    job.wait_for_job_state(first_job_id, "PRINTING", timeout=120)
    
    # Check 2nd job starts to print while 1st job is still printing
    job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)
    
    # Wait for 1st job "Curing" state
    job.wait_for_job_state(first_job_id, "DRYING", timeout=120)
    
    # Check 2nd job continues printing while 1st job is curing
    job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)
    
    # Wait for both jobs to finish
    job.wait_for_job_state(first_job_id, "SUCCESS", timeout=120)
    job.wait_for_job_state(second_job_id, "SUCCESS", timeout=180)
    
    # Go to homescreen
    spice.goto_homescreen()
