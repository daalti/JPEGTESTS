import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 11Page_cttudssv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:11Page-cttudssv.obj=d5f5f71cabd0dd7fb18bb4bc4a227ba02f127f2ac969d98bf4f31f8343389dcc
    +test_classification:System
    +name: test_pcl5_lowvaluenew_11page_cttudssv
    +test:
        +title: test_pcl5_lowvaluenew_11page_cttudssv
        +guid:04bb2b84-6cc3-4b28-a75b-9203c32ad0ff
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_11page_cttudssv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d5f5f71cabd0dd7fb18bb4bc4a227ba02f127f2ac969d98bf4f31f8343389dcc', timeout=600)
    outputsaver.save_output()
