import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ew_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ew_igm.obj=18d4dac329563628844f1503bd938c8988f346e65624334a0cd5809052a6df3c
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ew_igm
    +test:
        +title: test_pcl5_hpgl_polygon_ew_igm
        +guid:ce04fd20-da61-4d18-bb8d-6bde8ae3793d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ew_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('18d4dac329563628844f1503bd938c8988f346e65624334a0cd5809052a6df3c', timeout=600)
    outputsaver.save_output()
