import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-ValidRasterFormat-14.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ValidRasterFormat-14.pwg=e34d390ddfd339f690862440e620ecfc07dea6d4d73e7cbbfcac2a9c94e69888
    +name:test_pwg_ph_only_valid_raster_format_14
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_valid_raster_format_14
        +guid:881ca6a4-14a0-4eab-8761-14b08f315227
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_valid_raster_format_14(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e34d390ddfd339f690862440e620ecfc07dea6d4d73e7cbbfcac2a9c94e69888', 'FAILED')
    outputsaver.save_output()
