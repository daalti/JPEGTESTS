import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fp_comb_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fp_comb_igm.obj=8f74b6379c5624297dd48f39f53b989e50485aee557c19fbc72801ebf82ad58c
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_fp_comb_igm
    +test:
        +title: test_pcl5_hpgl_polygon_fp_comb_igm
        +guid:8872c887-b354-4756-b4ff-546c7c5316b4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_fp_comb_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8f74b6379c5624297dd48f39f53b989e50485aee557c19fbc72801ebf82ad58c', timeout=600)
    outputsaver.save_output()
