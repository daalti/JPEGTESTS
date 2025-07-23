import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PrintPWGRasterShortEdgeDuplexPortraitUsingMopriaTool.prn
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PrintPWGRasterShortEdgeDuplexPortraitUsingMopriaTool.prn=5041d4b1512169d0a43d38657fb4181bdb8e0b49209bcdc194617b65e47bbab8
    +name:test_pwg_mopria_shortedge_duplex_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_mopria_shortedge_duplex_portrait
        +guid:7c54d9dc-14aa-48cb-ae6f-83363b99378f
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
def test_pwg_mopria_shortedge_duplex_portrait(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('5041d4b1512169d0a43d38657fb4181bdb8e0b49209bcdc194617b65e47bbab8')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
