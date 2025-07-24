import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fp_nzw.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fp_nzw.obj=b87a4606e77bda07e593bc34588e722a23ad78868b378796489204dc426a152f
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_fp_nzw
    +test:
        +title: test_pcl5_hpgl_polygon_fp_nzw
        +guid:efe75a28-11b3-4d89-89a1-01847ebea01f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_fp_nzw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b87a4606e77bda07e593bc34588e722a23ad78868b378796489204dc426a152f', timeout=600)
    outputsaver.save_output()
