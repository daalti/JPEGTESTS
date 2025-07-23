import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-5 from *PwgCloudPrint-ValidRasterFormat-5.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-5.pwg=5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e
    +name:test_pwg_cloud_print_valid_raster_format_5_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_5_page
        +guid:3aa4cdb8-e15e-453d-9acd-508b6ed3937a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_5_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-5 Page- Print job completed successfully")
