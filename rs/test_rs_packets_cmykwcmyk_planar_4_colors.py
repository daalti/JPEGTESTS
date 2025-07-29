import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_packets_cmykwcmyk_planar_4_colors
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-XXXX
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:packets_cmykwcmyk_planar_4_colors.rs=b60ac9e2480c6e0a0f7effcd479a5adb5e21ab0d512b14590281f53c573d4842
    +test_classification:System
    +name:test_rs_packets_cmykwcmyk_planar_4_colors
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_rs_packets_cmykwcmyk_planar_4_colors
        +guid:84127684-8e2a-11eb-9dbc-172e62f9b431
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=RasterStreamPlanarICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_packets_cmykwcmyk_planar_4_colors(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b60ac9e2480c6e0a0f7effcd479a5adb5e21ab0d512b14590281f53c573d4842', timeout=700)
    outputsaver.save_output()

    logging.info("RasterStream job finished")
