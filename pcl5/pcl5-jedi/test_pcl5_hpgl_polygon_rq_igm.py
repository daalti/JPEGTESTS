import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rq_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rq_igm.obj=c3ceab48fd2651ab6e1e27a53b29ca5e5a0325dcc5fc3228febd2cb82dc9b893
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_rq_igm
    +test:
        +title: test_pcl5_hpgl_polygon_rq_igm
        +guid:2541cfc2-d69a-485c-8723-5f9c0fa2cf59
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_rq_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c3ceab48fd2651ab6e1e27a53b29ca5e5a0325dcc5fc3228febd2cb82dc9b893', timeout=600)
    outputsaver.save_output()
