import pytest

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check 1st job is cured before start to prit 2nd job with different PM
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-213727
    +timeout:650
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
    +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +test_classification:System
    +name:test_rs_color_2_jobs_different_pm
    +test:
        +title:test_rs_color_2_jobs_different_pm
        +guid:954d55b8-a4cf-431d-9030-289d3c157001
        +dut:
            +type:Emulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & DeviceClass=LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_color_2_jobs_different_pm(setup_teardown, spice, printjob, job):
    
    # Go to Job Queue App screen
    spice.homeMenuUI().goto_job_queue_app_floating_dock(spice)
    
    # Send first job to print
    first_job_id = printjob.start_print('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
    
    # Send second job to print
    second_job_id = printjob.start_print('85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8')
    
    ## Check 1st job is cured before starting 2nd job
    # Wait for "Curing" state and then "Success" state
    job.wait_for_job_state(first_job_id, "DRYING", timeout=180)
    job.wait_for_job_state(first_job_id, "SUCCESS", timeout=120)
    
    # Check 2nd job starts to print
    job.wait_for_job_state(second_job_id, "PREPARINGTOPRINT", timeout=120)
    job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)
    
    # Wait for second job completion
    printjob.wait_for_job_completion(second_job_id, 300)
    
    # Go to homescreen
    spice.goto_homescreen()
