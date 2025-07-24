import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5e.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5e.obj=4c228bcd20a780d776d30f9d4692d1d16d00734b0f4f60fb2beca9c8502eda2a
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5e
    +test:
        +title: test_pcl5_pcl_duplex_duplx5e
        +guid:ee59ec60-79b3-4554-a053-751ae1aba241
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5e(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4c228bcd20a780d776d30f9d4692d1d16d00734b0f4f60fb2beca9c8502eda2a', timeout=600)
    outputsaver.save_output()
