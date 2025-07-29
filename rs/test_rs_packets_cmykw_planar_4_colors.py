import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_packets_cmykw_planar_4_colors
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-XXXX
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:test_rs_packets_cmykw_planar_4_colors.rs=535e394b082b23cac7c8c7c13af70adff63ca30a9e7a523756bb64b8ef0ba5f1
    +test_classification:System
    +name:test_rs_packets_cmykw_planar_4_colors
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_rs_packets_cmykw_planar_4_colors
        +guid:a6e409ee-8e29-11eb-b26f-53d7035afb1c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=RasterStreamPlanarICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_packets_cmykw_planar_4_colors(setup_teardown, printjob, outputsaver):
    printjob.print_verify('535e394b082b23cac7c8c7c13af70adff63ca30a9e7a523756bb64b8ef0ba5f1', timeout=700)
    outputsaver.save_output()

    logging.info("RasterStream job finished")
