import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg first raster page from *FirstPrint_raster.Pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-11790
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:FirstPrint_raster.Pwg=84f172821aaf4871fce1b21a8a1f8aab6125d683c1fb33816225a01e8aeffce9
    +name:test_pwg_first_print_raster
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_first_print_raster
        +guid:17ad17d5-c612-4cbc-aecc-b043072bbdb1
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
def test_pwg_first_print_raster(setup_teardown, printjob, outputsaver):
    printjob.print_verify('84f172821aaf4871fce1b21a8a1f8aab6125d683c1fb33816225a01e8aeffce9')
    outputsaver.save_output()
