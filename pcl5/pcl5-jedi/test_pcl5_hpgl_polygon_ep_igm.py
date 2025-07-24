import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ep_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ep_igm.obj=88b7b65eeb303bc2d067fca32ff44b9355ec46001f0be0b8a3ab07b82187b794
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ep_igm
    +test:
        +title: test_pcl5_hpgl_polygon_ep_igm
        +guid:ff8afd55-ba70-4b7a-a450-a628bdac5386
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ep_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('88b7b65eeb303bc2d067fca32ff44b9355ec46001f0be0b8a3ab07b82187b794', timeout=600)
    outputsaver.save_output()
