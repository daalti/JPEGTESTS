import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-21 from *PwgCloudPrint-ValidRasterFormat-21.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-21.pwg=5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e
    +name:test_pwg_cloud_print_valid_raster_format_21_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_21_page
        +guid:0d771c27-fab3-43a4-9e4e-9bddd03f80a0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_21_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-21 Page- Print job completed successfully")
