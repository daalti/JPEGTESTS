import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using er_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:er_igm.obj=36ce32908a409ab4b6e1c1c786e67424e1eeed9399c0e60ae3d23da56dca5233
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_er_igm
    +test:
        +title: test_pcl5_hpgl_polygon_er_igm
        +guid:e580a1f7-9d90-4b42-9bac-e76a0a4ff303
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_er_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('36ce32908a409ab4b6e1c1c786e67424e1eeed9399c0e60ae3d23da56dca5233', timeout=600)
    outputsaver.save_output()
