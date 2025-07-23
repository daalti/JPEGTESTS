import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PrintPWGRaster3PagesLongEdgeDuplexPortraitUsingMopriaTool.prn
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PrintPWGRaster3PagesLongEdgeDuplexPortraitUsingMopriaTool.prn=7655a24419dd99ad7d72f193c86e40926f1f327d98ad803f97807fdc334e89ac
    +name:test_pwg_mopria_3page_longedge_duplex_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_mopria_3page_longedge_duplex_portrait
        +guid:c32abe09-7d07-4dd7-91f4-114b135428b6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_mopria_3page_longedge_duplex_portrait(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('7655a24419dd99ad7d72f193c86e40926f1f327d98ad803f97807fdc334e89ac')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
