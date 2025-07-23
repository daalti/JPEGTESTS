import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print-valid raster format-19 page from *PwgCloudPrint-ValidRasterFormat-19.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-19.pwg=7cca926b733b1e78d298a3d558b45df5137b49fff3de1c7906a724c55a5d038b
    +name:test_pwg_cloud_print_valid_raster_format_19_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_19_page
        +guid:fd1688e2-740a-403f-b022-d896b23c8b0d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintResolution=Print300

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_19_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7cca926b733b1e78d298a3d558b45df5137b49fff3de1c7906a724c55a5d038b')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Valid Raster Format-19completed successfully")
