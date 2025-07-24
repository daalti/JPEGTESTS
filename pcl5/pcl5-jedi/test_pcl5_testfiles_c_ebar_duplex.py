import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using c_ebar_duplex.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:c_ebar_duplex.pcl=48756167bdec468959f522c92e5c831997f67b5a9b152192b257b0942213bf73
    +test_classification:System
    +name: test_pcl5_testfiles_c_ebar_duplex
    +test:
        +title: test_pcl5_testfiles_c_ebar_duplex
        +guid:46a978fd-59f5-41a9-a025-96c3f2143357
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_c_ebar_duplex(setup_teardown, printjob, outputsaver):
    printjob.print_verify('48756167bdec468959f522c92e5c831997f67b5a9b152192b257b0942213bf73', timeout=600)
    outputsaver.save_output()
