import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 42Page_transpln.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:42Page-transpln.obj=4c70a8e716aea276fea482201790ed30c1e0d8fdba40c0ab0867b95c64bf9bcd
    +test_classification:System
    +name: test_pcl5_lowvaluenew_42page_transpln
    +test:
        +title: test_pcl5_lowvaluenew_42page_transpln
        +guid:34d18d40-d895-4a1d-940d-a3fdf63b1cb2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_42page_transpln(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4c70a8e716aea276fea482201790ed30c1e0d8fdba40c0ab0867b95c64bf9bcd', timeout=600)
    outputsaver.save_output()
