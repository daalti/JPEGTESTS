import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print-valid raster format-10 page from *PwgCloudPrint-ValidRasterFormat-10.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-10.pwg=9aa53ec78858441d7becdc848adc595240164d5e5169ca6d18112a612b1efdd9
    +name:test_pwg_cloud_print_valid_raster_format_10_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_10_page
        +guid:af317fc4-3bee-40f1-929c-8dbc28ba4ecb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_10_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9aa53ec78858441d7becdc848adc595240164d5e5169ca6d18112a612b1efdd9')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Valid Raster Format-10completed successfully")
