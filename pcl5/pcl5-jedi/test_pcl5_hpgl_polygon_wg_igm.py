import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using wg_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:wg_igm.obj=7d158518f870fe2348bcb3d2caacdf4b96929c2ef1384b6e35327f7a240d8f9c
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_wg_igm
    +test:
        +title: test_pcl5_hpgl_polygon_wg_igm
        +guid:278bdfab-32b4-418a-8d27-2110deb69538
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_wg_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7d158518f870fe2348bcb3d2caacdf4b96929c2ef1384b6e35327f7a240d8f9c', timeout=600)
    outputsaver.save_output()
