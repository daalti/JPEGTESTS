import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 25Page_palconid.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:25Page-palconid.obj=cc63bad60590b510885c422ad149dda1ec6287e73f1af0ecbb80f812bdb9f2cc
    +test_classification:System
    +name: test_pcl5_lowvaluenew_25page_palconid
    +test:
        +title: test_pcl5_lowvaluenew_25page_palconid
        +guid:dda1d674-2558-4407-9f7c-35724325d5c9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_25page_palconid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cc63bad60590b510885c422ad149dda1ec6287e73f1af0ecbb80f812bdb9f2cc', timeout=600)
    outputsaver.save_output()
