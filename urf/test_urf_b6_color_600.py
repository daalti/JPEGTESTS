import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf B6 Color 600 from *B6_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B6_Color_600.urf=c1bf52be1f1eae402a6a66de224a153e23a2c94067b73d6e90a1abaec36470fb
    +name:test_urf_b6_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b6_color_600_page
        +guid:7a59baeb-8242-4b8f-a1d0-52ed1a94b24f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jis_b6_128x182mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b6_color_600_page(setup_teardown, printjob, outputsaver, tray, media):
    default = tray.get_default_source()
    if tray.is_size_supported('jis_b6_128x182mm', default):
        tray.configure_tray(default, 'jis_b6_128x182mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
    
    jobid = printjob.start_print('c1bf52be1f1eae402a6a66de224a153e23a2c94067b73d6e90a1abaec36470fb')
    printjob.wait_verify_job_completion(jobid, timeout=120)
    outputsaver.save_output()
    tray.reset_trays()
