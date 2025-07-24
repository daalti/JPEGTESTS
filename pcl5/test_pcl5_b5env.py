
import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:b5env.pcl=0c2896b056a5d8470f43109ac1333e3dcc225a64d2538554c8cd68ac15b2ce6e
    +name:test_pcl5_b5env
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_b5env
        +guid:eac80531-40a5-46ce-ba64-6aaa805c38b5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_b5env(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('iso_b5_176x250mm','tray-1'):
        tray.configure_tray('tray-1', 'iso_b5_176x250mm', 'any')
    printjob.print_verify_multi('0c2896b056a5d8470f43109ac1333e3dcc225a64d2538554c8cd68ac15b2ce6e')
    outputsaver.save_output()