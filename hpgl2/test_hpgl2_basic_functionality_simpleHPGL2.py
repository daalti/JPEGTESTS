import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **simpleHPGL2.plt
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-45716
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:simpleHPGL2.plt=724baf1a99712f952baa0e016513eb3d876fb3b632d60e3c52acd52056a5d160
    +test_classification:System
    +name:test_hpgl2_basic_functionality_simpleHPGL2
    +test:
        +title:test_hpgl2_basic_functionality_simpleHPGL2
        +guid:5b673fcf-cc81-4cff-ae5f-a2a2c3dcc693
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_simpleHPGL2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('724baf1a99712f952baa0e016513eb3d876fb3b632d60e3c52acd52056a5d160')
    outputsaver.save_output()