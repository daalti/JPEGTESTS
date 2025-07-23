import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PrintPWGRasterLongEdgeDuplexPortraitUsingMopriaTool.prn
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PrintPWGRasterLongEdgeDuplexPortraitUsingMopriaTool.prn=5fd69b248b6c5b46ca91f748d7538fad5a0371b0551fd9ccd6a5ae44b6e58402
    +name:test_pwg_mopria_longedge_duplex_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_mopria_longedge_duplex_portrait
        +guid:d5140c01-e35b-4d9f-b355-7768004e9950
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_mopria_longedge_duplex_portrait(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('5fd69b248b6c5b46ca91f748d7538fad5a0371b0551fd9ccd6a5ae44b6e58402')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
