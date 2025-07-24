import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rr_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rr_igm.obj=365a1a90377241aa2a1c5636995c8c36a20c213762d76fa4960d688ec183b39f
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_rr_igm
    +test:
        +title: test_pcl5_hpgl_polygon_rr_igm
        +guid:65f652f7-9f2a-40bf-8ae7-0fe56d340e93
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_rr_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('365a1a90377241aa2a1c5636995c8c36a20c213762d76fa4960d688ec183b39f', timeout=600)
    outputsaver.save_output()
