import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:A3 rasterstream multiple pages (.rs) file print
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-14986
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689
    +name:test_rs_tower_a1_3pages
    +test:
        +title:test_rs_tower_a1_3pages
        +guid:ea248a31-814c-4c2d-9e7a-a40248b3ac19
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=RasterStreamICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_tower_a1_3pages(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689', timeout=300)
    outputsaver.save_output()
