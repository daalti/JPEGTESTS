import pytest 
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$

    +purpose: Simple print job of a A4 plain 5-Page PCL3GUI file 
    +test_tier:1
    +is_manual:False
    +test_classification: System
    +reqid: DUNE-174492
    +timeout:120
    +asset:Home
    +delivery_team:Home
    +feature_team:MMVertical 
    +test_framework:TUF 
    +external_files: EET_Plain_N_A4_Simplex_5pgs_.pcl=3c0b496acf86b1b7a054d34b4b81211c9c8cb9b75d00432b44960fe4564a12fc
    +test_classification:System
    +name:test_pcl3gui_A4_Simplex_5pgs
    +test:
        +title:test_pcl3gui_A4_Simplex_5pgs
        +guid:0f232fb0-2a59-4c9b-ae27-ec6dc6df2a67
        +dut:
            +type:Engine
            +configuration: DocumentFormat=PCL3GUI
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3gui_A4_Simplex_5pgs(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()

    printjob.print_verify('3c0b496acf86b1b7a054d34b4b81211c9c8cb9b75d00432b44960fe4564a12fc')
    outputsaver.save_output()

    logging.info("PCL3GUI A4 Simplex 5-page print completed successfully")

