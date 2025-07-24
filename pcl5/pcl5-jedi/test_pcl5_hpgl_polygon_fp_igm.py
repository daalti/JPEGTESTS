import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fp_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fp_igm.obj=c4504bdf498e6ea701be99dfc15f8437153490599d57e600bb27d5a297b645dc
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_fp_igm
    +test:
        +title: test_pcl5_hpgl_polygon_fp_igm
        +guid:be3126ec-1b6e-4e68-a1fa-d5b87797dd1e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_fp_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c4504bdf498e6ea701be99dfc15f8437153490599d57e600bb27d5a297b645dc', timeout=600)
    outputsaver.save_output()
