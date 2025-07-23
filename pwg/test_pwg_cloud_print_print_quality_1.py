import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print - print quality-1 page from *PwgCloudPrint-PrintQuality-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-PrintQuality-1.pwg=9ab58207d267317d47a69b3829f15b03f1f05626ae07d0ce3c046dabb11a74ac
    +name:test_pwg_cloud_print_print_quality_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_print_quality_1
        +guid:36a4b01a-e10e-4d3d-806f-c5bd6d569d6d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_print_quality_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9ab58207d267317d47a69b3829f15b03f1f05626ae07d0ce3c046dabb11a74ac')
    outputsaver.save_output()

    logging.info("PWG Cloud print-Print Quality-1 Pagecompleted successfully")
