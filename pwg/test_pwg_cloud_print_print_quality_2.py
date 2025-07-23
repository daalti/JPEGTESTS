import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print - print quality-2 page from *PwgCloudPrint-PrintQuality-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-PrintQuality-2.pwg=81c8acb0e88cbf3367c4e8faf94e349a203d98cf80b2943e18d24adaafbe60dd
    +name:test_pwg_cloud_print_print_quality_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_print_quality_2
        +guid:3942ea0a-53f8-4a84-bd10-45025ece87d4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_print_quality_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('81c8acb0e88cbf3367c4e8faf94e349a203d98cf80b2943e18d24adaafbe60dd')
    outputsaver.save_output()

    logging.info("PWG Cloud print-Print Quality-2 Pagecompleted successfully")
