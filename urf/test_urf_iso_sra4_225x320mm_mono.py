import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **iso_sra4_225x320mm_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:iso_sra4_225x320mm_Mono.urf=333b7c8dc34ea7cb1c0d3d2f43bde6fae6829b03f45f0f2a15cf9d761e67de97
    +name:test_urf_iso_sra4_225x320mm_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_iso_sra4_225x320mm_mono
        +guid:b088b62f-24e0-4ff1-8892-bb78c02ffc94
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_sra4_225x320mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_iso_sra4_225x320mm_mono(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()

    if tray.is_size_supported('iso_sra4_225x320mm', default):
        tray.configure_tray(default, 'iso_sra4_225x320mm', 'stationery')
    
    printjob.print_verify('333b7c8dc34ea7cb1c0d3d2f43bde6fae6829b03f45f0f2a15cf9d761e67de97')
    outputsaver.save_output()
    tray.reset_trays()
