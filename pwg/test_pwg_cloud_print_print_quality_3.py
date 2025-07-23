import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print-print quality-3 from *PwgCloudPrint-PrintQuality-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-PrintQuality-3.pwg=23786946e342d1612d21821f5dfbd747b8be869bbe9b7f053e563c19801f4eb0
    +name:test_pwg_cloud_print_print_quality_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_print_quality_3
        +guid:11ab9d9e-4a3b-4b39-9b76-0a56273176e9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_print_quality_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('23786946e342d1612d21821f5dfbd747b8be869bbe9b7f053e563c19801f4eb0')
    outputsaver.save_output()
