import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ci.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ci.obj=a302bec46e4b41662a86b393f4adc95a04ed9bd37ccf810a4f7c831e8daf0546
    +test_classification:System
    +name: test_pcl5_hpgl_vector_ci
    +test:
        +title: test_pcl5_hpgl_vector_ci
        +guid:b3a7e564-ae54-49ab-a335-05228427ee8f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_ci(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a302bec46e4b41662a86b393f4adc95a04ed9bd37ccf810a4f7c831e8daf0546', timeout=600)
    outputsaver.save_output()
