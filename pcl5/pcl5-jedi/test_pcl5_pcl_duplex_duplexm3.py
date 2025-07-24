import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplexm3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplexm3.obj=431098ccfa7e7d5e3c7b944cbde807d467a9d1d55d74db1ed3529208680747be
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplexm3
    +test:
        +title: test_pcl5_pcl_duplex_duplexm3
        +guid:bb875a77-d38a-460e-8bbe-5a0558a87367
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplexm3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('431098ccfa7e7d5e3c7b944cbde807d467a9d1d55d74db1ed3529208680747be', timeout=600)
    outputsaver.save_output()
