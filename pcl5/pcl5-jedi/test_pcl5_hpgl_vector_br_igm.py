import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using br_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:br_igm.obj=bcc25c09eaa8fac17c0f5ae54022e70e017cd03cef7f84e57ef7a440b35f3755
    +test_classification:System
    +name: test_pcl5_hpgl_vector_br_igm
    +test:
        +title: test_pcl5_hpgl_vector_br_igm
        +guid:c1fdacbe-98c3-40d6-b8af-c71cbe5ba8c3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_br_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bcc25c09eaa8fac17c0f5ae54022e70e017cd03cef7f84e57ef7a440b35f3755', timeout=600)
    outputsaver.save_output()
