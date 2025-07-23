import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print-valid raster format-13 page from *PwgCloudPrint-ValidRasterFormat-13.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-13.pwg=5513c79efb88892bab44579d5f332704c199f9fc72112eb65695ec24f64210e0
    +name:test_pwg_cloud_print_valid_raster_format_13_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_13_page
        +guid:6675c0d3-31ca-4363-a6fb-75b6c2b04196
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_13_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5513c79efb88892bab44579d5f332704c199f9fc72112eb65695ec24f64210e0')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Valid Raster Format-13completed successfully")
