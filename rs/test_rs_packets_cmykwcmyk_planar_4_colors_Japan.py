import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_packets_cmykwcmyk_planar_4_colors_Japan
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-XXXX
    +timeout:820
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:packets_cmykwcmyk_planar_4_colors_japan.rs=a7f2e4c9e48cd713cbe4cb044b2ce9c535e210a306c86ed6c971adab8a064b2b
    +test_classification:System
    +name:test_rs_packets_cmykwcmyk_planar_4_colors_Japan
    +test:
        +title:test_rs_packets_cmykwcmyk_planar_4_colors_Japan
        +guid:ba76976e-8e2a-11eb-a7fb-2f8cb3068006
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=RasterStreamPlanarICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_packets_cmykwcmyk_planar_4_colors_Japan(setup_teardown, printjob, outputsaver, tray, tcl):
    
    tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
    printjob.print_verify('a7f2e4c9e48cd713cbe4cb044b2ce9c535e210a306c86ed6c971adab8a064b2b', timeout=700)
    outputsaver.save_output()

    logging.info("RasterStream job finished")
