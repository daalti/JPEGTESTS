import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using unhinted.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:unhinted.obj=155484940f79601b7a78c19b3ea70bf50db23aa0bb08c10932f0295e8e431006
    +test_classification:System
    +name: test_pcl5_pcl_fontr_if_unhinted
    +test:
        +title: test_pcl5_pcl_fontr_if_unhinted
        +guid:32c008e4-bb06-4994-90f2-c366bf7d5c93
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_if_unhinted(setup_teardown, printjob, outputsaver):
    printjob.print_verify('155484940f79601b7a78c19b3ea70bf50db23aa0bb08c10932f0295e8e431006', timeout=600)
    outputsaver.save_output()
