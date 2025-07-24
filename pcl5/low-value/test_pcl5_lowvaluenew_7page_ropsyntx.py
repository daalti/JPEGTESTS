import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 7Page_ropsyntx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:7Page-ropsyntx.obj=b61eb8e8d666183ed0de133b697ad42b3bfc45d74937f023746608d9623d5c1d
    +test_classification:System
    +name: test_pcl5_lowvaluenew_7page_ropsyntx
    +test:
        +title: test_pcl5_lowvaluenew_7page_ropsyntx
        +guid:f155f96c-e068-4e52-8e7e-e3bdcadd06ba
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_7page_ropsyntx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b61eb8e8d666183ed0de133b697ad42b3bfc45d74937f023746608d9623d5c1d', timeout=600)
    outputsaver.save_output()
