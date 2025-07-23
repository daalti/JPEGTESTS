import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-7.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-7.pwg=63a133d4d7dbe3a8617f062883851926282580ade180f184233454b97ad808fb
    +name:test_pwg_cloud_print_orientation_7
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_7
        +guid:cc4527af-6c25-43a9-af27-e0d6847797c0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_7(setup_teardown, printjob, outputsaver):
    printjob.print_verify('63a133d4d7dbe3a8617f062883851926282580ade180f184233454b97ad808fb', 'FAILED')
    outputsaver.save_output()
