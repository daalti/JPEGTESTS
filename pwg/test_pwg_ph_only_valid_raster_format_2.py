import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only valid raster format-2 page from *PwgPhOnly-ValidRasterFormat-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ValidRasterFormat-2.pwg=2db8056eefa5a72b885e76181720b013f14a4fce311cc76acb008d2e71e51cc6
    +name:test_pwg_ph_only_valid_raster_format_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_valid_raster_format_2_page
        +guid:a7a96099-e059-4167-878a-728542dd8a11
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_valid_raster_format_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2db8056eefa5a72b885e76181720b013f14a4fce311cc76acb008d2e71e51cc6')
    outputsaver.save_output()

    logging.info("PWG Ph Only Valid Raster Foramt-2 - Print job completed successfully")
